import math

import numpy as np
import pytest
from scipy.special import expit
from scipy.stats import norm

from exercises.a_likely_story.likelihood import (
    MLEFit,
    NormalFit,
    bernoulli_log_likelihood,
    fit_mle,
    fit_normal_mle,
    linear_regression_log_likelihood,
    normal_log_likelihood,
)


def test_bernoulli_log_likelihood_sums_log_probabilities():
    flips = [1, 0, 1, 1]

    assert bernoulli_log_likelihood(0.75, flips) == pytest.approx(
        3 * math.log(0.75) + math.log(0.25)
    )


def test_bernoulli_log_likelihood_accepts_booleans():
    assert bernoulli_log_likelihood(0.2, [True, False]) == pytest.approx(
        math.log(0.2) + math.log(0.8)
    )


def test_bernoulli_log_likelihood_remains_finite_when_likelihood_underflows():
    flips = np.tile([1, 0], 5000)

    assert 0.5**10000 == 0.0
    assert bernoulli_log_likelihood(0.5, flips) == pytest.approx(10000 * math.log(0.5))


def test_bernoulli_log_likelihood_handles_certain_probabilities():
    assert bernoulli_log_likelihood(1.0, [1, 1, 1]) == 0.0
    assert bernoulli_log_likelihood(0.0, [0, 0]) == 0.0
    assert bernoulli_log_likelihood(0.0, [0, 1]) == -math.inf


@pytest.mark.parametrize("probability", [-0.1, 1.1, math.nan])
def test_bernoulli_log_likelihood_requires_a_probability(probability):
    with pytest.raises(ValueError, match="probability"):
        bernoulli_log_likelihood(probability, [0, 1])


def test_bernoulli_log_likelihood_requires_zeros_and_ones():
    with pytest.raises(ValueError, match="0 or 1"):
        bernoulli_log_likelihood(0.5, [0, 1, 2])


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


def test_fit_mle_finds_the_maximum_of_a_known_function():
    fit = fit_mle(lambda t: -((t[0] - 3) ** 2) - 2 * (t[1] + 2) ** 2, [0.0, 0.0])

    assert isinstance(fit, MLEFit)
    assert fit.parameters == pytest.approx((3.0, -2.0), abs=1e-4)
    assert all(isinstance(value, float) for value in fit.parameters)
    assert fit.log_likelihood == pytest.approx(0.0, abs=1e-8)


def test_fit_mle_recovers_the_proportion_of_heads():
    flips = [1, 1, 0, 1, 1, 0, 1, 1, 0, 1]
    fit = fit_mle(lambda t: bernoulli_log_likelihood(expit(t[0]), flips), [0.0])

    assert expit(fit.parameters[0]) == pytest.approx(0.7, abs=1e-4)
    assert fit.log_likelihood == pytest.approx(bernoulli_log_likelihood(0.7, flips))


@pytest.mark.filterwarnings("ignore")
def test_fit_mle_reports_an_optimiser_failure():
    with pytest.raises(RuntimeError, match="converge"), np.errstate(all="ignore"):
        fit_mle(lambda t: t[0], [0.0])


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


def test_linear_regression_log_likelihood_scores_the_residuals():
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([1.0, 2.5, 5.0])
    residuals = y - (1.0 + 2.0 * x)

    assert linear_regression_log_likelihood(1.0, 2.0, 0.5, x, y) == pytest.approx(
        float(np.sum(norm.logpdf(residuals, scale=0.5)))
    )


def test_linear_regression_log_likelihood_checks_its_inputs():
    with pytest.raises(ValueError, match="positive"):
        linear_regression_log_likelihood(0.0, 1.0, 0.0, [0.0, 1.0], [0.0, 1.0])
    with pytest.raises(ValueError, match="same length"):
        linear_regression_log_likelihood(0.0, 1.0, 1.0, [0.0, 1.0], [0.0])


def test_maximum_likelihood_regression_matches_least_squares():
    generator = np.random.default_rng(2025)
    x = np.linspace(0.0, 10.0, 30)
    y = 2.0 + 0.5 * x + generator.normal(0.0, 1.0, size=x.size)

    fit = fit_mle(
        lambda t: linear_regression_log_likelihood(t[0], t[1], math.exp(t[2]), x, y),
        [0.0, 0.0, 0.0],
    )
    slope, intercept = np.polyfit(x, y, 1)
    residuals = y - (intercept + slope * x)

    assert fit.parameters[0] == pytest.approx(intercept, rel=1e-4)
    assert fit.parameters[1] == pytest.approx(slope, rel=1e-4)
    assert math.exp(fit.parameters[2]) == pytest.approx(
        np.std(residuals, ddof=0), rel=1e-4
    )
