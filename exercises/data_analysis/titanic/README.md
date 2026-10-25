# Predicting survival on the Titanic 🚢

> **Difficulty:** 🌶️🌶️🌶️
>
> **Before you start:** basic Python, pandas and plotting, and the optional
> scientific stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** exploring data, thinking about informative features,
> comparing two classifiers with cross-validation, and evaluating on unseen data.
>
> **Check:** `uv run pytest exercises/data_analysis/titanic/ -q` checks the pipeline.
> Your notebook's plots, comparisons and explanations check the investigation;
> there is no required accuracy score.

Can you predict which passengers survived the Titanic disaster, and show that
your model works on passengers it has not seen? This is a first encounter with
a machine-learning workflow, not an exercise in implementing the algorithms.
The notebook provides the library code so you can focus on the data and the
experiment.

Work in the [Titanic notebook](investigate.ipynb). Its setup calls
`load_passengers()` in [titanic.py](titanic.py), which
returns all 1,309 labelled historical `titanic3` records as a pandas DataFrame
with numeric columns converted and blanks marked as missing, then reserves a
stratified 20% test set with a fixed seed.
See the [source note](data/TITANIC_SOURCE.md).

> [!IMPORTANT]
> Leave the test set alone until your final evaluation. Explore and compare
> models using only the training partition. The final test asks whether the
> choices you have already made work on unseen passengers.

## Data

The data is a pandas data frame. Here are the column descriptions.

| Column | Meaning | Use here |
| --- | --- | --- |
| `Survived` | Recorded outcome: 0 or 1 | Outcome |
| `Pclass` | Ticket class: 1, 2 or 3 | Categorical feature |
| `Sex` | Recorded sex | Categorical feature |
| `Age` | Age in years, including fractional ages | Numeric feature; some missing |
| `SibSp`, `Parch` | Counts of siblings/spouses and parents/children aboard | Numeric features |
| `Fare` | Recorded ticket fare | Numeric feature; some missing |
| `Embarked` | Port code: C, Q or S | Categorical feature; some missing |
| `PassengerId`, `Name`, `Ticket`, `Cabin` | Local row ID and other records | Excluded from these models |

## 1. Meet the passengers

Explore the training set by looking at: missing values, distributions,
and survival proportions by passenger class, recorded sex, age and family
counts. The notebook shows how to join features and labels for exploration,
count missing values, and summarise outcomes within groups.

Which features look informative? Which might carry similar information?

## 2. Build the classifiers

Open [titanic.py](titanic.py). `load_passengers()` only
fixes types and marks missing values, which learns nothing from the data. The
steps that *do* learn from data are supplied by `make_preprocessor()`, which
returns an unfitted `ColumnTransformer`:

- `SimpleImputer` fills in missing values (the median for numbers, the most
  common value for categories).
- `StandardScaler` puts numeric features on comparable scales.
- `OneHotEncoder` turns category labels into indicator columns.
- `ColumnTransformer` applies these steps to the named columns.

Your task is to complete `titanic_pipeline`. It should return an
**unfitted** scikit-learn
[`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html)
that chains data preprocessing (from `make_preprocessor()`) with either a
[logistic regression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) or
[random forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)
classifier. Logistic regression estimates a survival probability from a weighted
combination of the features; a random forest combines many decision trees and
can capture patterns a weighted sum cannot. See the docstring for details.

<details>
<summary>💡 Hint 1: assembling the pipeline</summary>

A `Pipeline` is built from a list of `(name, step)` pairs. Each step passes its
output to the next, and the last step is the model. For example,
`Pipeline([("scale", StandardScaler()), ("model", KNeighborsClassifier())])`
scales the inputs and then classifies them. Use the step names required by the
docstring for your pipeline, and import the classes you need.

</details>

<details>
<summary>💡 Hint 2: passing extra settings</summary>

Inside the function, `kwargs` is a dictionary of the extra settings supplied by
the caller. Passing `**kwargs` when constructing the chosen classifier unpacks
those entries as keyword arguments. Pass them to the classifier, not to the
preprocessor or the pipeline.

</details>

Check your work with `uv run pytest exercises/data_analysis/titanic/ -q`.

Why a pipeline? Replacement values and category encodings are learned from data
too, so they must be learned only from the training rows in each fold. Passing
the whole pipeline to cross-validation keeps imputation, scaling, encoding and
model fitting *within* each fold's training step. Otherwise, information from
the validation rows could leak into training and give an overly optimistic
estimate of performance on unseen data.

## 3. Compare using cross-validation

Cross-validation estimates how well a model predicts passengers it has not been
fitted to, without touching the test set. The notebook uses `cross_val_score`:
it splits the training rows into five folds, and for each fold fits a fresh copy
of the model on the other four and measures its **accuracy** (the fraction of
passengers predicted correctly) on the held-out fold.

Compare three models using the same folds:

1. A baseline that always predicts the most common outcome. This is the score
   to beat.
2. Your logistic-regression pipeline.
3. Your random-forest pipeline.

Use each classifier's default settings for this comparison. The only argument
to pass is `random_state=42`, which makes the forest's results repeatable.

Look at each model's mean accuracy and how much it varies between folds. Did
both models beat the baseline? Choose one and explain why. A small difference
is not proof that one method is always better.

<details>
<summary>💡 Hint: what if their scores are close?</summary>

You do not have to declare a clear winner. If the accuracies are similar, the
simpler model can be a reasonable choice. The standard deviation describes how
scores vary between folds; it is not a confidence interval or a formal test that
one model is better.

</details>

**Extension 🚀: does feature engineering help?** If you have time and want to
explore you could consider modifying or creating new features for prediction.

Approaches you could consider include:
- extracting titles from names
- combining `SibSp` and `Parch` into family size
- using cabin deck and ticket information
- better handling of missing-values

Try one change at a time and compare validation accuracy. Make sure you update
`make_preprocessor()` to include any new features, and keep any steps that learn
from data inside the pipeline.

**Extension 🚀: does tuning help?** Because `titanic_pipeline` passes extra
keyword arguments to the classifier, you can reuse it to try other settings. For
the random forest, `n_estimators` is the number of trees. Compare several
values using the same folds and `cross_val_score`. Does accuracy keep improving
as you add trees? Is the improvement substantial enough to change your choice,
or are the results broadly similar?

You could also try another setting, such as `max_depth`, which limits how deep
each tree can grow. Choose settings using validation accuracy only, never the
test set, and if you pick tuned settings, use them in the final evaluation
below.

## 4. Evaluate separately

We should now have arrived at what we think is our best model - now time
to evaluate it! What do you think our accuracy will be on the unseen test data?

Use the test set now and use it only once. Fit your chosen pipeline on all the
training rows, then call `score` on the test passengers: it predicts their
outcomes and returns the accuracy against their true outcomes. Compare it with
the baseline's test accuracy. Did the cross-validation result carry over?

Finish with a short conclusion: which features seemed useful, which model you
chose, and how its test accuracy compared with cross-validation. These
predictions cannot establish whether a particular modern person "would have
survived".
