# train_model_loki.py
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import re
import numpy as np
import requests
import time

# --- Loki Configuration ---
LOKI_URL = 'http://localhost:3100'
CONTAINER_NAME = 'MTU'  # Adjust based on your Loki config
QUERY_RANGE_SECONDS = 60  # Logs from last 60 seconds

# --- Parser for Loki log format ---
def parse_line(line):
    severity_map = {'DEBUG': 0, 'INFO': 1, 'WARNI': 2, 'ERROR': 3}

    match = re.match(r"(\w+):[\w_]+:(.*)", line)
    if match:
        severity, message = match.groups()
        severity_level = severity_map.get(severity, -1)

        # Only match messages that include a numeric value
        numeric_match = re.search(r"has a value of (\d+)", message)
        if numeric_match:
            value = int(numeric_match.group(1))
            return [severity_level, value]

    return None

# --- Fetch logs from Loki ---
def fetch_logs_from_loki():
    now_ns = int(time.time() * 1e9)
    start_ns = now_ns - (QUERY_RANGE_SECONDS * 1_000_000_000)

    query = f'{{container_name="{CONTAINER_NAME}"}}'
    params = {
        'query': query,
        'limit': 1000,
        'start': start_ns,
        'end': now_ns
    }

    try:
        response = requests.get(f'{LOKI_URL}/loki/api/v1/query_range', params=params)
        response.raise_for_status()
        entries = []
        for stream in response.json()['data']['result']:
            for entry in stream['values']:
                _, log_line = entry
                entries.append(log_line)
        return entries
    except Exception as e:
        print("[ERROR] Failed to fetch logs from Loki:", str(e))
        return []

# --- Main training logic ---
print("[INFO] Fetching logs from Loki...")
raw_logs = fetch_logs_from_loki()

parsed_data = []
for line in raw_logs:
    result = parse_line(line)
    if result is not None:
        parsed_data.append(result)

if not parsed_data:
    print("[ERROR] No valid data parsed. Training aborted.")
    exit(1)

X = pd.DataFrame(parsed_data, columns=['severity', 'value'])

# --- Train model ---
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

# --- Save model ---
joblib.dump(model, 'anomaly_model.pkl')
print("[INFO] Model trained and saved as 'anomaly_model.pkl'")
