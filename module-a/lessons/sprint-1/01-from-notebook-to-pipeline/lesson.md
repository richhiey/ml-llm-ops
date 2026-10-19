🏷️
# From notebook to pipeline

Linden Facilities can fit an energy-demand model in a notebook, but the planner needs the same 24-row prediction job tomorrow. A cell run out of order can silently use yesterday's features or a model fitted on different rows. A successful printout does not explain how to rebuild it.

## Your route through this lesson

Explain two paths—historical fitting/evaluation and planned prediction—and locate the five stage boundaries. Read the worked reasoning, use the tables/diagram to test your mental model, then attempt the applied check before opening its solution. No runtime is required for the reading; the linked notebook lets you inspect the implementation afterward.

**Finish with:** A five-stage sketch with the target and fitted preprocessing placed correctly.

Use the [setup and execution guide](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/docs/learning-guide.md) and [Colab guided notebook](https://colab.research.google.com/github/richhiey/ml-llm-ops/blob/main/module-a/notebooks/01-pipeline-and-extension.ipynb#scrollTo=stage-map). The [pipeline source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/pipeline.py) and [tracking/registry source](https://github.com/richhiey/ml-llm-ops/blob/main/module-a/src/campus_mlops/lifecycle.py) are the code you will inspect.

## Start with the job, not the notebook cells

Imagine the planner asks you to rerun yesterday's estimate after a colleague changes the occupancy plan. You can still see a fitted model in memory, but you cannot tell whether the temperature column was scaled before or after that model was fitted. Running the prediction cell again may produce numbers. It does not resolve which preparation those numbers depend on.

The useful question is: **what must another person supply to get the same job done?** In Linden's case, that includes the planned inputs, the fitted preprocessing and estimator, and the rules connecting them. A pipeline moves those dependencies from the author's memory into an inspectable execution path. A notebook may remain the interface; a terminal command can call the same functions.

## A pipeline makes dependencies explicit

A **pipeline** connects stages through declared inputs and outputs. Reproducibility means another engineer can recover the source, data, configuration and environment and obtain an agreed result. Neither requires a large orchestration framework: our Python functions already expose the boundaries.

| Stage | Linden input → output | Failure the boundary can expose |
|---|---|---|
| Ingestion | Fixed CSV → checked table | Duplicate `row_id` or absent fields |
| Preprocessing | Checked table → ordered features | Missing or invalid measurements |
| Training | Train features and target → fitted model | Fitting on held-out rows |
| Evaluation | Held-out features and target → RMSE/MAE | Scoring different rows across comparisons |
| Inference | Active fitted model and planned inputs → predictions | Loading a different version than intended |

The target is `demand_kwh`. The inputs are `temperature_c`, `hour`, and `occupancy`. `row_id` aligns records; `partition` fixes their evaluation role. Neither belongs among the model features. A **fitted model** includes learned preprocessing: Linden's scaler stores training means and scales alongside the regression coefficients.

## Walk a historical row and a planned row through the system

Consider an illustrative historical record with `temperature_c=12`, `hour=9`, `occupancy=40` and a known `demand_kwh`. Those values describe a teaching example, not a claimed row from the snapshot. Ingestion reads and checks its table. Preprocessing selects the three features in the declared order. If its `partition` is `train`, training may use its known target to fit the model. If the partition is `validation`, evaluation compares a prediction with that target without fitting on the row.

A planned record may have the same three feature values but no known demand yet. Inference can transform those features using the already fitted scaler and return `prediction_kwh`. It cannot compute the prediction's error until an actual demand value is observed. This is why “the CSV was produced” and “the model met its error requirement” need different checks.

| Object | Learns from training rows? | Used again at inference? |
|---|---|---|
| Feature-column list | No; it is a declared interface | Yes, in the same order |
| Fitted scaler | Yes; it learns means and scales | Yes, without fitting again |
| Fitted Ridge estimator | Yes; it learns coefficients | Yes, to predict |
| Validation RMSE | No; it measures a held-out result | No; it is decision evidence |

## Training and inference share a contract

A **contract** names what a stage accepts and guarantees. Training sees known demand values; inference sees only planned features. Both need the same column order and transformations. Fitting another scaler on tomorrow's batch changes the meaning of its inputs even if the code runs.

The helper stores a `StandardScaler` and a Ridge regressor together. Ridge is a linear model with a penalty that limits coefficient size. Evaluation happens on the snapshot's fixed validation rows; the separate final rows are reserved until configuration selection is complete.

## Why the boundaries catch different mistakes

Suppose a supplier duplicates a record. That is an ingestion problem because the identity of the input table is wrong before any model work. Suppose the planned table includes `hour=24`. That is a feature-contract problem: the number is finite, but outside the accepted domain. Suppose a colleague fits the scaler using validation rows. The table may be well formed, yet learned preprocessing has used held-out information. A single final score cannot tell you which of these went wrong.

A stage boundary gives you a smaller question to test: did the input meet the contract, and did this function return the promised object? This makes investigation manageable. It does not automatically supply scheduling, retries or monitoring; those are additional concerns around the sequence.

## Put the five stages back together

Before opening code, sketch two paths on paper: historical data through fitting and evaluation; planned features through a fitted model to a CSV. Mark the target's location and the point where fitting stops. Compare your sketch with the stage table and diagram. If your inference path fits a scaler, or your evaluation path uses training rows as its held-out check, revise the sketch and explain the failure that would result.

The repository's `pipeline.py` implements the first four stages; `batch_predict` in `lifecycle.py` owns inference. You will inspect those boundaries in the guided execution. For now, the goal is to explain why the boundaries exist, not memorize function names.

## Check for Understanding

Linden's teammate fits a new scaler on the planned batch and says the model is unchanged because the regression coefficients came from yesterday's file. Diagnose the resulting contract failure and specify the artifact that must be handed over.

▶️ **Solution** *(toggle)*

> **Result you should get:** the batch is transformed with different learned statistics, so the regression receives a different feature representation. Hand over the fitted scaler and regressor together.
>
> **How:** trace which object learned means/scales during training. Inference must reuse that fitted object; it may validate/extract planned features but must not fit on the batch.

![From notebook to pipeline: evidence path](assets/from-notebook-to-pipeline__01__en.png)

## Learning outcome

Explain why a reproducible training/inference pipeline replaces a one-off notebook workflow, and identify the 5 stages a production ML pipeline must cover - ingestion, preprocessing, training, evaluation, inference.

## Summary

Linden’s notebook result now has an explicit path from source data to prediction. You can inspect the stage boundaries and see why fitted preprocessing must travel with the model.
