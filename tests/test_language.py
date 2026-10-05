import math
from itertools import islice

import pytest

from pyproblems.language import (
    adjacent_elements_product,
    exponentiate,
    fibonacci,
    first_non_repeating_character,
    fizzbuzz,
)


def test_exponentiate_accepts_iterables():
    values = exponentiate([0.0, 1.0, 2.0])
    assert values == pytest.approx([1.0, math.e, math.e**2])

    generated_values = exponentiate(value for value in [0.0, 1.0])
    assert generated_values == pytest.approx([1.0, math.e])


@pytest.mark.parametrize(
    ("values", "expected"),
    [
        ([3, 6, -2, -5, 7, 3], 21),
        ([-1, -2], 2),
        ([1, 2, 3, 0], 6),
        ([1, -2, 3], -2),
        ([-2, 3], -6),
        ([-1, 2, -3, 4], -2),
        ([0, -1], 0),
        ([5], None),
        ([], None),
    ],
)
def test_adjacent_elements_product(values, expected):
    assert adjacent_elements_product(values) == expected


def test_adjacent_elements_product_accepts_one_shot_iterators():
    assert adjacent_elements_product(iter([4, -3, -8])) == 24
    assert adjacent_elements_product(iter([1, -2, 3])) == -2


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, []),
        (1, ["1"]),
        (5, ["1", "2", "Fizz", "4", "Buzz"]),
        (
            16,
            [
                "1",
                "2",
                "Fizz",
                "4",
                "Buzz",
                "Fizz",
                "7",
                "8",
                "Fizz",
                "Buzz",
                "11",
                "Fizz",
                "13",
                "14",
                "FizzBuzz",
                "16",
            ],
        ),
    ],
)
def test_fizzbuzz(n, expected):
    assert fizzbuzz(n) == expected


@pytest.mark.parametrize("n", [-1, -10])
def test_fizzbuzz_rejects_negative_input(n):
    with pytest.raises(ValueError, match="non-negative"):
        fizzbuzz(n)


@pytest.mark.parametrize("n", [1.5, "5", True])
def test_fizzbuzz_requires_an_integer(n):
    with pytest.raises(TypeError, match="integer"):
        fizzbuzz(n)


def test_fibonacci_is_an_independent_infinite_generator():
    first = fibonacci()
    second = fibonacci()

    assert iter(first) is first
    assert list(islice(first, 9)) == [0, 1, 1, 2, 3, 5, 8, 13, 21]
    assert list(islice(second, 6)) == [0, 1, 1, 2, 3, 5]


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abacabad", "c"),
        ("abacabaabacaba", "_"),
        ("z", "z"),
        ("bcb", "c"),
        ("a b!a", " "),
        ("", "_"),
    ],
)
def test_first_non_repeating_character(text, expected):
    assert first_non_repeating_character(text) == expected


def test_first_non_repeating_character_is_case_sensitive():
    assert first_non_repeating_character("aA") == "a"
