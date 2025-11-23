import pandas as pd
from typing import Dict, Any

def transform_alpha_vantage_time_series(raw: Dict[str, Any]) -> pd.DataFrame:
    """
    Normalize AlphaVantage Time Series JSON into a dataframe.
    """
    ts_key = None
    for k in raw.keys():
        if "Time Series" in k or "time series" in k.lower():
            ts_key = k
            break
    if ts_key is None:
        raise ValueError("No Time Series data found in Alpha Vantage response.")

    series = raw[ts_key]
    records = []
    for dt_str, values in series.items():
        dt = pd.to_datetime(dt_str)
        row = {"datetime": dt}
        for k, v in values.items():
            clean_k = k.split(".")[-1].strip().lower().replace(" ", "_")
            try:
                row[clean_k] = float(v)
            except:
                row[clean_k] = v
        records.append(row)

    df = pd.DataFrame(records)
    if "datetime" in df.columns:
        df = df.sort_values("datetime").reset_index(drop=True)
    return df
