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

def lambda_handler(event, context):
    engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{endpoint}/{database}')

    df = pd.read_sql("SELECT * FROM eth_staking;", engine)
    print(df)
    return event 

lambda_handler(0,0)
