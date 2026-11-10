"""Native Uvicorn entry file; the active registry version is pinned at startup."""

import os
from pathlib import Path
from src.registry import RegistryPredictor
from src.service import create_prediction_app

# Native Uvicorn reads deployment configuration from this terminal environment.
STATE_DIRECTORY = Path(os.environ.get("MLFLOW_STATE", "work/mlflow"))
REGISTERED_NAME = os.environ.get("MODEL_NAME", "fashion-mnist-cnn")
ACTIVE_ALIAS = os.environ.get("MODEL_ALIAS", "active")
app = create_prediction_app(
    RegistryPredictor(STATE_DIRECTORY, REGISTERED_NAME, ACTIVE_ALIAS)
)
