"""Learner contracts for leakage-safe Titanic pipelines, not accuracy targets."""

import numpy as np
import pandas as pd
import pytest
from sklearn.base import clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import NotFittedError
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.utils.validation import check_is_fitted

from pyproblems.titanic import (
    load_passengers,
    make_preprocessor,
    titanic_pipeline,
)


def test_load_passengers_returns_a_dataframe_with_numeric_columns():
    passengers = load_passengers()

    assert isinstance(passengers, pd.DataFrame)
    assert passengers.shape == (1309, 12)
    assert list(passengers.columns) == [
        "PassengerId",
        "Survived",
        "Pclass",
        "Name",
        "Sex",
        "Age",
        "SibSp",
        "Parch",
        "Ticket",
        "Fare",
        "Cabin",
        "Embarked",
    ]
    for column in ["PassengerId", "Survived", "Pclass", "SibSp", "Parch"]:
        assert passengers[column].dtype.kind == "i"
    for column in ["Age", "Fare"]:
        assert passengers[column].dtype.kind == "f"
    assert passengers["Survived"].sum() == 500
    assert passengers["Age"].iloc[0] == 29.0
    assert passengers["Ticket"].iloc[0] == "24160"


def test_load_passengers_marks_blanks_as_nan_in_every_column():
    passengers = load_passengers()

    assert passengers["Age"].isna().sum() == 263
    assert passengers["Fare"].isna().sum() == 1
    assert passengers["Embarked"].isna().sum() == 2
    assert passengers["Cabin"].isna().sum() == 1014
    # Missing text must be NaN, not None, so scikit-learn imputers see it.
    missing_text = passengers.loc[passengers["Embarked"].isna(), "Embarked"]
    assert all(isinstance(value, float) and np.isnan(value) for value in missing_text)


def test_load_passengers_feeds_the_preprocessor_without_extra_cleaning():
    passengers = load_passengers()
    features = passengers.drop(columns="Survived")

    prepared = make_preprocessor().fit_transform(features)

    assert prepared.shape == (1309, 12)
    assert np.isfinite(prepared).all()


@pytest.fixture
def passengers():
    return pd.DataFrame(
        {
            "Age": [10.0, 20.0, np.nan, 40.0, 50.0, 60.0],
            "Fare": [8.0, 12.0, 20.0, np.nan, 40.0, 60.0],
            "SibSp": [0, 1, 0, 1, 2, 0],
            "Parch": [0, 1, 0, 0, 1, 0],
            "Pclass": [3, 2, 1, 3, 2, 1],
            "Sex": ["male", "female", "male", "female", "male", "female"],
            "Embarked": ["S", "S", "C", np.nan, "C", "Q"],
            "PassengerId": range(1, 7),
            "Survived": [0, 1, 0, 1, 0, 1],
            "Name": list("abcdef"),
            "Ticket": list("uvwxyz"),
            "Cabin": [None] * 6,
        }
    )


def test_make_preprocessor_is_unfitted_and_numeric_columns_are_median_scaled(
    passengers,
):
    preprocessor = make_preprocessor()

    assert isinstance(preprocessor, ColumnTransformer)
    with pytest.raises(NotFittedError):
        check_is_fitted(preprocessor)
    transformed = preprocessor.fit_transform(passengers)
    assert transformed.shape == (6, 12)
    # Locate the four scaled numeric columns regardless of transformer order.
    for column in ["Age", "Fare", "SibSp", "Parch"]:
        imputed = passengers[column].fillna(passengers[column].median()).to_numpy()
        expected = (imputed - imputed.mean()) / imputed.std()
        assert any(
            np.allclose(transformed[:, i], expected)
            for i in range(transformed.shape[1])
        ), f"{column} was not median-imputed and standardised"


def test_make_preprocessor_ignores_other_columns_and_unseen_categories(passengers):
    preprocessor = make_preprocessor().fit(passengers)
    probe = passengers.iloc[:2].copy()
    before = preprocessor.transform(probe)

    changed = probe.copy()
    changed["Survived"] = 1 - changed["Survived"]
    changed["PassengerId"] = [999, 1000]
    changed["Name"] = "unseen name"
    changed["Ticket"] = "unseen ticket"
    changed["Cabin"] = "new cabin"
    np.testing.assert_allclose(preprocessor.transform(changed), before)

    unseen = probe.copy()
    unseen["Pclass"] = 4
    unseen["Embarked"] = ["unknown", np.nan]
    assert np.isfinite(preprocessor.transform(unseen)).all()


@pytest.mark.parametrize(
    ("model", "classifier", "setting", "value"),
    [
        ("logistic", LogisticRegression, "max_iter", 250),
        ("forest", RandomForestClassifier, "n_estimators", 25),
    ],
)
def test_pipeline_is_unfitted_and_passes_extra_arguments_to_the_classifier(
    model, classifier, setting, value
):
    pipeline = titanic_pipeline(model, random_state=17, **{setting: value})

    assert isinstance(pipeline, Pipeline)
    assert list(pipeline.named_steps) == ["preprocess", "classifier"]
    assert isinstance(pipeline.named_steps["preprocess"], ColumnTransformer)
    estimator = pipeline.named_steps["classifier"]
    assert isinstance(estimator, classifier)
    assert estimator.random_state == 17
    assert getattr(estimator, setting) == value
    with pytest.raises(NotFittedError):
        check_is_fitted(estimator)
    with pytest.raises(NotFittedError):
        check_is_fitted(pipeline.named_steps["preprocess"])
    clone(pipeline)


@pytest.mark.parametrize("model", ["logistic", "forest"])
def test_unknown_classifier_arguments_are_not_silently_ignored(model):
    with pytest.raises(TypeError):
        titanic_pipeline(model, not_a_classifier_setting=1)


@pytest.mark.parametrize("model", ["logistic", "forest"])
def test_pipeline_handles_missing_values_unknown_categories_and_probabilities(
    passengers, model
):
    labels = passengers["Survived"]
    pipeline = titanic_pipeline(model)
    pipeline.fit(passengers, labels)
    unseen = passengers.iloc[:2].copy()
    unseen.loc[:, "Age"] = np.nan
    unseen.loc[:, "Fare"] = np.nan
    unseen.loc[:, "Pclass"] = 4
    unseen.loc[:, "Embarked"] = ["unknown", np.nan]

    predictions = pipeline.predict(unseen)
    probabilities = pipeline.predict_proba(unseen)

    assert predictions.shape == (2,)
    assert set(predictions).issubset({0, 1})
    assert probabilities.shape == (2, 2)
    assert np.isfinite(probabilities).all()
    assert ((0 <= probabilities) & (probabilities <= 1)).all()
    np.testing.assert_allclose(probabilities.sum(axis=1), 1)


def test_pipeline_fits_on_training_rows_only_and_ignores_leaky_columns(passengers):
    pipeline = titanic_pipeline()
    pipeline.fit(passengers, passengers["Survived"])
    preprocess = pipeline.named_steps["preprocess"]
    probe = passengers.iloc[:2].copy()
    before = preprocess.transform(probe)
    predictions = pipeline.predict_proba(probe)
    changed = probe.copy()
    changed["Survived"] = 1 - changed["Survived"]
    changed["PassengerId"] = [999, 1000]
    changed["Name"] = "unseen name"
    changed["Ticket"] = "unseen ticket"
    changed["Cabin"] = "new cabin"
    np.testing.assert_allclose(pipeline.predict_proba(changed), predictions)
    # Predicting on new values must not refit the preprocessing.
    extreme = probe.copy()
    extreme["Age"] = 1e9
    pipeline.predict_proba(extreme)
    np.testing.assert_allclose(preprocess.transform(probe), before)


def test_invalid_model_is_rejected():
    with pytest.raises(ValueError, match="model"):
        titanic_pipeline("unsupported")
