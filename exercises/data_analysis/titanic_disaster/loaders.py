"""Load the Titanic passenger records."""

import csv
from importlib.resources import files


def load_titanic_data() -> list[dict[str, str | None]]:
    """Load labelled Titanic passenger records as strings, with blanks as None.

    The full titanic3 snapshot has 1,309 labelled records; PassengerId is a
    local row ID, not a Kaggle ID. Outcome-revealing boat/body fields are
    excluded. Split these records to evaluate predictions locally.
    Convert numeric columns in the analysis, leaving identifiers as strings.
    """
    resource = files("exercises.data_analysis.titanic_disaster").joinpath(
        "data", "titanic.csv"
    )
    with resource.open("r", encoding="utf-8", newline="") as source:
        return [
            {key: None if value == "" else value for key, value in row.items()}
            for row in csv.DictReader(source)
        ]
