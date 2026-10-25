import math
from itertools import islice

import pytest

from exercises.python_fundamentals.fundamentals import (
    add_tag,
    adjacent_elements_product,
    approximately_equal,
    average,
    copy_grid,
    exponentiate,
    fibonacci,
    first_non_repeating_character,
    fizzbuzz,
    keep_odd,
    look_and_say,
    make_grid,
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


def test_fibonacci_is_an_independent_infinite_generator():
    first = fibonacci()
    second = fibonacci()

    assert iter(first) is first
    assert list(islice(first, 9)) == [0, 1, 1, 2, 3, 5, 8, 13, 21]
    assert list(islice(second, 6)) == [0, 1, 1, 2, 3, 5]


def test_look_and_say_yields_string_terms():
    assert list(islice(look_and_say(), 9)) == [
        "1",
        "11",
        "21",
        "1211",
        "111221",
        "312211",
        "13112221",
        "1113213211",
        "31131211131221",
    ]


def test_look_and_say_iterators_continue_independently():
    first = look_and_say()
    second = look_and_say()

    assert iter(first) is first
    assert iter(second) is second
    assert list(islice(first, 6)) == ["1", "11", "21", "1211", "111221", "312211"]
    assert list(islice(second, 3)) == ["1", "11", "21"]
    assert next(first) == "13112221"
    assert next(second) == "1211"
    assert next(first) == "1113213211"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("abacabad", "c"),
        ("abacabaabacaba", None),
        ("z", "z"),
        ("bcb", "c"),
        ("a b!a", " "),
        ("a_a", "_"),
        ("__a", "a"),
        ("", None),
    ],
)
def test_first_non_repeating_character(text, expected):
    assert first_non_repeating_character(text) == expected


def test_first_non_repeating_character_is_case_sensitive():
    assert first_non_repeating_character("aA") == "a"


def test_gotcha_add_tag_does_not_share_state_between_calls():
    assert add_tag("first") == ["first"]
    assert add_tag("second") == ["second"]


def test_gotcha_add_tag_extends_the_list_it_is_given():
    tags = ["a"]

    assert add_tag("b", tags) is tags
    assert tags == ["a", "b"]


def test_gotcha_copy_grid_is_equal_but_shares_nothing():
    grid = [[1, 2], [3, 4]]

    copy = copy_grid(grid)

    assert copy == grid
    assert copy is not grid
    assert all(new is not old for new, old in zip(copy, grid, strict=True))
    copy[0][0] = 99
    assert grid == [[1, 2], [3, 4]]


def test_gotcha_make_grid_rows_are_independent():
    grid = make_grid(2, 3, fill=7)

    assert grid == [[7, 7, 7], [7, 7, 7]]
    grid[0][0] = 1
    assert grid == [[1, 7, 7], [7, 7, 7]]
    assert make_grid(1, 2) == [[0, 0]]


def test_gotcha_keep_odd_keeps_every_odd_value_without_changing_the_input():
    values = [1, 2, 4, 6, 7]

    assert keep_odd(values) == [1, 7]
    assert values == [1, 2, 4, 6, 7]
    assert keep_odd([-3, -2, 5]) == [-3, 5]
    assert keep_odd([2, 4]) == []


def test_gotcha_approximately_equal_ignores_rounding_but_not_real_differences():
    assert approximately_equal(0.1 + 0.2, 0.3)
    assert approximately_equal(1e12, 1e12 + 1e-3)
    assert not approximately_equal(0.1, 0.2)
    assert not approximately_equal(1.0, 1.001)


def test_gotcha_average_reads_a_one_shot_iterable_only_once():
    assert average([1, 2, 3]) == 2
    assert average(iter([1, 2, 3])) == 2
    assert average(x for x in (2, 4)) == 3
