from copy import deepcopy

import pytest

from pyproblems.data import load_sudoku_data
from pyproblems.sudoku import is_valid_placement, sudoku_checker, sudoku_solver

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

PACKAGED_PUZZLES = load_sudoku_data()
# Packaged puzzle 14 is labelled valid because its clues do not conflict, but it
# has no completion. The label says nothing about solvability.
LOCALLY_VALID_DEAD_END = 13


def assert_is_completion_of(puzzle, solution):
    assert solution is not None
    assert all(value is not None for row in solution for value in row)
    assert sudoku_checker(solution) is True
    assert all(
        solution[row][column] == value
        for row, values in enumerate(puzzle)
        for column, value in enumerate(values)
        if value is not None
    )


def test_valid_placement_checks_row_column_and_box():
    grid = deepcopy(SOLUTION)
    grid[0][2] = None

    assert is_valid_placement(grid, 0, 2, 4) is True
    assert is_valid_placement(grid, 0, 2, 5) is False


def test_valid_placement_reports_each_kind_of_conflict_on_its_own():
    grid = [[None] * 9 for _ in range(9)]
    grid[0][0] = 5

    assert is_valid_placement(grid, 0, 8, 5) is False  # same row only
    assert is_valid_placement(grid, 8, 0, 5) is False  # same column only
    assert is_valid_placement(grid, 1, 1, 5) is False  # same box only
    assert is_valid_placement(grid, 4, 4, 5) is True


def test_solver_returns_a_copy_of_a_completed_grid():
    solution = sudoku_solver(SOLUTION)

    assert solution == SOLUTION
    assert solution is not SOLUTION
    solution[0][0] = None
    assert SOLUTION[0][0] == 5


def test_solver_exhausts_a_dead_end_that_has_no_conflicting_clues():
    grid = deepcopy(SOLUTION)
    grid[0][0] = 1  # no clue repeats in its row, column or box
    grid[0][7] = None
    grid[2][0] = None
    original = deepcopy(grid)

    assert sudoku_solver(grid) is None
    assert grid == original


@pytest.mark.parametrize(
    "index",
    [
        index
        for index, puzzle in enumerate(PACKAGED_PUZZLES)
        if puzzle["answer"] and index != LOCALLY_VALID_DEAD_END
    ],
    ids=lambda index: f"puzzle{index + 1}",
)
def test_solver_completes_each_solvable_packaged_puzzle(index):
    puzzle = PACKAGED_PUZZLES[index]["grid"]
    original = deepcopy(puzzle)

    assert_is_completion_of(puzzle, sudoku_solver(puzzle))
    assert puzzle == original


def test_solver_rejects_every_packaged_puzzle_with_conflicting_clues():
    for puzzle in PACKAGED_PUZZLES:
        if not puzzle["answer"]:
            assert sudoku_solver(puzzle["grid"]) is None


def test_solver_finds_no_completion_for_the_packaged_locally_valid_dead_end():
    puzzle = PACKAGED_PUZZLES[LOCALLY_VALID_DEAD_END]

    assert puzzle["answer"] is True
    assert sudoku_solver(puzzle["grid"]) is None


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
