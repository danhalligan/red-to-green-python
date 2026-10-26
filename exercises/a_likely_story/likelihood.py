"""A likely story: likelihood and maximum-likelihood exercises."""

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class MLEFit:
    """The result of a maximum-likelihood fit."""

    parameters: tuple[float, ...]
    log_likelihood: float


@dataclass(frozen=True)
class NormalFit:
    """Maximum-likelihood estimates for a normal distribution."""

    mean: float
    standard_deviation: float
    log_likelihood: float


def bernoulli_log_likelihood(probability: float, flips: ArrayLike) -> float:
    """Calculate the log-likelihood of 0/1 flips with head probability p."""
    raise NotImplementedError


def normal_log_likelihood(
    mean: float, standard_deviation: float, observations: ArrayLike
) -> float:
    """Calculate the normal log-likelihood without multiplying densities."""
    raise NotImplementedError


def fit_mle(log_likelihood: Callable[[np.ndarray], float], start: ArrayLike) -> MLEFit:
    """Find the parameter vector that maximises ``log_likelihood``.

    ``log_likelihood`` takes a 1-D array of parameters and returns a number.
    Raise ``RuntimeError`` mentioning "converge" if the optimiser fails.
    """
    raise NotImplementedError


def fit_normal_mle(observations: ArrayLike) -> NormalFit:
    """Fit normal mean and standard deviation by numerical maximisation."""
    raise NotImplementedError


def linear_regression_log_likelihood(
    intercept: float,
    slope: float,
    standard_deviation: float,
    x: ArrayLike,
    y: ArrayLike,
) -> float:
    """Log-likelihood of y given x when y = intercept + slope * x + normal noise."""
    raise NotImplementedError
