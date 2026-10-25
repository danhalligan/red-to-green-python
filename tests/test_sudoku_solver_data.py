"""Integrity checks for the Sudoku puzzles."""

from exercises.algorithms.sudoku_solver.loaders import load_sudoku_data


def _grid_is_valid(grid: list[list[int | None]]) -> bool:
    groups = list(grid)
    groups.extend([[grid[row][column] for row in range(9)] for column in range(9)])
    groups.extend(
        [
            grid[row][column]
            for row in range(box_row, box_row + 3)
            for column in range(box_column, box_column + 3)
        ]
        for box_row in (0, 3, 6)
        for box_column in (0, 3, 6)
    )
    return all(
        len(values := [value for value in group if value is not None])
        == len(set(values))
        for group in groups
    )


def test_sudoku_grids_keep_shape_values_and_answers():
    puzzles = load_sudoku_data()

    assert len(puzzles) == 40
    assert sum(puzzle["answer"] for puzzle in puzzles) == 20
    assert sum(not puzzle["answer"] for puzzle in puzzles) == 20

    for puzzle in puzzles:
        grid = puzzle["grid"]
        assert len(grid) == 9
        assert all(len(row) == 9 for row in grid)
        assert all(value is None or 1 <= value <= 9 for row in grid for value in row)
        assert _grid_is_valid(grid) is puzzle["answer"]
