"""Integrity checks for the mysterious datasets."""

from statistics import correlation, mean, stdev

import pytest

from exercises.mysterious_data.loaders import load_xy_data


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
