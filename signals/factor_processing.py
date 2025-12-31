# signals/factor_processing.py
import pandas as pd

def zscore(df: pd.DataFrame, factor_cols: list[str], group_col: str = 'code') -> pd.DataFrame:
    """
    对指定因子列进行 Z-score 标准化
    df: DataFrame
    factor_cols: 需要标准化的列名列表
    group_col: 分组列，一般是 'code'
    """
    df = df.copy()
    for col in factor_cols:
        z_col = col + "_z"
        df[z_col] = df.groupby(group_col)[col].transform(lambda x: (x - x.mean()) / x.std())
    return df

def winsorize(df: pd.DataFrame, factor_cols: list[str], lower: float = 0.01, upper: float = 0.99, group_col: str = 'code') -> pd.DataFrame:
    """
    对因子列进行去极值处理（上下百分位截断）
    """
    df = df.copy()
    for col in factor_cols:
        def clip_group(x):
            lower_val = x.quantile(lower)
            upper_val = x.quantile(upper)
            return x.clip(lower_val, upper_val)
        df[col] = df.groupby(group_col)[col].transform(clip_group)
    return df
