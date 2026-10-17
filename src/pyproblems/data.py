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


def load_faithful_data() -> list[tuple[float, float]]:
    """Load Old Faithful eruption durations and waiting times from CSV."""
    resource = files("pyproblems.datasets").joinpath("faithful.csv")
    with resource.open("r", encoding="utf-8", newline="") as source:
        return [
            (float(row["eruptions"]), float(row["waiting"]))
            for row in csv.DictReader(source)
        ]


def load_titanic_data() -> list[dict[str, str | None]]:
    """Load labelled Titanic passenger records as strings, with blanks as None.

    The full titanic3 snapshot has 1,309 labelled records; PassengerId is a
    local row ID, not a Kaggle ID. Outcome-revealing boat/body fields are
    excluded. Split these records to evaluate predictions locally.
    Convert numeric columns in the analysis, leaving identifiers as strings.
    """
    resource = files("pyproblems.datasets").joinpath("titanic.csv")
    with resource.open("r", encoding="utf-8", newline="") as source:
        return [
            {key: None if value == "" else value for key, value in row.items()}
            for row in csv.DictReader(source)
        ]


def load_words() -> set[str]:
    """Load the packaged English word list (derived from SCOWL) as lowercase words."""
    resource = files("pyproblems.datasets").joinpath("words.txt")
    with resource.open("r", encoding="utf-8") as source:
        return {line.strip() for line in source if line.strip()}
