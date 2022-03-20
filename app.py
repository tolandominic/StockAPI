import json

import pandas as pd

import ApiCore
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate
from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
from datetime import date

import plotly.express as px
import plotly.graph_objects as go
import numpy as np

app = Dash(__name__)

app.layout = html.Div([
    dcc.Store(id='api-call-store'),
    html.H1('Stock Dashboard'),
    html.Div(children=[
        html.Label('Stock'),
        dcc.Input(id='symbol'),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='stock-graph-open'),
        ], style={'display': 'flex', 'flexDirection': 'column', 'flex': '1', 'flex-basis': '100%'}),
        html.Div([
            dcc.Graph(id='stock-graph-close')
        ], style={'display': 'flex', 'flexDirection': 'column', 'flex': '1', 'flex-basis': '100%'}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}),
    html.Div([
        html.Div([
            dcc.Graph(id='stock-graph-low'),
        ], style={'display': 'flex', 'flexDirection': 'column', 'flex': '1', 'flex-basis': '100%'}),
        html.Div([
            dcc.Graph(id='stock-graph-high')
        ], style={'display': 'flex', 'flexDirection': 'column', 'flex': '1', 'flex-basis': '100%'}),
    ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}),
    html.Div([
        html.Div(children=[
            dcc.Graph(id='stock-graph-volume')
        ], style={'display': 'flex', 'flexDirection': 'column', 'flex': '1', 'flex-basis': '100%'})
    ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'}),
    html.Div([
        html.Div(children=[
            dcc.Graph(id='stock-graph-vwap')
        ], style={'display': 'flex', 'flexDirection': 'column', 'flex': '1', 'flex-basis': '100%'})
    ], style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'})
])


@app.callback(
    Output(component_id='api-call-store', component_property='data'),
    Input(component_id='symbol', component_property='value')
)
def call_api(symbol):
    if symbol is None:
        raise PreventUpdate
    api = ApiCore.AlpacaApi()
    df = api.call(
        symbol=symbol,
        timeframe=TimeFrame(1, TimeFrameUnit.Hour),
        start=date(date.today().year - 1,
                   date.today().month,
                   date.today().day),
        end=date(date.today().year,
                 date.today().month,
                 date.today().day - 2))

    datasets = {
        'df_open': df['open'].to_json(orient='index', date_format='iso'),
        'df_close': df['close'].to_json(orient='index', date_format='iso'),
        'df_low': df['low'].to_json(orient='index', date_format='iso'),
        'df_high': df['high'].to_json(orient='index', date_format='iso'),
        'df_volume': df['volume'].to_json(orient='index', date_format='iso'),
        'df_trade_count': df['trade_count'].to_json(orient='index', date_format='iso'),
        'df_vwap': df['vwap'].to_json(orient='index', date_format='iso')
    }

    return json.dumps(datasets)


@app.callback(
    Output(component_id='stock-graph-open', component_property='figure'),
    Input(component_id='api-call-store', component_property='data')
)
def update_open(json_data):
    return generate_line_graph_figure(json_data, 'df_open')


@app.callback(
    Output(component_id='stock-graph-close', component_property='figure'),
    Input(component_id='api-call-store', component_property='data')
)
def update_close(json_data):
    return generate_line_graph_figure(json_data, 'df_close')


@app.callback(
    Output(component_id='stock-graph-low', component_property='figure'),
    Input(component_id='api-call-store', component_property='data')
)
def update_low(json_data):
    return generate_line_graph_figure(json_data, 'df_low')


@app.callback(
    Output(component_id='stock-graph-high', component_property='figure'),
    Input(component_id='api-call-store', component_property='data')
)
def update_high(json_data):
    return generate_line_graph_figure(json_data, 'df_high')


@app.callback(
    Output(component_id='stock-graph-vwap', component_property='figure'),
    Input(component_id='api-call-store', component_property='data')
)
def update_vwap(json_data):
    return generate_line_graph_figure(json_data, 'df_vwap')


@app.callback(
    Output(component_id='stock-graph-volume', component_property='figure'),
    Input(component_id='api-call-store', component_property='data')
)
def update_volume(json_data):
    datasets = json.loads(json_data)
    df_close = pd.read_json(datasets['df_close'], orient='index')
    df_volume = pd.read_json(datasets['df_volume'], orient='index')
    fig = px.line(df_close, range_x=[date(date.today().year,
                                          date.today().month,
                                          date.today().day - 7),
                                     date(date.today().year,
                                          date.today().month,
                                          date.today().day - 2)],
                  markers=True)

    # fig = px.bar(df, orientation='h', range_x=[date(date.today().year,
    #                                                 date.today().month,
    #                                                 date.today().day - 7),
    #                                            date(date.today().year,
    #                                                 date.today().month,
    #                                                 date.today().day - 2)])
    fig.add_bar(alignmentgroup='index', x=df_volume.index, y=df_volume.values)
    fig.update_layout(transition_duration=500, barmode='stack')

    return fig


def generate_line_graph_figure(json_data, dataset_key):
    datasets = json.loads(json_data)
    df = pd.read_json(datasets[dataset_key], orient='index')
    fig = px.line(df, range_x=[date(date.today().year,
                                    date.today().month,
                                    date.today().day - 7),
                               date(date.today().year,
                                    date.today().month,
                                    date.today().day - 2)],
                  markers=True)
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
