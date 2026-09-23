from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from xgboost import XGBRegressor

from .evaluation import regression_metrics
from .features import TARGET, create_features, feature_columns


def chronological_split(
    df: pd.DataFrame, test_size: float = 0.2
) -> tuple[pd.DataFrame, pd.DataFrame]:
    split_index = int(len(df) * (1 - test_size))
    return df.iloc[:split_index].copy(), df.iloc[split_index:].copy()


def train_model(
    df: pd.DataFrame,
    model_path: str | Path,
    test_size: float = 0.2,
    random_state: int = 42,
    n_estimators: int = 500,
    max_depth: int = 6,
    learning_rate: float = 0.05,
) -> dict:
    data = create_features(df)
    features = feature_columns()

    train, test = chronological_split(data, test_size)

    X_train, y_train = train[features], train[TARGET]
    X_test, y_test = test[features], test[TARGET]

    model = XGBRegressor(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        subsample=0.9,
        colsample_bytree=0.9,
        objective="reg:squarederror",
        random_state=random_state,
        n_jobs=4,
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    metrics = regression_metrics(y_test, predictions)

    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "features": features,
        },
        model_path,
    )

    return {
        "metrics": metrics,
        "train_rows": len(train),
        "test_rows": len(test),
        "model_path": str(model_path),
    }


def load_model(model_path: str | Path):
    artifact = joblib.load(model_path)
    return artifact["model"], artifact["features"]
