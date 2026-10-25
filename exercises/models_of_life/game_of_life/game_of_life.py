"""NumPy exercises for Conway's Game of Life."""

from collections.abc import Sequence
from importlib.resources import files
from typing import TYPE_CHECKING

import numpy as np
import yaml
from numpy.typing import ArrayLike, NDArray

if TYPE_CHECKING:
    from matplotlib.animation import FuncAnimation


def count_live_neighbors(board: ArrayLike) -> NDArray:
    """Return the available live-neighbour count for every board cell.

    `board` is a 2D array of zeroes and ones. Boards are bounded, not
    wrapping: cells outside the board are not counted, so a corner cell has only
    three possible neighbours. Return an array of the same shape.
    """
    raise NotImplementedError


def step_game_of_life(board: ArrayLike) -> NDArray:
    """Return a new board after one bounded Conway's Game of Life step.

    A live cell survives with two or three live neighbours; a dead cell becomes
    live with exactly three; every other cell is dead in the next generation.
    Return a new board of the same dimensions rather than modifying `board`.
    """
    raise NotImplementedError


def load_shape(name: str) -> NDArray[np.uint8]:
    """Load a named, packaged Game of Life pattern as a binary array."""
    resource = files("exercises.models_of_life.game_of_life").joinpath(
        "data", "game_of_life_shapes.yaml"
    )
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


def place_shape(
    name: str, shape: tuple[int, int], *, top: int = 1, left: int = 1
) -> NDArray[np.uint8]:
    """Return an empty board of `shape` with a named pattern placed on it.

    The pattern's top-left corner goes at row `top`, column `left`. Raise
    ValueError if the pattern does not fit on the board.
    """
    pattern = load_shape(name)
    rows, columns = pattern.shape
    if top < 0 or left < 0 or top + rows > shape[0] or left + columns > shape[1]:
        raise ValueError(f"pattern {name!r} does not fit on a {shape} board")
    board = np.zeros(shape, dtype=np.uint8)
    board[top : top + rows, left : left + columns] = pattern
    return board


def animate_boards(
    boards: Sequence[ArrayLike], *, interval: int = 100
) -> "FuncAnimation":
    """Return an animation of successive boards, `interval` milliseconds apart.

    In a notebook, show it with `HTML(animate_boards(frames).to_jshtml())`, using
    `HTML` from `IPython.display`. Needs matplotlib.
    """
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    frames = [np.asarray(board) for board in boards]
    figure, axes = plt.subplots(
        figsize=(8, 8 * frames[0].shape[0] / frames[0].shape[1])
    )
    image = axes.imshow(frames[0], cmap="binary", vmin=0, vmax=1)
    axes.set_xticks([])
    axes.set_yticks([])
    title = axes.set_title("Generation 0")

    def draw(generation: int):
        image.set_data(frames[generation])
        title.set_text(f"Generation {generation}")
        return image, title

    plt.close(figure)  # Show only the animation, not a static copy of the figure.
    return FuncAnimation(figure, draw, frames=len(frames), interval=interval)
