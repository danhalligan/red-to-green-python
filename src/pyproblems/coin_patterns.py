"""Coin-flip exercises: how long until a pattern appears?"""

import random
from collections.abc import Iterable, Iterator


def coin_flips(rng: random.Random) -> Iterator[str]:
    """Yield an endless stream of fair coin flips: "H" or "T".

    Use only `rng`, so a seeded generator gives a reproducible stream.
    """
    raise NotImplementedError


def flips_until(pattern: str, flips: Iterable[str]) -> int:
    """Return how many flips it takes for `pattern` to appear.

    Read `flips` one at a time and stop as soon as the most recent flips spell
    `pattern`; `flips` may be endless. For example, "HT" first appears after 5
    flips of "TTHHTH...", and "HH" after 2 flips of "HHH...".
    """
    raise NotImplementedError


def average_waiting_time(pattern: str, *, trials: int, rng: random.Random) -> float:
    """Estimate the mean number of flips until `pattern` first appears.

    Run `trials` experiments, each with a new stream of fair coin flips made
    from `rng`.
    """
    raise NotImplementedError


def expected_waiting_time(pattern: str) -> float:
    """Return the exact expected number of flips until `pattern` first appears."""
    raise NotImplementedError
