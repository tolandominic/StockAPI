key = 'O91TWB42TFMIKL9Q'

import requests
import json

weeklyClose = {}

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY_ADJUSTED&symbol=IBM&apikey=O91TWB42TFMIKL9Q'
r = requests.get(url)
data = r.json()
print (data)
for key in data["Weekly Adjusted Time Series"]:
    weeklyClose[key] = float(data["Weekly Adjusted Time Series"][key]["5. adjusted close"])


import plotly.express as px

fig = px.line(x=weeklyClose.keys(), y=weeklyClose.values(), title='Weekly Adjusted Close values for Stock')
fig.show()
