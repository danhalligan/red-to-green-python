import random
from itertools import islice, product

import pytest

from pyproblems.coin_patterns import (
    average_waiting_time,
    coin_flips,
    expected_waiting_time,
    flips_until,
)


def exact_waiting_time(pattern):
    """Expected flips to see `pattern`, by following the probabilities flip by flip.

    The state is the last few flips of a game that has not yet seen the pattern.
    The expectation is the sum over t of P(still waiting after t flips).
    """
    keep = len(pattern) - 1
    waiting = {"": 1.0}
    expected = 0.0
    for _ in range(10_000):
        expected += sum(waiting.values())
        following = {}
        for recent, chance in waiting.items():
            for flip in "HT":
                latest = recent + flip
                if not latest.endswith(pattern):
                    state = latest[-keep:] if keep else ""
                    following[state] = following.get(state, 0.0) + chance / 2
        waiting = following
        if sum(waiting.values()) < 1e-13:
            break
    return expected


def test_coin_flips_are_heads_and_tails_in_roughly_equal_measure():
    flips = list(islice(coin_flips(), 1000))

    assert set(flips) == {"H", "T"}
    assert 400 < flips.count("H") < 600


def test_coin_flips_never_run_out():
    assert len(list(islice(coin_flips(), 20_000))) == 20_000


def test_coin_flips_are_reproducible_with_a_seed():
    random.seed(7)
    first = list(islice(coin_flips(), 50))
    random.seed(7)
    second = list(islice(coin_flips(), 50))
    random.seed(8)
    other = list(islice(coin_flips(), 50))

    assert first == second
    assert first != other


@pytest.mark.parametrize(
    ("pattern", "flips", "expected"),
    [
        ("HH", "THHT", 3),
        ("HT", "TTHHTH", 5),
        ("HH", "HHH", 2),
        ("HHH", "HHHH", 3),
        ("T", "HHT", 3),
        ("HTH", "HTHTH", 3),
        ("THT", "HHTHTHH", 5),
        ("HHT", "HHHHT", 5),
        ("HT", "HT", 2),
    ],
)
def test_flips_until_counts_flips_to_the_end_of_the_first_match(
    pattern, flips, expected
):
    assert flips_until(pattern, flips) == expected


def test_flips_until_accepts_any_iterable():
    assert flips_until("HT", list("TTHT")) == 4
    assert flips_until("HT", iter("TTHT")) == 4
    assert flips_until("HT", (flip for flip in "TTHT")) == 4


def test_flips_until_stops_reading_as_soon_as_the_pattern_appears():
    def flips():
        yield "T"
        yield "H"
        raise AssertionError("read more flips than it needed to")

    assert flips_until("TH", flips()) == 2


def test_flips_until_works_on_an_endless_stream():
    count = flips_until("HHHHH", coin_flips())

    assert count >= 5


@pytest.mark.parametrize("pattern", ["H", "HH", "HT", "HHT", "THT"])
def test_average_waiting_time_is_close_to_the_exact_expectation(pattern):
    average = average_waiting_time(pattern, trials=20_000)

    assert average == pytest.approx(exact_waiting_time(pattern), rel=0.05)


def test_average_waiting_time_is_reproducible_with_a_seed():
    random.seed(42)
    first = average_waiting_time("HT", trials=200)
    random.seed(42)
    second = average_waiting_time("HT", trials=200)

    assert first == second


@pytest.mark.parametrize(
    "pattern",
    [
        "".join(flips)
        for length in range(1, 5)
        for flips in product("HT", repeat=length)
    ],
)
def test_expected_waiting_time_matches_the_exact_expectation(pattern):
    assert expected_waiting_time(pattern) == pytest.approx(
        exact_waiting_time(pattern), rel=1e-9
    )


def test_expected_waiting_time_copes_with_long_patterns():
    assert expected_waiting_time("H" * 20) == pytest.approx(2**21 - 2)
