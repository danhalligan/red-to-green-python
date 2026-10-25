import random

import pytest

from exercises.against_the_odds.hundred_prisoners.prisoners import (
    Room,
    TooManyDrawersError,
    clever_strategy,
    count_successes,
    cycle_lengths,
    estimate_survival,
    fixed_strategy,
    random_strategy,
    shuffled_drawers,
)

# Eight prisoners, four drawers each: the first arrangement lets everyone find
# their number with the clever strategy; in the second, all but one fail.
EASY_EIGHT = [6, 3, 5, 7, 0, 2, 4, 1]
HARD_EIGHT = [2, 0, 6, 4, 7, 5, 3, 1]


class RecordingRoom(Room):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.visited = []

    def open(self, drawer):
        self.visited.append(drawer)
        return super().open(drawer)


def test_a_room_reveals_only_the_drawers_that_are_opened():
    room = Room([2, 0, 1], limit=2, prisoner=1)

    assert room.open(0) == 2
    assert room.opened == 1
    assert not room.found
    assert room.open(1) == 0
    assert room.opened == 2


def test_a_room_notes_when_the_prisoner_sees_their_own_number():
    room = Room([2, 0, 1], limit=3, prisoner=1)

    room.open(0)
    room.open(2)

    assert room.found


def test_a_room_refuses_more_drawers_than_the_limit():
    room = Room([2, 0, 1], limit=1, prisoner=1)
    room.open(0)

    with pytest.raises(TooManyDrawersError):
        room.open(1)


def test_a_room_has_no_drawer_outside_the_cupboard():
    with pytest.raises(IndexError):
        Room([0, 1], limit=2, prisoner=0).open(2)


@pytest.mark.parametrize("size", [0, 1, 2, 10, 100])
def test_shuffled_drawers_hold_each_number_exactly_once(size):
    drawers = shuffled_drawers(size)

    assert sorted(drawers) == list(range(size))


def test_shuffled_drawers_are_actually_shuffled():
    seen = {tuple(shuffled_drawers(8)) for _ in range(10)}

    assert len(seen) > 5


def test_shuffled_drawers_are_reproducible_with_a_seed():
    random.seed(42)
    first = shuffled_drawers(30)
    random.seed(42)
    second = shuffled_drawers(30)

    assert first == second


def test_random_strategy_opens_different_drawers_up_to_the_limit():
    for _ in range(20):
        room = RecordingRoom(EASY_EIGHT, limit=4, prisoner=0)
        random_strategy(room)

        assert len(set(room.visited)) == len(room.visited)
        assert room.found or room.opened == 4


def test_random_strategy_always_succeeds_when_allowed_every_drawer():
    for _ in range(20):
        room = Room(HARD_EIGHT, limit=8, prisoner=3)
        random_strategy(room)

        assert room.found


def test_fixed_strategy_only_ever_opens_the_agreed_drawers():
    opened = set()
    for drawers in (EASY_EIGHT, HARD_EIGHT):
        for prisoner in range(8):
            room = RecordingRoom(drawers, limit=4, prisoner=prisoner)
            fixed_strategy(room)

            assert room.found or room.opened == 4
            opened |= set(room.visited)

    assert len(opened) <= 4


def test_fixed_strategy_saves_exactly_as_many_prisoners_as_drawers_opened():
    assert count_successes(fixed_strategy, EASY_EIGHT, 4) == 4
    assert count_successes(fixed_strategy, HARD_EIGHT, 4) == 4
    for _ in range(20):
        assert count_successes(fixed_strategy, shuffled_drawers(12), 5) == 5


@pytest.mark.parametrize("strategy", [random_strategy, fixed_strategy, clever_strategy])
def test_strategies_stay_within_the_limit(strategy):
    for prisoner in range(8):
        room = Room(HARD_EIGHT, limit=4, prisoner=prisoner)
        strategy(room)

        assert room.opened <= 4


def test_count_successes_gives_each_prisoner_a_fresh_room():
    def open_one_drawer(room):
        room.open(room.prisoner)

    drawers = [0, 2, 1, 3]

    assert count_successes(open_one_drawer, drawers, 1) == 2


def test_count_successes_counts_those_who_find_their_number():
    def do_nothing(room):
        pass

    def open_everything(room):
        for drawer in range(room.size):
            room.open(drawer)

    assert count_successes(do_nothing, EASY_EIGHT, 4) == 0
    assert count_successes(open_everything, EASY_EIGHT, 8) == 8


def test_count_successes_does_not_hide_a_strategy_that_breaks_the_limit():
    def greedy(room):
        for drawer in range(room.limit + 1):
            room.open(drawer)

    with pytest.raises(TooManyDrawersError):
        count_successes(greedy, EASY_EIGHT, 4)


def test_the_clever_strategy_can_save_everyone():
    assert count_successes(clever_strategy, EASY_EIGHT, 4) == 8


def test_the_clever_strategy_can_fail_almost_everyone():
    assert count_successes(clever_strategy, HARD_EIGHT, 4) == 1


@pytest.mark.parametrize("strategy", [random_strategy, fixed_strategy, clever_strategy])
def test_everyone_survives_when_every_drawer_may_be_opened(strategy):
    survival = estimate_survival(strategy, prisoners=6, limit=6, trials=50)

    assert survival == 1.0


def test_estimate_survival_fixed_strategy_never_frees_everyone():
    chance = estimate_survival(fixed_strategy, prisoners=6, limit=5, trials=200)

    assert chance == 0.0


def test_estimate_survival_random_strategy_for_two_prisoners():
    chance = estimate_survival(random_strategy, prisoners=2, limit=1, trials=4000)

    assert chance == pytest.approx(0.25, abs=0.04)


def test_estimate_survival_clever_strategy_for_two_prisoners():
    chance = estimate_survival(clever_strategy, prisoners=2, limit=1, trials=4000)

    assert chance == pytest.approx(0.5, abs=0.04)


def test_estimate_survival_random_strategy_for_ten_prisoners():
    chance = estimate_survival(random_strategy, prisoners=10, limit=5, trials=3000)

    assert chance < 0.01


def test_estimate_survival_clever_strategy_for_ten_prisoners():
    chance = estimate_survival(clever_strategy, prisoners=10, limit=5, trials=3000)

    assert 0.3 < chance < 0.41


def test_estimate_survival_is_reproducible_with_a_seed():
    random.seed(42)
    first = estimate_survival(random_strategy, prisoners=4, limit=2, trials=200)
    random.seed(42)
    second = estimate_survival(random_strategy, prisoners=4, limit=2, trials=200)

    assert first == second
    assert 0 < first < 1


@pytest.mark.parametrize(
    ("arrangement", "expected"),
    [
        ([], []),
        ([0], [1]),
        ([0, 1, 2, 3], [1, 1, 1, 1]),
        ([1, 0, 2], [1, 2]),
        ([1, 2, 3, 0], [4]),
        (EASY_EIGHT, [2, 3, 3]),
        (HARD_EIGHT, [1, 7]),
    ],
)
def test_cycle_lengths_known_values(arrangement, expected):
    assert sorted(cycle_lengths(arrangement)) == expected


def test_cycle_lengths_do_not_change_the_arrangement():
    arrangement = [1, 2, 0, 4, 3]
    cycle_lengths(arrangement)

    assert arrangement == [1, 2, 0, 4, 3]


def test_cycle_lengths_account_for_every_drawer_once():
    for size in range(1, 40):
        assert sum(cycle_lengths(shuffled_drawers(size))) == size


def test_successes_match_the_loop_lengths():
    for _ in range(100):
        drawers = shuffled_drawers(12)
        expected = sum(length for length in cycle_lengths(drawers) if length <= 6)

        assert count_successes(clever_strategy, drawers, 6) == expected
