import ApiCore
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from datetime import date

import plotly.express as px

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Stock Dashboard'),
    html.Div(children=[
        html.Label('Stock'),
        dcc.Input(id='symbol'),
        html.Label('Time Frame Unit'),
        dcc.Dropdown(id='timeframe-unit', options=['Minute', 'Hour', 'Day']),
        html.Label('Time Frame Amount'),
        dcc.Slider(
            id='timeframe-amount',
            min=1,
            max=1,
            marks={i: str(i) for i in range(1, 2)},
            value=1,
        ),
        html.Label('Start'),
        dcc.DatePickerRange(
            id='date_range',
            start_date=date(date.today().year, date.today().month, date.today().day-1),
            end_date=date(date.today().year, date.today().month, date.today().day-1),
            min_date_allowed=date(date.today().year-5, 1, 1),
            max_date_allowed=date(date.today().year, date.today().month, date.today().day))
    ], style={'padding': 10, 'flex': 1}),
    html.Div(children=[
        dcc.Graph(id='stock-graph')
    ], style={'padding': 10, 'flex': 1})
], style={'display': 'flex', 'flexDirection': 'column'})

print("here")
@app.callback(
    Output(component_id='stock-graph', component_property='figure'),
    Input(component_id='symbol', component_property='value'),
    Input(component_id='date_range', component_property='start_date'),
    Input(component_id='date_range', component_property='end_date')
    )
def update_stock(symbol, start_date, end_date):
    if symbol is None:
        raise PreventUpdate
    api = ApiCore.AlpacaApi()
    df = api.call(symbol=symbol, timeframe=TimeFrame(1, TimeFrameUnit.Minute), start=start_date, end=end_date)
    fig = px.line(df, y="close", markers=True)
    fig.update_layout(transition_duration=500)
    return fig


@app.callback(
    Output(component_id='timeframe-amount', component_property='marks'),
    Output(component_id='timeframe-amount', component_property='max'),
    Input(component_id='timeframe-unit', component_property='value')
    )
def update_slider(timeframe):
    if timeframe is None:
        return {i: str(i) for i in range(1, 2)}, 1
    if timeframe == TimeFrameUnit.Minute.name:
        return {i: str(i) for i in range(1, 59)}, 59
    elif timeframe == TimeFrameUnit.Hour.name:
        return {i: str(i) for i in range(1, 23)}, 23
    elif timeframe == TimeFrameUnit.Day.name:
        return {i: str(i) for i in range(1, 2)}, 2


if __name__ == '__main__':
    app.run_server(debug=True)
