import pandas as pd
import pandas_ta as ta
from bybit_api_functions import getHourlyData
from main import addPosition
import time
# import datetime


# total_hours = datetime.datetime.now() - datetime.timedelta(hours=699)
# epoch_time = int(time.mktime(total_hours.timetuple())) * 1000

# print(epoch_time)

data = getHourlyData()


print(data)
# def get_last_n_entries(number_of_hours):
#     # Calculate the epoch time for n hours ago
#     start_time = int(time.time()) - number_of_hours * 3600 * 1000

#     # Initialize the list to store all the entries
#     all_entries = []

#     # Loop until we've retrieved all the entries
#     while True:
#         # Make the API request with the appropriate query parameters
#         api_url = "https://your-api-url.com/your-endpoint"
#         query_params = {"since": starting_time, "limit": batch_size}
#         response = requests.get(api_url, params=query_params)

#         # Check if we received any new entries
#         new_entries = response.json()
#         if len(new_entries) == 0:
#             break

#         # Add the new entries to our list
#         all_entries.extend(new_entries)

#         # Update the starting time for the next batch
#         starting_time = new_entries[-1]['timestamp']

#     return all_entries






# df = pd.DataFrame(data, columns=['open_time','open','high','low','close','vol','turn_over'])

# df = df[["open_time","open", "high", "low", "close"]]

# df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")

# df.set_index("open_time", inplace=True)

# df = df.iloc[::-1]

# df["open"] = df.open.astype(float)
# df["high"] = df.high.astype(float)
# df["low"] = df.low.astype(float)
# df["close"] = df.close.astype(float)

# ## take the rolling atr so the yaxis doesn't shake too much
# df["atr"] = ta.atr(high=df.high, low=df.low, close=df.close)
# df["atr"] = df.atr.rolling(window=30).mean()

# df.to_csv('1h_bybit.csv')
