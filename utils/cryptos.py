import requests
import os

# Return the value in USD of BTC currently
def get_BTCUSD_rate():
    URL = "https://rest.coinapi.io/v1/exchangerate/BTC/USD"
    HEADERS = {
                'Accept': 'text/plain',
                 'Authorization':os.getenv('COIN_API_KEY')
              }
    
    response = requests.get(url=URL, headers=HEADERS)

    return response.json()['rate']


# Return the value in USD of ETH currently
def get_ETHUSD_rate():
    URL = "https://rest.coinapi.io/v1/exchangerate/ETH/USD"
    HEADERS = {
                'Accept': 'text/plain',
                 'Authorization':os.getenv('COIN_API_KEY')
              }
    
    response = requests.get(url=URL, headers=HEADERS)

    return response.json()['rate']