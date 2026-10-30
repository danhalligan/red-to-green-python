"""Plotting helper for the investigation notebook."""

import numpy as np
from scipy.stats import beta


def plot_mortality_distributions(ax, posteriors: dict[str, tuple[float, float]]):
    """Draw each ``label: (a, b)`` Beta density on ``ax`` as mortality percent.

    Use it for a prior, for posteriors, or both, then add your own title.
    """
    grid = np.linspace(0.001, 0.999, 999)
    for label, (a, b) in posteriors.items():
        ax.plot(100 * grid, beta.pdf(grid, a, b) / 100, label=label)
    ax.set_xlabel("60-day mortality (%)")
    ax.set_ylabel("Probability density (per percentage point)")
    ax.legend()
    return ax
