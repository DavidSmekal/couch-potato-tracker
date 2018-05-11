import json
import requests


# I don't think I need this file anymore
class Stocks:

    def __init__(self, stockTicker, stockName, price, currency):
        self.stockTicker = stockTicker
        self.stockName = stockName
        self.price = price
        self.currency = currency


# array of stocks (will just be strings that will get appended to the end of the url)
usersStocks = ['vfv.to', 'vxc.to', 'vab.to', 'vcn.to']

response = requests.get("https://query1.finance.yahoo.com/v7/finance/quote?symbols=VCN.to")
json = json.loads(response.content.decode('utf-8'))

print(json['quoteResponse']['result'][0]['quoteType'])

jsonStockTicker = json['quoteResponse']['result'][0]['symbol']
jsonStockName = json['quoteResponse']['result'][0]['longName']
jsonPrice = json['quoteResponse']['result'][0]['regularMarketPrice']
jsonCurrency = json['quoteResponse']['result'][0]['currency']

VCN = Stocks(jsonStockTicker, jsonStockName, jsonPrice, jsonCurrency)

print(VCN.price)

# for stocks in usersStocks:
#  content = requests.get("https://query1.finance.yahoo.com/v8/finance/chart/" + stocks)
#   stocks = json.loads(content.content)

#  jsonStockTicker = stocks['chart']['result'][0]['meta']['exchangeTimezoneName']
#   jsonStockName = stocks['chart']['result'][0]['meta']['symbol']
#  jsonPrice = stocks['chart']['result'][0]['meta']['chartPreviousClose']
#   jsonCurrency = stocks['chart']['result'][0]['meta']['currency']
#
#   stocks = Stocks(jsonStockTicker, jsonStockName, jsonPrice, jsonCurrency)
#   print(stocks.stockName)

##### stuff that works for single data.
