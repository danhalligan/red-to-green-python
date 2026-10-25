"""Integrity checks for the Spinning Plates data files."""

import csv
import json
from collections import Counter
from importlib.resources import files

DATA = files("exercises.data_analysis.spinning_plates").joinpath("data")


def test_plate_reader_export_has_its_sections_and_both_matrices():
    text = DATA.joinpath("plate_reader_export.txt").read_text(encoding="utf-8")

    for header in (
        "[Run Information]",
        "[Measurement Settings]",
        "[Biomarker (RFU)]",
        "[Reference (RFU)]",
        "[Instrument Notes]",
    ):
        assert header in text
    assert "Plate ID:          EXP-042" in text
    assert text.count("\nWell\t01\t02") == 2
    assert text.count("OVER") >= 1


def test_plate_layout_assigns_every_well_once_with_replicated_conditions():
    with DATA.joinpath("plate_layout.csv").open(encoding="utf-8", newline="") as f:
        layout = list(csv.DictReader(f))

    assert list(layout[0]) == [
        "well",
        "sample_type",
        "compound",
        "concentration_um",
        "replicate",
    ]
    assert [row["well"] for row in layout] == [
        f"{row}{column:02d}" for row in "ABCDEFGH" for column in range(1, 13)
    ]
    assert Counter(row["sample_type"] for row in layout) == {
        "treatment": 48,
        "vehicle": 16,
        "inhibitor": 16,
        "blank": 16,
    }
    treatments = Counter(
        (row["compound"], row["concentration_um"])
        for row in layout
        if row["sample_type"] == "treatment"
    )
    assert len(treatments) == 12
    assert set(treatments.values()) == {4}
    assert {compound for compound, _ in treatments} == {
        "Compound A",
        "Compound B",
        "Compound C",
    }
    assert all(
        row["concentration_um"] == ""
        for row in layout
        if row["sample_type"] != "treatment"
    )


def test_plate_run_record_names_the_plate_and_logs_the_run():
    record = json.loads(
        DATA.joinpath("plate_run_record.json").read_text(encoding="utf-8")
    )

    assert record["plate_id"] == "EXP-042"
    assert record["run_date"] == "2026-10-16"
    assert record["log"]
