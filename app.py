import json

import ApiCore
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from datetime import date

import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Stock Dashboard'),
    html.Div(children=[
        html.Label('Stock'),
        dcc.Input(id='symbol'),
    ]),
    html.Div(children=[
        html.H2('Hourly'),
        dcc.Graph(id='graphs_hourly')
    ]),
    html.Div(children=[
        html.H2('Daily'),
        dcc.Graph(id='graphs_daily')
    ])

])


@app.callback(
    Output(component_id='graphs_hourly', component_property='figure'),
    Input(component_id='symbol', component_property='value')
)
def update_graph_hourly(symbol):
    df = call_api(
        symbol=symbol,
        from_date=date(date.today().year, 1, date.today().day),
        timeframe=TimeFrame(1, TimeFrameUnit.Hour),
        window=30)
    return generate_graphs(df)


@app.callback(
    Output(component_id='graphs_daily', component_property='figure'),
    Input(component_id='symbol', component_property='value')
)
def update_graph_daily(symbol):
    df = call_api(
        symbol=symbol,
        from_date=date(date.today().year - 5, 1, date.today().day),
        timeframe=TimeFrame(1, TimeFrameUnit.Day),
        window=30)
    return generate_graphs(df)


def calculate_moving_average(df, window):
    df['sma'] = df['close'].rolling(window).mean()
    df['std'] = df['close'].rolling(window).std(ddof=0)
    return df


def calculate_maximum_drawdown(df, window):
    rolling_max = df['high'].rolling(window, min_periods=1).max()
    daily_drawdown = df['high'] / rolling_max - 1.0
    max_drawdown = daily_drawdown.rolling(window, min_periods=1).min()
    return max_drawdown


def call_api(symbol, from_date, timeframe, window):
    if symbol is None:
        raise PreventUpdate
    api = ApiCore.AlpacaApi()
    df = api.call(
        symbol=symbol,
        timeframe=timeframe,
        start=from_date,
        end=date(date.today().year,
                 date.today().month,
                 date.today().day - 2))
    df = calculate_moving_average(df, window)
    calculate_maximum_drawdown(df, window)
    return df


def generate_graphs(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Candlestick(x=df.index.values, open=df['open'], high=df['high'], low=df['low'], close=df['close'],
                       name='OHLC'),
        secondary_y=True)

    fig.add_trace(
        go.Bar(x=df.index, y=df['volume'].values, opacity=0.2, name='volume'),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df['sma'], name='sma', opacity=0.5, connectgaps=True, line={'color': 'black'}),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df['sma'] + (df['std'] * 2), name='upper band', opacity=0.5, connectgaps=True,
                   line={'color': 'gray', 'dash': 'dash'}),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df['sma'] - (df['std'] * 2), name='lower band', opacity=0.2, connectgaps=True,
                   fill='tonexty', fillcolor='rgba(170, 170, 170, 0.2)', line={'color': 'gray', 'dash': 'dash'}),
        secondary_y=True
    )
    fig.update_layout(
        xaxis=dict(
            rangebreaks=[
                dict(bounds=["sat", "mon"], pattern="day of week"),  # hide weekends, eg. hide sat to before mon
                # dict(bounds=[23, 13], pattern="hour"),  # hide hours outside of 8am-6pm EST
            ],
            rangeselector=dict(
                buttons=[
                    dict(count=1, label="1h", step="hour", stepmode="backward"),
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=7, label="1w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ]
            )
        ),
        height=1000,
    )
    fig.layout.yaxis2.showgrid = False
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
