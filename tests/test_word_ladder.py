import pytest

from pyproblems.data import load_words
from pyproblems.word_ladder import word_ladder


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
