# Fashion-MNIST dataset card

Fashion-MNIST contains 70,000 grayscale product thumbnails, each 28 by 28 pixels with one category label. The original split contains 60,000 training and 10,000 test images. Source products have expert-assigned silhouette categories reviewed by another team. Front-view thumbnails were converted to the compact benchmark format. White products were excluded during construction because they had low contrast against the original background. [Original dataset paper](https://arxiv.org/abs/1708.07747)

| Label | Category |
|---|---|
| `0` | T-shirt/top |
| `1` | Trouser |
| `2` | Pullover |
| `3` | Dress |
| `4` | Coat |
| `5` | Sandal |
| `6` | Shirt |
| `7` | Sneaker |
| `8` | Bag |
| `9` | Ankle boot |

## Local CPU partitions

`python scripts/prepare_data.py` downloads the four original compressed IDX files, checks their SHA256 values and records deterministic stratified partitions in `data/fashion-mnist/manifest.json`. An image identifier such as `train:56368` means index `56368` in the original training file. The labels never become input features.

| Partition | Images | Role |
|---|---|---|
| `train` | 12,000 | Fresh baseline and controlled experiment training |
| `validation` | 3,000 | Fixed candidate comparison |
| `reference` | 1,000 | Operational reference window |
| `current` | 1,000 | Independent incoming window |
| `adaptation` | 2,000 | Labeled training pool for a justified operational response |
| `shift_validation` | 2,000 | Independent changed-condition evaluation |

Each partition has equal counts from the ten classes, and all partition indices are disjoint. These pools occupy 21,000 official training images. The remaining official training images are unused by the CPU profile. The official test split is reserved until model selection is recorded. Constructed shift transformations retain their source-image IDs and recipes. Training and evaluation must not contain transformed copies of the same source image.

## Input and interpretation limits

The reusable preprocessing function accepts uint8 grayscale batches with shape `(N, 28, 28)`, creates a channel dimension and divides by 255 once. It does not reproduce the research team's original photograph-conversion pipeline. Incoming PNG files must already be prepared 28-by-28 grayscale thumbnails.

The task has one known category per image. Performance on phone photos, unfamiliar product types or multi-object scenes requires separate data and evaluation. Standard Fashion-MNIST splits also have documented near-duplicate images. Disjoint indices do not establish visual independence. [Near-duplicate study](https://arxiv.org/abs/1906.08255)

## Access and attribution

The data are available from the original repository under its MIT license. Retain the authors' attribution and original license when redistributing data. Cite Han Xiao, Kashif Rasul and Roland Vollgraf, *Fashion-MNIST, a Novel Image Dataset for Benchmarking Machine Learning Algorithms* (2017). [Dataset repository](https://github.com/zalandoresearch/fashion-mnist) · [Original license](https://github.com/zalandoresearch/fashion-mnist/blob/master/LICENSE)
