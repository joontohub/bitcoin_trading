import pybithumb
import datetime
import time



with open("sec.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv("XRP")
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5
    target = int(target)


    return target

def buy_crypto_currency(ticker):
   

    krw = bithumb.get_balance("XRP")[2]
    orderbook = pybithumb.get_orderbook("XRP")
    sell_price = orderbook['asks'][0]['price']
   
    unit = krw/int(sell_price)
    bithumb.buy_market_order("XRP", unit)

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0]
    bithumb.sell_market_order(ticker, unit)

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]



now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
today = now.strftime("%Y-%m-%d %H:%M:%S")

ma5 = get_yesterday_ma5("XRP")
target_price = get_target_price("XRP")


while True:
    try:

        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M:%S")
        now_price = int(pybithumb.get_current_price("XRP"))
        target = get_target_price("XRP")
        print("now activating", today,    "now price:", now_price , "target:" ,target)

    
        if mid < now < mid + datetime.timedelta(seconds=10):
            target_price = get_target_price("XRP")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

            ma5 = get_yesterday_ma5("XRP")
            sell_crypto_currency("XRP")
            print("@@ SELL @@")
        current_price = pybithumb.get_current_price("XRP")

        if (current_price > target_price) and (current_price > ma5):
            buy_crypto_currency("XRP")
            print("@@ BUY @@")
    except:
        print("@@@@@ error @@@@@ ")
    time.sleep(1)
