import math

import numpy as np
import pandas as pd
import pytest
from scipy.stats import norm

from pyproblems.data import load_xy_data
from pyproblems.statistics import (
    NormalFit,
    bootstrap_standard_error,
    fit_normal_mle,
    normal_log_likelihood,
    ols_coefficients,
    standard_error,
    summarize_xy,
    summarize_xy_datasets,
)


def test_standard_error_uses_sample_standard_deviation():
    assert standard_error([1, 2, 3]) == pytest.approx(1 / math.sqrt(3))


@pytest.mark.parametrize("values", [[], [1]])
def test_standard_error_requires_two_observations(values):
    with pytest.raises(ValueError, match="at least 2"):
        standard_error(values)


def test_ols_coefficients_matches_known_linear_relationship():
    predictors = np.array([0.0, 1.0, 2.0, 3.0])
    design = np.column_stack((np.ones(predictors.size), predictors))
    outcomes = 1.0 + 2.0 * predictors

    assert ols_coefficients(design, outcomes) == pytest.approx([1.0, 2.0])
    assert ols_coefficients(design, outcomes[:, None]) == pytest.approx([1.0, 2.0])
    assert ols_coefficients(design, outcomes) == pytest.approx(
        np.linalg.lstsq(design, outcomes, rcond=None)[0]
    )


@pytest.mark.parametrize(
    ("design", "outcomes"),
    [
        (np.ones(4), np.ones(4)),
        (np.ones((4, 2)), np.ones(4)),
        (np.ones((4, 1)), np.ones(3)),
        (np.ones((4, 1)), np.ones((4, 2))),
    ],
)
def test_ols_coefficients_rejects_invalid_shapes_and_rank(design, outcomes):
    with pytest.raises(ValueError):
        ols_coefficients(design, outcomes)


def test_summarize_xy_returns_named_statistics():
    summary = summarize_xy({"x": [1, 2, 3], "y": [1, 4, 5]})

    assert summary == pytest.approx(
        {
            "x_mean": 2.0,
            "y_mean": 10 / 3,
            "x_sd": 1.0,
            "y_sd": 2.0816659994661326,
            "corr": 0.9607689228305228,
        }
    )


def test_summarize_xy_datasets_preserves_names_and_common_summaries():
    summaries = summarize_xy_datasets(load_xy_data())

    assert isinstance(summaries, pd.DataFrame)
    assert list(summaries.index) == [f"Dataset{i}" for i in range(1, 14)]
    assert list(summaries.columns) == ["x_mean", "y_mean", "x_sd", "y_sd", "corr"]
    assert summaries["x_mean"].to_numpy() == pytest.approx([54.26] * 13, abs=0.01)
    assert summaries["y_mean"].to_numpy() == pytest.approx([47.83] * 13, abs=0.01)
    assert summaries["x_sd"].to_numpy() == pytest.approx([16.76] * 13, abs=0.01)
    assert summaries["y_sd"].to_numpy() == pytest.approx([26.93] * 13, abs=0.01)
    assert summaries["corr"].to_numpy() == pytest.approx([-0.065] * 13, abs=0.01)


def test_bootstrap_standard_error_is_reproducible_and_near_analytic_estimate():
    observations = np.arange(1.0, 31.0)
    first = bootstrap_standard_error(observations, rng=np.random.default_rng(42))
    second = bootstrap_standard_error(observations, rng=np.random.default_rng(42))

    assert first == second
    assert first == pytest.approx(standard_error(observations), rel=0.12)


def test_bootstrap_standard_error_checks_rng_and_resample_count():
    with pytest.raises(TypeError, match="Generator"):
        bootstrap_standard_error([1, 2, 3], rng=42)
    with pytest.raises(ValueError, match="at least two"):
        bootstrap_standard_error([1, 2, 3], resamples=1)


def test_normal_log_likelihood_sums_log_densities():
    observations = np.array([0.0, 1.0, -1.0])

    assert normal_log_likelihood(0.0, 1.0, observations) == pytest.approx(
        float(np.sum(norm.logpdf(observations)))
    )


def test_normal_log_likelihood_remains_finite_when_likelihood_underflows():
    observations = np.linspace(-20.0, 20.0, 1000)

    assert np.prod(norm.pdf(observations)) == 0.0
    assert math.isfinite(normal_log_likelihood(0.0, 1.0, observations))


@pytest.mark.parametrize("scale", [0.0, -1.0, math.inf])
def test_normal_log_likelihood_requires_positive_finite_scale(scale):
    with pytest.raises(ValueError, match="positive"):
        normal_log_likelihood(0.0, scale, [0.0, 1.0])


def test_fit_normal_mle_returns_numerical_maximum_likelihood_estimate():
    observations = [1.0, 2.0, 2.0, 4.0]
    fit = fit_normal_mle(observations)

    assert isinstance(fit, NormalFit)
    assert fit.mean == pytest.approx(np.mean(observations), abs=1e-6)
    assert fit.standard_deviation == pytest.approx(
        np.std(observations, ddof=0), abs=1e-6
    )
    assert fit.log_likelihood == pytest.approx(
        normal_log_likelihood(fit.mean, fit.standard_deviation, observations)
    )


def test_fit_normal_mle_rejects_constant_data():
    with pytest.raises(ValueError, match="identical"):
        fit_normal_mle([3.0, 3.0, 3.0])


def test_fit_normal_mle_matches_analytic_estimates_on_repeated_small_samples():
    generator = np.random.default_rng(2025)

    for _ in range(100):
        observations = generator.normal(10.0, 3.0, size=5)
        fit = fit_normal_mle(observations)
        expected_sd = np.std(observations, ddof=0)

        assert fit.mean == pytest.approx(np.mean(observations), abs=1e-4 * expected_sd)
        assert fit.standard_deviation == pytest.approx(expected_sd, rel=1e-4)


@pytest.mark.parametrize(("location", "scale"), [(1000.0, 0.01), (-50.0, 1e4)])
def test_fit_normal_mle_handles_shifted_and_rescaled_data(location, scale):
    generator = np.random.default_rng(7)
    observations = location + scale * generator.standard_normal(20)
    expected_sd = np.std(observations, ddof=0)
    fit = fit_normal_mle(observations)

    assert fit.mean == pytest.approx(np.mean(observations), abs=1e-3 * expected_sd)
    assert fit.standard_deviation == pytest.approx(expected_sd, rel=1e-3)
