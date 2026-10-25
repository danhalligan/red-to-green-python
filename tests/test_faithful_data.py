"""Integrity checks for the Old Faithful data."""

from exercises._shared.loaders import load_faithful_data


def test_faithful_data_has_documented_columns_and_rows():
    observations = load_faithful_data()

    assert len(observations) == 272
    assert observations[0] == (3.6, 79.0)
    assert all(len(row) == 2 for row in observations)
