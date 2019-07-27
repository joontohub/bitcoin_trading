import pybithumb
import datetime
import time



with open("sec.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

def get_target_price(ticker):
    df = pybithumb.get_ohlcv("BTC")
    yesterday = df.iloc[-2]

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = today_open + (yesterday_high - yesterday_low) * 0.5



    return target

def buy_crypto_currency(ticker):
    # 코인 두번째가 전체 원화 액수임 그래서 그냥 비티씨로 써도 되는거

    krw = bithumb.get_balance("BTC")[2]
    orderbook = pybithumb.get_orderbook("BTC")
    sell_price = orderbook['asks'][0]['price']
    unit = krw/float(sell_price)
    bithumb.buy_market_order("BTC", unit)

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

ma5 = get_yesterday_ma5("BTC")
target_price = get_target_price("BTC")


while True:
    try:

        now = datetime.datetime.now()
        if mid < now < mid + datetime.delta(seconds=10):
            target_price = get_target_price("BTC")
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)

            ma5 = get_yesterday_ma5("BTC")
            sell_crypto_currency("BTC")

        current_price = pybithumb.get_current_price("BTC")

        if (current_price > target_price) and (current_price > ma5):
            buy_crypto_currency("BTC")
    except:
        print("@@@@@ error @@@@@ ")
    time.sleep(1)
