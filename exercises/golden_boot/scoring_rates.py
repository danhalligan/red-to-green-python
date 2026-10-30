"""Golden Boot: Bayesian estimates of a goalscorer's rate per 90 minutes."""


def update_gamma(
    goals: int, nineties: float, prior_alpha: float, prior_beta: float
) -> tuple[float, float]:
    """Update a Gamma(prior_alpha, prior_beta) prior for a scoring rate.

    The rate is goals per 90 minutes. ``goals`` were scored in ``nineties``
    units of 90 minutes (270 minutes is 3.0), and the prior is a Gamma
    distribution with shape ``prior_alpha`` and *rate* ``prior_beta``. Return
    ``(shape, rate)``, the parameters of the Gamma posterior. Use the conjugate
    update; there is nothing to optimise.

    Raise ``ValueError`` if ``goals`` is not a whole number of at least 0, if
    ``nineties`` is not a finite number of at least 0, or if ``prior_alpha`` or
    ``prior_beta`` is not a finite positive number.
    """
    raise NotImplementedError


def posterior_summary(
    goals: int,
    nineties: float,
    prior_alpha: float = 6.0,
    prior_beta: float = 18.0,
) -> tuple[float, float, float]:
    """Summarise the posterior for a scoring rate, in goals per 90 minutes.

    Return ``(mean, lower, upper)``: the posterior mean and the ends of the
    central 95% credible interval. Use ``update_gamma`` for the posterior, and
    remember that SciPy's ``gamma`` takes a ``scale``, which is 1 / rate.

    The default prior has mean 6 / 18 = 1/3 of a goal per 90 minutes and is as
    informative as 18 matches. Invalid arguments raise ``ValueError``, as in
    ``update_gamma``.
    """
    raise NotImplementedError


def probability_greater(
    first: tuple[float, float],
    second: tuple[float, float],
    draws: int = 200_000,
    seed: int = 0,
) -> float:
    """Estimate P(rate_first > rate_second) from two Gamma posteriors.

    Each posterior is a ``(shape, rate)`` pair, such as the result of
    ``update_gamma``. Draw ``draws`` samples of each uncertain *rate* with
    ``numpy.random.default_rng(seed)`` and return the fraction of draws in which
    the first is larger. The draws describe our uncertainty about the rates; they
    are not simulated goals. The seed makes the answer repeatable.

    Raise ``ValueError`` if a shape or rate is not a finite positive number, or
    if ``draws`` is not a positive whole number.
    """
    raise NotImplementedError


def beta_posterior_summary(
    successes: int, trials: int, prior_alpha: float, prior_beta: float
) -> tuple[float, float, float]:
    """Summarise the posterior for a probability, such as shot conversion.

    ``successes`` of ``trials`` with a Beta(prior_alpha, prior_beta) prior gives
    a Beta(prior_alpha + successes, prior_beta + trials - successes) posterior.
    Return ``(mean, lower, upper)``: the posterior mean and the ends of the
    central 95% credible interval. This is the same idea as ``update_gamma``,
    for a probability and a count of trials instead of a rate and an exposure.

    Raise ``ValueError`` if the counts are not whole numbers with
    ``0 <= successes <= trials``, or if ``prior_alpha`` or ``prior_beta`` is not
    a finite positive number.
    """
    raise NotImplementedError
