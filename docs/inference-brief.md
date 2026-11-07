# Threadline's inference brief

Threadline's catalog specialists have reviewed category labels for prepared product thumbnails. The ML prototype suggests one of ten categories for a new thumbnail so a specialist can check the suggestion alongside the catalog record.

The primary client is the supplier-import team. Each evening, it receives a completed manifest and wants one output row for every accepted image before the next catalog review begins. A second client is a specialist reviewing an individual upload who needs a response while the item is open.

| Requirement | Nightly import | Individual review |
|---|---|---|
| Input arrival | A completed manifest of many images | One thumbnail at a time |
| Output | A CSV preserving every unique image identifier and its order | A response tied to the submitted image identifier |
| Priority | Complete delivery and throughput | Response latency and service availability |
| Model identity | Pin one verified model for the whole batch | Identify the model loaded by the running process |
| Failure handling | Reject invalid intake before publishing a partial result | Return an explicit validation response for that request |

For the local exercise, use a 20-image sample to verify mechanics and measure elapsed time. This is an exercise sample size, not a measured daily business volume. Record timing units and the work included in the timer. Batch elapsed time covers model loading, reading, prediction and writing inside the application function. The HTTP response's `inference_seconds` measures processing inside the running service and excludes client/network time.

All images must already satisfy the documented grayscale thumbnail contract. Category suggestions require human review. A top softmax score is not a calibrated guarantee of correctness. The team gives each of the ten known categories equal importance when comparing candidates, so validation macro F1 is the primary decision metric.

Recommend an inference pattern for the primary brief and explain the tradeoff for the other client. Local timing alone cannot establish cloud hosting costs or production availability. [Input and output contracts](https://github.com/richhiey/ml-llm-ops/blob/main/docs/contracts.md)
