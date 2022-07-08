import plotly.graph_objects as go
import pandas as pd


def candlestick(data):
    return go.Candlestick(
        text=[v['day'] for v in data],
        x=[v['day'] for v in data],
        open=[float(v['open']) for v in data],
        high=[v['high'] for v in data],
        low=[v['low'] for v in data],
        close=[v['close'] for v in data])


def line(x, y, name='', yaxis="y", **kwargs):
    ema_trace = go.Scatter(
        text=[v for v in x],
        x=x,
        y=y,
        mode='lines',
        name=name,
        yaxis=yaxis,
        **kwargs
    )
    return ema_trace


def bar(x, y, name='', yaxis="y"):
    go.Bar(
        text=[v for v in x],
        name=name,
        x=x,
        y=y, xaxis="x", yaxis=yaxis)


def macd_figure(x, macd, signal, his, yaxis="y2"):
    trace1 = go.Bar(
        text=[v for v in x],
        name="mxacd histogram",
        x=x,
        y=his, xaxis="x", yaxis=yaxis)
    trace2 = go.Scatter(
        text=[v for v in x],
        mode="lines",
        name="macd",
        type="scatter",
        line=dict(width=1, color="#000000", smoothing=1.3),
        x=x,
        y=macd,
        xaxis="x",
        yaxis=yaxis,
    )
    trace3 = go.Scatter(
        text=[v for v in x],
        mode="lines",
        name="macd signal",
        type="scatter",
        line=dict(
            color="#ff0000",
            width=0.5,
            smoothing=1.3
        ),
        x=x,
        y=signal,
        xaxis="x",
        yaxis=yaxis)
    return [trace1, trace2, trace3]


def vol_figure(x, vol, yaxis="y3"):
    trace = go.Bar(
        text=[v for v in x],
        name="volume",
        x=x,
        y=vol,
        xaxis="x",
        yaxis=yaxis
    )
    return trace


def rsi(x, rsi, yaxis="y4"):
    current = line(x, rsi, 'rsi', yaxis=yaxis, y0=10, dy=20)
    low = line(x, [30 for i in range(len(rsi))], '30',
               yaxis=yaxis, line=dict(width=1, dash="dash"))
    high = line(x, [70 for i in range(len(rsi))], '70',
                yaxis=yaxis, line=dict(width=1, dash="dash"))
    return [current, low, high]
