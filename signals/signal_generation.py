# signals/signal_generation.py
import pandas as pd

def generate_simple_signal(df: pd.DataFrame, factor_z_cols: list[str], method: str = 'all_positive') -> pd.DataFrame:
    """
    根据标准化因子生成交易信号
    factor_z_cols: Z-score 因子列列表
    method: 信号规则
        - 'all_positive': 所有因子 > 0 买入，<0 卖出
    """
    df = df.copy()
    def signal_row(row):
        if method == 'all_positive':
            if all(row[col] > 0 for col in factor_z_cols):
                return 1
            elif all(row[col] < 0 for col in factor_z_cols):
                return -1
            else:
                return 0
        else:
            return 0
    df['signal'] = df.apply(signal_row, axis=1)
    return df
