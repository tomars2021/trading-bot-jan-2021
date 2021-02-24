from binance.client import Client
import helper
import pandas as pd

# 1. website, fetch data
# https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=10
client = Client()
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "20 day ago UTC")
# print(klines)

# 2. analyse data, strategy

# 2.1 save data
filename = "./data/BTCUSDT.csv"
helper.save_data_to_local_csv(data=klines, filename=filename)

# 2.2 read data
df = pd.read_csv(filename)
df.columns = ["opentime", "open", "high","low","close","volume","closetime","QuoteAssetVolume","NumberOfTrades","TakerBuyBaseAssetVolume","TakerBuyQuoteAssetVolume", "ignore"]

print(df)

# 3. Sell / Buy / Wait