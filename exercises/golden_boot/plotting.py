"""Plotting helper for the investigation notebook."""

import numpy as np
from scipy.stats import gamma


def plot_rate_distributions(ax, posteriors: dict[str, tuple[float, float]]):
    """Draw each ``label: (shape, rate)`` Gamma density on ``ax``.

    Use it for a prior, for posteriors, or both, then add your own title. The
    horizontal axis is goals per 90 minutes.
    """
    grid = np.linspace(0, 1.5, 600)
    for label, (shape, rate) in posteriors.items():
        ax.plot(grid, gamma.pdf(grid, shape, scale=1 / rate), label=label)
    ax.set_xlabel("Goals per 90 minutes")
    ax.set_ylabel("Probability density")
    ax.legend()
    return ax
