import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
endpoint = 'https://api.bybit.com'

test_api_key = config.get('BYBIT_TEST', 'API_KEY', fallback='') or os.environ.get("TEST_API_KEY")
test_api_secret = config.get('BYBIT_TEST', 'API_SECRET', fallback='') or os.environ.get("TEST_API_SECRET")


# print(test_api_key)
# print(test_api_secret)

