"""No median feat: robust summaries, outlier flagging and Theil-Sen regression."""

from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike, NDArray


@dataclass(frozen=True)
class LineFit:
    """A straight line, ``y = intercept + slope * x``."""

    intercept: float
    slope: float


def trimmed_mean(values: ArrayLike, proportion: float = 0.1) -> float:
    """Average the values after discarding a proportion from each end.

    Sort the values, drop ``int(proportion * n)`` from the bottom and the same
    number from the top, and take the mean of what is left. ``proportion`` runs
    from 0 (the ordinary mean) towards 0.5 (the median).
    """
    raise NotImplementedError


def mad(values: ArrayLike, *, scale: bool = True) -> float:
    """Return the median absolute deviation from the median.

    With ``scale=True``, multiply by the constant that makes the result estimate
    the standard deviation when the data are normal.
    """
    raise NotImplementedError


def flag_outliers(values: ArrayLike, threshold: float = 3.5) -> NDArray[np.bool_]:
    """Return a boolean array that is True where a value is an outlier.

    A value is an outlier when it lies more than ``threshold`` scaled MADs from
    the median.
    """
    raise NotImplementedError


def theil_sen(x: ArrayLike, y: ArrayLike) -> LineFit:
    """Fit a line with the Theil-Sen estimator.

    The slope is the median of the slopes between every pair of points. The
    intercept is the median of ``y - slope * x``.
    """
    raise NotImplementedError
