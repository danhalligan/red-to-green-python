"""Beyond reasonable doubt: Bayesian inference for a two-arm clinical trial."""


def update_posterior(
    deaths: int, total: int, alpha: float = 1.0, beta: float = 1.0
) -> tuple[float, float]:
    """Update a Beta(alpha, beta) prior for a death probability with trial data.

    ``deaths`` of ``total`` patients died. Return ``(a, b)``, the parameters of
    the Beta posterior, so that ``scipy.stats.beta(*result)`` is the posterior
    distribution. Use the conjugate update; there is nothing to optimise.

    Raise ``ValueError`` if the counts are not whole numbers with
    ``0 <= deaths <= total``, or if ``alpha`` or ``beta`` is not a finite
    positive number.
    """
    raise NotImplementedError


def probability_of_benefit(
    ecmo_posterior: tuple[float, float],
    control_posterior: tuple[float, float],
    threshold: float = 0.0,
) -> float:
    """Return P(p_control - p_ecmo > threshold) under independent Beta posteriors.

    Each posterior is an ``(a, b)`` pair of Beta parameters, such as the result
    of ``update_posterior``. Mortality probabilities are on a 0 to 1 scale, so
    ``threshold`` is an absolute reduction: 0.05 means five percentage points.
    Positive differences favour the first argument, whose mortality is lower.

    Use deterministic numerical integration, not simulation. Raise
    ``ValueError`` if ``threshold`` is outside 0 to 1 or a posterior parameter
    is not positive.
    """
    raise NotImplementedError
