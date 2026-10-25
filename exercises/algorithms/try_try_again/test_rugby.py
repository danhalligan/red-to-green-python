import pytest

from exercises.algorithms.try_try_again.rugby import (
    count_scoring_combinations,
    count_scoring_sequences,
    smallest_score_with_more_sequences_than,
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
        (3, 2),
        (5, 1),
        (7, 1),
        (8, 4),
        (10, 5),
        (0, 1),
        (1, 0),
        (2, 0),
        (4, 0),
        (6, 4),
        (9, 8),
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


def test_count_scoring_sequences_when_the_commentator_gets_carried_away(time_limit):
    with time_limit(5):
        assert count_scoring_sequences(50) == 6156717
        assert count_scoring_sequences(100) == 141759302436945


def test_count_scoring_sequences_for_the_entire_season(time_limit):
    try:
        with time_limit(10):
            count = count_scoring_sequences(20_000)
    except RecursionError:
        pytest.fail(
            "Recursion went too deep. Can you work out the answers in an order "
            "that avoids deep recursion?",
            pytrace=False,
        )
    # Compare the size and last digits: str() of a huge int hits Python's limit.
    assert count.bit_length() == 9781
    assert count % 10**12 == 886499301161


def test_count_scoring_sequences_rejects_negative_scores():
    with pytest.raises(ValueError):
        count_scoring_sequences(-1)


@pytest.mark.parametrize(
    ("count", "score"),
    [(0, 0), (1, 3), (4, 9), (10, 11), (100, 18), (1000, 25)],
)
def test_smallest_score_with_more_sequences_than_small_thresholds(count, score):
    assert smallest_score_with_more_sequences_than(count) == score


@pytest.mark.parametrize("count", [0, 1, 4, 10, 100, 1000])
def test_smallest_score_with_more_sequences_than_agrees_with_the_counts(count):
    score = smallest_score_with_more_sequences_than(count)

    assert count_scoring_sequences(score) > count
    assert all(count_scoring_sequences(s) <= count for s in range(score))


def test_smallest_score_with_more_sequences_than_a_trillion(time_limit):
    with time_limit(5):
        assert smallest_score_with_more_sequences_than(10**9) == 66
        assert smallest_score_with_more_sequences_than(10**12) == 86


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
