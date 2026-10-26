"""Integrity checks for the Penguin parade data."""

from importlib.resources import files

import pytest

pd = pytest.importorskip("pandas")

from exercises.penguin_parade.loaders import (  # noqa: E402
    load_field_observations,
    load_isotope_results,
)

KEY = ["study_name", "individual_id"]


@pytest.fixture(scope="module")
def field():
    return load_field_observations()


@pytest.fixture(scope="module")
def lab():
    return load_isotope_results()


def test_field_observations_have_the_expected_shape_and_species(field):
    assert list(field.columns) == [
        "study_name",
        "sample_number",
        "individual_id",
        "species",
        "island",
        "sex",
        "bill_length_mm",
        "bill_depth_mm",
        "flipper_length_mm",
        "body_mass_g",
        "comments",
    ]
    assert len(field) == 344
    assert field["species"].value_counts().to_dict() == {
        "Adelie": 152,
        "Gentoo": 124,
        "Chinstrap": 68,
    }
    assert field["study_name"].value_counts().to_dict() == {
        "PAL0910": 120,
        "PAL0809": 114,
        "PAL0708": 110,
    }


def test_isotope_results_have_the_expected_shape(lab):
    assert list(lab.columns) == [
        "study_name",
        "sample_number",
        "individual_id",
        "delta15n",
        "delta13c",
    ]
    assert len(lab) == 331


def test_source_missingness_is_preserved(field, lab):
    assert field.isna().sum().to_dict() == {
        "study_name": 0,
        "sample_number": 0,
        "individual_id": 0,
        "species": 0,
        "island": 0,
        "sex": 11,
        "bill_length_mm": 2,
        "bill_depth_mm": 2,
        "flipper_length_mm": 2,
        "body_mass_g": 2,
        "comments": 290,
    }
    assert lab["delta15n"].isna().sum() == 1
    assert lab["delta13c"].isna().sum() == 0
    assert not (lab[["delta15n", "delta13c"]].isna().all(axis=1)).any()


def test_measurement_totals_match_the_source(field, lab):
    totals = {
        "bill_length_mm": 15021.3,
        "bill_depth_mm": 5865.7,
        "flipper_length_mm": 68713.0,
        "body_mass_g": 1437000.0,
    }
    for column, total in totals.items():
        assert field[column].sum() == pytest.approx(total, abs=1e-6)
    assert lab["delta15n"].sum() == pytest.approx(2882.01596, abs=1e-6)
    assert lab["delta13c"].sum() == pytest.approx(-8502.1625, abs=1e-6)


def test_the_season_and_individual_id_identify_each_penguin(field, lab):
    assert not field.duplicated(KEY).any()
    assert not lab.duplicated(KEY).any()

    matched = lab.merge(field[KEY], on=KEY, how="left", indicator=True)
    assert (matched["_merge"] == "both").all()


def test_simple_keys_are_not_safe_to_join_on(field, lab):
    def left_join_rows(keys):
        return len(field.merge(lab, on=keys, how="left", suffixes=("", "_lab")))

    assert left_join_rows(["individual_id"]) == 703
    assert left_join_rows(["sample_number"]) == 826
    assert left_join_rows(["study_name", "sample_number"]) == 619
    assert left_join_rows(KEY) == 344


def test_every_penguin_without_isotopes_has_a_comment_explaining_why(field, lab):
    missing = field.merge(lab[KEY], on=KEY, how="left", indicator=True)
    missing = missing[missing["_merge"] == "left_only"]

    assert len(missing) == 13
    assert missing["comments"].str.contains("blood|sampled").all()


def test_the_files_are_shuffled_independently(field, lab):
    assert not field.equals(field.sort_values(["species", "sample_number"]))
    assert not lab.equals(lab.sort_values(["study_name", "sample_number"]))
    shared = field[KEY].merge(lab[KEY], on=KEY)
    assert not shared.equals(lab[KEY].reset_index(drop=True))


def test_the_source_note_records_the_pinned_source_and_licence():
    note = (
        files("exercises.penguin_parade")
        .joinpath("data", "SOURCE.md")
        .read_text(encoding="utf-8")
    )

    assert "8db8ef55e61d9a36b81e39833655410ace199e37" in note
    assert "144f623143c9360fd77322a4f86acb06dc198814dbd2669724c63e6457b907bd" in note
    assert "CC0" in note
