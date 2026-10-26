"""Load the two Penguin parade files as DataFrames."""

from importlib.resources import files

import pandas as pd


def load_field_observations() -> pd.DataFrame:
    """Load the field team's measurements: one row per sampled penguin."""
    resource = files("exercises.penguin_parade").joinpath(
        "data", "field_observations.csv"
    )
    with resource.open("r", encoding="utf-8", newline="") as source:
        return pd.read_csv(source)


def load_isotope_results() -> pd.DataFrame:
    """Load the laboratory's blood-isotope results."""
    resource = files("exercises.penguin_parade").joinpath("data", "isotope_results.csv")
    with resource.open("r", encoding="utf-8", newline="") as source:
        return pd.read_csv(source)
