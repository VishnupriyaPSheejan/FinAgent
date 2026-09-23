from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from finagent.config import DATA_PATH, MODEL_PATH
from finagent.data import load_data, validate_data
from finagent.model import train_model


def main():
    df = load_data(DATA_PATH)
    validate_data(df)

    result = train_model(
        df,
        model_path=MODEL_PATH,
        test_size=0.2,
        random_state=42,
        n_estimators=500,
        max_depth=6,
        learning_rate=0.05,
    )

    print("\nTraining completed.")
    print(f"Rows: train={result['train_rows']}, test={result['test_rows']}")
    print("Metrics:")
    for key, value in result["metrics"].items():
        print(f"  {key}: {value:.4f}")
    print(f"Model saved to: {result['model_path']}")


if __name__ == "__main__":
    main()
