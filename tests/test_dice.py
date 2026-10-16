import random
from fractions import Fraction
from itertools import chain

import pytest

from pyproblems.dice import (
    HUSTLER_DICE,
    best_reply,
    champion,
    find_cycle_of_dice,
    win_probability,
)


def wins(die, other):
    """Count the (die face, other face) pairs where `die` is higher."""
    return sum(face > opposing for face in die for opposing in other)


def chance(die, other):
    return Fraction(wins(die, other), len(die) * len(other))


def random_dice(rng, count):
    sides = [rng.randint(2, 6) for _ in range(count)]
    return [tuple(rng.randint(1, 8) for _ in range(n)) for n in sides]


@pytest.mark.parametrize(
    ("die", "other", "expected"),
    [
        ((1, 2, 3), (1, 2, 3), Fraction(1, 3)),
        ((1, 2, 3, 4, 5, 6), (1, 2, 3, 4, 5, 6), Fraction(5, 12)),
        ((3, 3, 3), (1, 2, 3), Fraction(2, 3)),
        ((1, 2, 3), (3, 3, 3), Fraction(0)),
        ((4,), (1, 2, 3, 5), Fraction(3, 4)),
        ((1, 1, 1, 9), (5,), Fraction(1, 4)),
    ],
)
def test_win_probability_known_values(die, other, expected):
    result = win_probability(die, other)
    assert isinstance(result, Fraction)
    assert result == expected


def test_win_probability_matches_counting_every_pair_of_faces():
    rng = random.Random(3)
    for _ in range(40):
        die, other = random_dice(rng, 2)
        assert win_probability(die, other) == chance(die, other)


def test_win_probability_leaves_room_for_ties():
    rng = random.Random(4)
    for _ in range(40):
        die, other = random_dice(rng, 2)
        assert win_probability(die, other) + win_probability(other, die) <= 1


def test_win_probability_accepts_lists_and_tuples():
    assert win_probability([2, 2], (1, 3)) == Fraction(1, 2)


def test_hustler_dice_are_three_six_sided_dice_of_distinct_faces():
    assert len(HUSTLER_DICE) == 3
    assert all(len(die) == 6 for die in HUSTLER_DICE)
    faces = sorted(chain.from_iterable(HUSTLER_DICE))
    assert len(set(faces)) == 9


def test_best_reply_picks_the_die_most_likely_to_win():
    dice = [(3, 3, 3), (1, 1, 5), (4, 4, 4)]
    assert best_reply(dice, 0) == 2
    assert best_reply(dice, 2) == 1


def test_best_reply_breaks_ties_with_the_lowest_index():
    dice = [(1, 1), (5, 5), (6, 6), (4, 4)]
    assert best_reply(dice, 0) == 1


def test_best_reply_is_at_least_as_good_as_every_alternative():
    rng = random.Random(6)
    for _ in range(30):
        dice = random_dice(rng, 4)
        for chosen in range(4):
            reply = best_reply(dice, chosen)
            best = max(
                chance(dice[other], dice[chosen])
                for other in range(4)
                if other != chosen
            )
            assert reply != chosen
            assert chance(dice[reply], dice[chosen]) == best


def test_best_reply_needs_at_least_two_dice():
    with pytest.raises(ValueError):
        best_reply([(1, 2, 3)], 0)


def test_champion_is_the_die_that_beats_all_the_others():
    dice = [(1, 2, 3), (2, 3, 4), (5, 5, 5), (0, 9, 0)]
    assert champion(dice) == 2


def test_champion_is_none_when_no_die_beats_everything():
    assert champion([(1, 2, 3), (1, 2, 3)]) is None
    assert champion([(2, 4, 9), (1, 6, 8), (3, 5, 7)]) is None


def test_champion_needs_at_least_two_dice():
    with pytest.raises(ValueError):
        champion([(1, 2, 3)])


def test_find_cycle_of_dice_splits_faces_into_dice_that_beat_each_other(time_limit):
    faces = list(range(1, 10))
    with time_limit(20):
        dice = find_cycle_of_dice(faces)

    assert dice is not None
    assert len(dice) == 3
    assert all(len(die) == 3 for die in dice)
    assert sorted(chain.from_iterable(dice)) == faces
    for die, following in zip(dice, dice[1:] + dice[:1], strict=True):
        assert wins(die, following) > wins(following, die)


def test_find_cycle_of_dice_is_none_when_it_cannot_be_done():
    assert find_cycle_of_dice([1, 2, 3, 4], dice_count=2) is None
    assert find_cycle_of_dice([5] * 6, dice_count=3) is None


@pytest.mark.parametrize(("faces", "dice_count"), [(range(10), 3), (range(9), 1)])
def test_find_cycle_of_dice_rejects_impossible_splits(faces, dice_count):
    with pytest.raises(ValueError):
        find_cycle_of_dice(list(faces), dice_count)
