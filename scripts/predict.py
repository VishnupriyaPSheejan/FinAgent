from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from finagent.config import DATA_PATH, MODEL_PATH
from finagent.data import load_data
from finagent.features import create_features, feature_columns
from finagent.model import load_model


def main():
    if not MODEL_PATH.exists():
        print("Model not found. Run: python scripts/train.py")
        raise SystemExit(1)

    df = load_data(DATA_PATH)
    featured = create_features(df)
    model, features = load_model(MODEL_PATH)

    latest = featured.tail(1)
    prediction = float(model.predict(latest[features])[0])

    print(f"Latest date: {latest['date'].iloc[0].date()}")
    print(f"Predicted next-day transaction volume: {prediction:,.0f}")


if __name__ == "__main__":
    main()
