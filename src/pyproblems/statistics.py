"""Scientific-Python statistics exercises."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike


@dataclass(frozen=True)
class NormalFit:
    """Maximum-likelihood estimates for a normal distribution."""

    mean: float
    standard_deviation: float
    log_likelihood: float


def standard_error(values: ArrayLike) -> float:
    """Estimate standard error using the sample standard deviation."""
    raise NotImplementedError


def bootstrap_standard_error(
    values: ArrayLike,
    *,
    rng: np.random.Generator | None = None,
    resamples: int = 10000,
) -> float:
    """Estimate the standard error of the mean with bootstrap resampling."""
    raise NotImplementedError


def normal_log_likelihood(
    mean: float, standard_deviation: float, observations: ArrayLike
) -> float:
    """Calculate the normal log-likelihood without multiplying densities."""
    raise NotImplementedError


def fit_normal_mle(observations: ArrayLike) -> NormalFit:
    """Fit normal mean and standard deviation by numerical maximisation."""
    raise NotImplementedError


def gaussian_mixture_log_likelihood(
    mean1: float,
    standard_deviation1: float,
    mean2: float,
    standard_deviation2: float,
    weight1: float,
    observations: ArrayLike,
) -> float:
    """Calculate the log-likelihood for a two-normal mixture."""
    raise NotImplementedError
