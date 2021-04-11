from binance.client import Client
import helper
import pandas as pd
import strategy
import config
from binance.enums import *

WAIT = 0
BUY = 1
SELL = -1

# 1. website, fetch data
# https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=10
client = Client(api_key=config.API_KEY, api_secret=config.SECRET_KEY)
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "20 day ago UTC")
# print(klines)

# 2. analyse data, strategy

# 2.1 save data
filename = "./data/BTCUSDT.csv"
helper.save_data_to_local_csv(data=klines, filename=filename)

# 2.2 read data
df = pd.read_csv(filename)
df.columns = ["opentime", "open", "high","low","close","volume","closetime","QuoteAssetVolume","NumberOfTrades","TakerBuyBaseAssetVolume","TakerBuyQuoteAssetVolume", "ignore"]

# 2.3 run strategy
action = WAIT
rsi = strategy.RSI(data=df["close"], time_window=12)
current_rsi = rsi.values[-1]

if current_rsi > 70:
    action = SELL
elif current_rsi < 30:
    action = BUY

print("action: {}, current rsi:{}".format(action, int(current_rsi)))

current_price = df["close"].values[-1]
# print(current_price)

# 3. Sell / Buy / Wait
if action == BUY:
    # buy
    print("BUY:")
    try:
        order = client.create_test_order(
            symbol="BTCUSDT",
            side=SIDE_BUY,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=round(float(helper.my_account_balance(client, "USDT"))/current_price, 6),
            price=current_price
        )
    except Exception as e:
        print("WARNING: {}".format(e))
elif action == SELL:
    # sell
    print("SELL:")
    try:
        order = client.create_test_order(
            symbol="BTCUSDT",
            side=SIDE_SELL,
            type=ORDER_TYPE_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=int(float(helper.my_account_balance(client, "BTC")) * 100000) / 100000,
            price=current_price
        )
    except Exception as e:
        print("WARNING: {}".format(e))

# Actual API:
# client.order_limit_buy
# client.order_limit_sell