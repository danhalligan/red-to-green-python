"""Helpers for the investigation: knock values off course and simulate lines."""

from collections.abc import Iterator

import numpy as np
from numpy.typing import ArrayLike, NDArray


def glitch(
    values: ArrayLike,
    fraction: float = 0.1,
    *,
    size: float = 100.0,
    where: str = "random",
    direction: str = "up",
    rng: np.random.Generator | None = None,
) -> NDArray[np.float64]:
    """Return a copy of ``values`` in which some of them are wildly wrong.

    ``fraction`` of the values (rounded to a whole number) have ``size`` added or
    subtracted, so the glitched values keep their original noise. The original
    array is not changed, and the glitched positions are those where the result
    differs from it.

    ``where`` chooses the positions: ``"start"``, ``"end"`` or ``"random"``.
    ``direction`` is ``"up"``, ``"down"`` or ``"both"`` (a random sign for each
    glitch). Pass a seeded ``rng`` to make the random choices reproducible.
    """
    if where not in {"start", "end", "random"}:
        raise ValueError(f"where must be 'start', 'end' or 'random', not {where!r}")
    if direction not in {"up", "down", "both"}:
        raise ValueError(f"direction must be 'up', 'down' or 'both', not {direction!r}")

    rng = np.random.default_rng() if rng is None else rng
    glitched = np.array(values, dtype=float)
    n = len(glitched)
    count = round(fraction * n)

    if where == "start":
        index = np.arange(count)
    elif where == "end":
        index = np.arange(n - count, n)
    else:
        index = rng.choice(n, count, replace=False)

    if direction == "both":
        sign = rng.choice([-1.0, 1.0], size=count)
    else:
        sign = 1.0 if direction == "up" else -1.0
    glitched[index] += sign * size
    return glitched


def simulate(
    repetitions: int = 1000,
    *,
    n: int = 30,
    noise: str = "normal",
    glitches: float = 0.0,
    intercept: float = 1.0,
    slope: float = 2.0,
    sd: float = 3.0,
    size: float = 100.0,
    where: str = "random",
    direction: str = "up",
    rng: np.random.Generator | None = None,
) -> Iterator[tuple[NDArray[np.float64], NDArray[np.float64]]]:
    """Yield ``repetitions`` noisy straight-line datasets as ``(x, y)`` pairs.

    Each dataset has ``n`` points with ``x`` running from 0 to ``n - 1`` and
    ``y = intercept + slope * x`` plus noise with mean 0 and standard deviation
    ``sd``. ``noise`` is ``"normal"`` or ``"exponential"``, a skewed distribution
    whose mean is still 0 so that its median is below its mean.

    ``glitches`` is the fraction of the ``y`` values to knock off course; the
    default of 0 gives clean data. ``size``, ``where`` and ``direction`` are
    passed to :func:`glitch`. Pass a seeded ``rng`` to make the datasets
    reproducible.

    Use it for one dataset with ``x, y = next(simulate(rng=rng))`` or for many
    with ``for x, y in simulate(2000, rng=rng): ...``.
    """
    if noise not in {"normal", "exponential"}:
        raise ValueError(f"noise must be 'normal' or 'exponential', not {noise!r}")

    rng = np.random.default_rng() if rng is None else rng
    for _ in range(repetitions):
        x = np.arange(n, dtype=float)
        if noise == "normal":
            errors = rng.normal(0, sd, size=n)
        else:
            errors = rng.exponential(sd, size=n) - sd
        y = intercept + slope * x + errors
        if glitches > 0:
            y = glitch(
                y, glitches, size=size, where=where, direction=direction, rng=rng
            )
        yield x, y
