"""NumPy exercises for a simple model of a breeding rabbit population."""

from numpy.typing import ArrayLike, NDArray


def next_population(population: ArrayLike, growth_rate: float) -> NDArray:
    """Return the population after one breeding season.

    `population` is the fraction of the field's carrying capacity that is
    occupied, between 0 (no rabbits) and 1 (the field is full). It may be a
    single number or an array; return an array of the same shape. Rabbits breed
    in proportion to how many there are, `growth_rate * population`, but
    overcrowding cuts the rate by the fraction of the field already used,
    `1 - population`. Do not modify the input.
    """
    raise NotImplementedError


def simulate_population(
    growth_rate: float, *, start: float = 0.5, seasons: int = 100
) -> NDArray:
    """Return the population at the start and after each of `seasons` seasons.

    The result has `seasons + 1` values, beginning with `start`, and each
    value follows from the previous one by `next_population`.
    """
    raise NotImplementedError


def long_run_population(
    growth_rates: ArrayLike,
    *,
    start: float = 0.5,
    burn_in: int = 500,
    keep: int = 100,
) -> NDArray:
    """Return the populations the rabbits settle into, for many growth rates.

    Simulate every growth rate from the same `start`. Discard the first
    `burn_in` seasons, after `start`, as a transient, then keep the next `keep`
    populations. For a single growth rate return an array of shape `(keep,)`;
    for an array of `n` growth rates return shape `(n, keep)`, one row per rate.
    Aim to do all the growth rates together rather than one at a time, so that
    thousands of rates stay fast.
    """
    raise NotImplementedError
