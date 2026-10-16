"""Birthday paradox exercises."""

import random
from collections.abc import Sequence

DAYS_IN_YEAR = 365


def has_shared_birthday(birthdays: Sequence[int]) -> bool:
    """Return True if at least two people in the group share a birthday.

    Each birthday is a day number, such as 0 to 364 for a year. Nobody shares a
    birthday with themselves, so a group of 0 or 1 people is always False.
    """
    raise NotImplementedError


def estimate_shared_birthday_probability(
    people: int,
    *,
    trials: int,
    rng: random.Random,
    days: int = DAYS_IN_YEAR,
) -> float:
    """Estimate the chance that a random group has a shared birthday.

    Each trial gives each of `people` a birthday chosen independently and
    uniformly from `days` days. Return the fraction of `trials` groups with a
    shared birthday. Use only the supplied `rng`, so a seeded generator gives a
    reproducible estimate. Raise ValueError if `trials` is less than 1.
    """
    raise NotImplementedError


def shared_birthday_probability(people: int, days: int = DAYS_IN_YEAR) -> float:
    """Return the exact chance that a random group has a shared birthday.

    Assume every one of `days` days is equally likely for everybody, and that
    birthdays are independent. Raise ValueError if `people` is negative or
    `days` is less than 1.
    """
    raise NotImplementedError


def smallest_group_with_probability(threshold: float, days: int = DAYS_IN_YEAR) -> int:
    """Return the smallest group size whose chance of a shared birthday reaches
    `threshold`.

    Build on `shared_birthday_probability`. Raise ValueError unless
    0 < `threshold` < 1.
    """
    raise NotImplementedError
