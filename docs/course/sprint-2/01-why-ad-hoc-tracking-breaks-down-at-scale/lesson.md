🏷
# Why ad hoc tracking breaks down at scale

Threadline Retail, our fictional retailer, uses a convolutional neural network, or **CNN**, to suggest categories for prepared clothing thumbnails. This model learns visual patterns from labeled images. Catalog specialists check its suggestions. The first model misses many actual shirts, leaving the team with corrections to make. The engineers want to try several training changes and find out which ones help.

The model, task and research images stay familiar. The new challenge is keeping each learning attempt connected to the conditions and evidence that produced it.

# A score loses its meaning when its context disappears

A **configuration** is the training recipe, including settings such as four epochs and learning rate `0.001`. An epoch is one pass through the training examples, and the learning rate controls the size of weight updates. A **run** is one execution of that recipe. An **experiment** in MLflow groups related runs investigating the same task.

The **baseline** is the reference configuration and result against which changes are compared. A **candidate** is a configuration being considered as an improvement. Before recommending one for catalog review, Threadline needs to connect its recipe, score and saved model.

Consider these plausible record-keeping problems. They are teaching scenarios, not observed company incidents.

| Manual record | What can go wrong | What the team needs to retain |
|---|---|---|
| A notebook prints a better score | It may use different evaluation images or prepare pixels differently | The same image groups and measurement procedure |
| A spreadsheet says “learning rate reduced” | The author may also have changed epochs | Complete configuration for every run |
| Several files are named `best-model.pt` | The selected score can become detached from its weights | An identified model artifact connected to its run |
| Someone copies a rounded value into a report | A transcription error or near tie can change the ranking | Raw metric values and their supporting predictions |
| A colleague leaves with the notebook | The team cannot retrieve the code or installed package versions | Saved code and environment records |

A spreadsheet can still help discuss findings. It is a weak sole source of truth when its entries are manually copied from changing code and outputs.

# Systematic tracking preserves the question and its answer

MLflow is the tool that stores these experiment records. It records **parameters**, meaning settings such as epochs, **metrics**, meaning measured results, and **artifacts**, meaning saved files such as predictions and learned weights. A run ID uniquely identifies the record connecting them. The saved learned weights are the **checkpoint** used to reload this CNN for predictions.

Accuracy and macro F1 describe predictions on separate validation images, which the model did not learn from. Precision asks how many category suggestions were correct, while recall asks how many actual members were found. F1 combines those measures, and macro F1 averages the ten category F1 scores equally. A metric can also have a history, such as validation loss after each epoch. Loss measures disagreement with known labels, with smaller values indicating less disagreement.

This supports **auditability**: another person can inspect what happened and why the team made a decision. Tracking does not automatically make a comparison fair. A perfectly recorded run on another split still answers a different question.

Threadline will keep the original saved baseline as historical evidence. For the new study, **freeze the source** means keep the pipeline's Python code unchanged after completing the intake checks. Candidate recipes deliberately change a training setting while using that same code. Confirming the baseline recipe under the current code gives every comparison a recorded starting point.

The image **split** records which examples belong to training and validation. Keep it fixed too. Saving the source code and environment, including installed package versions, helps another engineer repeat the recipe later. The MLflow tracking guide shows how parameters, metrics and artifacts belong to one run. [MLflow tracking](https://mlflow.org/docs/3.5.1/ml/tracking/)

# Check for Understanding

You inherit a note saying “use the longer run,” an accuracy screenshot and two weight files with the same name in different folders. Prepare a short handoff request: identify at least three independent failure risks, the evidence you would retrieve for each, and what decision must wait until that evidence is available.

<details>
<summary>Solution</summary>

**Result you should get**

The handoff should request complete configurations, matching data/split and metric definitions, and a verified connection between the evaluated predictions and one retrievable model. It should withhold the model-selection decision until those conditions can be checked. Source and environment are also required to replay the result.

**How**

Separate “was a score observed?” from “which conditions and artifact produced it?” The screenshot supplies one observation, while a duplicate filename identifies neither weights nor configuration. Put each finding in a run record and compare only after checking the controls. A larger displayed accuracy cannot settle a macro-F1 decision.

</details>

## Learning outcome

Identify 3+ failure modes of tracking experiments manually (spreadsheets, notebook print statements) once a team runs many models, and explain why systematic tracking matters for auditability.

## Summary

Threadline can now specify the evidence each run must retain. The next decision is which changes form a fair experiment and which metric should choose between them.
