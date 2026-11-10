"""Load Fashion-MNIST with TorchVision and draw the ten categories."""
from pathlib import Path
import json
import numpy as np
import matplotlib.pyplot as plt
from torchvision.datasets import FashionMNIST

Path("work").mkdir(exist_ok=True)
data = Path("data/fashion-mnist")
manifest = json.loads((data / "manifest.json").read_text())
dataset = FashionMNIST(root=data, train=True, download=True)
images = dataset.data.numpy()
labels = dataset.targets.numpy()

class_names = manifest["class_names"]
train_ids = manifest["partitions"]["train"]
validation_ids = manifest["partitions"]["validation"]
print(images.shape, images.dtype, labels.shape)
print("Training counts", np.bincount(labels[train_ids], minlength=10))
print("Validation counts", np.bincount(labels[validation_ids], minlength=10))
assert set(train_ids).isdisjoint(validation_ids)

figure, axes = plt.subplots(2, 5, figsize=(11, 4.5), layout="constrained")
for label, axis in enumerate(axes.flat):
    image_id = next(index for index in train_ids if labels[index] == label)
    axis.imshow(images[image_id], cmap="gray", vmin=0, vmax=255)
    axis.set_title(class_names[label])
    axis.set_xlabel(f"train:{image_id}")
    axis.set_xticks([])
    axis.set_yticks([])
figure.savefig("work/training-examples.png", dpi=150)
