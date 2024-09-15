import requests
import os

def get_coin_usd(coin):
    URL = f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD"
    HEADERS = {
                'Accept': 'text/plain',
                 'Authorization':os.getenv('COIN_API_KEY')
              }
    
    response = requests.get(url=URL, headers=HEADERS)

    return response.json()['rate']