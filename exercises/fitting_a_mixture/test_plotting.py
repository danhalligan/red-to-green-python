import numpy as np
import pytest

from exercises.fitting_a_mixture.multivariate_mixture import MixtureParameters
from exercises.fitting_a_mixture.plotting import (
    animate_faithful_mixtures,
    plot_faithful_mixture,
)

pytestmark = pytest.mark.advanced

FAITHFUL_START = MixtureParameters(
    np.array([2.8, 75.0]),
    np.array([[0.8, 7.0], [7.0, 70.0]]),
    np.array([3.6, 58.0]),
    np.array([[0.8, 7.0], [7.0, 70.0]]),
    0.5,
)


@pytest.fixture
def probabilities(monkeypatch):
    """Stand in for the learner's E-step with fixed random probabilities."""
    values = np.random.default_rng(1).uniform(size=272)
    monkeypatch.setattr(
        "exercises.fitting_a_mixture.multivariate_mixture.expectation_step",
        lambda observations, parameters: values,
    )
    return values


def test_plot_faithful_mixture_colours_points_by_most_likely_component(
    probabilities,
):
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")

    axes = plot_faithful_mixture(FAITHFUL_START, title="Fit")
    colours = axes.collections[0].get_facecolor()[:, :3]

    assert len(colours) == 272
    expected = np.array(
        [
            matplotlib.colors.to_rgb("tab:blue" if p >= 0.5 else "tab:orange")
            for p in probabilities
        ]
    )
    assert colours == pytest.approx(expected)
    assert len(axes.patches) == 4
    assert axes.get_title() == "Fit"


def test_plot_faithful_mixture_without_parameters_is_a_plain_scatter_plot():
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")

    axes = plot_faithful_mixture(title="Data")

    assert len(axes.collections[0].get_offsets()) == 272
    assert len(axes.collections[0].get_facecolor()) == 1
    assert len(axes.patches) == 0
    assert axes.get_title() == "Data"


def test_animate_faithful_mixtures_makes_one_frame_per_parameter_set(
    probabilities,
):
    matplotlib = pytest.importorskip("matplotlib")
    matplotlib.use("Agg")

    animation = animate_faithful_mixtures([FAITHFUL_START] * 3, interval=50)

    assert animation.to_jshtml().count("data:image/png;base64") == 3
