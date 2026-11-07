🏷
# Batch vs real-time inference tradeoffs

Threadline's saved CNN can already produce categories through a batch job and a local HTTP service. The supplier-import team wants a complete result for a manifest each evening. A catalog specialist wants to inspect one suggestion while reviewing an individual item. The model is the same, but the delivery obligations differ.

# Match the arrival pattern to the delivery

**Batch inference** processes a collected group of inputs as one job. Threadline can validate the manifest, pin one saved model and publish a complete prediction CSV for the review team. The output preserves every accepted identifier and its order.

**Real-time inference** responds to an individual request while a client waits. The local HTTP process loads its model at startup and returns a suggestion for a submitted thumbnail. Serving this way introduces an availability obligation because a client can arrive while the process is unavailable.

| Question | Evening supplier import | Individual staff review |
|---|---|---|
| When do images arrive? | A completed manifest | One at a time |
| When is the output needed? | Before the next review batch starts | During the current interaction |
| What is success? | Complete, identified output and recoverable failure | An identified response within the client's acceptable wait |
| What must be operated? | A job and retained result | A continuously reachable process while clients need it |

The [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/docs/inference-brief.md) identifies the evening import as the primary client. A batch route fits that arrival pattern. The staff-review route has a different reason to use request/response delivery.

# Measure the right work

**Latency** is the time a client waits for one result. **Throughput** is how many images a system processes per unit time. A batch can have good throughput while its last item waits for the job to complete. A request service can have short processing time for one image while its capacity is limited by many concurrent clients.

The batch record's `elapsed_seconds` includes loading the model, reading images, predicting and writing the result inside the batch function. Divide delivered images by those seconds to describe observed throughput for that run. The HTTP response's `inference_seconds` measures work inside the already-running process. It excludes network/client time and the earlier model startup.

These timers answer different questions. Use them with their boundaries stated. One warm HTTP request and one small cold batch cannot establish which architecture handles a production workload better. Check input size, hardware, model identity and concurrency before comparing performance observations.

# Cost follows operating requirements

A batch worker can run when a manifest is ready. A request service needs provisioned capacity and operational attention during the hours clients depend on it. Retries, peaks, storage and monitoring also affect resource use.

The local exercise can measure elapsed time and process memory. It does not supply provider pricing or a production traffic trace. Explain the relevant cost drivers qualitatively, and name the missing evidence before estimating a hosting bill.

# Failure handling belongs in the recommendation

Threadline's batch contract publishes a complete output only after every accepted input has been processed. An invalid thumbnail causes the job to fail before that result is published. The team can inspect and quarantine rejected files, preserve their identities, then submit an accepted manifest.

A request service handles validation at the request boundary and returns HTTP `422` for an invalid input. A client must also handle an unavailable service or timeout. Model identity remains important in both patterns so the team can determine which saved weights produced a suggestion.

# Check for Understanding

The import team suggests sending every evening thumbnail as a separate HTTP request because one interactive demonstration felt fast. Write a recommendation for the primary brief. Name two measurements you would collect before claiming that this delivery change improves performance or cost. Explain how the staff-review client's recommendation can differ.

<details>
<summary>Solution</summary>

**Result you should get**

A defensible recommendation keeps batch delivery for the completed nightly manifest and supports request/response for interactive staff review. Evidence should cover a representative manifest's complete delivery time/throughput and the request service's end-to-end latency and capacity under a stated workload. Cost claims also need resource/pricing and operating-hours assumptions.

**How**

Start with each client's arrival pattern and deadline. Check what the demonstration timer included. A single quick response demonstrates a working request path, while the primary client needs complete, identified batch delivery. Compare the whole proposed workload before changing that architecture.

</details>

## Learning outcome

Compare batch and real-time inference patterns - latency, cost, throughput - and justify which pattern the provided inference brief requires.

## Summary

Threadline can choose delivery patterns from client needs and measured behavior while keeping its saved classifier and input contract consistent. Your recommendation identifies latency, throughput, cost drivers and failure handling in terms the catalog team can evaluate.
