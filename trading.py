from binance.client import Client

# 1. website, fetch data
# https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit=10
client = Client()
klines = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "20 day ago UTC")
print(klines)
# 2. analyse data, strategy

# 3. Sell / Buy / Wait