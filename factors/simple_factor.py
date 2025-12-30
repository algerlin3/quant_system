import pandas as pd
def calculate_moving_average(df, window=2):
    df['moving_average'] = df.groupby('code')['close'].transform(lambda x: x.rolling(window).mean())
    return df