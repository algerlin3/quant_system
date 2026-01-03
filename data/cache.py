from pathlib import Path
import pandas as pd
from utils.data_utils import ensure_datetime_column

CACHE_DIR = Path(__file__).parent / "raw_data"

def _cache_path(
    symbol: str,
    start: str,
    end: str,
    source: str,
) -> Path:
    filename = f"{symbol}_{start}_{end}_{source}.parquet"
    return CACHE_DIR / filename

def load_from_cache(
    symbol: str,
    start: str,
    end: str,
    source: str,
) -> pd.DataFrame | None:
    path = _cache_path(symbol, start, end, source)
    if path.exists():
        df = pd.read_parquet(path)
        # enforce datetime column on load
        return ensure_datetime_column(df)
    return None

def save_to_cache(
    df: pd.DataFrame,
    symbol: str,
    start: str,
    end: str,
    source: str,
):
    CACHE_DIR.mkdir(exist_ok=True, parents=True)
    path = _cache_path(symbol, start, end, source)
    df_to_write = ensure_datetime_column(df)
    # always write datetime as a column (no index)
    df_to_write.to_parquet(path, index=False)
