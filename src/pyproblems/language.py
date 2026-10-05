"""Core-Python programming exercises."""

from collections.abc import Iterable, Iterator
from pathlib import Path


def exponentiate(values: Iterable[float]) -> list[float]:
    """Return the exponential of each value in an iterable."""
    raise NotImplementedError


def adjacent_elements_product(values: Iterable[int]) -> int | None:
    """Return the largest adjacent product, or None when there is no pair."""
    raise NotImplementedError


def fizzbuzz(n: int) -> list[str]:
    """Return FizzBuzz labels from one through n, inclusive."""
    raise NotImplementedError


def summarize(
    values: Iterable[int | float | None], *, method: str = "mean"
) -> dict[str, float]:
    """Summarize finite numeric values, ignoring None and NaN observations."""
    raise NotImplementedError


def fibonacci() -> Iterator[int]:
    """Yield the Fibonacci sequence indefinitely, starting with zero."""
    raise NotImplementedError


def first_non_repeating_character(text: str) -> str:
    """Return the first unique character, or underscore if none exists."""
    raise NotImplementedError


def parse_measurements(path: Path) -> list[float]:
    """Read one finite number per non-empty line from a text file."""
    raise NotImplementedError


def sudoku(grid: list[list[int | None]]) -> bool:
    """Return whether a 9 by 9 Sudoku grid has no repeated given values."""
    raise NotImplementedError
