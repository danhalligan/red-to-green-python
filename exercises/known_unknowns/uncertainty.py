"""Known unknowns: standard error, bootstrap and confidence interval exercises."""

from collections.abc import Callable

import numpy as np
from numpy.typing import ArrayLike


def standard_error(values: ArrayLike) -> float:
    """Estimate standard error using the sample standard deviation."""
    raise NotImplementedError


def bootstrap_standard_error(
    values: ArrayLike,
    *,
    statistic: Callable[..., np.ndarray] = np.mean,
    rng: np.random.Generator | None = None,
    resamples: int = 10000,
) -> float:
    """Estimate the standard error of a statistic with bootstrap resampling.

    ``statistic`` is called as ``statistic(resamples, axis=1)`` on an array with
    one resample per row, as ``np.mean`` and ``np.median`` are.
    """
    raise NotImplementedError


def normal_interval(
    estimate: float,
    se: float,
    *,
    level: float = 0.95,
    df: float | None = None,
) -> tuple[float, float]:
    """Return ``estimate`` plus and minus a critical value times ``se``.

    The critical value comes from the normal distribution, or from the t
    distribution with ``df`` degrees of freedom when ``df`` is given.
    """
    raise NotImplementedError


def bootstrap_interval(
    values: ArrayLike,
    *,
    statistic: Callable[..., np.ndarray] = np.mean,
    level: float = 0.95,
    rng: np.random.Generator | None = None,
    resamples: int = 10000,
) -> tuple[float, float]:
    """Return the percentile bootstrap confidence interval of a statistic.

    ``statistic`` is called as in ``bootstrap_standard_error``.
    """
    raise NotImplementedError
