"""Expectation-maximisation exercises for Gaussian mixture models."""

from collections.abc import Callable, Iterator, Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

import numpy as np
from numpy.typing import ArrayLike, NDArray

if TYPE_CHECKING:
    from matplotlib.animation import FuncAnimation
    from matplotlib.axes import Axes


@dataclass(frozen=True)
class GaussianMixtureParameters:
    """Parameters for a two-component univariate Gaussian mixture.

    `weight1` is the probability that an observation comes from component one.
    """

    mean1: float
    standard_deviation1: float
    mean2: float
    standard_deviation2: float
    weight1: float


@dataclass(frozen=True)
class MultivariateGaussianMixtureParameters:
    """Parameters for a two-component multivariate Gaussian mixture.

    Each mean is a vector (for Old Faithful, duration and waiting time) and
    each covariance is a square matrix. `weight1` is the probability of
    component one.
    """

    mean1: NDArray
    covariance1: NDArray
    mean2: NDArray
    covariance2: NDArray
    weight1: float


ParametersT = TypeVar("ParametersT")
LatentT = TypeVar("LatentT")


@dataclass(frozen=True)
class EMResult(Generic[ParametersT]):
    """Parameters and likelihood from an EM run."""

    parameters: ParametersT
    log_likelihood: float
    iterations: int
    converged: bool


def gaussian_mixture_log_likelihood(
    mean1: float,
    standard_deviation1: float,
    mean2: float,
    standard_deviation2: float,
    weight1: float,
    observations: ArrayLike,
) -> float:
    """Calculate the log-likelihood for a two-normal mixture."""
    raise NotImplementedError


def hard_expectation_step(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> NDArray:
    """Assign each observation to its more likely component (hard E-step).

    Compare the weighted densities `weight1 * phi(x | mean1, sd1)` and
    `(1 - weight1) * phi(x | mean2, sd2)`. Break ties in favour of component
    one.

    Returns a Boolean array, the same length as `observations`, that is True
    where component one is more likely.
    """
    raise NotImplementedError


def hard_maximization_step(
    observations: ArrayLike, labels: ArrayLike
) -> GaussianMixtureParameters:
    """Estimate mixture parameters from hard component labels (hard M-step).

    `labels` is a Boolean array, True for component one. For each group, use
    the mean and *population* standard deviation (`ddof=0`) of its
    observations. `weight1` is the fraction of observations labelled as
    component one.

    Raises ValueError, rather than returning invalid parameters, if a group is
    empty or has zero variance.
    """
    raise NotImplementedError


def soft_expectation_step(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> NDArray:
    """Return each observation's posterior probability for component one.

    For observation x_i this is
    `weight1 * phi(x_i | mean1, sd1) / (weight1 * phi(x_i | mean1, sd1) +
    (1 - weight1) * phi(x_i | mean2, sd2))`.

    Work in log space so that observations far from both components give
    finite results. Returns a float array the same length as `observations`.
    """
    raise NotImplementedError


def soft_maximization_step(
    observations: ArrayLike, weights: ArrayLike
) -> GaussianMixtureParameters:
    """Estimate mixture parameters using fractional component weights.

    `weights` holds the probability r_i that each observation belongs to
    component one; component two uses `1 - r_i`. Each component's mean and
    *population* standard deviation (`ddof=0`) are weighted by these values,
    and `weight1` is the mean of `weights`. `numpy.average(..., weights=...)`
    gives the weighted mean, but the weighted standard deviation is up to you.

    Raises ValueError if a component has no weight or zero variance.
    """
    raise NotImplementedError


def mixture_log_likelihood(
    observations: ArrayLike, parameters: GaussianMixtureParameters
) -> float:
    """Calculate a two-component Gaussian mixture log-likelihood.

    This is the sum over observations of the log of the weighted sum of the two
    component densities. Compute it in log space (for example with
    `scipy.special.logsumexp`) so that a point far from both components still
    gives a finite value.
    """
    raise NotImplementedError


def em_steps(
    observations: ArrayLike,
    initial_parameters: ParametersT,
    expectation_step: Callable[[ArrayLike, ParametersT], LatentT],
    maximization_step: Callable[[ArrayLike, LatentT], ParametersT],
) -> Iterator[ParametersT]:
    """Yield the parameters after each EM iteration, starting with the initial ones.

    The first value yielded is `initial_parameters` itself. Each later value
    comes from one more iteration: call `expectation_step(observations,
    parameters)` on the latest parameters, then `maximization_step(observations,
    latent)` on its result, where `latent` is whatever the E-step returned.

    The generator is endless and lazy. It does no work until it is asked for the
    next value and never decides when to stop, so take what you need with `next`
    or `itertools.islice`. It cannot know what the parameters represent, so it
    works for any model with an E-step and an M-step.
    """
    raise NotImplementedError


def expectation_maximization(
    observations: ArrayLike,
    initial_parameters: ParametersT,
    expectation_step: Callable[[ArrayLike, ParametersT], LatentT],
    maximization_step: Callable[[ArrayLike, LatentT], ParametersT],
    log_likelihood: Callable[[ArrayLike, ParametersT], float],
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[ParametersT]:
    """Iterate supplied E- and M-steps until likelihood convergence.

    `expectation_step(observations, parameters)` returns labels or weights,
    `maximization_step(observations, those)` returns new parameters, and
    `log_likelihood(observations, parameters)` returns a float. Use `em_steps`
    for the iterations, and decide here when to stop.

    One iteration is one E-step followed by one M-step. Stop when the absolute
    change in log-likelihood between consecutive iterations is below
    `tolerance`, or when `max_iterations` is reached. Use the absolute change:
    hard EM optimises a different objective, so its log-likelihood can fall
    from one iteration to the next, and a large decrease is not convergence.
    Judge convergence only after an update, so `max_iterations=0` returns the
    initial parameters and log-likelihood, unconverged.

    Returns an `EMResult` with the fitted `parameters`,
    their `log_likelihood`, the number of `iterations` and whether it
    `converged`. Nothing here depends on what the parameters are.
    """
    raise NotImplementedError


def fit_hard_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: GaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[GaussianMixtureParameters]:
    """Fit a univariate mixture with hard expectation-maximisation.

    Call `expectation_maximization` with the hard E- and M-steps and
    `mixture_log_likelihood`.
    """
    raise NotImplementedError


def fit_soft_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: GaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[GaussianMixtureParameters]:
    """Fit a univariate mixture with soft expectation-maximisation.

    Call `expectation_maximization` with the soft E- and M-steps and
    `mixture_log_likelihood`.
    """
    raise NotImplementedError


def multivariate_mixture_log_likelihood(
    observations: ArrayLike,
    parameters: MultivariateGaussianMixtureParameters,
) -> float:
    """Calculate the log-likelihood for a multivariate Gaussian mixture.

    `observations` is an n by 2 array. The log-density of each component is
    available from `scipy.stats.multivariate_normal(...).logpdf`. Combine them
    in log space, as for the univariate case.
    """
    raise NotImplementedError


def multivariate_soft_expectation_step(
    observations: ArrayLike,
    parameters: MultivariateGaussianMixtureParameters,
) -> NDArray:
    """Return posterior component-one probabilities for multivariate data.

    The multivariate counterpart of `soft_expectation_step`, for an n by 2
    array of observations. Work in log space so the result stays finite far
    from both components.
    """
    raise NotImplementedError


def multivariate_soft_maximization_step(
    observations: ArrayLike,
    weights: ArrayLike,
) -> MultivariateGaussianMixtureParameters:
    """Estimate multivariate parameters using fractional component weights.

    The multivariate counterpart of `soft_maximization_step`. Use weighted
    means and weighted *population* covariance matrices; `numpy.cov` accepts
    `aweights`, and `ddof=0` gives the population version. `weight1` is the
    mean of `weights`.

    Raises ValueError if a covariance matrix is singular.
    """
    raise NotImplementedError


def fit_multivariate_gaussian_mixture(
    observations: ArrayLike,
    initial_parameters: MultivariateGaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[MultivariateGaussianMixtureParameters]:
    """Fit a multivariate Gaussian mixture using soft EM.

    Reuse `expectation_maximization` with the multivariate soft E- and M-steps
    and `multivariate_mixture_log_likelihood`: the loop itself should not need
    to change. The components keep the labels of `initial_parameters`.
    """
    raise NotImplementedError


def fit_faithful_gaussian_mixture(
    initial_parameters: MultivariateGaussianMixtureParameters,
    *,
    tolerance: float = 1e-10,
    max_iterations: int = 1000,
) -> EMResult[MultivariateGaussianMixtureParameters]:
    """Fit the multivariate mixture to the packaged Old Faithful data.

    Use `load_faithful_data()` from `exercises._shared.loaders` to get the (duration,
    waiting) observations, then call `fit_multivariate_gaussian_mixture`.
    """
    raise NotImplementedError


_COMPONENT_COLOURS = ("tab:blue", "tab:orange")


def _draw_faithful_mixture(
    axes: "Axes", parameters: MultivariateGaussianMixtureParameters, title: str
) -> None:
    from matplotlib.patches import Ellipse

    from exercises._shared.loaders import load_faithful_data

    observations = np.array(load_faithful_data())
    means = (np.asarray(parameters.mean1), np.asarray(parameters.mean2))
    covariances = (
        np.asarray(parameters.covariance1),
        np.asarray(parameters.covariance2),
    )

    # Colour each point by its more likely component, as in a hard E-step.
    assignment = np.where(
        multivariate_soft_expectation_step(observations, parameters) >= 0.5, 0, 1
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

    axes.set_xlabel("Eruption duration (minutes)")
    axes.set_ylabel("Waiting time (minutes)")
    axes.set_title(title)


def plot_faithful_mixture(
    parameters: MultivariateGaussianMixtureParameters,
    *,
    axes: "Axes | None" = None,
    title: str = "",
) -> "Axes":
    """Plot the Old Faithful data with a two-component bivariate mixture.

    Each eruption is coloured by the component that is most likely to have
    produced it, using your `multivariate_soft_expectation_step`. Each component
    is drawn in its own colour, with its mean and ellipses one and two standard
    deviations from the mean. Plots on `axes` if given, otherwise on a new
    figure, and returns the axes. Needs matplotlib.
    """
    import matplotlib.pyplot as plt

    if axes is None:
        _, axes = plt.subplots(figsize=(8, 6))
    _draw_faithful_mixture(axes, parameters, title)
    return axes


def animate_faithful_mixtures(
    history: Sequence[MultivariateGaussianMixtureParameters],
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
