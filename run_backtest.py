from data.fetcher import get_price_data
from factors import calculate_factor
from data.factor_cache import cache_factors, save_factor_to_cache

def main():
    df = get_price_data(
        symbol="AAPL",
        start="2020-01-01",
        end="2025-12-01",
    )

    factor_names = ["SMA_5", "MOM_5"]

    # 使用缓存的因子数据
    df_with_factor_cache, missing = cache_factors(df, factor_names, "2020-01-01", "2025-12-01")

    # 2️⃣ 计算缺失因子
    for factor in missing:
        if factor.startswith("SMA"):
            window = int(factor.split("_")[1])
            df_with_factor_cache = calculate_factor(df_with_factor_cache, "SMA", window=window)
        elif factor.startswith("MOM"):
            window = int(factor.split("_")[1])
            df_with_factor_cache = calculate_factor(df_with_factor_cache, "MOM", window=window)
        # 3️⃣ 保存缓存
        save_factor_to_cache(df_with_factor_cache[['code', factor]], factor, "2023-01-01", "2023-12-31")

    print(df_with_factor_cache.head())
    print(df_with_factor_cache.tail())

if __name__ == "__main__":
    main()
