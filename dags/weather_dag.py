from airflow.decorators import dag, task
from datetime import datetime, timedelta
from pathlib import Path
import sys, os

sys.path.insert(0, '/opt/airflow/src')

from extract_data import extract_weather_data
from transform_data import data_transformation
from load_data import load_weather_data
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

api_key = os.getenv('api_key')
url = f"https://api.openweathermap.org/data/2.5/weather?q=Minas Gerais,BR&units=metric&appid={api_key}"

@dag(
    dag_id='weather_etl_pipeline',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    },
    description = 'Pipeline Weather - MG',
    schedule='0 */1 * * *',
    start_date=datetime(2026, 6, 13),
    catchup=False,
    tags=['weather']
)
def weather_pipeline():
    @task
    def extract():
        extract_weather_data(url)

    @task
    def transform():
        df = data_transformation()
        df.to_parquet('/opt/airflow/data/temp_data.parquet', index=False)
        return data_transformation()

    @task
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/temp_data.parquet')
        load_weather_data('mg_weather', df)

    extract() >> transform() >> load()

weather_pipeline()