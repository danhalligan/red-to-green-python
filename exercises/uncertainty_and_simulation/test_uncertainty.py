import math

import numpy as np
import pytest

from exercises.uncertainty_and_simulation.uncertainty import (
    bootstrap_standard_error,
    standard_error,
)


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
