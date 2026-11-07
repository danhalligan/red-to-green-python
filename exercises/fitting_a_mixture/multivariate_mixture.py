"""Expectation-maximisation for a two-component bivariate Gaussian mixture.

These are the multivariate counterparts of the soft-EM functions in
`mixture_models.py`, so the names are shorter: import this module and call, for
example, `multivariate_mixture.fit(...)`.
"""

from dataclasses import dataclass

from numpy.typing import ArrayLike, NDArray

from exercises.fitting_a_mixture.mixture_models import EMResult


@dataclass(frozen=True)
class MixtureParameters:
    """Parameters for a two-component multivariate Gaussian mixture.

    Each mean is a vector (for Old Faithful, duration and waiting time) and
    each covariance is a square matrix. `weight1` is the probability of
    component one.
    """

    mean1: NDArray
    covariance1: NDArray
    mean2: NDArray
    covariance2: NDArray
    weight1: float


def log_likelihood(observations: ArrayLike, parameters: MixtureParameters) -> float:
    """Calculate the log-likelihood for a multivariate Gaussian mixture.

    The counterpart of `mixture_log_likelihood`. `observations` is an n by 2
    array. The log-density of each component is available from
    `scipy.stats.multivariate_normal(...).logpdf`. Combine them in log space,
    as for the univariate case.
    """
    raise NotImplementedError


def expectation_step(observations: ArrayLike, parameters: MixtureParameters) -> NDArray:
    """Return posterior component-one probabilities for multivariate data.

    The counterpart of `soft_expectation_step`, for an n by 2 array of
    observations. Work in log space so the result stays finite far from both
    components.
    """
    raise NotImplementedError


def maximization_step(observations: ArrayLike, weights: ArrayLike) -> MixtureParameters:
    """Estimate multivariate parameters using fractional component weights.

    The counterpart of `soft_maximization_step`. Use weighted means and weighted
    *population* covariance matrices; `numpy.cov` accepts `aweights`, and
    `ddof=0` gives the population version. `weight1` is the mean of `weights`.
    """
    raise NotImplementedError


def fit(
    observations: ArrayLike,
    initial_parameters: MixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[MixtureParameters]:
    """Fit a multivariate Gaussian mixture using soft EM.

    Reuse `expectation_maximization` with this module's E- and M-steps and
    `log_likelihood`: the loop itself should not need to change. The components
    keep the labels of `initial_parameters`.
    """
    raise NotImplementedError
