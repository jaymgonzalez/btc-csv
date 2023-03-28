import requests
import time
import hashlib
import hmac
import uuid
import configparser
import os
import json

def apiKeys(useTest=True):
    config = configparser.ConfigParser()
    config.read('config.ini')

    if useTest:
        api_key = config.get('BYBIT_TEST', 'API_KEY', fallback='') or os.environ.get("TEST_API_KEY")
        api_secret = config.get('BYBIT_TEST', 'API_SECRET', fallback='') or os.environ.get("TEST_API_SECRET")
        url="https://api-testnet.bybit.com"
    else:
        api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
        api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
        url = 'https://api.bybit.com'
        
    return api_key, api_secret, url

api_key, api_secret, url = apiKeys()

httpClient=requests.Session()
recv_window=str(5000)

def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': api_key,
        'X-BAPI-SIGN': signature,
        'X-BAPI-SIGN-TYPE': '2',
        'X-BAPI-TIMESTAMP': time_stamp,
        'X-BAPI-RECV-WINDOW': recv_window,
        'Content-Type': 'application/json'
    }
    if(method=="POST"):
        response = httpClient.request(method, url+endPoint, headers=headers, data=payload)
    else:
        response = httpClient.request(method, url+endPoint+"?"+payload, headers=headers)
    print(Info + " Response Time : " + str(response.elapsed))
    text = json.loads(response.text)
    if response.status_code == 200 and text['retMsg'] == 'OK':
        return text
    else: 
        raise ValueError(text)

def genSignature(payload):
    param_str= str(time_stamp) + api_key + recv_window + payload
    hash = hmac.new(bytes(api_secret, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature

def walletBalance(coin='USDT',accType='CONTRACT'):
    endpoint="/v5/account/wallet-balance"
    method="GET"
    params=f'accountType={accType}&coin={coin}';
    response = HTTP_Request(endpoint,method,params,"Balance")
    return response['result']['list'][0]['coin'][0]['walletBalance']

def getLatestPrice(symbol='BTCUSDT'):
    endpoint="/v5/market/kline"
    method="GET"
    params=f'category=linear&symbol={symbol}&interval=1&limit=1';
    response = HTTP_Request(endpoint,method,params,"price")
    return response['result']['list'][0][4]

def coinQty(totalPercentage=99,symbol='BTCUSDT'):
    coinPrice = float(getLatestPrice(symbol))
    balance = float(walletBalance())
    available = balance * (totalPercentage / 100)
    qty = available / coinPrice
    return round(qty, 4)

def createOrder(side, symbol='BTCUSDT'):
    qty = str(coinQty(50))
    endpoint="/v5/order/create"
    orderLinkId=uuid.uuid4().hex
    method="POST"
    params='{"category":"linear","symbol":"' + symbol + '","orderType":"Market","side":"' + side + '","orderLinkId":"' +  orderLinkId + '","qty":"' + qty + '","timeInForce":"GTC"}';
    HTTP_Request(endpoint,method,params,"Create")
    print(f'Position created! symbol: {symbol}, side: {side}, qty: {qty}')
    
def openPosition(symbol='BTCUSDT'):
    endpoint="/v5/position/list"
    method="GET"
    params=f'category=linear&symbol={symbol}';
    response = HTTP_Request(endpoint,method,params,"Orders")
    if response['result']['list'][0]['size'] == '0.000':
        return 0, 0
    else:
        position = response['result']['list'][0]
        return position['side'], position['size']
    
def closePosition(symbol='BTCUSDT'):
    currentSide, qty = openPosition(symbol)
    side = 'Buy' if currentSide == 'Sell' else 'Sell'
    endpoint="/v5/order/create"
    method="POST"
    params='{"category":"linear","symbol":"' + symbol + '","orderType":"Market","qty":"' + qty + '","reduceOnly":"true","side":"' + side + '"}';
    HTTP_Request(endpoint,method,params,"Close")
    print(f'Position closed! symbol: {symbol}, side: {side}, qty: {qty}')

def getHourlyData(symbol='BTCUSDT'):
    endpoint="/v5/market/kline"
    method="GET"
    params=f'category=linear&symbol={symbol}&interval=60';
    response = HTTP_Request(endpoint,method,params,"price")
    return response['result']['list']
