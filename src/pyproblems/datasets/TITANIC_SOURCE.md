# Titanic passenger data

`titanic.csv` contains all 1,309 labelled passenger records from the
[Harrell/Vanderbilt `titanic3` CSV](https://hbiostat.org/data/repo/titanic3.csv),
retrieved on 2026-10-17. The underlying dataset is also catalogued as
[OpenML Titanic, version 1, dataset 40945](https://www.openml.org/d/40945),
whose metadata lists its licence as **Public** and credits Frank E. Harrell Jr.
and Thomas Cason. Their compilation draws on historical passenger records,
including Encyclopedia Titanica; see the
[dataset description](https://www.openml.org/api/v1/json/data/40945).

SHA-256 of the downloaded source CSV:
`db6df9666818c69a753cd85d743e01502c8518b00579b6aada0d4fc5a66ccb9d`.

This is a complete labelled source dataset, not Kaggle's 891-row training
file plus guessed labels for its 418-row test file. No claim is made that
individual values or labels exactly match Kaggle's competition records.
Kaggle's example submission is a prediction baseline, not ground truth.

The packaged snapshot keeps source row order and retains `survived`, `pclass`,
`name`, `sex`, `age`, `sibsp`, `parch`, `ticket`, `fare`, `cabin` and `embarked`,
renamed to the familiar title-case column names used by the exercise.
`PassengerId` is an added **local row ID**, numbered 1 through 1,309, not a
Kaggle identifier. Values and blank cells in retained columns are preserved.
The source fields `boat`, `body` and `home.dest` are omitted. In particular,
lifeboat assignments and body-recovery records reveal information about the
outcome and must not be used to predict it.

The exercise reserves its own stratified test split from these labelled rows.
No network access or Kaggle account is needed when running it.

Source attribution is retained here; this dataset is not authored by this
project, and the repository's MIT code licence is not a claim of ownership of
the underlying data. See the linked source for its terms and documentation.
These historical passenger records do not include the ship's crew and are not
a random sample of modern passengers or disasters.
