import json
from AvApi import AvApi
import plotly.express as px

weeklyAdjustedApi = AvApi(function = 'TIME_SERIES_WEEKLY_ADJUSTED', stockSymbol = 'IBM',  apiKey = 'O91TWB42TFMIKL9Q')
weeklyClose = weeklyAdjustedApi.callFunction(queryKey = 'Weekly Adjusted Time Series', marketDataType = '5. adjusted close');

fig = px.line(x=weeklyClose.keys(), y=weeklyClose.values(), title='Weekly Adjusted Close values for Stock')
fig.show()
