"""Recursive backtracking exercises for Sudoku puzzles."""

Grid = list[list[int | None]]


def is_valid_placement(grid: Grid, row: int, column: int, value: int) -> bool:
    """Return whether value can be placed at a zero-based grid position."""
    raise NotImplementedError


def sudoku_solver(grid: Grid) -> Grid | None:
    """Return one solution, or None if no solution exists, without mutation."""
    raise NotImplementedError
