"""Five explicit stages. Feature extraction is shared by training and inference."""
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import root_mean_squared_error, mean_absolute_error

DATA = Path(__file__).parent / "data"
FEATURES = ["temperature_c", "hour", "occupancy"]
TARGET = "demand_kwh"

@dataclass(frozen=True)
class Config:
    alpha: float = 1.0
    range_guard: bool = False
    autolog: bool = False

    def __post_init__(self):
        if not np.isfinite(self.alpha) or self.alpha <= 0:
            raise ValueError("alpha must be finite and positive")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ingest(path=None):
    """CSV -> numeric table with fixed partitions and unique row_id; no row mutation."""
    path = Path(path or DATA / "demand-v1.csv")
    frame = pd.read_csv(path)
    required = ["row_id", *FEATURES, TARGET, "partition"]
    if list(frame.columns) != required:
        raise ValueError(f"Expected columns in order: {required}")
    if frame.empty or frame.row_id.duplicated().any() or frame.isna().any().any():
        raise ValueError("Rows must be nonempty, unique and complete")
    if set(frame.partition) != {"train", "validation", "final"}:
        raise ValueError("Expected fixed train/validation/final partitions")
    if not np.isfinite(frame[[*FEATURES, TARGET]].to_numpy(dtype=float)).all():
        raise ValueError("All features and targets must be finite")
    return frame


def validate_features(frame):
    if frame.empty or not set(FEATURES).issubset(frame.columns):
        raise ValueError("Nonempty input with all feature columns required")
    if not np.isfinite(frame[FEATURES].to_numpy(dtype=float)).all():
        raise ValueError("Features must be finite")
    return frame


def validate_ranges(frame):
    """Bounded extension: reject invalid readings; never clip/drop/reorder valid rows."""
    validate_features(frame)
    for column, low, high in [("temperature_c", -30, 50), ("hour", 0, 23), ("occupancy", 0, 100)]:
        if not frame[column].between(low, high).all():
            raise ValueError(f"{column} outside [{low}, {high}]")
    if not (frame.hour % 1 == 0).all():
        raise ValueError("hour must be an integer")
    return frame.copy(deep=True)


def preprocess(frame, config):
    """Table -> unchanged feature order; scaler is fitted on training rows by train()."""
    checked = validate_ranges(frame) if config.range_guard else validate_features(frame)
    return checked[FEATURES].copy()


def train(features, target, config):
    """Training-only features/target -> fitted scaler and Ridge model."""
    model = Pipeline([("scale", StandardScaler()), ("ridge", Ridge(alpha=config.alpha, solver="svd"))])
    return model.fit(features, target)


def evaluate(model, features, target):
    """Held-out inputs -> primary RMSE and diagnostic MAE, both kWh, lower better."""
    predictions = model.predict(features)
    return {"rmse_kwh": float(root_mean_squared_error(target, predictions)),
            "mae_kwh": float(mean_absolute_error(target, predictions))}


def run_pipeline(config=Config(), data_path=None, partition="validation"):
    if partition not in {"validation", "final"}:
        raise ValueError("Evaluation partition must be validation or final")
    frame = ingest(data_path)
    features = preprocess(frame, config)
    training = frame.partition == "train"
    heldout = frame.partition == partition
    model = train(features.loc[training], frame.loc[training, TARGET], config)
    metrics = evaluate(model, features.loc[heldout], frame.loc[heldout, TARGET])
    return model, metrics, frame
