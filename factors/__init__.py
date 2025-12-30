# factors/__init__.py
from factors.moving_average import calculate_sma
from factors.momentum import calculate_momentum

FACTOR_FUNCS = {
    "SMA": calculate_sma,
    "MOM": calculate_momentum,
}

def calculate_factor(df, factor_name, **kwargs):
    if factor_name not in FACTOR_FUNCS:
        raise ValueError(f"Unknown factor: {factor_name}")
    return FACTOR_FUNCS[factor_name](df, **kwargs)
