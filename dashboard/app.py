import os
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from dotenv import load_dotenv
import pandas as pd

from api_client.alpha_vantage import AlphaVantageClient
from etl.transform import transform_alpha_vantage_time_series
from analysis.visualize import finance_line_close, finance_price_figure

# Load .env file
load_dotenv()
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    html.H2("Finance ETL Dashboard"),
    dbc.Row([
        dbc.Col([html.Label("Stock symbol"), dcc.Input(id="symbol", type="text", value="AAPL", placeholder="Enter stock symbol")], width=4),
        dbc.Col([html.Label("Interval"), dcc.Dropdown(id="interval", options=[
            {"label": "60min", "value": "60min"},
            {"label": "30min", "value": "30min"},
            {"label": "15min", "value": "15min"},
            {"label": "5min", "value": "5min"},
        ], value="60min")], width=4),
        dbc.Col([dbc.Button("Fetch", id="fetch-button", color="primary")], width=4)
    ], className="my-2"),
    dbc.Row([dbc.Col(html.Div(id="error-box"), width=12)]),
    dbc.Row([dbc.Col(dcc.Loading(dcc.Graph(id="main-graph")), width=12)]),
    dbc.Row([dbc.Col(dcc.Loading(dcc.Graph(id="aux-graph")), width=12)]),
], fluid=True)

@app.callback(
    Output("main-graph", "figure"),
    Output("aux-graph", "figure"),
    Output("error-box", "children"),
    Input("fetch-button", "n_clicks"),
    State("symbol", "value"),
    State("interval", "value")
)
def fetch_and_plot(n_clicks, symbol, interval):
    empty_fig = {"data": [], "layout": {"title": "No data"}}
    try:
        if not ALPHAVANTAGE_API_KEY:
            raise RuntimeError("ALPHAVANTAGE_API_KEY not set in .env")
        if not symbol:
            raise ValueError("Stock symbol is required")

        client = AlphaVantageClient(ALPHAVANTAGE_API_KEY, cache_ttl=300)
        raw = client.get_time_series(symbol, interval=interval or "60min", outputsize="compact")
        df = transform_alpha_vantage_time_series(raw)
        for col in ["open", "high", "low", "close"]:
            if col not in df.columns:
                df[col] = None

        main_fig = finance_price_figure(df, title=f"{symbol} OHLC")
        aux_fig = finance_line_close(df, title=f"{symbol} Close Price")
        return main_fig, aux_fig, None
    except Exception as e:
        return empty_fig, empty_fig, dbc.Alert(str(e), color="danger", duration=4000)

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
