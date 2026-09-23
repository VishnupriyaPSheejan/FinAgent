from pathlib import Path

from finagent.config import DATA_PATH
from finagent.data import load_data, validate_data
from finagent.model import train_model


def test_training_pipeline(tmp_path: Path):
    df = load_data(DATA_PATH)
    validate_data(df)

    result = train_model(
        df,
        model_path=tmp_path / "model.joblib",
        test_size=0.2,
        n_estimators=10,
        max_depth=3,
        learning_rate=0.1,
    )

    assert (tmp_path / "model.joblib").exists()
    assert result["test_rows"] > 0
    assert result["metrics"]["rmse"] > 0
