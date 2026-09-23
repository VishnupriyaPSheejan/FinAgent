import pandas as pd

from finagent.features import create_features, feature_columns


def test_feature_creation():
    dates = pd.date_range("2025-01-01", periods=40)
    df = pd.DataFrame(
        {
            "date": dates,
            "transaction_volume": range(100, 140),
            "transaction_value_usd": [5000.0] * 40,
            "avg_transaction_value": [50.0] * 40,
            "digital_transaction_share": [0.5] * 40,
            "international_transaction_share": [0.1] * 40,
            "fed_funds_rate": [4.0] * 40,
            "inflation_rate": [2.5] * 40,
            "unemployment_rate": [4.0] * 40,
            "vix": [15.0] * 40,
            "sp500_index": [5000.0] * 40,
            "day_of_week": dates.dayofweek,
            "month": dates.month,
            "quarter": dates.quarter,
            "is_weekend": (dates.dayofweek >= 5).astype(int),
            "is_month_end": dates.is_month_end.astype(int),
            "is_quarter_end": dates.is_quarter_end.astype(int),
            "is_holiday": [0] * 40,
            "target_next_day_volume": range(101, 141),
        }
    )

    result = create_features(df)

    assert len(result) == 12
    assert all(column in result.columns for column in feature_columns())
