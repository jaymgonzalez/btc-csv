from pybit import usdt_perpetual
import configparser
import os
import datetime
import time

one_month_ago = datetime.datetime.now() - datetime.timedelta(hours=199)
epoch_time = int(time.mktime(one_month_ago.timetuple()))


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
endpoint = 'https://api.bybit.com'

session = usdt_perpetual.HTTP(endpoint,api_key,api_secret)

data = session.query_kline(symbol='BTCUSDT',interval='60',from_time=epoch_time)

print(data)