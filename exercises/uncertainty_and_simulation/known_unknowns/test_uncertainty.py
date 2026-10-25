import math

import numpy as np
import pytest

from exercises.uncertainty_and_simulation.known_unknowns.uncertainty import (
    bootstrap_interval,
    bootstrap_standard_error,
    normal_interval,
    standard_error,
)


@pytest.fixture
def needs_scipy():
    return pytest.importorskip("scipy.stats")


def test_standard_error_uses_sample_standard_deviation():
    assert standard_error([1, 2, 3]) == pytest.approx(1 / math.sqrt(3))


@pytest.mark.parametrize("values", [[], [1]])
def test_standard_error_requires_two_observations(values):
    with pytest.raises(ValueError, match="at least 2"):
        standard_error(values)


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


def test_bootstrap_standard_error_uses_the_supplied_statistic():
    observations = np.arange(1.0, 31.0)
    mean_se = bootstrap_standard_error(observations, rng=np.random.default_rng(7))
    doubled_se = bootstrap_standard_error(
        observations,
        statistic=lambda resamples, axis: 2 * np.mean(resamples, axis=axis),
        rng=np.random.default_rng(7),
    )

    assert doubled_se == pytest.approx(2 * mean_se)


def test_bootstrap_standard_error_of_median_ignores_a_single_outlier():
    observations = [*range(1, 30), 1000]
    mean_se = bootstrap_standard_error(observations, rng=np.random.default_rng(3))
    median_se = bootstrap_standard_error(
        observations, statistic=np.median, rng=np.random.default_rng(3)
    )

    assert median_se < mean_se / 5


def test_normal_interval_uses_the_normal_critical_value(needs_scipy):
    low, high = normal_interval(10, 2)

    assert low == pytest.approx(10 - 1.959964 * 2, rel=1e-5)
    assert high == pytest.approx(10 + 1.959964 * 2, rel=1e-5)


def test_normal_interval_uses_the_t_critical_value_given_degrees_of_freedom(
    needs_scipy,
):
    low, high = normal_interval(10, 2, df=4)

    assert low == pytest.approx(10 - 2.776445 * 2, rel=1e-5)
    assert high == pytest.approx(10 + 2.776445 * 2, rel=1e-5)


def test_normal_interval_respects_the_confidence_level(needs_scipy):
    low, high = normal_interval(0, 1, level=0.9)

    assert (low, high) == pytest.approx((-1.644854, 1.644854), rel=1e-5)


@pytest.mark.parametrize("level", [0, 1, -0.5, 1.5])
def test_normal_interval_requires_a_level_between_zero_and_one(level):
    with pytest.raises(ValueError, match="level"):
        normal_interval(10, 2, level=level)


def test_normal_interval_rejects_a_negative_se():
    with pytest.raises(ValueError, match="se"):
        normal_interval(10, -2)


def test_bootstrap_interval_is_reproducible_and_brackets_the_estimate():
    observations = np.arange(1.0, 101.0)
    first = bootstrap_interval(observations, rng=np.random.default_rng(5))
    second = bootstrap_interval(observations, rng=np.random.default_rng(5))

    assert first == second
    assert first[0] < observations.mean() < first[1]


def test_bootstrap_interval_matches_the_resample_mean_percentiles():
    observations = np.arange(1.0, 101.0)
    low, high = bootstrap_interval(observations, rng=np.random.default_rng(5))

    # The bootstrap standard error of the mean is about 28.9 / 10.
    assert low == pytest.approx(50.5 - 1.96 * 2.887, abs=0.5)
    assert high == pytest.approx(50.5 + 1.96 * 2.887, abs=0.5)


def test_bootstrap_interval_widens_with_the_confidence_level():
    observations = np.arange(1.0, 101.0)
    narrow = bootstrap_interval(observations, level=0.5, rng=np.random.default_rng(5))
    wide = bootstrap_interval(observations, level=0.99, rng=np.random.default_rng(5))

    assert wide[0] < narrow[0] < narrow[1] < wide[1]


def test_bootstrap_interval_uses_the_supplied_statistic():
    observations = [*range(1, 30), 1000]
    low, high = bootstrap_interval(
        observations, statistic=np.median, rng=np.random.default_rng(3)
    )

    assert 1 <= low <= high < 29


def test_bootstrap_interval_checks_its_arguments():
    with pytest.raises(TypeError, match="Generator"):
        bootstrap_interval([1, 2, 3], rng=42)
    with pytest.raises(ValueError, match="at least two"):
        bootstrap_interval([1, 2, 3], resamples=1)
    with pytest.raises(ValueError, match="level"):
        bootstrap_interval([1, 2, 3], level=1.5)
