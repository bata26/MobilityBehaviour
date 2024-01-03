import logging
from typing import Any
from requests import post, exceptions
import pandas as pd

if __name__ == '__main__':
    
    # Carica il file CSV
    nome_file = './data/mobilityShoes/smartShoeSensors.csv'  # Assicurati di inserire il nome corretto del tuo file CSV
    dataframe = pd.read_csv(nome_file)
    list = dataframe.values.tolist()
    result = []
    for item in list:
        json = {
            "uuid":item[0],
            "time_series":item[1:]
        }
        result.append(json)

    print(result[2])   
    
    connection_string = f'http://127.0.0.1:4000/record'
    try:
        response = post(url=connection_string, json=result[2])
    except exceptions.RequestException:
        logging.error(f'{connection_string} unreachable')
        exit(-1)

    if response.status_code != 200:
        error_message = response.json()['error']
        logging.error(f'Error: {error_message}')
        exit(-1)
