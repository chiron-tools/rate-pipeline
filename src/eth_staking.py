import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import time
import logging

logging.basicConfig(level=logging.INFO)


API_FORMAT = "https://beaconcha.in/api/v1/ethstore/{}"
DAY_ZERO = datetime(2020, 12, 1, tzinfo=timezone.utc)
REQ_LIMIT = 10
REWARDS_FILE = 'rewards.csv'

# Helper functions
def fetch_api_data(days_since_start):
    """Fetch APR data from the API for a given day offset."""
    url = API_FORMAT.format(days_since_start)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'OK' and data.get('data'):
            return float(data['data']['apr'])
        return 0
    except requests.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return None

def days_since_day_zero(date):
    """Calculate the number of days since DAY_ZERO."""
    return (date - DAY_ZERO).days


def update_data_frame(df):
    """Fetch new data and update DataFrame."""
    last_date = df['date'].max() if not df.empty else DAY_ZERO - timedelta(days=1)
    end_date = datetime.now(timezone.utc)
    num_requests = 0

    new_data = []
    for single_date in pd.date_range(start=last_date + timedelta(days=1), end=end_date, freq='D'):
        if num_requests >= REQ_LIMIT:
            break
        day_count = days_since_day_zero(single_date)
        apr = fetch_api_data(day_count)
        if apr is not None:
            new_data.append({'date': single_date, 'apr': apr})
            num_requests += 1

    if new_data:
        new_df = pd.DataFrame(new_data)
        df = pd.concat([df, new_df], ignore_index=True)

    return df

def get_staking_rates(df):

    df['date'] = pd.to_datetime(df['date'], unit='s', utc=True)
    df = update_data_frame(df)
    df = df[df['apr'] != 0.0]
    #df.to_csv(REWARDS_FILE, index=False)
    return df

if __name__ == '__main__':
    get_staking_rates()
