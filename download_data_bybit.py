import pandas as pd
import pandas_ta as ta
from bybit_api_functions import getKlineData, getOpenInterest, getFundingRate
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
import time


def getCustomData(number_of_entries=800, intervalInMinutes=60, function=getKlineData):
    # Calculate the epoch time for n hours ago
    start_time = int(time.time() - number_of_entries * intervalInMinutes * 60) * 1000

    # Initialize the list to store all the entries
    all_entries = []

    if function == getFundingRate:
        data = function(startTime=start_time)
        return data
    # Loop until we've retrieved all the entries
    while True:
        # Make the API request with the appropriate query parameters
        data = function(startTime=start_time, interval=intervalInMinutes)

        # Check if we received any new entries
        if len(data) == 1:
            break

        # Add the new entries to our list
        all_entries.extend(data)

        # Update the starting time for the next batch
        if function == getOpenInterest:
            start_time = int(data[0]["timestamp"])
        else:
            start_time = int(data[0][0])

    return all_entries


def downloadData(number_of_entries=400, interval=15, row=False):
    data = getCustomData(number_of_entries, interval)

    df = tidyData(data)

    if row:
        csv_df = pd.read_csv(f"{interval}m_bybit.csv", index_col=0)
        csv_df.reset_index(inplace=True)
        csv_df["open_time"] = pd.to_datetime(csv_df["open_time"])
        csv_df["open_time"] = csv_df["open_time"].apply(
            lambda x: int(x.timestamp() * 1000)
        )
        df = pd.concat([csv_df, df])

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.sort_values("open_time", inplace=True)
    df.drop_duplicates("open_time", inplace=True, keep="last")
    df.set_index("open_time", inplace=True)

    return df


def createDf(interval=15, row=True):
    df = downloadData(interval=interval, row=row)
    df = calculate_atr(df)
    df = addPosition(df)
    # df = addOpenInterest(df)
    # df = addFundingRate(df)
    df = addAdx(df)

    # df = df.drop(["fr", "oi"], axis=1)

    df.to_csv(f"{interval}m_bybit.csv")


def tidyData(data):
    df = pd.DataFrame(
        data, columns=["open_time", "open", "high", "low", "close", "vol", "turn_over"]
    )

    df = df[["open_time", "open", "high", "low", "close"]]

    df["open"] = df.open.astype(float)
    df["high"] = df.high.astype(float)
    df["low"] = df.low.astype(float)
    df["close"] = df.close.astype(float)
    df["position"] = pd.Series(dtype="float64")

    return df


def calculate_atr(df, length=16):
    df["atr"] = ta.atr(
        high=df.high, low=df.low, close=df.close, length=length, mamode="WMA"
    ).round(2)

    return df


def addOpenInterest(df):
    data = getCustomData(
        number_of_entries=400, intervalInMinutes=15, function=getOpenInterest
    )

    data_dict = {}
    for item in data:
        data_dict[item["timestamp"]] = round(float(item["openInterest"]), 2)

    new_df = pd.DataFrame.from_dict(data_dict, orient="index", columns=["oi"])
    new_df.index = pd.to_datetime(new_df.index, unit="ms")

    df = df.merge(new_df, how="left", left_index=True, right_index=True)

    df = df.rename(columns={"oi_y": "oi"})
    if "oi_x" in df:
        df.drop("oi_x", axis=1, inplace=True)

    return df


def addFundingRate(df):
    data = getCustomData(
        number_of_entries=400, intervalInMinutes=15, function=getFundingRate
    )

    data_dict = {}
    for item in data:
        data_dict[item["fundingRateTimestamp"]] = round(
            float(item["fundingRate"]) * 100, 5
        )

    new_df = pd.DataFrame.from_dict(data_dict, orient="index", columns=["fr"])
    new_df.index = pd.to_datetime(new_df.index, unit="ms")

    df = df.merge(new_df, how="left", left_index=True, right_index=True)

    df = df.rename(columns={"fr_y": "fr"})
    if "fr_x" in df:
        df.drop("fr_x", axis=1, inplace=True)

    df.fillna(method="ffill", inplace=True)

    return df


def addAdx(df):
    adx = ta.adx(df["high"], df["low"], df["close"], length=14).round(2)
    if "ADX_14" in df.columns:
        df.update(adx)
    else:
        df = df.join(adx)

    return df


def addPosition(df):
    df["close_smooth"] = savgol_filter(df.close, 49, 8).round(2)

    atr = df.atr.iloc[-1]

    peaks_idx, peaks_dict = find_peaks(
        df.close_smooth, distance=15, width=3, prominence=atr * 1.3
    )
    troughs_idx, troughs_dict = find_peaks(
        -1 * df.close_smooth, distance=15, width=3, prominence=atr * 1.3
    )

    # Set position values based on long and short signals
    df["position"].iloc[0] = 0
    df["position"].iloc[peaks_idx] = -1
    df["position"].iloc[troughs_idx] = 1

    df.fillna(method="ffill", inplace=True)

    return df


if __name__ == "__main__":
    createDf()
