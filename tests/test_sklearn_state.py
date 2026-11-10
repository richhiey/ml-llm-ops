"""Verify model identity through a reload of fitted tree state."""

import joblib
import numpy as np

from src.sklearn_model import build_model
from src.training import model_state_sha256


def test_random_forest_identity_tracks_predictions_across_reload(tmp_path):
    rng = np.random.default_rng(426)
    images = rng.integers(0, 256, (40, 28, 28), dtype=np.uint8)
    labels = np.arange(len(images)) % 2
    model = build_model({
        "estimator": "random_forest",
        "params": {"n_estimators": 3, "max_depth": 3},
        "seed": 426,
    }).fit(images, labels)
    path = tmp_path / "model.joblib"
    joblib.dump(model, path)
    restored = joblib.load(path)

    assert model_state_sha256(restored) == model_state_sha256(model)
    np.testing.assert_array_equal(restored.predict_proba(images), model.predict_proba(images))
    restored[-1].estimators_[0].tree_.value[0, 0, 0] += 1
    assert model_state_sha256(restored) != model_state_sha256(model)
