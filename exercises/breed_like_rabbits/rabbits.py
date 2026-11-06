"""NumPy exercises for a simple model of a breeding rabbit population."""

from numpy.typing import ArrayLike, NDArray


def breed(population: ArrayLike, growth_rate: ArrayLike) -> NDArray:
    """Return the population after one breeding season.

    `population` is the fraction of the field's carrying capacity that is
    occupied, between 0 (no rabbits) and 1 (the field is full). Rabbits breed
    in proportion to how many there are, `growth_rate * population`, but
    overcrowding cuts the rate by the fraction of the field already used,
    `1 - population`. Both arguments may be single numbers or arrays, which are
    combined elementwise (broadcast against each other). Do not modify the
    inputs.
    """
    raise NotImplementedError


def simulate_seasons(
    growth_rate: ArrayLike,
    *,
    start: float = 0.5,
    seasons: int = 100,
    discard: int = 0,
) -> NDArray:
    """Return the population at the start and after each of `seasons` seasons.

    The first row is `start` and each later row follows from the one before by
    `breed`, so there are `seasons + 1` rows. For a single growth rate the
    result has shape `(seasons + 1,)`. For an array of growth rates, simulate
    every rate at once from the same `start`, rather than one at a time, and
    return shape `(seasons + 1, *growth_rate.shape)`: one column per rate, so
    that thousands of rates stay fast.

    First run `discard` seasons without recording them, so that the rabbits can
    settle down. The first row is then the population after those `discard`
    seasons (still `start` when `discard` is 0), and `seasons` more follow.
    """
    raise NotImplementedError
