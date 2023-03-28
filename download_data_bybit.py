import pandas as pd
import pandas_ta as ta
from bybit_api_functions import getHourlyData
from main import addPosition
# import datetime
# import time


# total_hours = datetime.datetime.now() - datetime.timedelta(hours=699)
# epoch_time = int(time.mktime(total_hours.timetuple())) * 1000

# print(epoch_time)

data = getHourlyData()

df = pd.DataFrame(data, columns=['open_time','open','high','low','close','vol','turn_over'])

df = df[["open_time","open", "high", "low", "close"]]

df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

df.set_index("open_time", inplace=True)

df = df.iloc[::-1]

df["open"] = df.open.astype(float)
df["high"] = df.high.astype(float)
df["low"] = df.low.astype(float)
df["close"] = df.close.astype(float)

## take the rolling atr so the yaxis doesn't shake too much
df["atr"] = ta.atr(high=df.high, low=df.low, close=df.close)
df["atr"] = df.atr.rolling(window=30).mean()

df.to_csv('1h_bybit.csv')

addPosition('1h_bybit.csv')
