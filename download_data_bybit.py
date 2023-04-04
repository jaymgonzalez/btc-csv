import pandas as pd
import pandas_ta as ta
from bybit_api_functions import getKlineData
import time


def getCustomData(number_of_entries=800, intervalInMinutes=60):
    # Calculate the epoch time for n hours ago
    start_time = int(time.time() - number_of_entries * intervalInMinutes * 60) * 1000

    # Initialize the list to store all the entries
    all_entries = []

    # Loop until we've retrieved all the entries
    while True:
        # Make the API request with the appropriate query parameters
        data = getKlineData(start_time, interval=intervalInMinutes)

        # Check if we received any new entries
        if len(data) == 1:
            break

        # Add the new entries to our list
        all_entries.extend(data)

        # Update the starting time for the next batch
        start_time = int(data[0][0])

    return all_entries


def downloadData(number_of_entries=400, interval=15, row=False):

    data = getCustomData(number_of_entries, interval)

    df = tidyData(data)

    # print(df)

    if row:
        df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
        csv_df = pd.read_csv(f"{interval}m_bybit.csv", index_col=0)
        csv_df.reset_index(inplace=True, drop=True)
        csv_df["open_time"] = pd.to_datetime(csv_df["open_time"], unit="ms")
        csv_df["open_time"] = csv_df["open_time"].apply(
            lambda x: int(x.timestamp() * 1000)
        )
        # print(csv_df)
        df = pd.concat([csv_df, df])

    # print(type(df["open_time"]))
    df.drop_duplicates("open_time", inplace=True)
    df.sort_values("open_time", inplace=True)
    df.set_index("open_time", inplace=True)
    print(df)
    # df.to_csv(f"{interval}m_bybit.csv")


def tidyData(data):
    df = pd.DataFrame(
        data, columns=["open_time", "open", "high", "low", "close", "vol", "turn_over"]
    )

    df = df[["open_time", "open", "high", "low", "close"]]

    df["open"] = df.open.astype(float)
    df["high"] = df.high.astype(float)
    df["low"] = df.low.astype(float)
    df["close"] = df.close.astype(float)

    return df


# def drop_na_duplicates(df, column="open_time"):
#     # Remove duplicates and short df

#     # print(df)
#     return df


def calculate_atr(df):
    ## take the rolling atr so the yaxis doesn't shake too much
    df["atr"] = ta.atr(
        high=df.high, low=df.low, close=df.close, length=16, mamode="WMA"
    )
    df["atr"] = round(df.atr, 2)

    return df


# downloadData()
downloadData(number_of_entries=2, row=True)
