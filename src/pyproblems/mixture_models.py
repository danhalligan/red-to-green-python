"""Expectation-maximization exercises for Gaussian mixture models."""

from collections.abc import Callable
from dataclasses import dataclass

from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class GaussianMixtureParameters:
    """Parameters for a two-component univariate Gaussian mixture."""

    mean1: float
    standard_deviation1: float
    mean2: float
    standard_deviation2: float
    weight1: float


@dataclass(frozen=True)
class MultivariateGaussianMixtureParameters:
    """Parameters for a two-component multivariate Gaussian mixture."""

    mean1: NDArray
    covariance1: NDArray
    mean2: NDArray
    covariance2: NDArray
    weight1: float


@dataclass(frozen=True)
class ExpectationMaximizationResult:
    """Parameters and likelihood from an EM run."""

    parameters: GaussianMixtureParameters
    log_likelihood: float
    iterations: int
    converged: bool


@dataclass(frozen=True)
class MultivariateExpectationMaximizationResult:
    """Multivariate parameters and likelihood from an EM run."""

    parameters: MultivariateGaussianMixtureParameters
    log_likelihood: float
    iterations: int
    converged: bool


def hard_expectation_step(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> NDArray:
    """Assign each observation to its more likely component."""
    raise NotImplementedError


def hard_maximization_step(
    observations: ArrayLike, labels: ArrayLike
) -> GaussianMixtureParameters:
    """Estimate mixture parameters from hard component labels."""
    raise NotImplementedError


def soft_expectation_step(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> NDArray:
    """Return each observation's posterior probability for component one."""
    raise NotImplementedError


def soft_maximization_step(
    observations: ArrayLike, weights: ArrayLike
) -> GaussianMixtureParameters:
    """Estimate mixture parameters using fractional component weights."""
    raise NotImplementedError


def mixture_log_likelihood(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> float:
    """Calculate a two-component Gaussian mixture log-likelihood."""
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
) -> ExpectationMaximizationResult:
    """Iterate supplied E- and M-steps until likelihood convergence."""
    raise NotImplementedError


def fit_hard_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: GaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> ExpectationMaximizationResult:
    """Fit a univariate mixture with hard expectation-maximization."""
    raise NotImplementedError


def fit_soft_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: GaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> ExpectationMaximizationResult:
    """Fit a univariate mixture with soft expectation-maximization."""
    raise NotImplementedError


def multivariate_gaussian_mixture_log_likelihood(
    observations: ArrayLike,
    parameters: MultivariateGaussianMixtureParameters,
) -> float:
    """Calculate the log-likelihood for a multivariate Gaussian mixture."""
    raise NotImplementedError


def multivariate_soft_expectation_step(
    observations: ArrayLike,
    parameters: MultivariateGaussianMixtureParameters,
) -> NDArray:
    """Return posterior component-one probabilities for multivariate data."""
    raise NotImplementedError


def multivariate_soft_maximization_step(
    observations: ArrayLike,
    weights: ArrayLike,
) -> MultivariateGaussianMixtureParameters:
    """Estimate multivariate parameters using fractional component weights."""
    raise NotImplementedError


def fit_multivariate_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: MultivariateGaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> MultivariateExpectationMaximizationResult:
    """Fit a multivariate Gaussian mixture using soft EM."""
    raise NotImplementedError


def fit_faithful_gaussian_mixture(
    initial_parameters: MultivariateGaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> MultivariateExpectationMaximizationResult:
    """Fit the multivariate mixture to packaged Old Faithful observations."""
    raise NotImplementedError
