🏷
# What full reproducibility requires

Threadline's catalog lead can now retrieve a registered clothing classifier. A colleague asks a different question: “Can we repeat the work that produced it?” Reloading the saved weights answers which model we have. Repeating its training requires the examples, code, settings and environment that created those weights.

**Reproducibility** means making the necessary conditions available so another engineer can repeat the declared work and check its result. For this project, that includes both evaluating the saved model again and independently training its recorded recipe. The connected history from inputs to result is called **lineage**.

# A score is the end of a chain

Two runs can reach the same rounded score while using different images or code. Follow the chain behind the number.

| Record to retain | What Threadline needs to retrieve | What could go wrong without it |
|---|---|---|
| Code version | Actual source bytes, including training and preparation files | Current code may differ from what produced the saved model |
| Data snapshot | Original image and label bytes, category order and exact split IDs | A new split can change the score without improving learning |
| Parameters and configuration | All recipe settings, including seed, batch size, epochs and learning rate | “Train for longer” leaves the rest of the procedure ambiguous |
| Environment | Python, platform and installed package versions, plus the lock file | Numerical behavior or model loading can differ |
| Model artifact | Saved learned weights, their architecture declaration and the source run | An evaluation screenshot can become detached from the model used for prediction |

A **snapshot** retains a particular state rather than whichever files happen to be current. The run's `source.zip` is the source snapshot; `dataset.json` records the data identity and split; the verified compressed image and label files supply the actual examples; `config.json` records settings; `environment.json` records the measured environment; `model.pt` retains the checkpoint, the file containing learned weights and their declaration.

A Git commit identifies committed code. It does not include an uncommitted intake change. This is why the pipeline archives the actual source bytes and records whether the checkout had edits. The archive remains usable even when someone cannot retrieve the original private commit.

A content **fingerprint**, or hash, lets us check whether file contents match. It cannot retrieve a missing file. Keep the files and their addresses alongside the fingerprints. In the registry, the native model address connects to its experiment, and the validation tag connects to a retained replay report.

# Distinguish two different repetitions

| Activity | What stays saved | What happens again | Evidence |
|---|---|---|---|
| Saved-model evaluation | Original learned weights | Prepare the recorded validation images and compare predictions with labels | Original model identity, evaluation conditions and matching scores |
| Independent training replay | Original recipe and conditions | Construct a new CNN, learn from the recorded training examples, save it and evaluate it | Separate execution record, matching recipe identities and accepted metric differences |

The seed records a starting point for random choices, including initial weights. In this declared environment, repeating it reproduces the starting values. It does not replace the code, image order, optimizer settings or package records.

The independently trained model may learn exactly the same numbers. That is compatible with a genuine replay. Copying the original model directory and calling it a new run is different: it reuses the original execution record without repeating training.

# Decide what counts as agreement before measuring

A **tolerance** is the allowed difference. The [clean-state verification specification](https://github.com/richhiey/ml-llm-ops/blob/main/docs/reproducibility.md) declares the project's checks in advance.

Saved-model accuracy and macro F1 must agree with their recorded values within absolute `1e-12`, or one trillionth: effectively identical numerical results at this precision. Newly trained accuracy and macro F1 may each differ by at most `0.002` on the same validation images. On a `0–1` scale, `0.002` is **0.2 percentage points**.

Those numerical limits apply only after the declared source, data, split, configuration, environment and initial values match. A score inside tolerance with a different split is not a passed replay. A different machine can provide a useful portability observation; it does not satisfy this specification's same-environment requirement automatically.

The new checkpoint file has its own fingerprint. Its file bytes can differ while its learned weight values match exactly, so the report distinguishes file identity from learned-state equality. In the actual author replay, both macro F1 values were `0.8572382087673285` and the learned state matched exactly. That observation does not guarantee the same outcome on every machine.

# Keep proof of execution as well as artifacts

An internally consistent folder cannot establish that a fresh process actually ran. The interpreter path identifies the Python program being run; the import path shows which source folder its application code came from. They help detect accidentally using today's checkout instead of the archived source. Retain those paths and the command outputs showing preparation, original-model evaluation, new training and repeated evaluation.

The verification report checks the retained artifacts and rejects reuse of the original training record. The execution observations show how those artifacts were produced. Together they give a colleague a stronger basis for repeating and checking the result.

Monitoring uses the same habit. Keep the model identity and the incoming image bytes connected to their observed distributions and any known labels. A shifted incoming group measures another operating condition; it should not silently replace the recorded validation images in a training-replay claim.

# Check for Understanding

A colleague reports the same four-decimal macro F1 as the registered run. They used today's source files, cannot find the original split IDs, and copied `model.pt` into a folder named `retrained`.

Prepare a recovery checklist identifying the missing records, the result they have actually demonstrated, and the evidence needed for an independent training claim. State how you would interpret a later close score with a mismatched environment.

<details>
<summary>Solution</summary>

**Result you should get**

The colleague has not established an independent training replay. They need the original code, exact data/split, full settings, environment records and connected model/run evidence. The copied weights may support a saved-model evaluation once its conditions are checked. A close score under another environment remains a portability observation under this specification.

**How**

Trace the number backward through the five records. Retrieve the archived recipe, use a fresh environment, execute its training into a new destination and retain the actual command and interpreter evidence. Compare unrounded metrics only after checking the recorded identities.

</details>

## Learning outcome

Identify the code version, data snapshot, parameters/configuration, environment, and model artifact that must be traceable together for a training run to be reproducible.

## Summary

Threadline can explain a model's result through a connected recipe rather than a filename and score. The saved-model check and independent training replay answer different questions, and both need their conditions and evidence preserved.
