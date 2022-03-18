import os
from alpaca_trade_api.rest import REST, TimeFrame

os.environ['APCA_API_KEY_ID'] = str("PKRFNDHYLVETHJ0X2R1W")
os.environ['APCA_API_SECRET_KEY'] = str("pT68PuCaHcXhLOm50x63u6EZnv8JJd9rSddZWzas")
os.environ['APCA_API_BASE_URL'] = str("https://paper-api.alpaca.markets")

api = REST()

thisdf = api.get_bars("AAPL", TimeFrame.Day, "2021-06-01", "2021-06-30", adjustment='raw').df
print (thisdf)
import plotly.express as px

px.line(thisdf, y="close", markers=True).show()