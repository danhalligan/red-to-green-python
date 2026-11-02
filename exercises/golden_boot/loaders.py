"""Load the Premier League 2017/18 player-match table."""

from importlib.resources import files

import pandas as pd


def load_premier_league() -> pd.DataFrame:
    """Load one row per player and match for the 2017/18 Premier League.

    Columns: ``player_id``, ``player_name``, ``role`` (``FW``, ``MD``, ``DF`` or
    ``GK``), ``team``, ``match_number`` (the team's n-th match, 1 to 38),
    ``minutes``, ``goals``, ``penalty_goals``, ``non_penalty_goals`` and
    ``shots`` (non-penalty shots).
    """
    resource = files("exercises.golden_boot").joinpath(
        "data", "premier_league_2017_18.csv"
    )
    with resource.open("r", encoding="utf-8", newline="") as source:
        return pd.read_csv(source)
