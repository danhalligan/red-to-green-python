import numpy as np
import pytest
from numpy.testing import assert_array_equal

from pyproblems.game_of_life import (
    count_live_neighbors,
    load_shape,
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
