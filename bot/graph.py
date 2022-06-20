import plotly.graph_objects as go
import pandas as pd


def candlestick(data):
    fig = go.Figure(
        layout=go.Layout(xaxis=dict(title_text='time', type='category')),
        data=[
            go.Candlestick(
                x=[v['day'] for v in data],
                open=[float(v['open']) for v in data],
                high=[v['high'] for v in data],
                low=[v['low'] for v in data],
                close=[v['close'] for v in data])
        ])
    fig.update_layout(xaxis_rangeslider_visible=False)
    fig.update_traces(showlegend=False)
    return fig


def ma_line(x, y, name=''):
    ema_trace = go.Scatter(x=x, y=y, mode='lines', name=name)
    return ema_trace
