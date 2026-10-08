"""NumPy exercises for Conway's Game of Life."""

from importlib.resources import files

import numpy as np
import yaml
from numpy.typing import ArrayLike, NDArray


def count_live_neighbors(board: ArrayLike) -> NDArray:
    """Return the available live-neighbour count for every board cell."""
    raise NotImplementedError


def step_game_of_life(board: ArrayLike) -> NDArray:
    """Return a new board after one bounded Conway's Game of Life step."""
    raise NotImplementedError


def load_shape(name: str) -> NDArray[np.uint8]:
    """Load a named, packaged Game of Life pattern as a binary array."""
    resource = files("pyproblems.datasets").joinpath("game_of_life_shapes.yaml")
    with resource.open("r", encoding="utf-8") as source:
        patterns = yaml.safe_load(source)

    try:
        rows = patterns[name].splitlines()
    except (KeyError, TypeError, AttributeError) as error:
        raise ValueError(f"unknown Game of Life pattern: {name!r}") from error

    if not rows or len({len(row) for row in rows}) != 1:
        raise ValueError(f"pattern {name!r} must be a non-empty rectangle")
    if any(set(row) - {".", "O"} for row in rows):
        raise ValueError(f"pattern {name!r} may contain only '.' and 'O'")

    return np.array([[cell == "O" for cell in row] for row in rows], dtype=np.uint8)


def render_board(board: ArrayLike) -> str:
    """Render a binary board as rows of ``O`` and ``.`` characters."""
    array = np.asarray(board)
    if array.ndim != 2 or not np.isin(array, (0, 1)).all():
        raise ValueError("board must be a two-dimensional array of zeroes and ones")
    return "\n".join("".join("O" if cell else "." for cell in row) for row in array)
