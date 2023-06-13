import requests
import os
from pathlib import Path
import pandas as pd


class tickerDS:
    def __init__(self, csv_file):
        df = pd.read_csv(csv_file)
        self.stock_ticker_to_name = {}

        for index, row in df.iterrows():
            symbol = str(row['Symbol'])
            name = str(row['Name'])
            self.stock_ticker_to_name[symbol] = name

    def getTicker(self, ticker_symbol):
        try:
            self.stock_ticker_to_name[ticker_symbol]
        except KeyError:
            print(f"{ticker_symbol} not in table")

    def hasKey(self, ticker_symbol):
        if ticker_symbol in self.stock_ticker_to_name:
            return True
        else:
            return False


# Possibly use in future #
# NASDAQ_API_KEY = '4CF_GQPYyMyt7VRNxn5k'
# def download_nasdaq_screener_csv(url, save_path):
#     headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36
#     (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
#     response = requests.get(url, headers=headers)
#
#     print('Try')
#     if response.status_code == 200:
#         with open(save_path, 'wb') as file:
#             file.write(response.content)
#         print(f"File downloaded and saved to: {save_path}")
#     else:
#         print(f"Failed to download file {response.status_code}")
#
#
# def delete_old_csv(file_path):
#     try:
#         os.remove(file_path)
#         print(f"File '{file_path}' has been deleted")
#     except OSError as err:
#         print(f"Error occurred while deleting the file: {err}")
#
#
# def getNasdaqCSV():
#     url = "https://www.nasdaq.com/api/v3/screener/csv"
#     url2 = "https://api.nasdaq.com/api/screener/stocks"
#     save_path = "/Users/colewalker/PycharmProjects/ReadStockDataReddit/nasdaq_Screener.json"
#
#     # delete_old_csv(save_path)
#     print('Download')
#     download_nasdaq_screener_csv(url2, save_path)
#     convertJsonFileToCSV()
#
#
# def convertJsonFileToCSV():
#     p = Path(r'/Users/colewalker/PycharmProjects/ReadStockDataReddit/nasdaq_Screener.json')
#     with open('nasdaq_Screener.json', encoding='utf-8') as input_file:
#         stock_data = pd.read_json(input_file.read())
#     stock_data.to_csv('stock_data.csv', encoding='utf-8', index=False)
#
