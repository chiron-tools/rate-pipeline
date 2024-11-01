import pandas as pd

def ensure_seconds_timestamp(x):
    if isinstance(x, pd.Timestamp):
        return int(x.timestamp())  # Convert pd.Timestamp to Unix time in seconds
    elif isinstance(x, int) and len(str(x)) > 10:
        return int(x / 1000)  # Convert milliseconds to seconds if needed
    return x  # Return as is if already in seconds

