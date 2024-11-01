import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

from src.eth_staking import get_staking_rates
from config.config import Config

config = Config()
load_dotenv()

username = os.getenv('DB_USER')
password = os.getenv("DB_PASS")
endpoint = config.SQL_ENDPOINT
database = config.DB_NAME

def ensure_seconds_timestamp(x):
    if isinstance(x, pd.Timestamp):
        return int(x.timestamp())  # Convert pd.Timestamp to Unix time in seconds
    elif isinstance(x, int) and len(str(x)) > 10:
        return int(x / 1000)  # Convert milliseconds to seconds if needed
    return x  # Return as is if already in seconds

def lambda_handler(event, context):
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{endpoint}/{database}')

    existing_df = pd.read_sql("SELECT * FROM eth_staking;", engine)
    
    new_df = get_staking_rates(existing_df)

    existing_df['date'] = existing_df['date'].apply(ensure_seconds_timestamp)
    new_df['date'] = new_df['date'].apply(ensure_seconds_timestamp)

    merged_df = pd.merge(new_df, existing_df, on=['date', 'apr'], how='left', indicator=True)
    new_rows_df = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not new_rows_df.empty:
        new_rows_df.to_sql('eth_staking', engine, if_exists='append', index=False)
        print("New rows added to the database.")
    else:
        print("No new rows to add.")

    print(new_df)  # Optionally print the updated DataFrame
    return event

lambda_handler(0, 0)

