import pandas as pd
from typing import Iterable

def ensure_datetime_column(df: pd.DataFrame, col: str = "datetime") -> pd.DataFrame:
    """
    Ensure df has a datetime column named `col`. If the index is a DatetimeIndex, reset it.
    Convert the column to datetime dtype.
    """
    df = df.copy()
    if isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index()
    if col not in df.columns:
        raise KeyError(f"DataFrame must contain a '{col}' column or a DatetimeIndex")
    df[col] = pd.to_datetime(df[col])
    return df

def ensure_required_columns(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    """
    Ensure df contains all columns in cols. Raises KeyError with missing list if not.
    """
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise KeyError(f"DataFrame is missing required columns: {missing}")
    return df