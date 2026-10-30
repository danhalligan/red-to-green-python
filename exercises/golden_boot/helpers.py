"""Supplied helpers for the investigation notebook."""

import numpy as np
from scipy.stats import beta


def probability_greater(
    first: tuple[float, float],
    second: tuple[float, float],
    draws: int = 200_000,
    seed: int = 0,
) -> float:
    """Estimate P(rate_first > rate_second) from two Gamma posteriors.

    Each posterior is a ``(shape, rate)`` pair, such as the result of
    ``update_gamma``. The estimate comes from simulating the two *uncertain
    rates*, not from simulating matches, and the seed makes it repeatable.
    """
    rng = np.random.default_rng(seed)
    first_rate = rng.gamma(first[0], 1 / first[1], draws)
    second_rate = rng.gamma(second[0], 1 / second[1], draws)
    return float(np.mean(first_rate > second_rate))


def beta_posterior_summary(
    successes: int, trials: int, prior_alpha: float, prior_beta: float
) -> tuple[float, float, float]:
    """Posterior mean and central 95% interval for a probability.

    ``successes`` of ``trials`` with a Beta(prior_alpha, prior_beta) prior. This
    is the Beta-binomial update, used by the optional extension for the
    probability that a shot becomes a goal.
    """
    a = prior_alpha + successes
    b = prior_beta + trials - successes
    lower, upper = beta.ppf([0.025, 0.975], a, b)
    return float(beta.mean(a, b)), float(lower), float(upper)
