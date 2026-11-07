"""Supplied plotting helpers for the Old Faithful mixture. Nothing to write here."""

from collections.abc import Sequence
from typing import TYPE_CHECKING

import numpy as np

from exercises.fitting_a_mixture import multivariate_mixture
from exercises.fitting_a_mixture.loaders import load_faithful_data
from exercises.fitting_a_mixture.multivariate_mixture import MixtureParameters

if TYPE_CHECKING:
    from matplotlib.animation import FuncAnimation
    from matplotlib.axes import Axes

_COMPONENT_COLOURS = ("tab:blue", "tab:orange")


def _draw_faithful_mixture(
    axes: "Axes", parameters: MixtureParameters | None, title: str
) -> None:
    from matplotlib.patches import Ellipse

    observations = np.array(load_faithful_data())
    axes.set_xlabel("Eruption duration (minutes)")
    axes.set_ylabel("Waiting time (minutes)")
    axes.set_title(title)

    if parameters is None:
        axes.scatter(
            observations[:, 0], observations[:, 1], color="tab:gray", s=20, alpha=0.8
        )
        return

    means = (np.asarray(parameters.mean1), np.asarray(parameters.mean2))
    covariances = (
        np.asarray(parameters.covariance1),
        np.asarray(parameters.covariance2),
    )

    # Colour each point by its more likely component, as in a hard E-step.
    assignment = np.where(
        multivariate_mixture.expectation_step(observations, parameters) >= 0.5, 0, 1
    )

    axes.scatter(
        observations[:, 0],
        observations[:, 1],
        c=[_COMPONENT_COLOURS[index] for index in assignment],
        s=20,
        alpha=0.8,
    )
    for mean, covariance, colour in zip(
        means, covariances, _COMPONENT_COLOURS, strict=True
    ):
        values, vectors = np.linalg.eigh(covariance)
        angle = np.degrees(np.arctan2(vectors[1, -1], vectors[0, -1]))
        for radius in (1, 2):
            axes.add_patch(
                Ellipse(
                    mean,
                    2 * radius * np.sqrt(values[-1]),
                    2 * radius * np.sqrt(values[0]),
                    angle=angle,
                    fill=False,
                    edgecolor=colour,
                    linewidth=2 if radius == 1 else 1,
                )
            )
        axes.plot(*mean, marker="x", color=colour, markersize=10, markeredgewidth=2)


def plot_faithful_mixture(
    parameters: MixtureParameters | None = None,
    *,
    axes: "Axes | None" = None,
    title: str = "",
) -> "Axes":
    """Plot the Old Faithful data, optionally with a two-component mixture.

    With no `parameters` this is a plain scatter plot of the data. Given
    parameters, each eruption is coloured by the component that is most likely
    to have produced it, using your `multivariate_mixture.expectation_step`,
    and each component is drawn in its own colour, with its mean and ellipses
    one and two standard deviations from the mean. Plots on `axes` if given,
    otherwise on a new figure, and returns the axes. Needs matplotlib.
    """
    import matplotlib.pyplot as plt

    if axes is None:
        _, axes = plt.subplots(figsize=(8, 6))
    _draw_faithful_mixture(axes, parameters, title)
    return axes


def animate_faithful_mixtures(
    history: Sequence[MixtureParameters],
    *,
    interval: int = 200,
) -> "FuncAnimation":
    """Return an animation of successive mixtures, `interval` milliseconds apart.

    `history` holds the parameters after each EM iteration, starting with the
    initial values; `list(islice(em_steps(...), n))` makes one. In a notebook,
    show it with
    `HTML(animate_faithful_mixtures(history).to_jshtml())`, using `HTML` from
    `IPython.display`. Needs matplotlib.
    """
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation

    figure, axes = plt.subplots(figsize=(8, 6))

    def draw(iteration: int):
        axes.clear()
        _draw_faithful_mixture(axes, history[iteration], f"Iteration {iteration}")
        axes.set_xlim(1, 6)
        axes.set_ylim(35, 105)

    plt.close(figure)  # Show only the animation, not a static copy of the figure.
    return FuncAnimation(figure, draw, frames=len(history), interval=interval)
