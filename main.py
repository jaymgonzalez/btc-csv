import pandas as pd
from scipy.signal import savgol_filter
from scipy.signal import find_peaks


def addPosition(csvPath):
    df = pd.read_csv(csvPath, index_col=0)

    df["close_smooth"] = savgol_filter(df.close, 49, 8)
    df["close_smooth"] = round(df.close_smooth, 2)

    atr = df.atr.iloc[-1]

    peaks_idx, peaks_dict = find_peaks(
        df.close_smooth, distance=15, width=3, prominence=atr * 1.3
    )
    troughs_idx, troughs_dict = find_peaks(
        -1 * df.close_smooth, distance=15, width=3, prominence=atr * 1.3
    )

    print(peaks_dict)
    print(troughs_dict)

    # Create a new column in the DataFrame called "position" if not existent
    if "position" not in df.columns:
        df["position"] = 0

    # Set position values based on long and short signals
    df["position"].iloc[peaks_idx] = -1
    df["position"].iloc[troughs_idx] = 1

    # Adjust the position column to hold the most recent position until there is a signal to go in the other direction
    prev_pos = 0
    for i in range(len(df)):
        if df.iloc[i]["position"] != 0:
            prev_pos = df.iloc[i]["position"]
        else:
            df.iloc[i, df.columns.get_loc("position")] = prev_pos

    df.to_csv(csvPath)


# addPosition("1h_bybit.csv")

# def findSR(timeFrame):

#     return
