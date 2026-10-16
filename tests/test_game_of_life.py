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
    }

    for name, dimensions in expected_dimensions.items():
        assert load_shape(name).shape == dimensions

    assert np.count_nonzero(load_shape("gosper_glider_gun")) == 36


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
