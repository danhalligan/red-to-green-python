from statistics import correlation, mean, stdev

import pytest

from pyproblems.data import (
    load_steak_toast_tea,
    load_sudoku_data,
    load_xy_data,
)


def test_steak_toast_tea_preserves_rows_invalid_values_and_missingness():
    responses = load_steak_toast_tea()

    assert len(responses) == 79
    assert list(responses[0]) == ["Steak", "Toast", "Tea"]
    assert sum(row["Steak"] is None for row in responses) == 1
    assert sum(row["Toast"] is None for row in responses) == 0
    assert sum(row["Tea"] is None for row in responses) == 6
    assert sum(row["Steak"] == "0" for row in responses) == 1


def test_xy_data_preserves_names_dimensions_and_summary_statistics():
    datasets = load_xy_data()

    assert list(datasets) == [f"Dataset{i}" for i in range(1, 14)]
    assert all(len(data["x"]) == len(data["y"]) == 142 for data in datasets.values())

    first = datasets["Dataset1"]
    assert mean(first["x"]) == pytest.approx(54.2632732394366)
    assert mean(first["y"]) == pytest.approx(47.8322528169014)
    assert stdev(first["x"]) == pytest.approx(16.7651420391168)
    assert stdev(first["y"]) == pytest.approx(26.9354034869391)
    assert correlation(first["x"], first["y"]) == pytest.approx(-0.0644718527009517)

    for data in datasets.values():
        assert mean(data["x"]) == pytest.approx(54.26, abs=0.01)
        assert mean(data["y"]) == pytest.approx(47.83, abs=0.01)
        assert stdev(data["x"]) == pytest.approx(16.76, abs=0.01)
        assert stdev(data["y"]) == pytest.approx(26.93, abs=0.01)
        assert correlation(data["x"], data["y"]) == pytest.approx(-0.065, abs=0.01)


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
