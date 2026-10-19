🏷️
# Batch vs real-time inference tradeoffs

Linden Facilities receives all 24 planned hourly inputs together. The planner needs one complete file within `60` seconds; nobody is waiting on individual HTTP responses. The inference pattern should follow that use case.

## Your route through this lesson

Connect input arrival, latency, throughput and resource obligations to a serving choice. Read the worked reasoning, use the tables/diagram to test your mental model, then attempt the applied check before opening its solution. No runtime is required for the reading; the linked notebook lets you inspect the implementation afterward.

**Finish with:** A bounded batch recommendation and its acceptance measurements.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb#scrollTo=batch-proof). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Which latency matters?

Use the comparison below to connect each pattern to the waiting time and resource obligation it creates. Latency is elapsed time until the required result is available; throughput counts completed records per unit time.

| Dimension | Batch | Real-time requests |
|---|---|---|
| Inputs | A bounded group available together | Arrive individually over time |
| Useful latency | Whole job completes before deadline | Individual response budget |
| Resource cost | Resources needed during the job | Often keep a service warm and available |
| Throughput | Can reuse one model load for many rows | Depends on workers, concurrency and queuing |
| Linden fit | Matches the supplied planning brief | Adds an availability obligation the brief does not need |

The [inference brief](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/inference-brief.md) selects batch. Request serving remains a prepared architectural comparison, not a measured endpoint in this scaffold. Neither pattern is universally cheaper or faster; hardware, workload and availability needs matter.

## Separate waiting time from work completed

A planner who needs the whole file cannot use “the first prediction is ready” as a success condition. If 23 rows arrive quickly and the last row never arrives, the planning job has failed. The relevant latency therefore ends when the complete output is available, including model loading and file writing.

Throughput answers a different question: how many rows were completed per second? In an illustrative job with 24 rows and 6 seconds elapsed, throughput is `24 / 6 = 4` rows/second. This arithmetic is not a measurement of our helper. It also does not mean every independent request would return in `0.25` seconds: the job may spend most of its time loading the model and then predict all rows together.

## What a permanent service adds

Real-time inference accepts inputs as callers submit them and returns responses within a request budget. The model is often kept in memory so each request avoids loading it again. That can help response latency, but the system must also handle startup, concurrent callers, failures and periods with no traffic. “The model is small” does not remove those obligations.

Batch inference can load the model once, process a bounded input and exit after writing results. This fits work that arrives together and has a completion deadline. It may be a poor choice when a caller must wait for the next scheduled batch to get an urgent answer. The same fitted model can support either pattern; the surrounding input, execution and delivery contract changes.

## Reason about cost without inventing a price

Cost depends on resource use and availability requirements, not the word “batch” or “API”. Compare what must run and for how long:

| Question | Linden's brief | What a different request brief would need |
|---|---|---|
| When do inputs arrive? | All 24 planned rows together | Arrival rate and peak bursts |
| When is output useful? | Complete file within 60 seconds | Budget for each caller |
| What must stay available? | The process while a job executes | A service during its availability window |
| What should be measured? | Complete rows, elapsed job time, selected version | Request latency distribution, throughput under load, availability |

A busy service can use hardware efficiently. An infrequent batch can avoid keeping a worker idle. Neither observation provides a universal price ranking. Linden's defensible recommendation is that batch meets the stated delivery need with a smaller availability obligation; actual cost would require resource and pricing evidence.

## What our evidence can establish

`batch.json` records the row count, elapsed seconds, rows per second, source run and resolved model version. Timing includes loading the model and writing the CSV. We check completion against `60` seconds, not against one author's exact observed time.

The active alias is resolved once at job start. The job then loads the corresponding version URI. An alias change during a job should not mix versions across its rows; the next job resolves again. That is a small but meaningful serving contract.

## Write the decision a planner could accept

A useful decision contains four connected statements: the arrival pattern, the needed delivery time, the chosen pattern and the evidence that will show it worked. For Linden: inputs are available together; the planner needs one complete 24-row file within 60 seconds; choose batch; verify row alignment, version identity and whole-job completion.

Now change only one requirement: a caller needs an answer for each new reading within 200 ms. That is an illustrative alternative, not the implemented brief. The existing batch measurement cannot establish that request budget. You would need a serving design and a load test that includes queuing and network work. Keep the actual Linden recommendation separate from that hypothetical redesign.

## Check for Understanding

A teammate recommends a permanent endpoint because one local batch row takes little compute. Identify the missing evidence and decide which completion measure Linden should accept now.

▶️ **Solution** *(toggle)*

> **Result you should get:** choose batch completion for all `24` rows within `60` seconds. One row's compute time does not establish request latency or justify a permanent service.
>
> **How:** map the input arrival pattern and planner deadline to the measured job. For an endpoint, request arrival rate, network/queue latency and availability costs would still need evidence.

![Batch vs real-time inference tradeoffs: evidence path](assets/batch-vs-real-time-inference-tradeoffs__01__en.png)

## Learning outcome

Compare batch and real-time inference patterns - latency, cost, throughput - and justify which pattern the provided inference brief requires.

## Summary

Linden’s shared input arrival and whole-job deadline support batch inference. You can justify that choice without inventing request-serving timings or universal cost claims.
