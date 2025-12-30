# factors/base.py
import pandas as pd

def add_grouped_column(df: pd.DataFrame, group_col: str, target_col: str, new_col: str, func) -> pd.DataFrame:
    """
    按 group_col 分组，对 target_col 应用 func，生成新列 new_col
    """
    df[new_col] = df.groupby(group_col)[target_col].transform(func)
    return df
