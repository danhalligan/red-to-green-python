"""Core-Python programming exercises."""

from collections.abc import Iterable, Iterator


def exponentiate(values: Iterable[float]) -> list[float]:
    """Return the exponential of each value in an iterable."""
    raise NotImplementedError


def adjacent_elements_product(values: Iterable[int]) -> int | None:
    """Return the largest adjacent product, or None when there is no pair."""
    raise NotImplementedError


def fizzbuzz(n: int) -> list[str]:
    """Return FizzBuzz labels from one through n, inclusive."""
    raise NotImplementedError


def first_non_repeating_character(text: str) -> str | None:
    """Return the first unique character, or None if none exists."""
    raise NotImplementedError


def add_tag(tag: str, tags: list[str] | None = None) -> list[str]:
    """Append tag to tags and return the list, starting a new list if none is given."""
    raise NotImplementedError


def copy_grid(grid: list[list[int]]) -> list[list[int]]:
    """Return an equal grid that shares no lists with the original."""
    raise NotImplementedError


def make_grid(rows: int, columns: int, fill: int = 0) -> list[list[int]]:
    """Return a grid of `fill` values whose rows are independent lists."""
    raise NotImplementedError


def keep_odd(values: list[int]) -> list[int]:
    """Return the odd values as a new list, leaving the input unchanged."""
    raise NotImplementedError


def approximately_equal(first: float, second: float) -> bool:
    """Return whether two numbers differ only by floating-point rounding."""
    raise NotImplementedError


def average(values: Iterable[float]) -> float:
    """Return the mean of any iterable, including a one-shot iterator."""
    raise NotImplementedError


def fibonacci() -> Iterator[int]:
    """Yield the Fibonacci sequence indefinitely, starting with zero."""
    raise NotImplementedError


def look_and_say() -> Iterator[str]:
    """Yield look-and-say terms indefinitely as strings, starting with '1'."""
    raise NotImplementedError
