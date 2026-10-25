"""Contracts for the plate-reader helpers, using tiny plates with exact answers."""

from importlib.resources import files

import numpy as np
import pandas as pd
import pytest

from exercises.data_analysis.spinning_plates.spinning_plates import (
    join_layout,
    mark_usable,
    normalise_to_reference,
    parse_plate_reader,
    percent_of_vehicle,
    pivot_channels,
    remap_readings,
    subtract_blank,
    summarise_replicates,
    validate_plate,
    z_prime,
)

nan = np.nan

DATASETS = files("exercises.data_analysis.spinning_plates").joinpath("data")


def load_plate_reader_export():
    return DATASETS.joinpath("plate_reader_export.txt").read_text(encoding="utf-8")


def load_layout():
    with DATASETS.joinpath("plate_layout.csv").open(encoding="utf-8") as source:
        return pd.read_csv(source)


MINI_EXPORT = (
    "Mini Reader - Export\n"
    "\n"
    "\n"
    "[Run Information]\n"
    "Instrument:   Mini Reader\n"
    "Plate ID:     TEST-001\n"
    "Run date:     2026-01-01\n"
    "\n"
    "\n"
    "[Measurement Settings]\n"
    "Channel 1:    Biomarker   Gain 80\n"
    "Channel 2:    Reference   Gain 60\n"
    "\n"
    "[Biomarker (RFU)]\n"
    "Well\t01\t02\t03\n"
    "A\t100.5\tOVER\t300\n"
    "B\t---\t500\t600.25\n"
    "\n"
    "\n"
    "[Reference (RFU)]\n"
    "Well\t01\t02\t03\n"
    "A\t10\t20\t30\n"
    "B\t40\t50\t5\n"
    "\n"
    "\n"
    "[Instrument Notes]\n"
    "A02  Biomarker  Detector saturated (OVER)\n"
    "B03  Reference  Low signal warning\n"
    "Door opened during Reference read (12 s)\n"
    "\n"
    "[End of Export]\n"
)

WELLS = ["A01", "A02", "A03", "B01", "B02", "B03"]
TIDY_COLUMNS = ["plate_id", "well", "row", "column", "channel", "signal", "qc_flag"]
WIDE_COLUMNS = [
    "plate_id",
    "well",
    "row",
    "column",
    "biomarker",
    "reference",
    "biomarker_flag",
    "reference_flag",
]
LAYOUT_COLUMNS = ["sample_type", "compound", "concentration_um", "replicate"]


def signal_of(readings, well, channel):
    rows = readings[(readings["well"] == well) & (readings["channel"] == channel)]
    assert len(rows) == 1, f"expected one {channel} reading for {well}"
    return rows.iloc[0]


def tidy_readings():
    channels = {
        "biomarker": (
            [100.5, nan, 300.0, nan, 500.0, 600.25],
            ["ok", "saturated", "ok", "missing", "ok", "ok"],
        ),
        "reference": (
            [10.0, 20.0, 30.0, 40.0, 50.0, 5.0],
            ["ok", "ok", "ok", "ok", "ok", "low_signal"],
        ),
    }
    records = []
    for channel, (signals, flags) in channels.items():
        for well, signal, flag in zip(WELLS, signals, flags, strict=True):
            records.append(
                {
                    "plate_id": "TEST-001",
                    "well": well,
                    "row": well[0],
                    "column": int(well[1:]),
                    "channel": channel,
                    "signal": signal,
                    "qc_flag": flag,
                }
            )
    return pd.DataFrame(records)


def wide_wells():
    return pd.DataFrame(
        {
            "plate_id": "TEST-001",
            "well": WELLS,
            "row": [well[0] for well in WELLS],
            "column": [1, 2, 3, 1, 2, 3],
            "biomarker": [100.5, nan, 300.0, nan, 500.0, 600.25],
            "reference": [10.0, 20.0, 30.0, 40.0, 50.0, 5.0],
            "biomarker_flag": ["ok", "saturated", "ok", "missing", "ok", "ok"],
            "reference_flag": ["ok", "ok", "ok", "ok", "ok", "low_signal"],
        }
    )


def mini_layout():
    return pd.DataFrame(
        {
            "well": WELLS,
            "sample_type": [
                "blank",
                "vehicle",
                "treatment",
                "treatment",
                "inhibitor",
                "treatment",
            ],
            "compound": [
                None,
                "DMSO",
                "Compound A",
                "Compound A",
                "Reference inhibitor",
                None,
            ],
            "concentration_um": [nan, nan, 1.0, 10.0, nan, nan],
            "replicate": [1, 1, 1, 1, 1, 1],
        }
    )


# Stage 1: the instrument's revenge


def test_parse_returns_one_row_per_well_and_channel():
    readings = parse_plate_reader(MINI_EXPORT)

    assert list(readings.columns) == TIDY_COLUMNS
    assert len(readings) == 12
    assert set(readings["channel"]) == {"biomarker", "reference"}
    assert set(readings["plate_id"]) == {"TEST-001"}
    assert sorted(readings["well"].unique()) == WELLS
    assert readings.groupby("channel")["well"].nunique().to_dict() == {
        "biomarker": 6,
        "reference": 6,
    }


def test_parse_reads_both_channels_into_the_right_wells():
    readings = parse_plate_reader(MINI_EXPORT)

    assert signal_of(readings, "A01", "biomarker")["signal"] == 100.5
    assert signal_of(readings, "B03", "biomarker")["signal"] == 600.25
    assert signal_of(readings, "A03", "reference")["signal"] == 30.0
    assert signal_of(readings, "B02", "reference")["signal"] == 50.0
    b02 = signal_of(readings, "B02", "biomarker")
    assert (b02["row"], b02["column"]) == ("B", 2)
    assert readings["column"].dtype.kind == "i"
    assert readings["signal"].dtype.kind == "f"


def test_parse_marks_saturated_and_missing_readings_instead_of_dropping_them():
    readings = parse_plate_reader(MINI_EXPORT)

    saturated = signal_of(readings, "A02", "biomarker")
    missing = signal_of(readings, "B01", "biomarker")
    assert np.isnan(saturated["signal"]) and saturated["qc_flag"] == "saturated"
    assert np.isnan(missing["signal"]) and missing["qc_flag"] == "missing"


def test_parse_flags_low_signal_notes_but_keeps_the_reading():
    readings = parse_plate_reader(MINI_EXPORT)

    low = signal_of(readings, "B03", "reference")
    assert low["signal"] == 5.0 and low["qc_flag"] == "low_signal"
    # The same well in the other channel has no note.
    assert signal_of(readings, "B03", "biomarker")["qc_flag"] == "ok"
    assert readings["qc_flag"].value_counts().to_dict() == {
        "ok": 9,
        "saturated": 1,
        "missing": 1,
        "low_signal": 1,
    }


@pytest.mark.parametrize(
    "text",
    [
        MINI_EXPORT.replace("Plate ID:     TEST-001\n", ""),
        "Plate ID: TEST-001\n\n[Run Information]\nRun date: 2026-01-01\n",
    ],
    ids=["no-plate-id", "no-measurements"],
)
def test_parse_rejects_exports_without_a_plate_id_or_measurements(text):
    with pytest.raises(ValueError):
        parse_plate_reader(text)


def test_validate_accepts_a_complete_plate():
    assert validate_plate(tidy_readings(), rows="AB", n_columns=3) is None


@pytest.mark.parametrize("problem", ["missing", "duplicated", "unexpected"])
def test_validate_rejects_missing_duplicated_or_unexpected_wells(problem):
    readings = tidy_readings()
    if problem == "missing":
        readings = readings[readings["well"] != "B02"]
    elif problem == "duplicated":
        readings = pd.concat([readings, readings.iloc[[0]]])
    else:
        extra = readings.iloc[[0]].assign(well="C01", row="C")
        readings = pd.concat([readings, extra])

    with pytest.raises(ValueError):
        validate_plate(readings, rows="AB", n_columns=3)


def test_validate_checks_every_channel():
    readings = tidy_readings()
    drop = (readings["channel"] == "reference") & (readings["well"] == "A01")

    with pytest.raises(ValueError):
        validate_plate(readings[~drop], rows="AB", n_columns=3)


def test_validate_uses_a_96_well_plate_by_default():
    with pytest.raises(ValueError):
        validate_plate(tidy_readings())


def test_packaged_export_parses_to_a_valid_96_well_plate():
    readings = parse_plate_reader(load_plate_reader_export())

    assert len(readings) == 192
    assert set(readings["plate_id"]) == {"EXP-042"}
    validate_plate(readings)
    assert readings["qc_flag"].value_counts().to_dict() == {
        "ok": 187,
        "saturated": 2,
        "missing": 2,
        "low_signal": 1,
    }
    assert readings["signal"].isna().sum() == 4


# Stage 2: one well, one row


def test_pivot_gives_one_row_per_well_with_a_column_per_channel():
    wells = pivot_channels(tidy_readings())

    assert list(wells.columns) == WIDE_COLUMNS
    assert wells["well"].tolist() == WELLS
    assert wells["column"].tolist() == [1, 2, 3, 1, 2, 3]
    assert wells["biomarker"].tolist() == pytest.approx(
        [100.5, nan, 300.0, nan, 500.0, 600.25], nan_ok=True
    )
    assert wells["reference"].tolist() == [10.0, 20.0, 30.0, 40.0, 50.0, 5.0]
    assert wells["biomarker"].dtype == float
    assert wells["reference"].dtype == float


def test_pivot_keeps_the_qc_flags_with_their_readings():
    wells = pivot_channels(tidy_readings())

    assert wells["biomarker_flag"].tolist() == [
        "ok",
        "saturated",
        "ok",
        "missing",
        "ok",
        "ok",
    ]
    assert wells["reference_flag"].tolist() == ["ok"] * 5 + ["low_signal"]


def test_pivot_returns_wells_in_plate_order_with_a_fresh_index():
    shuffled = tidy_readings().iloc[::-1]
    wells = pivot_channels(shuffled)

    assert wells["well"].tolist() == WELLS
    assert wells.index.tolist() == list(range(6))
    assert wells["reference"].tolist() == [10.0, 20.0, 30.0, 40.0, 50.0, 5.0]


def test_pivot_leaves_the_input_unchanged():
    readings = tidy_readings()
    before = readings.copy()

    pivot_channels(readings)

    pd.testing.assert_frame_equal(readings, before)


def test_join_adds_layout_columns_without_losing_or_reordering_wells():
    wells = wide_wells()
    # A shuffled layout must still be matched by well, not by position.
    joined = join_layout(wells, mini_layout().iloc[::-1])

    assert list(joined.columns) == WIDE_COLUMNS + LAYOUT_COLUMNS
    assert joined["well"].tolist() == WELLS
    assert joined["sample_type"].tolist() == [
        "blank",
        "vehicle",
        "treatment",
        "treatment",
        "inhibitor",
        "treatment",
    ]
    assert joined["concentration_um"].tolist() == pytest.approx(
        [nan, nan, 1.0, 10.0, nan, nan], nan_ok=True
    )
    pd.testing.assert_frame_equal(joined[WIDE_COLUMNS], wells)


def test_join_rejects_wells_listed_twice():
    layout = mini_layout()
    duplicated_layout = pd.concat([layout, layout.iloc[[2]]])
    duplicated_wells = pd.concat([wide_wells(), wide_wells().iloc[[0]]])

    with pytest.raises(ValueError):
        join_layout(wide_wells(), duplicated_layout)
    with pytest.raises(ValueError):
        join_layout(duplicated_wells, layout)


def test_join_rejects_wells_missing_from_either_table():
    layout = mini_layout()

    with pytest.raises(ValueError):
        join_layout(wide_wells(), layout[layout["well"] != "B02"])
    with pytest.raises(ValueError):
        join_layout(wide_wells().iloc[:-1], layout)


def test_join_leaves_the_inputs_unchanged():
    wells, layout = wide_wells(), mini_layout()
    wells_before, layout_before = wells.copy(), layout.copy()

    join_layout(wells, layout)

    pd.testing.assert_frame_equal(wells, wells_before)
    pd.testing.assert_frame_equal(layout, layout_before)


def test_packaged_layout_joins_to_every_well_of_the_export():
    wells = pivot_channels(parse_plate_reader(load_plate_reader_export()))
    joined = join_layout(wells, load_layout())

    assert len(joined) == 96
    assert joined["well"].is_unique
    assert joined["sample_type"].value_counts().to_dict() == {
        "treatment": 48,
        "vehicle": 16,
        "inhibitor": 16,
        "blank": 16,
    }
    pd.testing.assert_frame_equal(joined[WIDE_COLUMNS], wells)


# Stage 3: the controls don't make sense

SWAPS = {
    "A01": "B03",
    "A02": "B02",
    "A03": "B01",
    "B01": "A03",
    "B02": "A02",
    "B03": "A01",
}


def test_remap_moves_readings_and_flags_between_wells():
    original = wide_wells()
    remapped = remap_readings(original, SWAPS.__getitem__)
    first, last = remapped.iloc[0], remapped.iloc[-1]

    assert first["well"] == "A01"
    assert first["biomarker"] == 600.25
    assert first["reference"] == 5.0
    assert first["reference_flag"] == "low_signal"
    assert np.isnan(remapped.iloc[2]["biomarker"])
    assert remapped.iloc[2]["biomarker_flag"] == "missing"
    assert last["biomarker"] == 100.5 and last["reference"] == 10.0


def test_remap_leaves_labels_where_they_are():
    original = join_layout(wide_wells(), mini_layout())
    remapped = remap_readings(original, SWAPS.__getitem__)

    assert remapped["well"].tolist() == WELLS
    for column in ["plate_id", "row", "column", *LAYOUT_COLUMNS]:
        pd.testing.assert_series_equal(remapped[column], original[column])


def test_remap_with_the_identity_changes_nothing():
    original = wide_wells()

    pd.testing.assert_frame_equal(remap_readings(original, lambda well: well), original)


def test_remap_twice_with_a_self_inverse_mapping_restores_the_table():
    original = wide_wells()
    once = remap_readings(original, SWAPS.__getitem__)

    assert not once["reference"].equals(original["reference"])
    pd.testing.assert_frame_equal(remap_readings(once, SWAPS.__getitem__), original)


def test_remap_can_move_only_the_requested_columns():
    original = wide_wells()
    remapped = remap_readings(original, SWAPS.__getitem__, columns=["reference"])

    assert remapped["reference"].tolist() == [5.0, 50.0, 40.0, 30.0, 20.0, 10.0]
    pd.testing.assert_series_equal(remapped["biomarker"], original["biomarker"])
    pd.testing.assert_series_equal(
        remapped["reference_flag"], original["reference_flag"]
    )


def test_remap_rejects_mappings_that_are_not_permutations():
    wells = wide_wells()

    with pytest.raises(ValueError):
        remap_readings(wells, lambda well: "H12")  # not on this plate
    with pytest.raises(ValueError):
        remap_readings(wells, lambda well: "A01")  # everyone reads A01


def test_remap_leaves_the_input_unchanged():
    wells = wide_wells()
    before = wells.copy()

    remap_readings(wells, SWAPS.__getitem__)

    pd.testing.assert_frame_equal(wells, before)


def test_z_prime_separates_controls_by_their_spread():
    assert z_prime([10, 11, 12], [0, 1, 2]) == pytest.approx(0.4)
    assert z_prime([9, 10, 11], [0, 1, 2]) == pytest.approx(1 / 3)


def test_z_prime_does_not_care_which_group_is_which_or_how_it_is_ordered():
    assert z_prime([0, 1, 2], [12, 10, 11]) == pytest.approx(0.4)


def test_z_prime_ignores_missing_values_and_goes_negative_for_overlap():
    assert z_prime([10, nan, 12, 11], pd.Series([0, 1, 2, nan])) == pytest.approx(0.4)
    assert z_prime([10, 14, 18], [8, 12, 16]) < 0


# Stage 4: the experiment comes back to life


def test_mark_usable_excludes_saturated_and_missing_readings_in_any_channel():
    wells = pd.DataFrame(
        {
            "well": ["A01", "A02", "A03", "A04"],
            "biomarker_flag": ["ok", "saturated", "ok", "low_signal"],
            "reference_flag": ["ok", "ok", "missing", "ok"],
        }
    )

    marked = mark_usable(wells)

    assert marked["usable"].tolist() == [True, False, False, True]
    assert marked["usable"].dtype == bool
    assert list(marked.columns) == [*wells.columns, "usable"]
    assert "usable" not in wells


def test_mark_usable_follows_the_policy_it_is_given():
    wells = pd.DataFrame(
        {
            "biomarker_flag": ["ok", "saturated", "ok", "low_signal"],
            "reference_flag": ["ok", "ok", "missing", "ok"],
        }
    )

    marked = mark_usable(wells, exclude_flags=("low_signal",))

    assert marked["usable"].tolist() == [True, True, True, False]


def analysis_table():
    return pd.DataFrame(
        {
            "well": ["A01", "A02", "A03", "B01", "B02", "B03"],
            "sample_type": ["blank"] * 3 + ["vehicle"] + ["treatment"] * 2,
            "biomarker": [100.0, 120.0, 9000.0, 1100.0, 610.0, 360.0],
            "reference": [50.0, 70.0, 9000.0, 560.0, 1060.0, 560.0],
            "usable": [True, True, False, True, True, False],
        }
    )


def test_subtract_blank_uses_the_mean_of_the_usable_blank_wells():
    table = analysis_table()

    result = subtract_blank(table)

    # Blank levels are 110 (biomarker) and 60 (reference); A03 is unusable.
    assert result["biomarker_net"].tolist() == pytest.approx(
        [-10, 10, nan, 990, 500, nan], nan_ok=True
    )
    assert result["reference_net"].tolist() == pytest.approx(
        [-10, 10, nan, 500, 1000, nan], nan_ok=True
    )


def test_subtract_blank_keeps_the_raw_measurements():
    table = analysis_table()
    before = table.copy()

    result = subtract_blank(table)

    pd.testing.assert_frame_equal(result[list(table.columns)], before)
    pd.testing.assert_frame_equal(table, before)


def test_subtract_blank_needs_usable_blank_wells():
    table = analysis_table()
    table["usable"] = table["sample_type"] != "blank"

    with pytest.raises(ValueError):
        subtract_blank(table)


def test_normalise_divides_the_biomarker_by_the_reference():
    wells = pd.DataFrame(
        {
            "biomarker_net": [500.0, 250.0, 30.0, nan],
            "reference_net": [1000.0, 500.0, 50.0, 800.0],
        }
    )

    result = normalise_to_reference(wells)

    assert result["normalised"].tolist() == pytest.approx(
        [0.5, 0.5, nan, nan], nan_ok=True
    )
    pd.testing.assert_frame_equal(result[list(wells.columns)], wells)


def test_normalise_treats_a_near_zero_reference_as_unmeasurable():
    wells = pd.DataFrame({"biomarker_net": [30.0, 5.0], "reference_net": [50.0, 0.0]})

    assert normalise_to_reference(wells, min_reference=40)["normalised"].tolist() == (
        pytest.approx([0.6, nan], nan_ok=True)
    )
    assert normalise_to_reference(wells)["normalised"].isna().all()


def test_percent_of_vehicle_scales_the_vehicle_mean_to_100():
    wells = pd.DataFrame(
        {
            "sample_type": ["vehicle"] * 3 + ["treatment", "blank"],
            "value": [2.0, 4.0, nan, 1.5, 0.0],
        },
        index=[10, 11, 12, 13, 14],
    )

    percent = percent_of_vehicle(wells, "value")

    assert percent.index.tolist() == [10, 11, 12, 13, 14]
    assert percent.tolist() == pytest.approx(
        [200 / 3, 400 / 3, nan, 50.0, 0.0], nan_ok=True
    )
    assert wells["value"].tolist() == pytest.approx(
        [2.0, 4.0, nan, 1.5, 0.0], nan_ok=True
    )


def test_percent_of_vehicle_needs_vehicle_values():
    wells = pd.DataFrame({"sample_type": ["vehicle", "treatment"], "value": [nan, 1.0]})

    with pytest.raises(ValueError):
        percent_of_vehicle(wells, "value")


def test_summarise_replicates_groups_by_compound_and_concentration():
    wells = pd.DataFrame(
        {
            "sample_type": ["treatment"] * 8 + ["vehicle", "inhibitor"],
            "compound": ["Compound B"] * 2
            + ["Compound A"] * 6
            + ["DMSO", "Reference inhibitor"],
            "concentration_um": [1.0, 1.0, 10.0, 10.0, 10.0, 1.0, 1.0, 1.0, nan, nan],
            "value": [8.0, 8.0, 4.0, 6.0, nan, 10.0, 20.0, 30.0, 100.0, 1.0],
        }
    )

    summary = summarise_replicates(wells, "value")

    assert list(summary.columns) == [
        "compound",
        "concentration_um",
        "n",
        "mean",
        "sd",
        "sem",
    ]
    assert summary["compound"].tolist() == ["Compound A", "Compound A", "Compound B"]
    assert summary["concentration_um"].tolist() == [1.0, 10.0, 1.0]
    assert summary["n"].tolist() == [3, 2, 2]
    assert summary["mean"].tolist() == pytest.approx([20.0, 5.0, 8.0])
    assert summary["sd"].tolist() == pytest.approx([10.0, 2**0.5, 0.0])
    assert summary["sem"].tolist() == pytest.approx([10 / 3**0.5, 1.0, 0.0])
    assert summary.index.tolist() == [0, 1, 2]


def test_packaged_plate_runs_through_the_whole_pipeline_keeping_the_raw_data():
    wells = join_layout(
        pivot_channels(parse_plate_reader(load_plate_reader_export())), load_layout()
    )

    processed = normalise_to_reference(subtract_blank(mark_usable(wells)))
    summary = summarise_replicates(
        processed.assign(percent=percent_of_vehicle(processed, "normalised")),
        "percent",
    )

    pd.testing.assert_frame_equal(processed[list(wells.columns)], wells)
    # B11 and E01 are missing and D11 is saturated, whichever well is which.
    assert processed["usable"].sum() == 93
    assert len(summary) == 12
    assert summary["n"].between(0, 4).all()
