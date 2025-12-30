from pathlib import Path
import pandas as pd

CACHE_DIR = Path(__file__).parent / "raw_data"

def _cache_path(
    symbol: str,
    start: str,
    end: str,
    source: str,
) -> Path:
    filename = f"{symbol}_{start}_{end}_{source}.csv"
    return CACHE_DIR / filename

def load_from_cache(
    symbol: str,
    start: str,
    end: str,
    source: str,
) -> pd.DataFrame | None:
    path = _cache_path(symbol, start, end, source)
    if path.exists():
        return pd.read_csv(path, index_col=0, parse_dates=True)
    return None

def save_to_cache(
    df: pd.DataFrame,
    symbol: str,
    start: str,
    end: str,
    source: str,
):
    CACHE_DIR.mkdir(exist_ok=True)
    path = _cache_path(symbol, start, end, source)
    df.to_csv(path)
