"""Local HTTP prediction service using the same saved model and preprocessing as batch jobs."""

from pathlib import Path
import time

from fastapi import FastAPI, HTTPException
import numpy as np
from pydantic import BaseModel, ConfigDict, Field, StrictInt

from catalog_mlops.inference import Predictor


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    image_id: str = Field(min_length=1, max_length=200)
    pixels: list[list[StrictInt]]


def create_app(run_directory: Path) -> FastAPI:
    return create_prediction_app(Predictor(run_directory))


def create_prediction_app(predictor) -> FastAPI:
    """Serve the saved or registry-resolved model already loaded at startup."""
    app = FastAPI(title="Catalog thumbnail classifier", version="1.0.0")

    @app.get("/health")
    def health():
        return {"status": "ready", "model": predictor.identity}

    @app.post("/predict")
    def predict(request: PredictionRequest):
        started = time.perf_counter()
        try:
            raw = np.asarray(request.pixels)
            if raw.shape != (28, 28) or raw.min() < 0 or raw.max() > 255:
                raise ValueError("Expected 28 rows of 28 integer pixels in the range 0 to 255")
            prediction = predictor.predict(raw.astype(np.uint8)[None, :, :], [request.image_id])[0]
        except (ValueError, OverflowError) as error:
            raise HTTPException(status_code=422, detail=str(error)) from error
        return {"prediction": prediction, "model": predictor.identity,
                "inference_seconds": time.perf_counter() - started}

    return app
