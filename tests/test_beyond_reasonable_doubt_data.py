"""Integrity checks for the Beyond reasonable doubt data."""

from importlib.resources import files

import pytest

pd = pytest.importorskip("pandas")

from exercises.beyond_reasonable_doubt.loaders import load_trial_results  # noqa: E402


def test_trial_counts_are_the_published_ones():
    results = load_trial_results()

    assert list(results.columns) == ["group", "patients", "deaths"]
    assert results.to_dict("records") == [
        {"group": "early_ecmo", "patients": 124, "deaths": 44},
        {"group": "conventional_care", "patients": 125, "deaths": 57},
    ]


def test_source_note_cites_both_publications():
    source = (
        files("exercises.beyond_reasonable_doubt")
        .joinpath("data", "SOURCE.md")
        .read_text(encoding="utf-8")
    )

    assert "10.1056/NEJMoa1800385" in source
    assert "10.1001/jama.2018.14276" in source
