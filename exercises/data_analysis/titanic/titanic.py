"""Titanic survival prediction: prepared data and classifier pipelines."""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from exercises.data_analysis.titanic.loaders import load_titanic_data

NUMERIC_COLUMNS = ["PassengerId", "Survived", "Pclass", "Age", "SibSp", "Parch", "Fare"]
TEXT_COLUMNS = ["Name", "Sex", "Ticket", "Cabin", "Embarked"]


def load_passengers() -> pd.DataFrame:
    """Return the packaged Titanic passengers as a DataFrame, ready to explore.

    The loader supplies every value as a string. Here the numeric columns
    (PassengerId, Survived, Pclass, Age, SibSp, Parch and Fare) are converted to
    numbers, and blank cells in every column become numpy.nan, which
    scikit-learn's imputers treat as missing.

    This only fixes types and marks missing values. It learns nothing from the
    data, so it is safe to apply before splitting. Imputation, scaling and
    encoding are learned from data, so they happen inside the pipeline instead
    (see make_preprocessor and titanic_pipeline).
    """
    passengers = pd.DataFrame(load_titanic_data())
    for column in NUMERIC_COLUMNS:
        passengers[column] = pd.to_numeric(passengers[column], errors="raise")
    text = passengers[TEXT_COLUMNS]
    passengers[TEXT_COLUMNS] = text.where(text.notna(), np.nan)
    return passengers


def make_preprocessor() -> ColumnTransformer:
    """Return an unfitted ColumnTransformer that prepares passengers for a model.

    Numeric Age, Fare, SibSp and Parch have missing values replaced by the
    training median and are then standardised. Categorical Pclass, Sex and
    Embarked have missing values replaced by the most common training value and
    are then one-hot encoded; categories not seen in training are ignored.
    All other columns are dropped.

    Nothing is fitted here: the transformer learns its medians, scales and
    categories from whichever rows it is later fitted on.
    """
    numeric = Pipeline(
        [
            ("impute", SimpleImputer(strategy="median")),
            ("scale", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        [
            ("impute", SimpleImputer(strategy="most_frequent")),
            ("encode", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        [
            ("numeric", numeric, ["Age", "Fare", "SibSp", "Parch"]),
            ("categorical", categorical, ["Pclass", "Sex", "Embarked"]),
        ],
        remainder="drop",
        sparse_threshold=0,
    )


def titanic_pipeline(model: str = "logistic", **kwargs: Any) -> Pipeline:
    """Return an unfitted Pipeline: make_preprocessor() followed by a classifier.

    The Pipeline has two steps, named "preprocess" and "classifier".
    `model` chooses the classifier: "logistic" for a logistic regression or
    "forest" for a random forest. Raise ValueError for any other model.

    Pass any extra keyword arguments on to the classifier, for example
    random_state=42 to make results reproducible.

    Do not fit anything here: the whole Pipeline is fitted later, so its
    preprocessing is learned separately from the training rows in each
    cross-validation fold.
    """
    # TODO: add the scikit-learn imports you need at the top of the file, then
    # build and return the Pipeline.
    raise NotImplementedError
