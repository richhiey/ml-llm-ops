"""ASGI application loaded directly by Uvicorn, from the repository root.

RUN_DIRECTORY pins the saved CNN at startup. Change this explicit path when
operating a different retained model, then restart the server.
"""
from pathlib import Path
from catalog_mlops.service import create_app

RUN_DIRECTORY = Path("work/runs/baseline")
app = create_app(RUN_DIRECTORY)
