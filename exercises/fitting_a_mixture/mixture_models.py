"""Expectation-maximisation exercises for Gaussian mixture models."""

from collections.abc import Callable, Iterator
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


ParametersT = TypeVar("ParametersT")
LatentT = TypeVar("LatentT")


@dataclass(frozen=True)
class EMResult(Generic[ParametersT]):
    """Parameters and likelihood from an EM run."""

    parameters: ParametersT
    log_likelihood: float
    iterations: int
    converged: bool


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


def em_steps(
    observations: ArrayLike,
    initial_parameters: ParametersT,
    expectation_step: Callable[[ArrayLike, ParametersT], LatentT],
    maximization_step: Callable[[ArrayLike, LatentT], ParametersT],
) -> Iterator[ParametersT]:
    """Yield the parameters after each EM iteration, starting with the initial ones.

    The first value yielded is `initial_parameters` itself. Each later value
    comes from one more iteration: call `expectation_step(observations,
    parameters)` on the latest parameters, then `maximization_step(observations,
    latent)` on its result, where `latent` is whatever the E-step returned.

    The generator is endless and lazy. It does no work until it is asked for the
    next value and never decides when to stop, so take what you need with `next`
    or `itertools.islice`. It cannot know what the parameters represent, so it
    works for any model with an E-step and an M-step.
    """
    raise NotImplementedError


def expectation_maximization(
    observations: ArrayLike,
    initial_parameters: ParametersT,
    expectation_step: Callable[[ArrayLike, ParametersT], LatentT],
    maximization_step: Callable[[ArrayLike, LatentT], ParametersT],
    log_likelihood: Callable[[ArrayLike, ParametersT], float],
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[ParametersT]:
    """Iterate supplied E- and M-steps until likelihood convergence.

    `expectation_step(observations, parameters)` returns labels or weights,
    `maximization_step(observations, those)` returns new parameters, and
    `log_likelihood(observations, parameters)` returns a float. Use `em_steps`
    for the iterations, and decide here when to stop.

    One iteration is one E-step followed by one M-step. Stop when the absolute
    change in log-likelihood between consecutive iterations is below
    `tolerance`, or when `max_iterations` is reached. Use the absolute change:
    hard EM optimises a different objective, so its log-likelihood can fall
    from one iteration to the next, and a large decrease is not convergence.
    Judge convergence only after an update, so `max_iterations=0` returns the
    initial parameters and log-likelihood, unconverged.

    Returns an `EMResult` with the fitted `parameters`,
    their `log_likelihood`, the number of `iterations` and whether it
    `converged`. Nothing here depends on what the parameters are.
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
