# data/factor_cache.py
from pathlib import Path
import pandas as pd
from utils.data_utils import ensure_datetime_column, ensure_required_columns

# 默认因子缓存目录
FACTOR_CACHE_DIR = Path(__file__).parent / "factor_data"
FACTOR_CACHE_DIR.mkdir(exist_ok=True, parents=True)

def _factor_cache_path(factor_name: str, start: str, end: str) -> Path:
    """
    根据因子名称和时间区间生成缓存路径（始终使用 parquet）
    """
    ext = ".parquet"
    filename = f"{factor_name}_{start}_{end}{ext}"
    return FACTOR_CACHE_DIR / filename

def _ensure_factor_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    确保因子数据框具有 'datetime' 列（如果适用，还包括 'code' 列）并且 'datetime' 列的数据类型正确。
    如果数据框的索引是 DatetimeIndex，则重置索引。
    """
    df = ensure_datetime_column(df)
    df = ensure_required_columns(df, ["code"])
    return df

def load_factor_from_cache(factor_name: str, start: str, end: str) -> pd.DataFrame | None:
    """
    尝试从缓存读取因子数据（始终使用 parquet）
    """
    path = _factor_cache_path(factor_name, start, end)
    if path.exists():
        df = pd.read_parquet(path)
        return _ensure_factor_df(df)
    return None

def save_factor_to_cache(df: pd.DataFrame, factor_name: str, start: str, end: str):
    """
    保存因子数据到缓存（始终使用 parquet）
    """
    path = _factor_cache_path(factor_name, start, end)
    df_to_write = _ensure_factor_df(df)
    df_to_write.to_parquet(path, index=False)

def cache_factors(df: pd.DataFrame, factor_names: list[str], start: str, end: str) -> pd.DataFrame:
    """
    自动处理多个因子：
    - 检查缓存，已存在因子直接读取（parquet）
    - 缺失因子返回原 df，需要计算
    """
    cached = {}
    missing = []

    for factor in factor_names:
        factor_df = load_factor_from_cache(factor, start, end)
        if factor_df is not None:
            cached[factor] = factor_df[['code', 'datetime', factor]]
        else:
            missing.append(factor)

    # 合并已有缓存因子
    if cached:
        merged = df.copy()
        for factor, factor_df in cached.items():
            merged = merged.merge(factor_df, on=['code','datetime'], how='left')
    else:
        merged = df.copy()

    return merged, missing
