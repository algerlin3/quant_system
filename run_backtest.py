# run_backtest.py
from datetime import datetime

from data.fetcher import get_price_data
from signals.signal_generation import generate_simple_signal
from signals.factor_processing import zscore, winsorize
from factors import calculate_factor
from data.factor_cache import cache_factors, save_factor_to_cache
from backtest.engine import (
    prepare_backtest_data,
    calculate_strategy_return,
    calculate_equity_curve,
)
from metrics.metrics import calculate_metrics
import pandas as pd

def run_backtest():
    # ========= 参数区 =========
    symbol_list = "AAPL"
    start = "2022-01-01"
    end = "2023-12-31"
    initial_capital = 1.0

    # ========= Phase 1: 数据 =========
    df_price = get_price_data(
        symbol=symbol_list,
        start=start,
        end=end,
    )

    # ========= Phase 2: 因子 & 信号 =========
    factor_names = ["SMA_5", "MOM_5"]

    df_with_factor_cache, missing = cache_factors(df_price, factor_names, start, end)

    for factor in missing:
        if factor.startswith("SMA"):
            window = int(factor.split("_")[1])
            df_with_factor_cache = calculate_factor(df_with_factor_cache, "SMA", window=window)
        elif factor.startswith("MOM"):
            window = int(factor.split("_")[1])
            df_with_factor_cache = calculate_factor(df_with_factor_cache, "MOM", window=window)
        # 3️⃣ 保存缓存
        save_factor_to_cache(df_with_factor_cache[['code', factor]], factor, start, end)

    df_factors = pd.concat([df_with_factor_cache, df_price], axis=1)

    df_factors = df_factors.loc[:,~df_factors.columns.duplicated()]

    df_factors = winsorize(df_factors, factor_cols=factor_names)
    df_factors = zscore(df_factors, factor_cols=factor_names)

    z_cols = [f + "_z" for f in factor_names]

    df_signal = generate_simple_signal(df_factors, z_cols)

    # ========= Phase 3: 回测 =========
    df_bt = prepare_backtest_data(df_signal)

    portfolio_ret = calculate_strategy_return(df_bt)

    equity_curve = calculate_equity_curve(
        portfolio_ret,
        initial_capital=initial_capital,
    )
    print(equity_curve)
    # ========= Phase 4: 绩效 =========
    metrics = calculate_metrics(
        portfolio_return=portfolio_ret["portfolio_return"],
        equity=equity_curve["equity"],
    )

    # ========= 输出 =========
    print("\n====== Backtest Result ======")
    print(metrics)
    print("\n====== Equity Curve ======")
    print(equity_curve.tail())

if __name__ == "__main__":
    run_backtest()
