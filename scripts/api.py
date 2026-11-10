"""Serve a saved run or a registered model using Uvicorn from the project root."""

import os
from pathlib import Path

from src.service import create_app, create_prediction_app

registered_name = os.environ.get("MODEL_NAME")
if registered_name:
    from src.registry import RegistryPredictor

    state = Path(os.environ.get("MLFLOW_STATE", "work/mlflow"))
    alias = os.environ.get("MODEL_ALIAS", "active")
    app = create_prediction_app(RegistryPredictor(state, registered_name, alias))
else:
    run_directory = Path(os.environ.get("MODEL_RUN_DIRECTORY", "work/runs/baseline"))
    app = create_app(run_directory)
