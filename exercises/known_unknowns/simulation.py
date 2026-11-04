"""Helpers for the investigation: run a coverage study and plot its results."""

from collections.abc import Callable, Mapping

import numpy as np
import pandas as pd

# Two populations whose true mean is 1.0. Their true medians differ.
POPULATIONS: dict[str, Callable[[np.random.Generator, int], np.ndarray]] = {
    "normal": lambda rng, n: rng.normal(1.0, 1.0, size=n),
    "exponential": lambda rng, n: rng.exponential(1.0, size=n),
}


def coverage_study(
    methods: Callable[[np.ndarray], Mapping[str, tuple[float, float]]],
    truth: Mapping[str, float],
    *,
    rng: np.random.Generator,
    sizes: tuple[int, ...] = (5, 10, 30, 100),
    repetitions: int = 1000,
) -> pd.DataFrame:
    """Measure how often each interval method contains the true value.

    ``methods(sample)`` takes one sample and returns a dictionary that maps each
    method's name to its interval, ``(low, high)``. ``truth`` maps each
    population name in ``POPULATIONS`` to the true value being estimated. Every
    sample and every random choice in ``methods`` should use the same ``rng``,
    so that a seeded generator makes the study reproducible.

    Returns one row for every population, sample size and method, with its
    ``coverage``, the Monte Carlo standard error ``mc_se`` of that coverage, and
    the ``mean_width`` of its intervals.
    """
    rows = []
    for population, draw in POPULATIONS.items():
        for n in sizes:
            intervals = [methods(draw(rng, n)) for _ in range(repetitions)]
            for method in intervals[0]:
                lows, highs = np.array([found[method] for found in intervals]).T
                coverage = np.mean(
                    (lows <= truth[population]) & (truth[population] <= highs)
                )
                rows.append(
                    {
                        "population": population,
                        "n": n,
                        "method": method,
                        "coverage": coverage,
                        "mc_se": np.sqrt(coverage * (1 - coverage) / repetitions),
                        "mean_width": np.mean(highs - lows),
                    }
                )
    return pd.DataFrame(rows)


def plot_coverage(table: pd.DataFrame) -> None:
    """Plot coverage against sample size, with a panel for each population.

    ``table`` is the result of ``coverage_study``. The error bars are 95% Monte
    Carlo intervals, and the dashed line marks the nominal 95% coverage.
    """
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, (population, group) in zip(axes, table.groupby("population"), strict=True):
        for method, line in group.groupby("method"):
            ax.errorbar(
                line["n"],
                line["coverage"],
                1.96 * line["mc_se"],
                marker="o",
                label=method,
            )
        ax.axhline(0.95, color="grey", linestyle="--")
        ax.set_xscale("log")
        ax.set_xlabel("Sample size n")
        ax.set_title(population)
    axes[0].set_ylabel("Coverage of nominal 95% interval")
    axes[0].legend()
    fig.tight_layout()
