#!/usr/bin/env bash
curl -X POST "http://127.0.0.1:8000/forecast" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_volume": 1100000,
    "transaction_value_usd": 55000000,
    "avg_transaction_value": 50,
    "digital_transaction_share": 0.58,
    "international_transaction_share": 0.12,
    "fed_funds_rate": 4.5,
    "inflation_rate": 2.7,
    "unemployment_rate": 4.2,
    "vix": 18,
    "sp500_index": 5200,
    "day_of_week": 2,
    "month": 9,
    "quarter": 3,
    "is_weekend": 0,
    "is_month_end": 0,
    "is_quarter_end": 0,
    "is_holiday": 0,
    "lag_1": 1080000,
    "lag_7": 1040000,
    "lag_14": 1050000,
    "lag_28": 1020000,
    "rolling_mean_7": 1060000,
    "rolling_std_7": 45000,
    "rolling_mean_28": 1040000,
    "rolling_std_28": 50000
  }'
