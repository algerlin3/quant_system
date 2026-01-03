# metrics/metrics.py
import numpy as np
import pandas as pd

TRADING_DAYS = 252

def total_return(equity: pd.Series) -> float:
    """
    总收益率，安全处理 NaN/0 起点
    """
    equity = equity.dropna()
    if equity.empty:
        return 0.0
    start = float(equity.iloc[0])
    end = float(equity.iloc[-1])
    if start == 0:
        return 0.0
    return end / start - 1

def annual_return(equity: pd.Series) -> float:
    """
    年化收益率，使用时间区间（如果有 datetime index）或样本数进行年化。
    对于数据不足或异常（如起始值为 0）返回 0.0。
    """
    equity = equity.dropna()
    if equity.empty:
        return 0.0
    start = float(equity.iloc[0])
    end = float(equity.iloc[-1])
    if start == 0:
        return 0.0

    # If index is datetime, compute elapsed years precisely
    if isinstance(equity.index, pd.DatetimeIndex) and len(equity.index) >= 2:
        days = (equity.index[-1] - equity.index[0]).days
        years = days / 365.25
        if years <= 0:
            return 0.0
        return (end / start) ** (1 / years) - 1

    # Fallback to using number of observations
    n_periods = len(equity)
    if n_periods < 2:
        return 0.0
    return (end / start) ** (TRADING_DAYS / n_periods) - 1

def annual_volatility(portfolio_return: pd.Series) -> float:
    """
    年化波动率
    """
    return portfolio_return.std() * np.sqrt(TRADING_DAYS)

def sharpe_ratio(
    portfolio_return: pd.Series,
    risk_free_rate: float = 0.0,
) -> float:
    """
    夏普比率（年化）
    """
    excess_return = portfolio_return - risk_free_rate / TRADING_DAYS
    return (
        excess_return.mean() / excess_return.std()
        * np.sqrt(TRADING_DAYS)
        if excess_return.std() != 0
        else 0.0
    )

def max_drawdown(equity: pd.Series) -> float:
    """
    最大回撤
    """
    cum_max = equity.cummax()
    drawdown = equity / cum_max - 1
    return drawdown.min()

def calculate_metrics(
    portfolio_return: pd.Series,
    equity: pd.Series,
    risk_free_rate: float = 0.0,
) -> pd.DataFrame:
    """
    汇总所有绩效指标
    """
    metrics = {
        "Total Return": total_return(equity),
        "Annual Return": annual_return(equity),
        "Annual Volatility": annual_volatility(portfolio_return),
        "Sharpe Ratio": sharpe_ratio(portfolio_return, risk_free_rate),
        "Max Drawdown": max_drawdown(equity),
    }

    return pd.DataFrame(metrics, index=["Strategy"])
