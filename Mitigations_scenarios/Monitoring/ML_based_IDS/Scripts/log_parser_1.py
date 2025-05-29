import re
import numpy as np

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

    # Ignore anything else (like coil status)
    return None

