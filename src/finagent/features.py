from __future__ import annotations

import pandas as pd

TARGET = "target_next_day_volume"

BASE_FEATURES = [
    "transaction_volume",
    "transaction_value_usd",
    "avg_transaction_value",
    "digital_transaction_share",
    "international_transaction_share",
    "fed_funds_rate",
    "inflation_rate",
    "unemployment_rate",
    "vix",
    "sp500_index",
    "day_of_week",
    "month",
    "quarter",
    "is_weekend",
    "is_month_end",
    "is_quarter_end",
    "is_holiday",
]


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy().sort_values("date").reset_index(drop=True)

    for lag in (1, 7, 14, 28):
        data[f"lag_{lag}"] = data["transaction_volume"].shift(lag)

    for window in (7, 28):
        data[f"rolling_mean_{window}"] = (
            data["transaction_volume"].rolling(window).mean()
        )
        data[f"rolling_std_{window}"] = (
            data["transaction_volume"].rolling(window).std()
        )

    data = data.dropna().reset_index(drop=True)
    return data


def feature_columns() -> list[str]:
    lag_features = [f"lag_{x}" for x in (1, 7, 14, 28)]
    rolling_features = []
    for window in (7, 28):
        rolling_features.extend(
            [f"rolling_mean_{window}", f"rolling_std_{window}"]
        )
    return BASE_FEATURES + lag_features + rolling_features
