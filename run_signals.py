from pathlib import Path
from data.factor_cache import load_factor_from_cache
from signals.factor_processing import zscore, winsorize
from signals.signal_generation import generate_simple_signal
import pandas as pd

def main():
    TICKERS = ["AAPL"]
    START_DATE = "2023-01-01"
    END_DATE = "2023-12-31"
    FACTOR_NAMES = ["SMA_5","MOM_5"]

    all_factor_dfs = []
    for factor in FACTOR_NAMES:
        factor_df = load_factor_from_cache(factor, START_DATE, END_DATE)
        all_factor_dfs.append(factor_df)
    
    df_factors = pd.concat(all_factor_dfs, axis=1)
    df_factors = df_factors.loc[:,~df_factors.columns.duplicated()]

    df_factors = winsorize(df_factors, factor_cols=FACTOR_NAMES)
    df_factors = zscore(df_factors, factor_cols=FACTOR_NAMES)

    z_cols = [f + "_z" for f in FACTOR_NAMES]
    df_factors = generate_simple_signal(df_factors, z_cols)

    print(df_factors[df_factors['signal'] != 0])
if __name__ == "__main__":
    main()