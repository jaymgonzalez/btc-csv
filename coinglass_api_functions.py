import requests
import configparser
import os


config = configparser.ConfigParser()
config.read("config.ini")

api_key = config.get("COINGLASS", "API_KEY", fallback="") or os.environ.get(
    "COINGLASS_API_KEY"
)


url = "https://open-api.coinglass.com/public/v2/indicator/top_long_short_position_ratio?ex=binance&pair=BTCUSDT&interval=h1&start_time=1668481704000&end_time=1681988502000"

headers = {
    "accept": "application/json",
    "coinglassSecret": api_key,
}

response = requests.get(url, headers=headers)

print(response.text)
