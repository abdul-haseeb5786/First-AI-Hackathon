# api_client/alpha_vantage.py
import requests
from typing import Dict, Any
from urllib.parse import urlencode
from utils.cache import get_cache, set_cache

BASE_URL = "https://www.alphavantage.co/query"

class AlphaVantageClient:
    def __init__(self, api_key: str, cache_ttl: int = 300):
        self.api_key = api_key
        self.cache_ttl = cache_ttl

    def _call(self, params: Dict[str, str]) -> Dict:
        params = params.copy()
        params["apikey"] = self.api_key
        url = f"{BASE_URL}?{urlencode(params)}"
        cached = get_cache(url)
        if cached is not None:
            return cached
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            raise ValueError(f"Alpha Vantage API error: {resp.status_code} - {resp.text}")
        data = resp.json()
        if "Error Message" in data:
            raise ValueError(f"AlphaVantage error: {data['Error Message']}")
        if "Note" in data:
            set_cache(url, data, ttl_seconds=60)
            raise ValueError(f"AlphaVantage note: {data['Note']}")
        set_cache(url, data, ttl_seconds=self.cache_ttl)
        return data

    def get_time_series(self, symbol: str, interval: str = "60min", outputsize: str = "compact") -> Dict:
        if interval.endswith("min"):
            function = "TIME_SERIES_INTRADAY"
            params = {"function": function, "symbol": symbol, "interval": interval, "outputsize": outputsize}
        else:
            function = "TIME_SERIES_DAILY"
            params = {"function": function, "symbol": symbol, "outputsize": outputsize}
        return self._call(params)
