"""Native Uvicorn entry file; the active registry version is pinned at startup."""

from pathlib import Path
from catalog_mlops.registry import RegistryPredictor
from catalog_mlops.service import create_prediction_app

# Set these visible deployment choices before launching Uvicorn.
STATE_DIRECTORY = Path("work/mlflow")
REGISTERED_NAME = "threadline-catalog"
ACTIVE_ALIAS = "active"
app = create_prediction_app(
    RegistryPredictor(STATE_DIRECTORY, REGISTERED_NAME, ACTIVE_ALIAS)
)
