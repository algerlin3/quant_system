# backtest/engine.py
import pandas as pd
from utils.data_utils import ensure_datetime_column

def prepare_backtest_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    对回测数据做最基本的预处理：
    - 确保 datetime 列且为 datetime dtype
    - 排序
    - 计算收益率（按 code 分组）
    - 对 signal 做 T+1 滞后（按 code 分组）
    """
    df = ensure_datetime_column(df)

    # 排序（非常重要）
    df.sort_values(["code", "datetime"], inplace=True)

    # 计算个股日收益率
    df["return"] = df.groupby("code")["close"].pct_change()

    # 信号 T+1 执行（防止未来函数）
    df["position"] = df.groupby("code")["signal"].shift(1).fillna(0)

    return df

def calculate_strategy_return(
    df: pd.DataFrame,
    method: str = "equal_weight",
) -> pd.DataFrame:
    """
    计算策略每日组合收益，返回以 datetime 为索引的 DataFrame:
    index: DatetimeIndex
    columns: ['portfolio_return']
    """
    df = ensure_datetime_column(df)
    # 逐个股票的策略收益
    df["strategy_return"] = df["position"] * df["return"]

    if method == "equal_weight":
        # 每日组合收益：按日期对所有股票取等权平均
        portfolio_return = (
            df.groupby("datetime")["strategy_return"]
            .mean()
            .to_frame("portfolio_return")
            .sort_index()
        )
        # 把 datetime 设为索引（DatetimeIndex）
        portfolio_return.index = pd.to_datetime(portfolio_return.index)
        portfolio_return.index.name = "datetime"
    else:
        raise ValueError(f"Unknown method: {method}")

    return portfolio_return

def calculate_equity_curve(
    portfolio_return: pd.DataFrame,
    initial_capital: float = 1.0,
) -> pd.DataFrame:
    """
    根据组合收益计算净值曲线。接受以 datetime 为索引或包含 datetime 列的 DataFrame。
    返回以 datetime 为索引，包含 columns ['portfolio_return','equity']
    """
    df = portfolio_return.copy()
    # 如果有 datetime 列则转为 index
    if "datetime" in df.columns:
        df = df.set_index("datetime")
    # 确保索引为 DatetimeIndex 并按时间排序
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    equity = df.copy()
    equity["equity"] = (1 + equity["portfolio_return"]).cumprod()
    equity["equity"] *= initial_capital
    return equity
