"""Scientific-Python statistics exercises."""

from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np
import pandas as pd
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class NormalFit:
    """Maximum-likelihood estimates for a normal distribution."""

    mean: float
    standard_deviation: float
    log_likelihood: float


@dataclass(frozen=True)
class GaussianMixtureFit:
    """Ordered maximum-likelihood estimates for a two-normal mixture."""

    mean1: float
    standard_deviation1: float
    mean2: float
    standard_deviation2: float
    weight1: float
    log_likelihood: float


def standard_error(values: ArrayLike) -> float:
    """Estimate standard error using the sample standard deviation."""
    raise NotImplementedError


def ols_coefficients(
    design_matrix: ArrayLike, outcomes: ArrayLike
) -> NDArray[np.float64]:
    """Estimate OLS coefficients by solving the normal equations."""
    raise NotImplementedError


def summarize_xy(dataset: Mapping[str, Sequence[float]]) -> dict[str, float]:
    """Calculate means, sample standard deviations, and correlation for x/y."""
    raise NotImplementedError


def summarize_xy_datasets(
    datasets: Mapping[str, Mapping[str, Sequence[float]]],
) -> pd.DataFrame:
    """Return one row of summary statistics for each named x/y dataset."""
    raise NotImplementedError


def bootstrap_standard_error(
    values: ArrayLike,
    *,
    rng: np.random.Generator | None = None,
    resamples: int = 1000,
) -> float:
    """Estimate the standard error of the mean with bootstrap resampling."""
    raise NotImplementedError


def normal_log_likelihood(
    mean: float, standard_deviation: float, observations: ArrayLike
) -> float:
    """Calculate the normal log-likelihood without multiplying densities."""
    raise NotImplementedError


def normal_likelihood(
    mean: float, standard_deviation: float, observations: ArrayLike
) -> float:
    """Calculate the joint density for independent normal observations."""
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


def fit_gaussian_mixture(observations: ArrayLike) -> GaussianMixtureFit:
    """Fit a two-normal mixture from deterministic starts and order by mean."""
    raise NotImplementedError
