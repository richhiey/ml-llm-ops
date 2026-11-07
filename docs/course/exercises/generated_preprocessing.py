"""AI-authored review candidate for the course. Deliberately flawed and inactive.

Claim to investigate: each input is prepared on the saved model's expected scale.
This is exercise material and is never imported by the application.
"""

import numpy as np


def prepare_candidate(images):
    raw = np.asarray(images, dtype=np.float32)
    maximum = raw.max(axis=(1, 2), keepdims=True)
    normalized = raw / maximum
    return normalized[:, None, :, :]
