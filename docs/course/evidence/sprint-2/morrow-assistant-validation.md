# Partner assistant validation

The actual partner request and unedited response are retained separately. The six configurations' raw scores and category recalls were independently recomputed from their 3,000-row prediction CSVs. Each full ID and table value in the response matches the retained comparison.

The predeclared policy accepts baseline, weight decay and translation. It rejects longer training for T-shirt/top recall, and lower learning rate/dropout for sneaker recall. Among the accepted distinct configurations, run `cfc92f3749474862bcc32a9269b797d5` has the largest macro F1: `0.8337648911681302`. Its T-shirt/top recall `0.9` and sneaker recall `0.92` pass both thresholds. The baseline difference is `0.0015635475941703225`.

The original eight-epoch run keeps the largest unrestricted raw score, `0.8572382087673285`, but its T-shirt/top recall `0.6466666666666666` fails the partner requirement. The response correctly preserves that experimental result while changing the eligible set. It excludes the baseline autologging repeat from distinct-candidate counting and limits the conclusion to further validation under one fixed split/seed. The checked recommendation required no factual correction.

A small observed macro-F1 difference does not establish significance or a reliable cross-seed gain. This validation is an authored assessment rehearsal, not a student submission or production approval.
