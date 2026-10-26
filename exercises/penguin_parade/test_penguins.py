import math

import numpy as np
import pandas as pd
import pytest

from exercises.penguin_parade.penguins import reconcile_samples, summarise_isotopes

FIELD_COLUMNS = [
    "study_name",
    "sample_number",
    "individual_id",
    "species",
    "body_mass_g",
]
LAB_COLUMNS = ["study_name", "sample_number", "individual_id", "delta15n", "delta13c"]

# Identifiers are reused as they are in the real study: N1A1 appears in two
# seasons, and sample number 1 is used by two species in the same season.
FIELD_ROWS = [
    ("PAL0708", 1, "N1A1", "Adelie", 3700),
    ("PAL0708", 1, "N7A1", "Gentoo", 5000),
    ("PAL0809", 51, "N1A1", "Adelie", 3600),
    ("PAL0809", 35, "N2A2", "Gentoo", 5100),
]
LAB_ROWS = [
    ("PAL0708", 1, "N1A1", 8.9, -25.0),
    ("PAL0708", 1, "N7A1", 8.2, -26.1),
    ("PAL0809", 51, "N1A1", 9.0, -25.4),
]


@pytest.fixture
def field():
    return pd.DataFrame(FIELD_ROWS, columns=FIELD_COLUMNS)


@pytest.fixture
def lab():
    return pd.DataFrame(LAB_ROWS, columns=LAB_COLUMNS)


def isotopes_by_penguin(result):
    return (
        result.set_index(["study_name", "individual_id"])[["delta15n", "delta13c"]]
        .sort_index()
        .astype(float)
    )


def test_reconcile_gives_one_row_per_field_observation_in_field_order(field, lab):
    expected = field.copy()
    expected["delta15n"] = [8.9, 8.2, 9.0, np.nan]
    expected["delta13c"] = [-25.0, -26.1, -25.4, np.nan]

    pd.testing.assert_frame_equal(reconcile_samples(field, lab), expected)


def test_reconcile_matches_records_by_identity_not_row_position(field, lab):
    expected = isotopes_by_penguin(reconcile_samples(field, lab))

    shuffled_lab = lab.iloc[[2, 0, 1]]
    shuffled_field = field.iloc[[3, 1, 0, 2]]

    pd.testing.assert_frame_equal(
        isotopes_by_penguin(reconcile_samples(field, shuffled_lab)), expected
    )
    result = reconcile_samples(shuffled_field, shuffled_lab)
    assert result["individual_id"].tolist() == ["N2A2", "N7A1", "N1A1", "N1A1"]
    pd.testing.assert_frame_equal(isotopes_by_penguin(result), expected)


def test_reconcile_keeps_an_id_reused_in_two_seasons_apart(field, lab):
    result = reconcile_samples(field, lab)
    n1a1 = result[result["individual_id"] == "N1A1"].set_index("study_name")

    assert len(result) == 4
    assert n1a1.loc["PAL0708", "delta15n"] == pytest.approx(8.9)
    assert n1a1.loc["PAL0809", "delta15n"] == pytest.approx(9.0)


def test_reconcile_keeps_a_sample_number_reused_by_two_species_apart(field, lab):
    result = reconcile_samples(field, lab)
    season = result[result["study_name"] == "PAL0708"].set_index("species")

    assert season.loc["Adelie", "delta13c"] == pytest.approx(-25.0)
    assert season.loc["Gentoo", "delta13c"] == pytest.approx(-26.1)


def test_reconcile_keeps_penguins_with_missing_or_partial_lab_results(field, lab):
    lab.loc[1, "delta15n"] = np.nan
    result = reconcile_samples(field, lab)

    assert len(result) == 4
    gentoo = result.set_index("individual_id").loc["N7A1"]
    assert math.isnan(gentoo["delta15n"])
    assert gentoo["delta13c"] == pytest.approx(-26.1)
    unmatched = result[result["individual_id"] == "N2A2"].iloc[0]
    assert math.isnan(unmatched["delta15n"]) and math.isnan(unmatched["delta13c"])


def test_reconcile_rejects_duplicate_lab_results(field, lab):
    repeated = pd.concat([lab, lab.iloc[[0]].assign(delta15n=9.9)], ignore_index=True)

    with pytest.raises(ValueError):
        reconcile_samples(field, repeated)


def test_reconcile_rejects_duplicate_field_observations(field, lab):
    repeated = pd.concat([field, field.iloc[[0]].assign(body_mass_g=3750)])

    with pytest.raises(ValueError):
        reconcile_samples(repeated, lab)


def test_reconcile_rejects_lab_results_with_no_field_observation(field, lab):
    orphan = pd.DataFrame([("PAL0910", 120, "N99A1", 8.0, -26.0)], columns=LAB_COLUMNS)

    with pytest.raises(ValueError):
        reconcile_samples(field, pd.concat([lab, orphan], ignore_index=True))


def test_reconcile_does_not_modify_its_inputs(field, lab):
    field_before, lab_before = field.copy(), lab.copy()
    reconcile_samples(field, lab)

    pd.testing.assert_frame_equal(field, field_before)
    pd.testing.assert_frame_equal(lab, lab_before)


@pytest.fixture
def isotope_data():
    return pd.DataFrame(
        {
            "species": ["Gentoo", "Adelie", "Adelie", "Chinstrap", "Adelie", "Gentoo"],
            "delta15n": [8.0, 9.0, 10.0, np.nan, np.nan, np.nan],
            "delta13c": [-26.0, -25.0, np.nan, np.nan, np.nan, -27.0],
        }
    )


def test_summarise_isotopes_gives_one_ordinary_row_per_species(isotope_data):
    result = summarise_isotopes(isotope_data)

    assert list(result.columns) == [
        "species",
        "n_observations",
        "n_delta15n",
        "n_delta13c",
        "mean_delta15n",
        "mean_delta13c",
        "sd_delta15n",
        "sd_delta13c",
    ]
    assert result["species"].tolist() == ["Adelie", "Chinstrap", "Gentoo"]
    assert result.index.equals(pd.RangeIndex(3))


def test_summarise_isotopes_counts_each_measurement_separately(isotope_data):
    result = summarise_isotopes(isotope_data)

    assert result["n_observations"].tolist() == [3, 1, 2]
    assert result["n_delta15n"].tolist() == [2, 0, 1]
    assert result["n_delta13c"].tolist() == [1, 0, 2]


def test_summarise_isotopes_ignores_missing_values_in_means_and_deviations(
    isotope_data,
):
    result = summarise_isotopes(isotope_data).set_index("species")

    assert result.loc["Adelie", "mean_delta15n"] == pytest.approx(9.5)
    assert result.loc["Adelie", "mean_delta13c"] == pytest.approx(-25.0)
    assert result.loc["Adelie", "sd_delta15n"] == pytest.approx(math.sqrt(0.5))
    assert result.loc["Gentoo", "mean_delta13c"] == pytest.approx(-26.5)
    assert result.loc["Gentoo", "sd_delta13c"] == pytest.approx(math.sqrt(0.5))
    # A single valid value has no sample standard deviation.
    assert math.isnan(result.loc["Adelie", "sd_delta13c"])
    assert math.isnan(result.loc["Gentoo", "sd_delta15n"])


def test_summarise_isotopes_keeps_species_without_valid_measurements(isotope_data):
    chinstrap = summarise_isotopes(isotope_data).set_index("species").loc["Chinstrap"]

    assert chinstrap["n_observations"] == 1
    assert chinstrap["n_delta15n"] == chinstrap["n_delta13c"] == 0
    assert math.isnan(chinstrap["mean_delta15n"])
    assert math.isnan(chinstrap["sd_delta13c"])


def test_summarise_isotopes_does_not_modify_its_input(isotope_data):
    before = isotope_data.copy()
    summarise_isotopes(isotope_data)

    pd.testing.assert_frame_equal(isotope_data, before)
