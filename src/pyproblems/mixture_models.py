"""Expectation-maximisation exercises for Gaussian mixture models."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class GaussianMixtureParameters:
    """Parameters for a two-component univariate Gaussian mixture.

    `weight1` is the probability that an observation comes from component one.
    """

    mean1: float
    standard_deviation1: float
    mean2: float
    standard_deviation2: float
    weight1: float


@dataclass(frozen=True)
class MultivariateGaussianMixtureParameters:
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


ParametersT = TypeVar(
    "ParametersT", GaussianMixtureParameters, MultivariateGaussianMixtureParameters
)


@dataclass(frozen=True)
class EMResult(Generic[ParametersT]):
    """Parameters and likelihood from an EM run."""

    parameters: ParametersT
    log_likelihood: float
    iterations: int
    converged: bool


def hard_expectation_step(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> NDArray:
    """Assign each observation to its more likely component (hard E-step).

    Compare the weighted densities `weight1 * phi(x | mean1, sd1)` and
    `(1 - weight1) * phi(x | mean2, sd2)`. Break ties in favour of component
    one.

    Returns a Boolean array, the same length as `observations`, that is True
    where component one is more likely.
    """
    raise NotImplementedError


def hard_maximization_step(
    observations: ArrayLike, labels: ArrayLike
) -> GaussianMixtureParameters:
    """Estimate mixture parameters from hard component labels (hard M-step).

    `labels` is a Boolean array, True for component one. For each group, use
    the mean and *population* standard deviation (`ddof=0`) of its
    observations. `weight1` is the fraction of observations labelled as
    component one.

    Raises ValueError, rather than returning invalid parameters, if a group is
    empty or has zero variance.
    """
    raise NotImplementedError


def soft_expectation_step(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> NDArray:
    """Return each observation's posterior probability for component one.

    For observation x_i this is
    `weight1 * phi(x_i | mean1, sd1) / (weight1 * phi(x_i | mean1, sd1) +
    (1 - weight1) * phi(x_i | mean2, sd2))`.

    Work in log space so that observations far from both components give
    finite results. Returns a float array the same length as `observations`.
    """
    raise NotImplementedError


def soft_maximization_step(
    observations: ArrayLike, weights: ArrayLike
) -> GaussianMixtureParameters:
    """Estimate mixture parameters using fractional component weights.

    `weights` holds the probability r_i that each observation belongs to
    component one; component two uses `1 - r_i`. Each component's mean and
    *population* standard deviation (`ddof=0`) are weighted by these values,
    and `weight1` is the mean of `weights`. `numpy.average(..., weights=...)`
    gives the weighted mean, but the weighted standard deviation is up to you.

    Raises ValueError if a component has no weight or zero variance.
    """
    raise NotImplementedError


def mixture_log_likelihood(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> float:
    """Calculate a two-component Gaussian mixture log-likelihood.

    This is the sum over observations of the log of the weighted sum of the two
    component densities. Compute it in log space (for example with
    `scipy.special.logsumexp`) so that a point far from both components still
    gives a finite value.
    """
    raise NotImplementedError


def expectation_maximization(
    observations: ArrayLike,
    initial_parameters: GaussianMixtureParameters,
    expectation_step: Callable,
    maximization_step: Callable,
    log_likelihood: Callable,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[GaussianMixtureParameters]:
    """Iterate supplied E- and M-steps until likelihood convergence.

    `expectation_step(observations, parameters)` returns labels or weights,
    `maximization_step(observations, those)` returns new parameters, and
    `log_likelihood(observations, parameters)` returns a float.

    One iteration is one E-step followed by one M-step. Stop when the absolute
    change in log-likelihood between consecutive iterations is below
    `tolerance`, or when `max_iterations` is reached. Use the absolute change:
    hard EM optimises a different objective, so its log-likelihood can fall
    from one iteration to the next, and a large decrease is not convergence.
    Judge convergence only after an update, so `max_iterations=0` returns the
    initial parameters and log-likelihood, unconverged.

    Returns an `EMResult` with the fitted `parameters`,
    their `log_likelihood`, the number of `iterations` and whether it
    `converged`. The component labels can be swapped without changing the
    model, so return the component with the lower mean first.
    """
    raise NotImplementedError


def fit_hard_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: GaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[GaussianMixtureParameters]:
    """Fit a univariate mixture with hard expectation-maximisation.

    Call `expectation_maximization` with the hard E- and M-steps and
    `mixture_log_likelihood`.
    """
    raise NotImplementedError


def fit_soft_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: GaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[GaussianMixtureParameters]:
    """Fit a univariate mixture with soft expectation-maximisation.

    Call `expectation_maximization` with the soft E- and M-steps and
    `mixture_log_likelihood`.
    """
    raise NotImplementedError


def multivariate_mixture_log_likelihood(
    observations: ArrayLike,
    parameters: MultivariateGaussianMixtureParameters,
) -> float:
    """Calculate the log-likelihood for a multivariate Gaussian mixture.

    `observations` is an n by 2 array. The log-density of each component is
    available from `scipy.stats.multivariate_normal(...).logpdf`. Combine them
    in log space, as for the univariate case.
    """
    raise NotImplementedError


def multivariate_soft_expectation_step(
    observations: ArrayLike,
    parameters: MultivariateGaussianMixtureParameters,
) -> NDArray:
    """Return posterior component-one probabilities for multivariate data.

    The multivariate counterpart of `soft_expectation_step`, for an n by 2
    array of observations. Work in log space so the result stays finite far
    from both components.
    """
    raise NotImplementedError


def multivariate_soft_maximization_step(
    observations: ArrayLike,
    weights: ArrayLike,
) -> MultivariateGaussianMixtureParameters:
    """Estimate multivariate parameters using fractional component weights.

    The multivariate counterpart of `soft_maximization_step`. Use weighted
    means and weighted *population* covariance matrices; `numpy.cov` accepts
    `aweights`, and `ddof=0` gives the population version. `weight1` is the
    mean of `weights`.

    Raises ValueError if a covariance matrix is singular.
    """
    raise NotImplementedError


def fit_multivariate_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: MultivariateGaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[MultivariateGaussianMixtureParameters]:
    """Fit a multivariate Gaussian mixture using soft EM.

    Iterate the multivariate soft E- and M-steps as in
    `expectation_maximization`, using `multivariate_mixture_log_likelihood`.
    Return the component with the smaller first mean coordinate first.
    """
    raise NotImplementedError


def fit_faithful_gaussian_mixture(
    initial_parameters: MultivariateGaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[MultivariateGaussianMixtureParameters]:
    """Fit the multivariate mixture to the packaged Old Faithful data.

    Use `load_faithful_data()` from `pyproblems.data` to get the (duration,
    waiting) observations, then call `fit_multivariate_gaussian_mixture`.
    """
    raise NotImplementedError
