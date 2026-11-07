"""Plot the retained learning curve and recompute metrics from the prediction CSV.

Uses JSON, CSV, NumPy, scikit-learn and Matplotlib directly; no project helpers.
Evaluation of the saved weights themselves is in scripts/evaluate.py.
"""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    args = parser.parse_args()
    with (args.run / "validation-predictions.csv").open() as stream:
        rows = list(csv.DictReader(stream))
    truth = np.asarray([int(row["label"]) for row in rows])
    predictions = np.asarray([int(row["prediction"]) for row in rows])
    class_names = ("T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
                   "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot")
    print("Count", len(rows))
    print("Accuracy", accuracy_score(truth, predictions))
    print("Macro F1", f1_score(truth, predictions, average="macro"))
    print(classification_report(truth, predictions, labels=range(10),
                                target_names=class_names, zero_division=0))
    history = json.loads((args.run / "history.json").read_text())
    epochs = [row["epoch"] for row in history]
    figure, axis = plt.subplots(figsize=(8, 4), layout="constrained")
    axis.plot(epochs, [row["train_loss"] for row in history], "o-", label="Training")
    axis.plot(epochs, [row["validation_loss"] for row in history], "s--", label="Validation")
    axis.set(xlabel="Epoch", ylabel="Cross-entropy loss (unitless)", xticks=epochs)
    axis.legend()
    figure.savefig("work/learning-history.png", dpi=150)
    plt.close(figure)
    matrix = confusion_matrix(truth, predictions, labels=range(10))
    figure, axis = plt.subplots(figsize=(9, 7), layout="constrained")
    image = axis.imshow(matrix, cmap="Greens", vmin=0)
    axis.set_xticks(range(10), class_names, rotation=40, ha="right")
    axis.set_yticks(range(10), class_names)
    axis.set_xlabel("Predicted category")
    axis.set_ylabel("Actual category")
    figure.colorbar(image, ax=axis, label="Images")
    figure.savefig("work/confusion-matrix.png", dpi=150)
    plt.close(figure)
    print("Saved work/learning-history.png and work/confusion-matrix.png")
