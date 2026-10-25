"""Load datasets shared by several exercises."""

import csv
from importlib.resources import files


def load_faithful_data() -> list[tuple[float, float]]:
    """Load Old Faithful eruption durations and waiting times from CSV."""
    resource = files("exercises._shared").joinpath("data", "faithful.csv")
    with resource.open("r", encoding="utf-8", newline="") as source:
        return [
            (float(row["eruptions"]), float(row["waiting"]))
            for row in csv.DictReader(source)
        ]


def load_words() -> set[str]:
    """Load the packaged English word list (derived from SCOWL) as lowercase words."""
    resource = files("exercises._shared").joinpath("data", "words.txt")
    with resource.open("r", encoding="utf-8") as source:
        return {line.strip() for line in source if line.strip()}
