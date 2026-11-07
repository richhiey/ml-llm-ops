"""One explicit raw-image boundary and one normalization shared by every route."""

import numpy as np
import torch


def validate_images(images: np.ndarray) -> np.ndarray:
    """Accept a nonempty uint8 batch of 28-by-28 grayscale thumbnails unchanged."""
    if not isinstance(images, np.ndarray):
        raise ValueError("Images must be a NumPy array")
    if images.dtype != np.uint8:
        raise ValueError("Raw image pixels must use uint8, representing values from 0 to 255")
    if images.ndim != 3 or images.shape[1:] != (28, 28) or len(images) == 0:
        raise ValueError("Expected a nonempty batch with shape (N, 28, 28)")
    return images


def preprocess(images: np.ndarray) -> torch.Tensor:
    raw = validate_images(images)
    return normalize_pixels(torch.from_numpy(raw.copy()).unsqueeze(1))


def normalize_pixels(raw: torch.Tensor) -> torch.Tensor:
    if raw.dtype != torch.uint8 or raw.ndim != 4 or tuple(raw.shape[1:]) != (1, 28, 28):
        raise ValueError("Expected uint8 grayscale tensors with shape (N, 1, 28, 28)")
    return raw.to(dtype=torch.float32).div(255.0)
