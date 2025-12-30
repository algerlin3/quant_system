import yfinance as yf
import pandas as pd

def fetch_from_yfinance(
    symbol: str,
    start: str,
    end: str,
    interval: str = "1d",
) -> pd.DataFrame:
    df = yf.download(
        symbol,
        start=start,
        end=end,
        interval=interval,
        auto_adjust=False,
        progress=False,
        multi_level_index=False,
    )

    if df.empty:
        raise ValueError(f"No data returned for {symbol}")

    # sync column names
    df = df.rename(
        columns={
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Adj Close": "adjusted close",
            "Volume": "volume",
        }
    )

    df = df[["open", "high", "low", "close", "adjusted close", "volume"]]
    df.index.name = "datetime"

    return df
