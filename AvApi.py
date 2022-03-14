import requests

class AvApi:
    def __init__(self, function, stockSymbol, apiKey):
        self.function = function
        self.stockSymbol = stockSymbol
        self.apiKey = apiKey
        self.url = 'https://www.alphavantage.co/query?function={function}&symbol={stockSymbol}&apikey={apiKey}'.format(function=function, stockSymbol=stockSymbol, apiKey=apiKey)

    def callFunction(self, queryKey, marketDataType):
        marketData = {}
        r = requests.get(self.url)
        data = r.json()
        for key in data[queryKey]:
            print (marketDataType)
            marketData[key] = float(data[queryKey][key][marketDataType])
            #marketData[key] = float(data[queryKey][key]["5. adjusted close"])
        return marketData
