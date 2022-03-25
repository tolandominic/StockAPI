import os
from alpaca_trade_api.rest import REST


class AlpacaApi:
    def __init__(self):
        os.environ['APCA_API_KEY_ID'] = str("PKRFNDHYLVETHJ0X2R1W")
        os.environ['APCA_API_SECRET_KEY'] = str("pT68PuCaHcXhLOm50x63u6EZnv8JJd9rSddZWzas")
        os.environ['APCA_API_BASE_URL'] = str("https://paper-api.alpaca.markets")
        self.api = REST()

    def call(self, symbol, timeframe, start, end):
        return self.api.get_bars(symbol=symbol, timeframe=timeframe, start=start, end=end, adjustment='raw').df

