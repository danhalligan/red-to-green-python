"""A helper for the investigation: knock some values far off course."""

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
