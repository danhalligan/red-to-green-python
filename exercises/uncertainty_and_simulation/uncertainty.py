"""Standard error and bootstrap exercises."""

import numpy as np
from numpy.typing import ArrayLike


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
