from datetime import date

import pandas as pd
from alpaca_trade_api import TimeFrame, TimeFrameUnit

from apiCore import AlpacaApi


def calculate_moving_average(df, window):
    df['sma'] = df['close'].rolling(window).mean()
    df['std'] = df['close'].rolling(window).std(ddof=0)
    return df


def calculate_maximum_drawdown(df, window):
    rolling_max = df['close'].rolling(window, min_periods=1).max()
    daily_drawdown = df['close'] / rolling_max - 1.0
    df['drawdown'] = daily_drawdown.rolling(window, min_periods=1).min()
    return df


def calculate_beta(df, window, index_symbol):
    index_df = AlpacaApi().call(
        symbol=index_symbol,
        start=date(date.today().year - 5, date.today().month, date.today().day),
        end=date(date.today().year, date.today().month, date.today().day - 1),
        timeframe=TimeFrame(1, TimeFrameUnit.Week)
    )
    df['index_close_pct'] = index_df.close.pct_change()
    df['stock_close_pct'] = df.close.pct_change()
    df['index_stock_covariance'] = pd.Series(df.stock_close_pct).rolling(window).cov(other=df.index_close_pct)
    df['index_variance'] = pd.Series(df.index_close_pct).rolling(window).var()
    df['beta'] = df['index_stock_covariance'] / pd.Series(df['index_variance'])
    return df
