"""Optional data refresh from live APIs.

Uses only urllib (no extra dependencies). Fetches from:
- World Bank API (income level, lending type)
- REST Countries API (names, flags, phone, borders, etc.)

Writes to ~/.cache/paises/ then can be used to rebuild bundled data.
"""

from __future__ import annotations

import json
import os
import urllib.request
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "paises"

WB_URL = "http://api.worldbank.org/v2/countries?format=json&per_page=304"
REST_COUNTRIES_URL = "https://restcountries.com/v3.1/all"


def _fetch_json(url: str) -> list | dict:
    """Fetch JSON from a URL using urllib."""
    req = urllib.request.Request(url, headers={"User-Agent": "paises/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def refresh_world_bank() -> Path:
    """Fetch fresh World Bank country data and cache it."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    data = _fetch_json(WB_URL)
    out_path = CACHE_DIR / "wb_countries.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"World Bank data saved to {out_path}")
    return out_path


def refresh_rest_countries() -> Path:
    """Fetch fresh REST Countries data and cache it."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    data = _fetch_json(REST_COUNTRIES_URL)
    out_path = CACHE_DIR / "rest_countries.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"REST Countries data saved to {out_path}")
    return out_path


def refresh_all() -> dict[str, Path]:
    """Refresh all data sources."""
    return {
        "world_bank": refresh_world_bank(),
        "rest_countries": refresh_rest_countries(),
    }


if __name__ == "__main__":
    paths = refresh_all()
    for name, path in paths.items():
        print(f"  {name}: {path}")
