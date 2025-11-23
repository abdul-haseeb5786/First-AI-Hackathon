import plotly.graph_objs as go
import pandas as pd

def finance_price_figure(df: pd.DataFrame, title: str = "Price") -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=df["datetime"], open=df.get("open"), high=df.get("high"), low=df.get("low"), close=df.get("close"), name="OHLC"
    ))
    fig.update_layout(title=title, xaxis_title="Datetime", yaxis_title="Price")
    return fig

def finance_line_close(df: pd.DataFrame, title: str = "Close Price") -> go.Figure:
    fig = go.Figure()
    if "datetime" in df.columns and "close" in df.columns:
        fig.add_trace(go.Scatter(x=df["datetime"], y=df["close"], mode="lines", name="close"))
    fig.update_layout(title=title, xaxis_title="Datetime", yaxis_title="Close")
    return fig
