"""Load the Steak, Tea, and Toast poll responses."""

import csv
from importlib.resources import files


def load_steak_toast_tea() -> list[dict[str, str | None]]:
    """Load poll responses, mapping blank and ``NA`` cells to ``None``."""
    resource = files("exercises.data_analysis.steak_tea_toast").joinpath(
        "data", "steak_toast_tea.csv"
    )
    with resource.open("r", encoding="utf-8", newline="") as source:
        rows = csv.DictReader(source)
        return [
            {key: None if value in ("", "NA") else value for key, value in row.items()}
            for row in rows
        ]
