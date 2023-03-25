import requests
import time
import hashlib
import hmac
import uuid
import configparser
import os


config = configparser.ConfigParser()
config.read('config.ini')

# api_key = config.get('BYBIT', 'API_KEY', fallback='') or os.environ.get("API_KEY")
# api_secret = config.get('BYBIT', 'API_SECRET', fallback='') or os.environ.get("API_SECRET")
# endpoint = 'https://api.bybit.com'

test_api_key = config.get('BYBIT_TEST', 'API_KEY', fallback='') or os.environ.get("TEST_API_KEY")
test_api_secret = config.get('BYBIT_TEST', 'API_SECRET', fallback='') or os.environ.get("TEST_API_SECRET")
httpClient=requests.Session()
recv_window=str(5000)
url="https://api-testnet.bybit.com" # Testnet endpoint

def HTTP_Request(endPoint,method,payload,Info):
    global time_stamp
    time_stamp=str(int(time.time() * 10 ** 3))
    signature=genSignature(payload)
    headers = {
        'X-BAPI-API-KEY': test_api_key,
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
    print(url+endPoint+"?"+payload)
    print(response.text)
    print(Info + " Response Time : " + str(response.elapsed))

def genSignature(payload):
    param_str= str(time_stamp) + test_api_key + recv_window + payload
    hash = hmac.new(bytes(test_api_secret, "utf-8"), param_str.encode("utf-8"),hashlib.sha256)
    signature = hash.hexdigest()
    return signature


def createOrder():
    endpoint="/v5/order/create"
    method="POST"
    orderLinkId=uuid.uuid4().hex
    params='{"category":"linear","symbol":"BTCUSDT","orderType":"Market","side":"Buy","orderLinkId":"' +  orderLinkId + '","qty":"0.1","timeInForce":"GTC"}';
    HTTP_Request(endpoint,method,params,"Create")
    
def walletBalance(coin = 'USDT'):
    endpoint="/v5/account/wallet-balance"
    method="GET"
    params=f'accountType=SPOT&coin={coin}';
    HTTP_Request(endpoint,method,params,"Balance")

walletBalance('BTC')
#Create Order

# #Get Order List
# endpoint="/spot/v3/private/order"
# method="GET"
# params='orderLinkId=' + orderLinkId
# HTTP_Request(endpoint,method,params,"List")

# #Cancel Order
# endpoint="/spot/v3/private/cancel-order"
# method="POST"
# params='{"orderLinkId":"' +  orderLinkId +'"}'
# HTTP_Request(endpoint,method,params,"Cancel")