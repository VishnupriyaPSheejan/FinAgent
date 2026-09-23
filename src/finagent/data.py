from pathlib import Path
import pandas as pd


def load_data(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path, parse_dates=["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df


def validate_data(df: pd.DataFrame) -> None:
    required = {
        "date",
        "transaction_volume",
        "target_next_day_volume",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if not df["date"].is_monotonic_increasing:
        raise ValueError("Dates must be sorted in ascending order.")
