from pybit.spot import HTTP as spot_session
import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
endpoint = 'https://api.bybit.com'



# For ease of use, create abstraction layer to use `auth_required` functions. 
# To use actual API, use `is_testnet` = False
class SpotManager:
    def __init__(self, api_key: str, api_secret: str, is_testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.endpoint = endpoint
        if is_testnet:
            self.endpoint = 'https://api-testnet.bybit.com'
        self.session = spot_session(
            endpoint=self.endpoint,
            api_key=api_key,
            api_secret=api_secret
        )

spot_manager = SpotManager(api_key, api_secret, is_testnet=False)
data = spot_manager.session.get_wallet_balance()

print(data + "test")