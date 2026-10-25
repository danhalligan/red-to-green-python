"""Likelihood and maximum-likelihood exercises."""

from dataclasses import dataclass

from numpy.typing import ArrayLike


@dataclass(frozen=True)
class NormalFit:
    """Maximum-likelihood estimates for a normal distribution."""

    mean: float
    standard_deviation: float
    log_likelihood: float


def normal_log_likelihood(
    mean: float, standard_deviation: float, observations: ArrayLike
) -> float:
    """Calculate the normal log-likelihood without multiplying densities."""
    raise NotImplementedError


def fit_normal_mle(observations: ArrayLike) -> NormalFit:
    """Fit normal mean and standard deviation by numerical maximisation."""
    raise NotImplementedError
