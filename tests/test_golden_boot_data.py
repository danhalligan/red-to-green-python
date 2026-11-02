"""Integrity checks for the Golden Boot data."""

from importlib.resources import files

import pytest

pd = pytest.importorskip("pandas")

from exercises.golden_boot.loaders import load_premier_league  # noqa: E402

COLUMNS = [
    "player_id",
    "player_name",
    "role",
    "team",
    "match_number",
    "minutes",
    "goals",
    "penalty_goals",
    "non_penalty_goals",
    "shots",
]


@pytest.fixture(scope="module")
def matches():
    return load_premier_league()


def test_columns_and_size(matches):
    assert list(matches.columns) == COLUMNS
    assert len(matches) == 10350
    assert matches["player_id"].nunique() == 512


def test_every_team_has_38_matches_and_there_are_20_teams(matches):
    per_team = matches.groupby("team")["match_number"].nunique()

    assert len(per_team) == 20
    assert set(per_team) == {38}
    assert matches["match_number"].between(1, 38).all()


def test_season_totals_match_the_source(matches):
    assert matches["goals"].sum() == 988
    assert matches["penalty_goals"].sum() == 56
    assert matches["non_penalty_goals"].sum() == 932
    assert matches["shots"].sum() == 8798


def test_rows_are_consistent(matches):
    assert (matches["minutes"] > 0).all()
    assert matches["minutes"].max() <= 95
    scored = matches["penalty_goals"] + matches["non_penalty_goals"]
    assert (matches["goals"] == scored).all()
    assert not matches.duplicated(["player_id", "team", "match_number"]).any()
    assert set(matches["role"]) == {"FW", "MD", "DF", "GK"}


def test_forwards_are_the_expected_population(matches):
    forwards = matches[matches["role"] == "FW"].groupby("player_id")["minutes"].sum()

    assert len(forwards) == 107
    assert forwards.median() == 1081


def test_names_have_no_literal_escape_sequences(matches):
    assert not matches["player_name"].str.contains("\\\\u", regex=False).any()
    assert "S. Agüero" in set(matches["player_name"])


def test_shortlist_season_totals(matches):
    totals = matches.groupby("player_name")[["goals", "penalty_goals", "shots"]].sum()
    minutes = matches.groupby("player_name")["minutes"].sum()

    assert totals.loc["Mohamed Salah", "goals"] == 32
    assert totals.loc["S. Agüero", "goals"] == 21
    assert totals.loc["J. Vardy", ["goals", "penalty_goals"]].tolist() == [20, 5]
    assert totals.loc["H. Kane", ["goals", "shots"]].tolist() == [29, 172]
    assert minutes.loc["A. Mitrović"] == 90


def test_source_note_credits_the_authors_and_licence():
    source = (
        files("exercises.golden_boot")
        .joinpath("data", "SOURCE.md")
        .read_text(encoding="utf-8")
    )

    assert "Pappalardo" in source
    assert "CC BY 4.0" in source
    assert "s41597-019-0247-7" in source
