import plotly.graph_objects as go
from plotly.subplots import make_subplots
import calculations as calc


def generate_drawdown_graph(df, window):
    df = calc.calculate_maximum_drawdown(df, window)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.drawdown, name='drawdown', connectgaps=True, line={'color': 'red'}))
    fig.update_layout(
        yaxis=dict(
            tickformat=',.0%'
        ),
        height=1000
    )
    return fig


def generate_beta_graph(df, window):
    df = calc.calculate_beta(df, window, 'SPY')
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df.beta, mode='lines', name='beta', line={'color': 'blue'}))

    fig.update_layout(
        yaxis=dict(
            tickformat='.2f'
        ),
        height=500
    )
    return fig


def generate_graphs(df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Candlestick(x=df.index.values, open=df.open, high=df.high, low=df.low, close=df.close,
                       name='OHLC'),
        secondary_y=True)

    fig.add_trace(
        go.Bar(x=df.index, y=df.volume.values, opacity=0.2, name='volume'),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df.sma.values, name='sma', opacity=0.5, connectgaps=True, line={'color': 'black'}),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df.sma.values + (df['std'].values * 2), name='upper band', opacity=0.5, connectgaps=True,
                   line={'color': 'gray', 'dash': 'dash'}),
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=df.sma - (df['std'].values * 2), name='lower band', opacity=0.2, connectgaps=True,
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
