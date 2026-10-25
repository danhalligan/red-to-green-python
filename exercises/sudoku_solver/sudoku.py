"""Sudoku exercises: validity checking and recursive backtracking."""

Grid = list[list[int | None]]


def sudoku_checker(grid: Grid) -> bool:
    """Return whether a 9 by 9 Sudoku grid has no repeated given values.

    `grid` is a list of nine rows of nine entries, each an integer 1 to 9 or
    `None` for a blank. A grid is valid when no row, column or 3 by 3 box
    contains the same digit twice; blanks never conflict. Raise ValueError for
    a malformed grid.
    """
    raise NotImplementedError


def is_valid_placement(grid: Grid, row: int, column: int, value: int) -> bool:
    """Return whether value can be placed at a zero-based grid position.

    `row` and `column` are zero-based and blank cells are `None`. The placement
    is valid if `value` does not already appear in the same row, column or 3 by
    3 box (ignoring the cell being filled).
    """
    raise NotImplementedError


def sudoku_solver(grid: Grid) -> Grid | None:
    """Return one solution, or None if no solution exists, without mutation.

    Use recursive backtracking: fill the first blank cell with each valid digit
    in turn, recurse, and undo the choice if it leads to a dead end. Stop at the
    first complete solution.

    Work on a copy so the input grid is unchanged. Return None if the clues
    already conflict or no completion exists. Raise ValueError for a malformed
    grid (not nine rows of nine entries, each an integer 1 to 9 or None).
    """
    raise NotImplementedError
