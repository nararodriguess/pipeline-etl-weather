from sqlalchemy import create_engine, text
# for encoding the password in the connection string
from urllib.parse import quote_plus 
import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from the .env file
env_path = Path(__file__).resolve().parent.parent / 'config' / '.env' #../config/.env
load_dotenv(env_path)

user = os.getenv('user')
password = os.getenv('password')
database = os.getenv('database')
host = '172.31.80.1' #'host.docker.internal' # Use this for Docker, otherwise use 'localhost' or the actual host IP

def get_engine ():
    # Create the connection string
    logging.info(f"Connecting in {host}: 5432/{database}.")
    return create_engine(
        f"postgresql://{user}:{quote_plus(password)}@{host}:5432/{database}"
    )

engine = get_engine()

def load_weather_data(table_name:str, df):
    """
    Load data into the database.
    Args:
        table_name (str): The name of the table to load data into.
        df (pd.DataFrame): The DataFrame containing the data to be loaded.
    """
    try:
        df.to_sql(
            name=table_name, 
            con=engine, 
            if_exists='append', 
            index=False
        )
        logging.info(f"Data loaded successfully into {table_name} table.")

        with engine.connect() as connection:
            result = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            logging.info(f"Total rows in {table_name}: {count}")

    except Exception as e:
        logging.error(f"Error loading data into {table_name} table: {e}")



if __name__ == "__main__":
    df = pd.read_csv('data/transformed_data.csv')
    load_weather_data('mg_weather', df)