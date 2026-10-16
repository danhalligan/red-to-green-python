import random

import pytest

from pyproblems.birthday import (
    estimate_shared_birthday_probability,
    has_shared_birthday,
    shared_birthday_probability,
    smallest_group_with_probability,
)


def exact_by_multiplying(people, days):
    """Chance of a shared birthday, built up one person at a time."""
    nobody_shares = 1.0
    for already_here in range(people):
        nobody_shares *= (days - already_here) / days
    return 1 - nobody_shares


def test_a_repeated_day_is_a_shared_birthday():
    assert has_shared_birthday([3, 9, 3])
    assert has_shared_birthday((200, 200))
    assert not has_shared_birthday([3, 9, 4])


@pytest.mark.parametrize("group", [[], [5]])
def test_a_group_of_fewer_than_two_never_shares_a_birthday(group):
    assert not has_shared_birthday(group)


@pytest.mark.parametrize(
    ("people", "days", "expected"),
    [
        (0, 10, 0.0),
        (1, 10, 0.0),
        (2, 1, 1.0),
        (2, 10, 0.1),
        (3, 6, 4 / 9),
        (5, 10, 0.6976),
        (11, 10, 1.0),
    ],
)
def test_exact_probability_known_values(people, days, expected):
    assert shared_birthday_probability(people, days) == pytest.approx(expected)


@pytest.mark.parametrize(("people", "days"), [(10, 50), (23, 1000), (60, 200)])
def test_exact_probability_matches_multiplying_it_out(people, days):
    expected = exact_by_multiplying(people, days)
    assert shared_birthday_probability(people, days) == pytest.approx(expected)


def test_exact_probability_never_decreases_with_group_size():
    chances = [shared_birthday_probability(people, 50) for people in range(80)]
    assert chances == sorted(chances)
    assert chances[-1] == 1.0


def test_exact_probability_copes_with_huge_groups():
    assert shared_birthday_probability(5000, 10_000) == pytest.approx(1.0)


def test_exact_probability_defaults_to_a_year():
    assert shared_birthday_probability(40) == shared_birthday_probability(40, 365)


@pytest.mark.parametrize(("people", "days"), [(-1, 365), (5, 0)])
def test_exact_probability_rejects_impossible_inputs(people, days):
    with pytest.raises(ValueError):
        shared_birthday_probability(people, days)


def test_estimate_is_close_to_the_true_chance():
    estimate = estimate_shared_birthday_probability(
        4, trials=20_000, rng=random.Random(1), days=10
    )
    assert estimate == pytest.approx(0.496, abs=0.03)


def test_estimate_is_certain_or_impossible_at_the_extremes():
    rng = random.Random(2)
    assert estimate_shared_birthday_probability(2, trials=50, rng=rng, days=1) == 1.0
    assert estimate_shared_birthday_probability(1, trials=50, rng=rng, days=10) == 0.0


def test_estimate_is_reproducible_with_a_seeded_generator():
    first = estimate_shared_birthday_probability(
        10, trials=500, rng=random.Random(42), days=50
    )
    second = estimate_shared_birthday_probability(
        10, trials=500, rng=random.Random(42), days=50
    )
    assert first == second
    assert 0 < first < 1


def test_estimate_uses_only_the_supplied_generator():
    random.seed(5)
    before = random.getstate()
    estimate_shared_birthday_probability(5, trials=50, rng=random.Random(1), days=20)
    assert random.getstate() == before


def test_estimate_rejects_fewer_than_one_trial():
    with pytest.raises(ValueError):
        estimate_shared_birthday_probability(5, trials=0, rng=random.Random(1))


@pytest.mark.parametrize(
    ("threshold", "days", "expected"),
    [(0.25, 10, 3), (0.5, 10, 5), (0.99, 10, 9), (0.0001, 10, 2), (0.9999, 3, 4)],
)
def test_smallest_group_known_values(threshold, days, expected):
    assert smallest_group_with_probability(threshold, days) == expected


@pytest.mark.parametrize("days", [10, 100, 365])
@pytest.mark.parametrize("threshold", [0.1, 0.5, 0.9, 0.999])
def test_smallest_group_is_the_first_to_reach_the_threshold(threshold, days):
    size = smallest_group_with_probability(threshold, days)
    assert exact_by_multiplying(size, days) >= threshold
    assert exact_by_multiplying(size - 1, days) < threshold


@pytest.mark.parametrize("threshold", [0, 1, -0.5, 1.5])
def test_smallest_group_rejects_thresholds_outside_zero_to_one(threshold):
    with pytest.raises(ValueError):
        smallest_group_with_probability(threshold)
