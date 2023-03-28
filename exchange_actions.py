import configparser
import os
import pandas as pd


config = configparser.ConfigParser()
config.read('config.ini')

api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
endpoint = 'https://api.bybit.com'

test_api_key = config.get('BYBIT_TEST', 'API_KEY', fallback='') or os.environ.get("TEST_API_KEY")
test_api_secret = config.get('BYBIT_TEST', 'API_SECRET', fallback='') or os.environ.get("TEST_API_SECRET")


# print(test_api_key)
# print(test_api_secret)

def getPosition(csvPath='1h.csv'):
    df = pd.read_csv(csvPath)
    
    num_rows, num_cols = df.shape
    
    # Get the value of the last column and last row
    last_value = df.iloc[num_rows - 1, num_cols - 1]
    
    # Return the last value
    return 'Buy' if last_value == 1 else 'Sell'

print(getPosition())