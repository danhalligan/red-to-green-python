"""Load the mystery datasets."""

import json
from importlib.resources import files
from typing import TypedDict, cast


class XYDataset(TypedDict):
    x: list[float]
    y: list[float]


def load_xy_data() -> dict[str, XYDataset]:
    """Load the named mystery datasets as parallel ``x`` and ``y`` lists."""
    resource = files("exercises.mysterious_data").joinpath("data", "xy.json")
    with resource.open("r", encoding="utf-8") as source:
        return cast(dict[str, XYDataset], json.load(source))
