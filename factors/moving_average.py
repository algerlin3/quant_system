# factors/moving_average.py
from factors.base import add_grouped_column
import pandas as pd

def calculate_sma(df, code_col='code', price_col='close', window=5) -> pd.DataFrame:
    """
    计算简单移动平均（SMA）
    """
    col_name = f"SMA_{window}"
    return add_grouped_column(df, group_col=code_col, target_col=price_col, new_col=col_name, func=lambda x: x.rolling(window).mean())
