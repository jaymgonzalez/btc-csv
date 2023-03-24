import pandas as pd
import pandas_ta as ta
from binance.client import Client

client = Client()

# BTC
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "1 hour ago UTC")

row = pd.DataFrame(klines, columns = ["open_time", "open", "high", "low", "close", "vol", "close_time", "quote_vol", "trades", "taker_base_vol", "taker_quote_vol", "ignore"])

row = row[["open_time","open", "high", "low", "close"]]

row["open_time"] = pd.to_datetime(row["open_time"], unit="ms")

row["open"] = row.open.astype(float)
row["high"] = row.high.astype(float)
row["low"] = row.low.astype(float)
row["close"] = row.close.astype(float)

row.set_index("open_time", inplace=True)

df = pd.read_csv('1h.csv', index_col=0)

# print(row.index[0])
# print(df.index[-1])

if str(df.index[-1]) != str(row.index[0]):
  new_df = pd.concat([df, row])
  new_df["atr"] = ta.atr(high=new_df.high, low=new_df.low, close=new_df.close)
  new_df["atr"] = new_df.atr.rolling(window=30).mean()
  
  new_df.to_csv('1h.csv')




