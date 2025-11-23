# Finance ETL Dashboard

A **finance-focused ETL pipeline and dashboard** built with **Streamlit** and **Plotly**.  
Fetch real-time stock data from AlphaVantage, transform it with pandas, and visualize OHLC & close prices.

---

## Features

- Extract → Transform → Load (ETL) pipeline for financial data
- Fetch real-time stock data via AlphaVantage API
- User-selected parameters:
  - Stock symbol (e.g., AAPL)
  - Interval (5min, 15min, 30min, 60min)
  - Date range
- Interactive Plotly charts:
  - Candlestick (OHLC)
  - Close price line chart
- Error handling for invalid stock symbols or API failures
- Local caching of API responses
- Modular code structure:
  - `api_client/` – API clients
  - `etl/` – Transformation functions
  - `analysis/` – Visualization functions
  - `dashboard/` – Streamlit front-end

---

## Setup

1. **Clone the repository**:

```bash
git clone <repo-url>
cd <repo-folder>
