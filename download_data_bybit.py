from pybit import inverse_perpetual
import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
endpoint = 'https://api.bybit.com'

session = inverse_perpetual.HTTP(endpoint,api_key,api_secret)

session.orderbook(symbol='BTCUSD')