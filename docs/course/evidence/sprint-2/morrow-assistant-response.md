Recommend the weight-decay configuration from run `cfc92f3749474862bcc32a9269b797d5` for further validation under Morrow's supplier-trial requirements. It achieves T-shirt/top recall `0.9` and sneaker recall `0.92`, satisfying both gates, and has the highest validation macro F1 among eligible distinct configurations at `0.8337648911681302`. It changes only weight decay from `0.0` to `0.001`. Its macro-F1 gain over baseline run `c538c971fdf44099b750af1d9513458b`, whose score is `0.8322013435739599`, is `0.0015635475941703225`, approximately `0.156` percentage points.

The original unrestricted winner, run `99ce416e13ee4eeba47f6adf05d4ed7c`, retains the highest raw macro F1 at `0.8572382087673285`. Its T-shirt/top recall of `0.6466666666666666` fails Morrow's `0.80` requirement, so it is excluded from this partner's eligible set. The dropout configuration also scores above the recommendation, at `0.8342234426065518`, but fails the sneaker recall gate. Applying the predeclared gates changes which configurations can be recommended while preserving every recorded metric and the unrestricted ranking.

| Configuration and full run ID | Validation macro F1 | T-shirt/top recall | Sneaker recall | Partner decision |
|---|---:|---:|---:|---|
| Baseline `c538c971fdf44099b750af1d9513458b` | `0.8322013435739599` | `0.88` | `0.93` | Passes both gates, lower macro F1 than weight decay |
| Eight epochs `99ce416e13ee4eeba47f6adf05d4ed7c` | `0.8572382087673285` | `0.6466666666666666` | `0.9366666666666666` | Fails T-shirt/top recall |
| Lower learning rate `1f87f84d63604000ab49e1c3405f9da1` | `0.7955162471435455` | `0.8266666666666667` | `0.8933333333333333` | Fails sneaker recall |
| Weight decay `cfc92f3749474862bcc32a9269b797d5` | `0.8337648911681302` | `0.9` | `0.92` | Passes both gates, highest eligible macro F1 |
| Dropout `519ae2bd2cc941b7abd632338d44c104` | `0.8342234426065518` | `0.8566666666666667` | `0.8733333333333333` | Fails sneaker recall |
| Translation `a8a29bfff80945c9b488b3008021ec6c` | `0.7841395984919902` | `0.8566666666666667` | `0.9066666666666666` | Passes both gates, lower macro F1 than weight decay |

Run `5673c459ef284ea4904a9d42d38d8e7e` is the autologging repeat of the baseline configuration and adds no distinct candidate. This recommendation is based on the fixed validation set and seed `426`. The small observed gain and partner gate compliance support further validation. Repeatability and operational acceptance require additional evidence.
