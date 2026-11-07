"""Read the research arrays with NumPy and draw the ten categories. No project helpers."""
from pathlib import Path
import gzip
import json
import struct
import numpy as np
import matplotlib.pyplot as plt

Path("work").mkdir(exist_ok=True)
data = Path("data/fashion-mnist")
manifest = json.loads((data / "manifest.json").read_text())
with gzip.open(data / "train-images-idx3-ubyte.gz", "rb") as stream:
    magic, count, height, width = struct.unpack(">IIII", stream.read(16))
    images = np.frombuffer(stream.read(), dtype=np.uint8).reshape(count, height, width)
with gzip.open(data / "train-labels-idx1-ubyte.gz", "rb") as stream:
    label_magic, label_count = struct.unpack(">II", stream.read(8))
    labels = np.frombuffer(stream.read(), dtype=np.uint8)
assert (magic, height, width) == (2051, 28, 28)
assert label_magic == 2049 and label_count == count

class_names = ("T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot")
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
