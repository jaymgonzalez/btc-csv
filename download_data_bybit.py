import pandas as pd
import pandas_ta as ta
from bybit_api_functions import getHourlyData
import time


def getCustomHourlyData(number_of_hours=800):
    # Calculate the epoch time for n hours ago
    start_time = int(time.time() - number_of_hours * 3600) * 1000

    # Initialize the list to store all the entries
    all_entries = []

    # Loop until we've retrieved all the entries
    while True:
        # Make the API request with the appropriate query parameters
        data = getHourlyData(start_time)

        # Check if we received any new entries
        if len(data) == 1:
            break

        # Add the new entries to our list
        all_entries.extend(data)

        # Update the starting time for the next batch
        start_time = int(data[0][0])

    return all_entries


data = getCustomHourlyData()

df = pd.DataFrame(
    data, columns=["open_time", "open", "high", "low", "close", "vol", "turn_over"]
)

df = df[["open_time", "open", "high", "low", "close"]]

# Remove duplicates and short df
df = df.drop_duplicates("open_time")
df = df.sort_values("open_time")
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

df.to_csv("1h_bybit.csv")
