import pytest

from exercises._shared.loaders import load_words
from exercises.word_ladder.word_ladder import (
    longest_shortest_ladder,
    word_ladder,
)


def assert_valid_route(route, words):
    assert all(word in words for word in route)
    assert len(set(route)) == len(route)
    assert all(
        sum(first != second for first, second in zip(left, right, strict=True)) == 1
        for left, right in zip(route, route[1:], strict=False)
    )


def test_play_to_game_returns_a_shortest_valid_route():
    words = load_words()
    route = word_ladder("play", "game", words)

    assert route is not None
    assert route[0] == "play"
    assert route[-1] == "game"
    assert len(route) - 1 == 9
    assert all(word in words for word in route)
    assert all(
        sum(first != second for first, second in zip(left, right, strict=True)) == 1
        for left, right in zip(route, route[1:], strict=False)
    )


@pytest.mark.parametrize(
    ("target", "moves"),
    [("plan", 1), ("snap", 3), ("pool", 4), ("golf", 6), ("ball", 7)],
)
def test_word_ladder_matches_the_readme_move_counts(target, moves):
    route = word_ladder("play", target, load_words())

    assert route is not None
    assert len(route) - 1 == moves


def test_word_ladder_returns_none_when_no_route_exists():
    assert word_ladder("cat", "dog", {"cat", "dog"}) is None


def test_word_ladder_returns_single_word_when_start_is_target():
    assert word_ladder("play", "play", {"play"}) == ["play"]


def test_longest_shortest_ladder_finds_the_furthest_four_letter_words():
    words = load_words()
    route = longest_shortest_ladder(words)

    assert {route[0], route[-1]} == {"amen", "whoa"}
    assert len(route) - 1 == 17
    assert_valid_route(route, words)


def test_longest_shortest_ladder_uses_only_words_of_the_requested_length():
    words = {"bat", "cat", "cot", "cog", "dog", "zip", "zap", "bats", "bass", "boss"}

    three = longest_shortest_ladder(words, length=3)
    four = longest_shortest_ladder(words, length=4)

    assert {three[0], three[-1]} == {"bat", "dog"}
    assert len(three) - 1 == 4
    assert_valid_route(three, words)
    assert {four[0], four[-1]} == {"bats", "boss"}
    assert len(four) - 1 == 2


def test_longest_shortest_ladder_of_a_single_word_is_that_word():
    assert longest_shortest_ladder({"cat"}, length=3) == ["cat"]


def test_longest_shortest_ladder_rejects_a_missing_word_length():
    with pytest.raises(ValueError):
        longest_shortest_ladder({"cat", "cot"}, length=4)
