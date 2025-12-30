import pandas as pd
from data.sources import fetch_from_yfinance
from data.schemas import required_columns
from data.cache import load_from_cache, save_to_cache

def get_price_data(
    symbol: str,
    start: str,
    end: str,
    source: str = "yfinance",
    use_cache: bool = True,
) -> pd.DataFrame:

    if use_cache:
        cached = load_from_cache(symbol, start, end, source)
        if cached is not None:
            print(f"[CACHE HIT] {symbol}")
            return cached

    if source == "yfinance":
        df = fetch_from_yfinance(symbol, start, end)
    else:
        raise ValueError(f"Unknown data source: {source}")

    _validate_dataframe(df)

    if use_cache:
        save_to_cache(df, symbol, start, end, source)

    return df

def _validate_dataframe(df: pd.DataFrame):
    missing = set(required_columns) - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
