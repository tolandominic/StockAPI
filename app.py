from dash import Dash, html, dcc, Input, Output
from alpaca_trade_api.rest import TimeFrame, TimeFrameUnit
from datetime import date

from apiCore import AlpacaApi
import plot as plot
import calculations as calc

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Stock Dashboard'),
    html.Div(children=[
        html.Label('Stock'),
        dcc.Input(id='symbol')
    ]),
    html.Div(children=[
        html.H2('Hourly'),
        dcc.Graph(id='graphs_hourly')
    ]),
    html.Div(children=[
        html.H2('Daily'),
        dcc.Graph(id='graphs_daily')
    ]),
    html.Div(children=[
        html.H2('Maximum Drawdown'),
        html.Label('Window'),
        dcc.Input(id='drawdown_window', type='number', min=1, max=252, value=252),
        dcc.Graph(id='drawdown_daily')
    ]),
    html.Div(children=[
        html.H2('Beta'),
        dcc.Input(id='beta_window', type='number', min=1, max=252, value=20),
        dcc.Graph(id='graphs_beta')
    ]),

])


@app.callback(
    Output(component_id='graphs_hourly', component_property='figure'),
    Input(component_id='symbol', component_property='value')
)
def update_graph_hourly(symbol):
    df = AlpacaApi().call(
        symbol=symbol,
        start=date(date.today().year, 1, date.today().day),
        end=date(date.today().year, date.today().month, date.today().day - 1),
        timeframe=TimeFrame(1, TimeFrameUnit.Hour))
    df = calc.calculate_moving_average(df, 30)
    return plot.generate_graphs(df)


@app.callback(
    Output(component_id='graphs_daily', component_property='figure'),
    Input(component_id='symbol', component_property='value')
)
def update_graph_daily(symbol):
    df = AlpacaApi().call(
        symbol=symbol,
        start=date(date.today().year - 5, 1, date.today().day),
        end=date(date.today().year, date.today().month, date.today().day - 1),
        timeframe=TimeFrame(1, TimeFrameUnit.Day),
    )

    df = calc.calculate_moving_average(df, 30)
    return plot.generate_graphs(df)


@app.callback(
    Output(component_id='drawdown_daily', component_property='figure'),
    Input(component_id='symbol', component_property='value'),
    Input(component_id='drawdown_window', component_property='value')
)
def update_drawdown_graph_daily(symbol, window):
    df = AlpacaApi().call(
        symbol=symbol,
        start=date(date.today().year - 5, 1, date.today().day),
        end=date(date.today().year, date.today().month, date.today().day - 1),
        timeframe=TimeFrame(1, TimeFrameUnit.Day)
    )
    return plot.generate_drawdown_graph(df, window)


@app.callback(
    Output(component_id='graphs_beta', component_property='figure'),
    Input(component_id='symbol', component_property='value'),
    Input(component_id='beta_window', component_property='value')
)
def update_beta_graph(symbol, window):
    df = AlpacaApi().call(
        symbol=symbol,
        start=date(date.today().year - 5, date.today().month, date.today().day),
        end=date(date.today().year, date.today().month, date.today().day - 1),
        timeframe=TimeFrame(1, TimeFrameUnit.Week)
    )
    return plot.generate_beta_graph(df, window)


if __name__ == '__main__':
    app.run_server(debug=True)
