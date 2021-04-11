from binance.client import Client
import csv

def save_data_to_local_csv(data, filename):
    csvfile = open(filename, "w", newline="")
    data_writer = csv.writer(csvfile, delimiter=",")

    for item in data:
        data_writer.writerow(item)

    csvfile.close()

def my_account_balance(client, symbol):
    usdt = client.get_asset_balance(symbol)["free"]
    return usdt