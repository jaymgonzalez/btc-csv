import pandas as pd
from main import addPosition
from bybit_api_functions import openPosition, closePosition, createOrder

atr_threshold = 70


def getLastTickData(csvPath="15m_bybit.csv"):
    df = pd.read_csv(csvPath)

    pos = df.position.iloc[-1]

    atr = df.atr.iloc[-1]

    # Return the last value
    return "Buy" if pos == 1 else "Sell", atr


def positionManagement():

    csv_pos, atr = getLastTickData()
    openPositionSide, _ = openPosition()

    if openPositionSide == 0 and atr > atr_threshold:
        createOrder(csv_pos)
    elif openPositionSide != csv_pos and atr > atr_threshold:
        closePosition()
        createOrder(csv_pos)
    elif openPositionSide != 0 and atr < atr_threshold:
        closePosition()


addPosition("15m_bybit.csv")
positionManagement()
