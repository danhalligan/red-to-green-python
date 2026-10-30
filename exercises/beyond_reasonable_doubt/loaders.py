"""Load the trial counts as a DataFrame."""

from importlib.resources import files

import pandas as pd


def load_trial_results() -> pd.DataFrame:
    """Load the 60-day mortality counts: one row per randomised group."""
    resource = files("exercises.beyond_reasonable_doubt").joinpath(
        "data", "eolia_60_day_mortality.csv"
    )
    with resource.open("r", encoding="utf-8", newline="") as source:
        return pd.read_csv(source)
