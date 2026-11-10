"""Pixel features consumed by fitted image classifiers."""

import numpy as np


def flatten_pixels(images: np.ndarray) -> np.ndarray:
    """Convert each image to one row of scaled pixel features."""
    return images.reshape(len(images), 784).astype(np.float32) / 255.0
