"""Load packaged datasets without requiring scientific Python dependencies."""

import csv
import json
from importlib.resources import files
from typing import TypedDict, cast


class SudokuPuzzle(TypedDict):
    answer: bool
    grid: list[list[int | None]]


class XYDataset(TypedDict):
    x: list[float]
    y: list[float]


def load_steak_toast_tea() -> list[dict[str, str | None]]:
    """Load poll responses, mapping blank and ``NA`` cells to ``None``."""
    resource = files("pyproblems.datasets").joinpath("steak_toast_tea.csv")
    with resource.open("r", encoding="utf-8", newline="") as source:
        rows = csv.DictReader(source)
        return [
            {key: None if value in ("", "NA") else value for key, value in row.items()}
            for row in rows
        ]


def load_sudoku_data() -> list[SudokuPuzzle]:
    """Load Sudoku answers and row-major 9 by 9 grids."""
    resource = files("pyproblems.datasets").joinpath("sudoku.json")
    with resource.open("r", encoding="utf-8") as source:
        return cast(list[SudokuPuzzle], json.load(source))


def load_xy_data() -> dict[str, XYDataset]:
    """Load the named mystery datasets as parallel ``x`` and ``y`` lists."""
    resource = files("pyproblems.datasets").joinpath("xy.json")
    with resource.open("r", encoding="utf-8") as source:
        return cast(dict[str, XYDataset], json.load(source))
