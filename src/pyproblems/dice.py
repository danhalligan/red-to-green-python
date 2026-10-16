"""Dice exercises: exact win probabilities and the hustler's game."""

from collections.abc import Sequence
from fractions import Fraction

Die = tuple[int, ...]

# Each face of a die is equally likely; ties are possible between dice.
HUSTLER_DICE: tuple[Die, ...] = (
    (2, 2, 4, 4, 9, 9),
    (1, 1, 6, 6, 8, 8),
    (3, 3, 5, 5, 7, 7),
)


def win_probability(die: Sequence[int], other: Sequence[int]) -> Fraction:
    """Return the exact chance that `die` rolls strictly higher than `other`.

    Each face of a die is equally likely, and the two dice are rolled
    independently. A tie is not a win. Return a `Fraction`, not a float, so
    that results can be compared exactly.
    """
    raise NotImplementedError


def best_reply(dice: Sequence[Sequence[int]], chosen: int) -> int:
    """Return the index of the die to pick after your opponent takes dice[chosen].

    Pick the die, other than `dice[chosen]` itself, that is most likely to roll
    higher than it. If several are equally good, pick the lowest index. Raise
    ValueError if there are fewer than two dice.
    """
    raise NotImplementedError


def champion(dice: Sequence[Sequence[int]]) -> int | None:
    """Return the index of a die that beats every other die, or None.

    Die X beats die Y if `win_probability(X, Y)` is greater than
    `win_probability(Y, X)`. Raise ValueError if there are fewer than two dice.
    """
    raise NotImplementedError


def find_cycle_of_dice(
    faces: Sequence[int], dice_count: int = 3
) -> tuple[Die, ...] | None:
    """Split `faces` between dice that beat each other in a circle.

    Share the faces equally between `dice_count` dice, using every face exactly
    once, so that the first die beats the second, the second beats the third,
    and so on, with the last beating the first. "Beats" is as in `champion`.
    Return any such dice, or None if there are none. Raise ValueError unless
    `dice_count` is at least 2 and `len(faces)` divides evenly by it.
    """
    raise NotImplementedError
