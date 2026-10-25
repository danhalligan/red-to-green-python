"""Load packaged datasets without requiring scientific Python dependencies."""

import csv
from importlib.resources import files


def load_faithful_data() -> list[tuple[float, float]]:
    """Load Old Faithful eruption durations and waiting times from CSV."""
    resource = files("pyproblems.datasets").joinpath("faithful.csv")
    with resource.open("r", encoding="utf-8", newline="") as source:
        return [
            (float(row["eruptions"]), float(row["waiting"]))
            for row in csv.DictReader(source)
        ]
