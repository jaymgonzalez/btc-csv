from binance.client import Client
import pandas as pd
import pandas_ta as ta
from scipy.signal import savgol_filter
from scipy.signal import find_peaks

client = Client()

# ETH
# klines = client.get_historical_klines("ETHUSDT", Client.KLINE_INTERVAL_1HOUR, "6 months ago UTC")

# BTC
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1HOUR, "6 months ago UTC")

df = pd.DataFrame(klines, columns = ["open_time", "open", "high", "low", "close", "vol", "close_time", "quote_vol", \
                                    "trades", "taker_base_vol", "taker_quote_vol", "ignore"])

df = df[["open_time","open", "high", "low", "close"]]

df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

df["open"] = df.open.astype(float)
df["high"] = df.high.astype(float)
df["low"] = df.low.astype(float)
df["close"] = df.close.astype(float)

## take the rolling atr so the yaxis doesn't shake too much
df["atr"] = ta.atr(high=df.high, low=df.low, close=df.close)
df["atr"] = df.atr.rolling(window=30).mean()

df.set_index("open_time", inplace=True)

df2 = df

df2["close_smooth"] = savgol_filter(df2.close, 49, 5)

atr = df2.atr.iloc[-1]

peaks_idx, _ = find_peaks(df2.close_smooth, distance=15, width=3, prominence=atr)
troughs_idx, _ = find_peaks(-1*df2.close_smooth, distance=15, width=3, prominence=atr)


print(peaks_idx)
print(troughs_idx)