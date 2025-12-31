from data.fetcher import get_price_data


def main():
    df = get_price_data(
        symbol="AAPL",
        start="2020-01-01",
        end="2025-12-01",
    )

if __name__ == "__main__":
    main()
