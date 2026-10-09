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


def fibonacci() -> Iterator[int]:
    """Yield the Fibonacci sequence indefinitely, starting with zero."""
    raise NotImplementedError


def first_non_repeating_character(text: str) -> str:
    """Return the first unique character, or underscore if none exists."""
    raise NotImplementedError
