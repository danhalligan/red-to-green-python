import math

import numpy as np
import pytest
from scipy.stats import norm

from pyproblems.statistics import (
    fit_gaussian_mixture,
    gaussian_mixture_log_likelihood,
)

pytestmark = pytest.mark.advanced


def test_gaussian_mixture_log_likelihood_uses_log_sum_exp():
    observations = np.array([-1.0, 0.0, 1.0, 8.0])
    component_a = np.log(0.3) + norm.logpdf(observations, loc=0, scale=1)
    component_b = np.log(0.7) + norm.logpdf(observations, loc=8, scale=2)
    expected = np.sum(np.logaddexp(component_a, component_b))

    actual = gaussian_mixture_log_likelihood(
        mean1=0,
        standard_deviation1=1,
        mean2=8,
        standard_deviation2=2,
        weight1=0.3,
        observations=observations,
    )

    assert actual == pytest.approx(expected)


@pytest.mark.parametrize(
    "parameters",
    [
        {"standard_deviation1": 0},
        {"standard_deviation2": -1},
        {"weight1": 0},
        {"weight1": 1},
        {"mean1": math.nan},
    ],
)
def test_gaussian_mixture_log_likelihood_rejects_invalid_parameters(
    parameters,
):
    arguments = {
        "mean1": 0.0,
        "standard_deviation1": 1.0,
        "mean2": 5.0,
        "standard_deviation2": 1.0,
        "weight1": 0.5,
        "observations": [0.0, 5.0],
    }
    arguments.update(parameters)

    with pytest.raises(ValueError):
        gaussian_mixture_log_likelihood(**arguments)


def test_fit_gaussian_mixture_returns_stable_ordered_fit():
    generator = np.random.default_rng(314159)
    observations = np.concatenate(
        (generator.normal(-3.0, 0.7, 160), generator.normal(4.0, 1.1, 240))
    )

    fitted = fit_gaussian_mixture(observations)
    repeated = fit_gaussian_mixture(observations)

    assert set(fitted) == {
        "mean1",
        "standard_deviation1",
        "mean2",
        "standard_deviation2",
        "weight1",
        "log_likelihood",
    }
    assert fitted["mean1"] <= fitted["mean2"]
    assert fitted["standard_deviation1"] > 0
    assert fitted["standard_deviation2"] > 0
    assert 0 < fitted["weight1"] < 1
    assert fitted["log_likelihood"] > gaussian_mixture_log_likelihood(
        mean1=float(np.mean(observations)),
        standard_deviation1=float(np.std(observations)),
        mean2=float(np.mean(observations)),
        standard_deviation2=float(np.std(observations)),
        weight1=0.5,
        observations=observations,
    )
    assert fitted == repeated


def test_fit_gaussian_mixture_rejects_constant_data():
    with pytest.raises(ValueError, match="vary"):
        fit_gaussian_mixture([2.0, 2.0, 2.0, 2.0])
