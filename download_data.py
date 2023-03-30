import pandas as pd
import pandas_ta as ta
from binance.client import Client

client = Client()

# BTC
klines = client.get_historical_klines(
    "BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 month ago UTC"
)

df = pd.DataFrame(
    klines,
    columns=[
        "open_time",
        "open",
        "high",
        "low",
        "close",
        "vol",
        "close_time",
        "quote_vol",
        "trades",
        "taker_base_vol",
        "taker_quote_vol",
        "ignore",
    ],
)

df = df[["open_time", "open", "high", "low", "close"]]

print(df)


df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

df["open"] = df.open.astype(float)
df["high"] = df.high.astype(float)
df["low"] = df.low.astype(float)
df["close"] = df.close.astype(float)

## take the rolling atr so the yaxis doesn't shake too much
df["atr"] = ta.atr(high=df.high, low=df.low, close=df.close)
df["atr"] = df.atr.rolling(window=30).mean()

df.set_index("open_time", inplace=True)

df.to_csv("1h.csv")
