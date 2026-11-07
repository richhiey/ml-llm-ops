# Threadline's catalog classification service

Threadline Retail is a fictional online fashion retailer. Its catalog team maintains a category for each product so customers and internal tools can find the right kinds of items. Fashion specialists assign category labels and a second reviewer checks their work. The ML team has been asked to investigate whether product thumbnails can support useful category suggestions for that team.

The course uses Fashion-MNIST, a research benchmark built from front-view product images and expert-reviewed fashion categories. Its original work emphasized an accessible, compact classification benchmark that presents more visual ambiguity than handwritten digits. Threadline's service, staff, supplier incidents and operational policies are a fictional course scenario inspired by that setting. [Original dataset paper](https://arxiv.org/abs/1708.07747)

## The first assignment

The catalog team has labeled examples and a list of ten supported categories. The engineers receive a working pipeline scaffold. They must show that a small CNN can learn from those examples, retain its learned weights, and assign a category to an unseen prepared thumbnail.

The team needs evidence before deciding whether to trial the suggestions. A single accuracy number does not show whether shirts are repeatedly mistaken for T-shirts or pullovers. The engineers therefore retain validation predictions, inspect a confusion matrix and review per-category recall. Predictions remain suggestions for expert review. A high softmax score is a model score, not proof that the suggestion is correct.

Supplier images arrive through two workflows. A nightly import needs one identified prediction per thumbnail. A catalog specialist also needs to check a single thumbnail while reviewing an item. Students run the same saved CNN through a batch job and a local HTTP service, then explain which delivery pattern fits each workflow. The pipeline's input contract is prepared 28-by-28 grayscale thumbnails. Shape validation and a justified extension to intake protect that contract.

## The improvement assignment

The first trained model is the team's baseline. Some categories work better than others. Threadline asks the engineers to improve the observed weaknesses while keeping their evidence comparable.

Students declare five hypotheses before training. They investigate longer training, a smaller learning rate, weight decay, dropout and small image translations. Each experiment starts from fresh weights and changes one declared factor relative to the baseline. Every comparison uses the same training IDs, validation IDs, label order and evaluation procedure.

The catalog brief gives each category equal importance, so validation macro F1 is the primary comparison metric. Overall accuracy, class recall, confusion matrices, loss curves and runtime explain the result. The best observed candidate must be identified by its actual MLflow run and saved artifact. A candidate that loses is retained as evidence. Students check an assistant's written recommendation against the raw run records before accepting it.

## The operating assignment

The catalog team is ready for a controlled local trial of the selected model. Another engineer must be able to retrieve the exact recipe and reproduce its evaluation. The active selection must point to a known approved model version. A fresh batch or service process must reveal which version and source run it actually loaded.

During the trial, a prepared supplier window contains a different mix of garments. Another exercise window uses a changed thumbnail-quality recipe, such as reduced contrast or blur. These are constructed course incidents. Students compare the windows with a pinned model, investigate the input and prediction signals, and identify which conclusions require independent expert labels.

If labels establish a quality problem, the team can evaluate a candidate on separate training and evaluation pools. Ordinary and changed-condition validation results remain visible together. A shift alert alone does not establish that retraining is appropriate. Rejecting a poor candidate preserves the existing selection but does not prove that an input-quality problem has been solved.

A separate trial activates an unsuitable model version. Students inspect the evidence, restore a suitable approved version, execute fresh inference and retain the change event. Their audit connects the monitoring observation, decision, selected version, source run and actual predictions. The finished project explains how to repeat a result and how to recover a consumer after a bad change.

## The connection across the project

| Project stage | Threadline's question | Evidence carried forward |
|---|---|---|
| Sprint 1 | Can this pipeline learn and deliver useful category suggestions? | Baseline recipe, saved CNN, validation errors, tested intake, batch and HTTP predictions |
| Sprint 2 | Which controlled change produced a better observed classifier? | Five candidate runs, baseline comparison, checked recommendation and selected artifact |
| Sprint 3 | Can another engineer reproduce, monitor and recover the selected service? | Complete lineage, clean replay, registry selection, justified drift response and rollback with fresh inference |

The supplied lesson names remain unchanged. The catalog assignment develops inside those lessons as the engineering responsibilities grow.
