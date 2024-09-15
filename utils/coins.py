import requests
import os

def get_coin_usd(coin):
    URL = f"https://rest.coinapi.io/v1/exchangerate/{coin}/USD"
    HEADERS = {
                'Accept': 'text/plain',
                 'Authorization':os.getenv('COIN_API_KEY')
              }
    
    response = requests.get(url=URL, headers=HEADERS)

    json = response.json()
    if 'rate' in json.keys():
        return json['rate']        
    else:
        raise Exception(f'Impossible to get the price of this coin ({coin})')   
    