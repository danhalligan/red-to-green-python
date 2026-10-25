"""Load the Sudoku puzzles."""

import json
from importlib.resources import files
from typing import TypedDict, cast


class SudokuPuzzle(TypedDict):
    answer: bool
    grid: list[list[int | None]]


def load_sudoku_data() -> list[SudokuPuzzle]:
    """Load Sudoku answers and row-major 9 by 9 grids."""
    resource = files("exercises.algorithms.sudoku").joinpath("data", "sudoku.json")
    with resource.open("r", encoding="utf-8") as source:
        return cast(list[SudokuPuzzle], json.load(source))
