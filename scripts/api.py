"""ASGI application loaded directly by Uvicorn, from the repository root.

RUN_DIRECTORY pins the saved CNN at startup. Set MODEL_RUN_DIRECTORY in the service terminal
when operating a different retained model, then restart the server.
"""
import os
from pathlib import Path
from src.service import create_app

RUN_DIRECTORY = Path(os.environ.get("MODEL_RUN_DIRECTORY", "work/runs/baseline"))
app = create_app(RUN_DIRECTORY)
