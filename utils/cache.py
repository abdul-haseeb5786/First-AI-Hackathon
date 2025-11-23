# utils/cache.py
import os
import json
import time
from typing import Any, Optional

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def _cache_path(key: str) -> str:
    safe_key = key.replace("/", "_").replace(" ", "_")
    return os.path.join(CACHE_DIR, f"{safe_key}.json")

def set_cache(key: str, value: Any, ttl_seconds: Optional[int] = 300):
    payload = {
        "ts": time.time(),
        "ttl": ttl_seconds,
        "value": value
    }
    with open(_cache_path(key), "w", encoding="utf-8") as f:
        json.dump(payload, f)

def get_cache(key: str) -> Optional[Any]:
    path = _cache_path(key)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            payload = json.load(f)
        ts = payload.get("ts", 0)
        ttl = payload.get("ttl", 0)
        if ttl > 0 and (time.time() - ts) > ttl:
            try:
                os.remove(path)
            except Exception:
                pass
            return None
        return payload.get("value")
    except Exception:
        return None
