# Threadline's catalog classification task

Threadline Retail is a fictional online clothing shop. Every product needs a category, such as `Dress`, `Shirt` or `Bag`, so customers can find it through the shop's categories and filters. A wrongly categorized item can disappear from the results a shopper expects.

Catalog staff inspect product images and assign those categories. The project investigates a possible aid: a model suggests a category, and a person checks it. The task is image classification—choosing one category from a fixed list based on an image. The course does not assume that every suggestion is correct or that staff review can be removed.

## The real research data behind the story

Fashion-MNIST supplies real product thumbnails and known category labels. Each image is a `28×28` grayscale grid, with brightness recorded at each pixel. Its ten clothing, footwear and bag categories include visually similar items that a small model can confuse.

The original research created a compact image-classification benchmark. Threadline, its staff and supplier incidents are the fictional setting used to learn from it. [Original dataset paper](https://arxiv.org/abs/1708.07747) · [Dataset card and limits](https://github.com/richhiey/ml-llm-ops/blob/main/docs/dataset-card.md)

## First, make one model learn and inspect its mistakes

A machine-learning model learns from examples rather than receiving a hand-written rule for every image. Training adjusts its learned numbers, called weights, using images with known labels. This project uses a small convolutional neural network, or CNN, which learns useful patterns from small areas of the images.

Separate labeled images let the team check its predictions without updating those weights. The author's first trained reference model found only `117` of `300` actual shirts. It confused many of the others with coats or T-shirts/tops. That gives the catalog team a concrete weakness to investigate rather than treating overall accuracy as the whole result.

Students save the model and use it for two clients: an evening file of many images awaiting suggestions, and a staff member waiting for one suggestion while reviewing an item. Incoming files must satisfy the image-format and brightness rules before prediction.

## Then, ask which change helps

The team plans five separate changes to the training settings. Each starts a new model from the same initial values, learns on the same images and is checked in the same way. This helps distinguish the effect of one chosen setting from other changes.

MLflow keeps the settings, measurements and saved files together for each training attempt, called a run. Students compare actual runs, inspect category tradeoffs and check an assistant's written recommendation against the recorded evidence.

The unfamiliar partner, Morrow Market, adds minimum recall requirements for two categories. Its decision can differ from Threadline's equal-category ranking. The partner's requirements remain part of its brief when work continues.

## Finally, make the chosen model retrievable and recoverable

The team needs to know which saved model should answer requests. A model registry records versions and the evidence attached to them. Students will check that a colleague can repeat a past result using its recorded images, code, settings and Python packages.

They will also distinguish two operating questions: do incoming images differ from earlier images, and, when checked labels are available, has prediction quality fallen? A changed input pattern alone does not answer the quality question. Later exercises deliberately change thumbnails to investigate this distinction.

If an unsuitable replacement is selected, the team must restore a previously approved version and verify which model a newly started prediction process actually loads. The change record must connect the observation, decision, selected version and resulting predictions.

| Project stage | Question for the catalog team |
|---|---|
| Sprint 1 | Can one small model learn the categories, and where does it make mistakes? |
| Sprint 2 | Which controlled change produced a better observed result for this brief? |
| Sprint 3 | Can another engineer repeat the result, check ongoing behavior and recover from a bad selection? |
