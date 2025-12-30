# data/factor_cache.py
from pathlib import Path
import pandas as pd

# 默认因子缓存目录
FACTOR_CACHE_DIR = Path(__file__).parent / "factor_data"
FACTOR_CACHE_DIR.mkdir(exist_ok=True, parents=True)

def _factor_cache_path(factor_name: str, start: str, end: str, use_parquet: bool = False) -> Path:
    """
    根据因子名称和时间区间生成缓存路径
    """
    ext = ".parquet" if use_parquet else ".csv"
    filename = f"{factor_name}_{start}_{end}{ext}"
    return FACTOR_CACHE_DIR / filename

def load_factor_from_cache(factor_name: str, start: str, end: str, use_parquet: bool = False) -> pd.DataFrame | None:
    """
    尝试从缓存读取因子数据
    """
    path = _factor_cache_path(factor_name, start, end, use_parquet)
    if path.exists():
        if use_parquet:
            return pd.read_parquet(path)
        else:
            return pd.read_csv(path)
    return None

def save_factor_to_cache(df: pd.DataFrame, factor_name: str, start: str, end: str, use_parquet: bool = False):
    """
    保存因子数据到缓存
    """
    path = _factor_cache_path(factor_name, start, end, use_parquet)
    if use_parquet:
        df.to_parquet(path, index=False)
    else:
        df.to_csv(path, index=False)

def cache_factors(df: pd.DataFrame, factor_names: list[str], start: str, end: str, use_parquet: bool = False) -> pd.DataFrame:
    """
    自动处理多个因子：
    - 检查缓存，已存在因子直接读取
    - 缺失因子返回原 df，需要计算
    """
    cached = {}
    missing = []

    for factor in factor_names:
        factor_df = load_factor_from_cache(factor, start, end, use_parquet)
        if factor_df is not None:
            cached[factor] = factor_df[[ 'code', 'datetime', factor ]]
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
