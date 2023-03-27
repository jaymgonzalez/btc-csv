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

