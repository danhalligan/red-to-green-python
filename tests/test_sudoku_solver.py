from copy import deepcopy

import pytest

from pyproblems.language import sudoku_checker
from pyproblems.sudoku import is_valid_placement, sudoku_solver

SOLUTION = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9],
]


def test_valid_placement_checks_row_column_and_box():
    grid = deepcopy(SOLUTION)
    grid[0][2] = None

    assert is_valid_placement(grid, 0, 2, 4) is True
    assert is_valid_placement(grid, 0, 2, 5) is False


def test_solver_finds_a_solution_without_mutating_input():
    grid = deepcopy(SOLUTION)
    grid[0][2] = None
    original = deepcopy(grid)

    assert sudoku_solver(grid) == SOLUTION
    assert grid == original


def test_solver_returns_one_valid_solution_for_an_ambiguous_grid():
    grid = deepcopy(SOLUTION)
    for row, column in ((0, 3), (0, 4), (3, 3), (3, 4)):
        grid[row][column] = None

    solution = sudoku_solver(grid)

    assert solution is not None
    assert len(solution) == 9
    assert sudoku_checker(solution) is True
    assert all(
        solution[row][column] == value
        for row, values in enumerate(grid)
        for column, value in enumerate(values)
        if value is not None
    )


def test_solver_returns_none_for_an_inconsistent_grid():
    grid = deepcopy(SOLUTION)
    grid[0][0] = grid[0][1]

    assert sudoku_solver(grid) is None


@pytest.mark.parametrize("grid", [[[None] * 9 for _ in range(8)]])
def test_solver_rejects_malformed_grids(grid):
    with pytest.raises(ValueError):
        sudoku_solver(grid)
