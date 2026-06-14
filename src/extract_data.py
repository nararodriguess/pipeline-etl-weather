import requests
import json
from pathlib import Path


import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def extract_weather_data(url:str) -> list:
    """
    Extracts data from the given URL and returns it as a list of dictionaries.

    Args:
        url (str): The URL to extract data from.

    Returns:
        list: A list of dictionaries containing the extracted data.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        output_path = 'data/raw_data.json'
        output_dir = Path(output_path).parent
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=4)

        logging.info(f"Data successfully extracted and saved to {output_path}")
        return data

    if not data:
        logging.warning("No data found in the response.")
        return []

    else:
        logging.error(f"Failed to retrieve data. Status code: {response.status_code}")
        return []
