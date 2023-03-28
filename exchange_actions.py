import pandas as pd
from bybit_api_functions import openPosition, closePosition, createOrder

def getCsvPosition(csvPath='1h.csv'):
    df = pd.read_csv(csvPath)
    
    num_rows, num_cols = df.shape
    
    # Get the value of the last column and last row
    last_value = df.iloc[num_rows - 1, num_cols - 1]
    
    # Return the last value
    return 'Buy' if last_value == 1 else 'Sell'

csvPositionSide = getCsvPosition()
openPositionSide, _ = openPosition()

if openPositionSide == 0:
    createOrder(csvPositionSide)
elif openPositionSide != csvPositionSide:
    closePosition()
    createOrder(csvPositionSide)
