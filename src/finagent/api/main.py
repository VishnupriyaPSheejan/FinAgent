from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ..config import DATA_PATH, MODEL_PATH
from ..data import load_data
from ..features import create_features
from ..model import load_model

app = FastAPI(
    title="FinAgent Forecast API",
    version="0.1.0",
    description="Time-series forecasting API for the FinAgent project.",
)


class ForecastRequest(BaseModel):
    transaction_volume: float = Field(gt=0)
    transaction_value_usd: float = Field(gt=0)
    avg_transaction_value: float = Field(gt=0)
    digital_transaction_share: float = Field(ge=0, le=1)
    international_transaction_share: float = Field(ge=0, le=1)
    fed_funds_rate: float
    inflation_rate: float
    unemployment_rate: float
    vix: float = Field(gt=0)
    sp500_index: float = Field(gt=0)
    day_of_week: int = Field(ge=0, le=6)
    month: int = Field(ge=1, le=12)
    quarter: int = Field(ge=1, le=4)
    is_weekend: int = Field(ge=0, le=1)
    is_month_end: int = Field(ge=0, le=1)
    is_quarter_end: int = Field(ge=0, le=1)
    is_holiday: int = Field(ge=0, le=1)
    lag_1: float = Field(gt=0)
    lag_7: float = Field(gt=0)
    lag_14: float = Field(gt=0)
    lag_28: float = Field(gt=0)
    rolling_mean_7: float = Field(gt=0)
    rolling_std_7: float = Field(ge=0)
    rolling_mean_28: float = Field(gt=0)
    rolling_std_28: float = Field(ge=0)


class ForecastResponse(BaseModel):
    predicted_next_day_volume: float


@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_exists": MODEL_PATH.exists(),
        "data_exists": DATA_PATH.exists(),
    }


@app.post("/forecast", response_model=ForecastResponse)
def forecast(request: ForecastRequest):
    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=503,
            detail="Model not trained. Run: python scripts/train.py",
        )

    model, features = load_model(MODEL_PATH)
    row = pd.DataFrame([request.model_dump()])
    prediction = float(model.predict(row[features])[0])

    return ForecastResponse(
        predicted_next_day_volume=max(0.0, prediction)
    )
