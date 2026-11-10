"""Classification metrics derived from retained predictions and fixed label order."""

import numpy as np
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support
import torch
from torch import nn
from torch.utils.data import DataLoader

from src.data import CLASS_NAMES
from src.preprocessing import normalize_pixels


def score_predictions(truth: np.ndarray, predicted: np.ndarray) -> dict:
    if len(truth) == 0 or truth.shape != predicted.shape:
        raise ValueError("Truth and predictions must be equally sized nonempty vectors")
    precision, recall, f1, support = precision_recall_fscore_support(
        truth, predicted, labels=np.arange(10), zero_division=0)
    matrix = confusion_matrix(truth, predicted, labels=np.arange(10))
    return {
        "count": len(truth), "accuracy": float(accuracy_score(truth, predicted)),
        "macro_f1": float(f1.mean()), "confusion_matrix": matrix.tolist(),
        "class_names": list(CLASS_NAMES),
        "per_class": {
            name: {"precision": float(precision[i]), "recall": float(recall[i]),
                   "f1": float(f1[i]), "support": int(support[i])}
            for i, name in enumerate(CLASS_NAMES)
        },
    }


def evaluate(model: nn.Module, loader: DataLoader) -> tuple[dict, np.ndarray, np.ndarray]:
    model.eval()
    truth, predictions, scores = [], [], []
    total_loss = 0.0
    with torch.inference_mode():
        for raw, labels in loader:
            inputs = normalize_pixels(raw)
            logits = model(inputs)
            total_loss += nn.functional.cross_entropy(logits, labels, reduction="sum").item()
            maximum, predicted = logits.softmax(dim=1).max(dim=1)
            truth.append(labels.numpy())
            predictions.append(predicted.numpy())
            scores.append(maximum.numpy())
    truth = np.concatenate(truth)
    predicted = np.concatenate(predictions)
    report = score_predictions(truth, predicted)
    report["loss"] = total_loss / len(truth)
    return report, predicted, np.concatenate(scores)
