"""Integrity checks for the Steak, Tea, and Toast poll data."""

from exercises.data_analysis.steak_tea_toast.loaders import load_steak_toast_tea


def test_steak_toast_tea_preserves_rows_invalid_values_and_missingness():
    responses = load_steak_toast_tea()

    assert len(responses) == 79
    assert list(responses[0]) == ["Steak", "Toast", "Tea"]
    assert sum(row["Steak"] is None for row in responses) == 1
    assert sum(row["Toast"] is None for row in responses) == 0
    assert sum(row["Tea"] is None for row in responses) == 6
    assert sum(row["Steak"] == "0" for row in responses) == 1


def test_steak_toast_tea_preserves_out_of_scale_responses():
    responses = load_steak_toast_tea()
    displayed = {
        "Steak": set("12345"),
        "Toast": set("123456"),
        "Tea": set("abcdef"),
    }
    out_of_scale = {
        column: sorted(
            row[column]
            for row in responses
            if row[column] is not None and row[column] not in displayed[column]
        )
        for column in displayed
    }

    assert out_of_scale == {"Steak": ["0", "1.5", "2.5"], "Toast": ["3.5"], "Tea": []}

    # Treating every response outside the displayed choices as missing.
    missing = {
        column: sum(row[column] not in displayed[column] for row in responses)
        for column in displayed
    }
    assert missing == {"Steak": 4, "Toast": 1, "Tea": 6}
    assert (
        sum(
            row["Steak"] in displayed["Steak"] and row["Toast"] in displayed["Toast"]
            for row in responses
        )
        == 75
    )
    assert (
        sum(
            row["Toast"] in displayed["Toast"] and row["Tea"] in displayed["Tea"]
            for row in responses
        )
        == 72
    )
