"""The 100 prisoners problem.

Prisoners and drawers are both numbered from 0. Drawer `i` holds a number, and
together the numbers are an arrangement of 0 to n - 1, each exactly once.
"""

from collections.abc import Callable, Sequence


class TooManyDrawersError(Exception):
    """Raised when a prisoner tries to open more drawers than allowed."""


class Room:
    """The cupboard as one prisoner sees it. Provided: nothing to implement.

    A prisoner can open drawers one at a time with `open`, but cannot see what
    is in the others. The room counts the drawers opened (`opened`) and notes
    whether the prisoner has seen their own number (`found`).
    """

    def __init__(self, drawers: Sequence[int], limit: int, prisoner: int) -> None:
        self._drawers = tuple(drawers)
        self.size = len(self._drawers)
        self.limit = limit
        self.prisoner = prisoner
        self.opened = 0
        self.found = False

    def open(self, drawer: int) -> int:
        """Open a drawer and return the number inside it."""
        if not 0 <= drawer < self.size:
            raise IndexError(f"there is no drawer {drawer}")
        if self.opened >= self.limit:
            raise TooManyDrawersError(
                f"prisoner {self.prisoner} may open only {self.limit} drawers"
            )
        self.opened += 1
        number = self._drawers[drawer]
        self.found = self.found or number == self.prisoner
        return number


# A strategy opens drawers through the room.
Strategy = Callable[[Room], None]


def shuffled_drawers(size: int) -> list[int]:
    """Return a random arrangement of the numbers 0 to `size` - 1.

    Entry `i` is the number inside drawer `i`. Use the `random` module, so that
    `random.seed` gives a reproducible arrangement.
    """
    raise NotImplementedError


def random_strategy(room: Room) -> None:
    """Open `room.limit` different drawers, chosen at random.

    Stopping early once `room.found` is fine. Assume `room.limit` is at most
    `room.size`.
    """
    raise NotImplementedError


def clever_strategy(room: Room) -> None:
    """Look for `room.prisoner`'s number in a way that beats `random_strategy`.

    Open drawers one at a time through `room`, stopping when the number is found
    or `room.limit` drawers have been opened. The prisoner may remember what
    they have seen so far, but nothing else.
    """
    raise NotImplementedError


def count_successes(strategy: Strategy, drawers: Sequence[int], limit: int) -> int:
    """Return how many prisoners find their own number.

    Each prisoner enters a fresh `Room` for these `drawers` (everything is
    closed again after the last prisoner), runs `strategy(room)` once, and
    succeeds if `room.found` is then True.
    """
    raise NotImplementedError


def estimate_survival(
    strategy: Strategy,
    *,
    prisoners: int,
    limit: int,
    trials: int,
) -> float:
    """Estimate the chance that every prisoner finds their own number.

    Each trial fills the drawers afresh with `shuffled_drawers`. Return the
    fraction of `trials` in which all `prisoners` succeed.
    """
    raise NotImplementedError


def cycle_lengths(arrangement: Sequence[int]) -> list[int]:
    """Return the length of each closed loop in the arrangement, in any order.

    Drawer `i` points to drawer `arrangement[i]`. Following the pointers from
    any drawer eventually returns to it, and every drawer belongs to exactly one
    such loop. For example, [1, 0, 2] has loops of length 2 and 1.
    """
    raise NotImplementedError
