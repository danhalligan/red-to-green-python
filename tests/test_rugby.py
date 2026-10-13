import pytest

from pyproblems.rugby import (
    count_scoring_combinations,
    count_scoring_sequences,
)

# (name, points, can only follow a try)
EVENTS = (
    ("penalty", 3, False),
    ("drop goal", 3, False),
    ("try", 5, False),
    ("conversion", 2, True),
)


def sequences_by_the_rules(points):
    """Count sequences by trying every legal event in turn; small scores only."""

    def extend(total, last_was_try):
        if total == points:
            return 1
        return sum(
            extend(total + value, name == "try")
            for name, value, needs_try in EVENTS
            if total + value <= points and (last_was_try or not needs_try)
        )

    return extend(0, False)


def tallies_by_the_rules(points):
    """Count tallies of (penalties, drop goals, tries, conversions) directly."""
    return sum(
        3 * penalties + 3 * drops + 5 * tries + 2 * conversions == points
        for penalties in range(points // 3 + 1)
        for drops in range(points // 3 + 1)
        for tries in range(points // 5 + 1)
        for conversions in range(tries + 1)
    )


@pytest.mark.parametrize(
    ("points", "expected"),
    [
        (0, 1),
        (1, 0),
        (2, 0),
        (3, 2),
        (4, 0),
        (5, 1),
        (6, 4),
        (7, 1),
        (8, 4),
        (9, 8),
        (10, 5),
        (11, 12),
        (12, 18),
        (20, 241),
        (30, 6981),
    ],
)
def test_count_scoring_sequences_known_values(points, expected):
    assert count_scoring_sequences(points) == expected


@pytest.mark.parametrize("points", range(26))
def test_count_scoring_sequences_matches_a_search_that_follows_the_rules(points):
    assert count_scoring_sequences(points) == sequences_by_the_rules(points)


def test_count_scoring_sequences_handles_a_large_score(time_limit):
    with time_limit(5):
        assert count_scoring_sequences(100) == 141759302436945


def test_count_scoring_sequences_rejects_negative_scores():
    with pytest.raises(ValueError):
        count_scoring_sequences(-1)


@pytest.mark.parametrize(
    ("points", "expected"),
    [(0, 1), (3, 2), (5, 1), (6, 3), (7, 1), (8, 2), (9, 4), (10, 3), (12, 6)],
)
def test_count_scoring_combinations_known_values(points, expected):
    assert count_scoring_combinations(points) == expected


@pytest.mark.parametrize("points", range(0, 101, 5))
def test_count_scoring_combinations_matches_a_direct_count_of_tallies(points):
    assert count_scoring_combinations(points) == tallies_by_the_rules(points)


@pytest.mark.parametrize("points", range(41))
def test_count_scoring_combinations_never_exceeds_the_sequences(points):
    assert count_scoring_combinations(points) <= count_scoring_sequences(points)


def test_count_scoring_combinations_rejects_negative_scores():
    with pytest.raises(ValueError):
        count_scoring_combinations(-1)
