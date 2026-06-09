import pandas as pd
from pathlib import Path
import json


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent / 'data' / 'raw_data.json'
columns_names_to_drop = ['weather', 'weather_icon']
columns_names_to_rename = {
    'base': 'base',
    'visibility': 'visibility',
    'dt': 'datetime',
    'timezone': 'timezone',
    'id': 'city_id',
    'name': 'city_name',
    'cod': 'code',
    'coord.lon': 'longitude',
    'coord.lat': 'latitude',
    'main.temp': 'temperature',
    'main.feels_like': 'feels_like',
    'main.temp_min': 'temp_min',
    'main.temp_max': 'temp_max',
    'main.pressure': 'pressure',
    'main.humidity': 'humidity',
    'main.sea_level': 'sea_level',
    'main.grnd_level': 'grnd_level',
    'wind.speed': 'wind_speed',
    'wind.deg': 'wind_deg',
    'wind.gust': 'wind_gust',
    'clouds.all': 'clouds',
    'sys.type': 'sys_type',
    'sys.id': 'sys_id',
    'sys.country': 'country',
    'sys.sunrise': 'sunrise',
    'sys.sunset': 'sunset'
}
columns_names_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_dataframe(path_name:str) -> pd.DataFrame:
    """
    Creates a DataFrame from the given input path.

    Args:
        input_path (str): The path to the input JSON file.
    """
    logging.info(f"Creating DataFrame from {path_name}")

    path = path_name
    if not path.exists():
        raise FileNotFoundError(f"The file {path} does not exist.")
    
    with open(path) as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    logging.info(f"DataFrame created successfully with length {len(df)}.")
    return df


def normalize_dataframe(df: pd.DataFrame, columns_to_drop: list[str]) -> pd.DataFrame:
    """
    Normalizes the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be normalized.

    Returns:
        pd.DataFrame: The normalized DataFrame.
    """
    logging.info("Normalizing DataFrame.")
    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather  = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1).drop(columns=columns_names_to_drop)

    logging.info("DataFrame normalized successfully.")
    return df


def rename_columns (df: pd.DataFrame, columns_names:dict[str, str]) -> pd.DataFrame:
    """
    Renames the columns of the given DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to be renamed.

    Returns:
        pd.DataFrame: The renamed DataFrame.
    """
    logging.info("Renaming DataFrame columns.")
    
    df = df.rename(columns=columns_names_to_rename)

    logging.info("DataFrame columns renamed successfully.")
    return df


def normalize_datetime(df: pd.DataFrame, column_name: list[str]) -> pd.DataFrame:
    logging.info("Normalizing datetime columns.")
    for name in column_name:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
        logging.info(f"Datetime column {name} normalized successfully.")
    
    logging.info("Datetime columns normalized successfully.")
    return df

def data_transformation():
    df = create_dataframe(path_name)
    df = normalize_dataframe(df, columns_names_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime(df, columns_names_to_normalize_datetime)

    output_path = 'data/transformed_data.csv'
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)
    logging.info(f"Data transformed and saved to {output_path}")

if __name__ == "__main__":
    data_transformation()