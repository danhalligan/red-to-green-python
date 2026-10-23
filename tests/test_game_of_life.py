import numpy as np
import pytest
from numpy.testing import assert_array_equal

from pyproblems.game_of_life import (
    animate_boards,
    count_live_neighbors,
    load_shape,
    place_shape,
    render_board,
    step_game_of_life,
)


def test_neighbour_counts_include_only_available_boundary_cells():
    board = np.array([[1, 1], [1, 0]])

    assert_array_equal(count_live_neighbors(board), [[2, 2], [2, 3]])


def test_step_keeps_a_block_still_life_unchanged():
    block = np.array([[1, 1], [1, 1]])

    assert_array_equal(step_game_of_life(block), block)


def test_step_advances_a_blinker():
    vertical = np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]])
    horizontal = np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]])

    assert_array_equal(step_game_of_life(vertical), horizontal)


def test_packaged_patterns_have_expected_dimensions():
    expected_dimensions = {
        "glider": (3, 3),
        "lightweight_spaceship": (4, 5),
        "middleweight_spaceship": (5, 6),
        "heavyweight_spaceship": (5, 7),
        "gosper_glider_gun": (9, 36),
        "block": (2, 2),
        "beehive": (3, 4),
        "blinker": (1, 3),
        "toad": (2, 4),
        "beacon": (4, 4),
        "pulsar": (13, 13),
        "pentadecathlon": (3, 10),
        "r_pentomino": (3, 3),
        "diehard": (3, 8),
        "eater": (4, 4),
        "figure_eight": (6, 6),
        "tumbler": (5, 9),
        "pi_heptomino": (3, 3),
        "acorn": (3, 7),
    }

    for name, dimensions in expected_dimensions.items():
        assert load_shape(name).shape == dimensions

    assert np.count_nonzero(load_shape("gosper_glider_gun")) == 36
    assert np.count_nonzero(load_shape("pulsar")) == 48
    assert np.count_nonzero(load_shape("pentadecathlon")) == 12
    assert np.count_nonzero(load_shape("eater")) == 7
    assert np.count_nonzero(load_shape("figure_eight")) == 18
    assert np.count_nonzero(load_shape("tumbler")) == 16
    assert np.count_nonzero(load_shape("pi_heptomino")) == 7
    assert np.count_nonzero(load_shape("acorn")) == 7


def test_shape_loader_rejects_unknown_names():
    with pytest.raises(ValueError, match="unknown Game of Life pattern"):
        load_shape("not-a-pattern")


def test_renderer_uses_the_shape_file_glyphs():
    assert render_board([[1, 0], [0, 1]]) == "O.\n.O"


def test_place_shape_puts_the_pattern_on_an_empty_board():
    board = place_shape("glider", (6, 8), top=2, left=3)

    assert board.shape == (6, 8)
    assert_array_equal(board[2:5, 3:6], load_shape("glider"))
    assert np.count_nonzero(board) == 5


def test_place_shape_rejects_a_pattern_that_does_not_fit():
    with pytest.raises(ValueError, match="does not fit"):
        place_shape("gosper_glider_gun", (10, 20))


def test_animate_boards_makes_one_frame_per_board():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")
    boards = [np.zeros((4, 4), dtype=np.uint8) for _ in range(3)]

    animation = animate_boards(boards, interval=50)

    assert animation.to_jshtml().count("data:image/png;base64") == 3


def test_a_glider_travels_diagonally_and_keeps_its_shape():
    board = place_shape("glider", (10, 10), top=1, left=1)
    start = load_shape("glider")

    for _ in range(4):
        board = step_game_of_life(board)

    assert_array_equal(board[2:5, 2:5], start)
    assert np.count_nonzero(board) == 5


def test_the_glider_gun_fires_a_new_glider_every_thirty_generations():
    board = place_shape("gosper_glider_gun", (40, 70))
    populations = []

    for generation in range(91):
        if generation % 30 == 0:
            populations.append(np.count_nonzero(board))
        board = step_game_of_life(board)

    # The gun is 36 cells and every glider it fires adds 5.
    assert populations == [36, 41, 46, 51]


@pytest.mark.parametrize("name", ["block", "beehive", "eater"])
def test_still_lifes_do_not_change(name):
    board = place_shape(name, (10, 10), top=3, left=3)

    assert_array_equal(step_game_of_life(board), board)


@pytest.mark.parametrize(
    ("name", "period"),
    [
        ("blinker", 2),
        ("toad", 2),
        ("beacon", 2),
        ("pulsar", 3),
        ("figure_eight", 8),
        ("tumbler", 14),
        ("pentadecathlon", 15),
    ],
)
def test_oscillators_return_after_exactly_their_period(name, period):
    start = place_shape(name, (30, 30), top=9, left=9)
    board = start
    returns = []

    for _ in range(period):
        board = step_game_of_life(board)
        returns.append(np.array_equal(board, start))

    assert returns == [False] * (period - 1) + [True]


def test_the_r_pentomino_grows_from_five_cells_to_eighteen_in_eight_generations():
    board = place_shape("r_pentomino", (30, 30), top=13, left=13)
    populations = []

    for _ in range(9):
        populations.append(np.count_nonzero(board))
        board = step_game_of_life(board)

    assert populations == [5, 6, 7, 9, 8, 9, 12, 11, 18]


def test_the_diehard_pattern_vanishes_completely_at_generation_130():
    board = place_shape("diehard", (40, 40), top=18, left=16)
    alive = []

    for _ in range(130):
        board = step_game_of_life(board)
        alive.append(bool(board.any()))

    assert alive == [True] * 129 + [False]


def test_the_acorn_starts_from_seven_cells_and_grows_quickly():
    board = place_shape("acorn", (40, 40), top=18, left=16)
    populations = []

    for _ in range(10):
        populations.append(np.count_nonzero(board))
        board = step_game_of_life(board)

    assert populations == [7, 8, 10, 11, 11, 13, 15, 15, 18, 20]


def test_the_pi_heptomino_settles_into_a_period_two_pattern_at_generation_173():
    board = place_shape("pi_heptomino", (60, 60), top=28, left=28)
    boards = []

    assert np.count_nonzero(board) == 7
    for _ in range(176):
        boards.append(board)
        board = step_game_of_life(board)

    assert not np.array_equal(boards[172], boards[174])
    assert np.array_equal(boards[173], boards[175])
    assert np.count_nonzero(boards[173]) == 55


def test_the_eater_swallows_a_glider_and_survives_unchanged():
    eater = place_shape("eater", (30, 30), top=20, left=20)
    board = place_shape("glider", (30, 30), top=3, left=3) + eater
    populations = []

    for _ in range(59):
        populations.append(np.count_nonzero(board))
        board = step_game_of_life(board)

    assert populations[0] == 12  # the eater's 7 cells plus the glider's 5
    assert populations[-1] == 7
    assert_array_equal(board, eater)
