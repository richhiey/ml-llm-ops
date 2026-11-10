"""A small CNN whose complete architecture is visible in one place."""

from dataclasses import asdict, dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class TrainingConfig:
    seed: int = 426
    epochs: int = 4
    batch_size: int = 64
    learning_rate: float = 0.001
    weight_decay: float = 0.0
    dropout: float = 0.0
    translation_pixels: int = 0
    cpu_threads: int = 2

    def __post_init__(self):
        for name in ("seed", "epochs", "batch_size", "translation_pixels", "cpu_threads"):
            if type(getattr(self, name)) is not int:
                raise ValueError(f"{name} must be an integer")
        if self.epochs < 1 or self.batch_size < 1 or self.cpu_threads < 1 or self.seed < 0:
            raise ValueError("Epochs, batch size and thread count must be positive, seed nonnegative")
        if not 0 < self.learning_rate < 1 or not 0 <= self.weight_decay < 1:
            raise ValueError("Invalid learning rate or weight decay")
        if not 0 <= self.dropout < 1 or not 0 <= self.translation_pixels <= 3:
            raise ValueError("Invalid dropout or translation magnitude")

    def to_dict(self) -> dict:
        return asdict(self)


class CatalogCNN(nn.Module):
    def __init__(self, dropout: float = 0.0):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(32 * 7 * 7, 32), nn.ReLU(),
            nn.Dropout(dropout), nn.Linear(32, 10),
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        return self.classifier(self.features(images))
