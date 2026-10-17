# Fitting a Gaussian mixture 😱

> **Before you start:** the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **Recommended first:**
> [Recovering the parameters](recovering-the-parameters.md)
> (likelihood and numerical maximum likelihood), which this builds on.
>
> **You’ll practise:** the mixture likelihood, constrained numerical
> optimisation, and working in log space.
>
> **Check:** `uv run pytest tests/test_advanced_models.py -q`
>
> **Optional:** this direct-optimisation exercise can be skipped. The
> expectation-maximisation exercise does not depend on it.

Suppose observations come from one of two Gaussian distributed populations, but
we do not know which population produced each observation. If the first
population has weight $\pi$, the density for one observation is

$$
f(x\mid\theta) = \pi \phi(x\mid\mu_1,\sigma_1) + (1-\pi) \phi(x\mid\mu_2,\sigma_2),
$$

where $\phi$ is the Gaussian density function and
$\theta=(\mu_1,\sigma_1,\mu_2,\sigma_2,\pi)$. The likelihood is the product
of these mixture densities across observations and the log-likelihood is the
sum of the log mixture densities across observations.

In [statistics.py](../../src/pyproblems/statistics.py), implement
`gaussian_mixture_log_likelihood` and `fit_gaussian_mixture`. The likelihood
function takes named component means, positive standard deviations, a mixture
weight (strictly between zero and one), and the observations.

Use `scipy.optimize.minimize` to numerically maximise the log-likelihood across
all model parameters. Note that optimising a mixture is trickier than fitting a
single normal, so there is a 💡 hint for the optimisation, including setting a
minimum standard deviation.[^mixture-hint]

[^mixture-hint]: For unconstrained optimisation, represent each standard
    deviation as a floor plus the exponential of an unconstrained parameter, and
    represent `weight1` with the logistic transform so it stays between zero and
    one. Try several deterministic starting points, keep the best successful
    result, and report the component with the smaller mean first. Mixture
    fitting can have local optima, so do not rely on one arbitrary start. Derive
    the starting points from the location and spread of the data, so shifted or
    rescaled observations give correspondingly shifted or rescaled fits.

    There is one catch: the likelihood has no true maximum. If you centre one
    component on a single observation and shrink its standard deviation towards
    zero, its density at that point grows without bound (a very narrow normal
    curve is very tall), while the other component still explains the remaining
    points. An optimiser can therefore chase this spike forever. To stop that,
    keep each standard deviation at or above a floor of `1e-3` times the sample
    standard deviation of the observations, so the fit is always finite. The
    likelihood function itself should still accept any positive standard
    deviation.
