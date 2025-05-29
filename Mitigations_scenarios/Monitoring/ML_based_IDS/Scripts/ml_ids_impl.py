# ml_ids_monitor.py
import time
import requests
import joblib
import re
import numpy as np

# --- Config ---
LOKI_URL = 'http://172.18.0.21:3100'  # ip address of loki SIEM
CONTAINER_NAME = 'MTU'
MODEL_PATH = 'anomaly_model.pkl'
FETCH_INTERVAL = 10  # seconds

# --- Parser ---
def parse_line(line):
    severity_map = {'DEBUG': 0, 'INFO': 1, 'WARNI': 2, 'ERROR': 3}

    match = re.match(r"(\w+):[\w_]+:(.*)", line)
    if match:
        severity, message = match.groups()
        severity_level = severity_map.get(severity, -1)

        numeric_match = re.search(r"has a value of (\d+)", message)
        if numeric_match:
            value = int(numeric_match.group(1))
            return np.array([[severity_level, value]])

    return None

# --- Load the pre-trained ML model ---
model = joblib.load(MODEL_PATH)

# --- Fetch logs from Loki ---
def fetch_logs_from_loki():
    query = f'{{container_name="{CONTAINER_NAME}"}}'
    now_ns = int(time.time() * 1e9)
    start_ns = now_ns - int(30 * 1e9)  # 30 seconds ago in nanoseconds

    params = {
        'query': query,
        'limit': 100,
        'start': start_ns,
        'end': now_ns
    }
    try:
        response = requests.get(f'{LOKI_URL}/loki/api/v1/query_range', params=params)
        if response.ok:
            data = response.json()
            entries = []
            for stream in data['data']['result']:
                for entry in stream['values']:
                    _, log_line = entry
                    entries.append(log_line)
            return entries
        else:
            print("[ERROR] Loki query failed:", response.text)
            return []
    except Exception as e:
        print("[EXCEPTION] Failed to fetch logs:", str(e))
        return []

# --- Main loop ---
def main():
    print("[INFO] Starting ML IDS with Loki integration...")
    while True:
        log_lines = fetch_logs_from_loki()
        for line in log_lines:
            print(f"[DEBUG] Raw log line: {line.strip()}")
            print(f"[DEBUG] Parsed features: {parse_line(line)}")
            features = parse_line(line)
            print(features)
            if features is not None:
                prediction = model.predict(features)
                if prediction[0] == -1:
                    print("\U0001F6A8 Anomaly Detected:", line.strip())
                else:
                    print("No Anomaly found ...")
        time.sleep(FETCH_INTERVAL)

if __name__ == '__main__':
    main()
