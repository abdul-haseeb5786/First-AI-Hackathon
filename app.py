import os
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from dotenv import load_dotenv
from datetime import datetime

from api_client.alpha_vantage import AlphaVantageClient
from etl.transform import transform_alpha_vantage_time_series
from analysis.visualize import finance_line_close, finance_price_figure

# Load .env
load_dotenv()
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

st.set_page_config(page_title="Finance ETL Dashboard", layout="wide")
st.title("💹 Finance ETL Dashboard")

# --- User Inputs ---
symbol = st.text_input("Stock Symbol", "AAPL")
interval = st.selectbox("Interval", ["60min", "30min", "15min", "5min"], index=0)

date_range = st.date_input(
    "Select Date Range",
    value=[pd.to_datetime("2023-01-01"), pd.to_datetime("2023-12-31")]
)

# Fetch Button
if st.button("Fetch Finance Data"):
    try:
        if not ALPHAVANTAGE_API_KEY:
            st.error("ALPHAVANTAGE_API_KEY not set in .env")
        if not symbol:
            st.error("Stock symbol is required")
        
        # Fetch data
        client = AlphaVantageClient(ALPHAVANTAGE_API_KEY)
        raw = client.get_time_series(symbol, interval=interval)
        df = transform_alpha_vantage_time_series(raw)

        # Ensure OHLC columns exist
        for col in ["open", "high", "low", "close"]:
            if col not in df.columns:
                df[col] = None

        # Filter by date range
        start_date, end_date = date_range
        df = df[(df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)]

        if df.empty:
            st.warning("No data available for the selected date range.")
        else:
            # Plot
            st.plotly_chart(finance_price_figure(df, f"{symbol} OHLC"), use_container_width=True)
            st.plotly_chart(finance_line_close(df, f"{symbol} Close Price"), use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")
