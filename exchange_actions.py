from pybit.spot import HTTP as spot_session
import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
endpoint = 'https://api.bybit.com'

test_api_key = config.get('BYBIT_TEST', 'API_KEY', fallback='') or os.environ.get("TEST_API_KEY")
test_api_secret = config.get('BYBIT_TEST', 'API_SECRET', fallback='') or os.environ.get("TEST_API_SECRET")


print(test_api_key)
print(test_api_secret)

# For ease of use, create abstraction layer to use `auth_required` functions. 
# To use actual API, use `is_testnet` = False
class SpotManager:
    def __init__(self, api_key: str, api_secret: str, is_testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint
        if is_testnet:
            self.endpoint = 'https://api.bybit.com'
            self.api_key = test_api_key
            self.api_secret = test_api_secret
        self.session = spot_session(
            endpoint=self.endpoint,
            api_key=api_key,
            api_secret=api_secret,
            # recv_window=10000
        )

spot_manager = SpotManager(api_key, api_secret, is_testnet=False)
data = spot_manager.session.wal

print(data)