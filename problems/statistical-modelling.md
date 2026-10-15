# Statistical Modelling

[← All problems](../README.md)

## Gaussian-mixture 😱

> **Prerequisites:** [Scientific Python](scientific-python.md) Q5 (likelihood and numerical maximum
> likelihood).
>
> **You’ll practise:** the mixture likelihood, constrained numerical
> optimisation, and working in log space.
>
> **Check:** `uv run pytest tests/test_advanced_models.py -q`
>
> **Optional:** this direct-optimisation exercise can be skipped. The
> expectation-maximisation section that follows does not depend on it.

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

In [statistics.py](../src/pyproblems/statistics.py), implement
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

## Gaussian-mixture EM 😱

> **Prerequisites:** [Scientific Python](scientific-python.md) Q5 (likelihood and maximum likelihood),
> and the optional scientific stack.
>
> **You’ll practise:** expectation-maximisation, hard and soft assignment,
> weighted estimates, and fitting a bivariate mixture to real data.
>
> **Check:** `uv run pytest tests/test_mixture_models.py -m advanced -q`

Recall from the likelihood question in [Scientific Python](scientific-python.md) that the ML estimates
of a normal distribution are simply the sample mean and the *population*
standard deviation.  However, when we do not know which distribution each
observation came from, we can't easily use this analytical result. Although the
approach of numerically optimising over all parameters works (as shown above),
it is slow and impractical, particularly if we consider mixtures of more
distributions!

A much more efficient approach is
[Expectation-Maximisation](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)
(EM), which treats this as a *missing data* problem. We introduce a set of
unknown labels which tell us which distribution each observation came from. 
This is useful because, with the labels, estimation becomes easy again:
the ML estimates for each distribution are just its mean and population standard
deviation, with no optimisation.

The EM approach when the labels are missing is:

1. Guess the parameter values.
2. Use the parameter values to infer likely labels (the E-step).
3. Use the labels to obtain ML estimates of the parameters of each distribution
   in the mixture, and of the relative contribution of each (the M-step).
4. Iterate steps 2 and 3 until convergence.

Under iteration, EM typically converges to a local optimum, which we hope is the
global optimum and therefore gives the ML estimates.

### E-step

How do we infer the labels? We can simply assign each observation to the
component it is most likely to have come from. Assigning labels this way is
called "hard" EM, because the labels are categorical.

Work in [mixture_models.py](../src/pyproblems/mixture_models.py), where the
mixture parameters are held in a `GaussianMixtureParameters` object. Write
`hard_expectation_step(observations, parameters)`, which says whether each
observation is more likely to have come from component one, by comparing the
weighted densities $\pi\,\phi(x\mid\mu_1,\sigma_1)$ and
$(1-\pi)\,\phi(x\mid\mu_2,\sigma_2)$.

### M-step

Using these (imperfect) labels we can update our estimated parameters by maximum
likelihood: the mean and population standard deviation within each group, and
the fraction of observations in component one. Write
`hard_maximization_step(observations, labels)`.

### Iteration

Write `expectation_maximization`, which iterates a supplied E-step and M-step
until the log-likelihood stops changing, and `mixture_log_likelihood`, which
calculates the log-likelihood of a mixture as in the previous section. Stop on
the *absolute* change in log-likelihood.[^abs-change] The docstrings give the
exact signatures, stopping rule and return values, and the tests check them.

[^abs-change]: Hard EM optimises a different objective, so its log-likelihood
    can fall from one iteration to the next, whereas soft EM never decreases it
    (apart from rounding). A large decrease is therefore not convergence.

Then write `fit_hard_gaussian_mixture`, which calls `expectation_maximization`
using the hard steps. Check that it gives a reasonable fit to some sample data,
for example:

```python
rng = np.random.default_rng(42)
x = np.concatenate((rng.normal(-3, 2, 100), rng.normal(3, 1, 200)))
initial = GaussianMixtureParameters(0, 2, 1, 2, 0.3)
fitted = fit_hard_gaussian_mixture(x, initial)
```

Plot a histogram of `x` with the fitted mixture density over the top. The data
came from a normal with mean -3 and standard deviation 2 (weight 1/3) and one
with mean 3 and standard deviation 1 (weight 2/3), so the fit should be close.

### Soft EM

An alternative is to use the relative *probability* that an observation belongs
to each component, which is termed a "soft" EM algorithm. It is a slight tweak
to the approach above: instead of assigning each observation to its most
probable component, we *weight* its contribution to our ML estimates by the
probability that it came from that component. The more certain we are that an
observation belongs to component one, the more it contributes to the estimates
for component one.

For a univariate two-component mixture, let $r_i$ be the probability that
observation $x_i$ belongs to component one. The soft E-step computes

$$
r_i = \frac{\pi\,\phi(x_i\mid\mu_1,\sigma_1)}
{\pi\,\phi(x_i\mid\mu_1,\sigma_1)+(1-\pi)\,\phi(x_i\mid\mu_2,\sigma_2)}.
$$

In the M-step, the component-one updates are weighted versions of the usual
estimates: $\mu_1=\sum_i r_i x_i/\sum_i r_i$ and
$\sigma_1^2=\sum_i r_i(x_i-\mu_1)^2/\sum_i r_i$. Component two uses weights
$1-r_i$, and $\pi$ is the average of the $r_i$ values.

Write `soft_expectation_step`, `soft_maximization_step` and
`fit_soft_gaussian_mixture`, and check the fit on the same sample data.
The docstrings give the details.

### Multivariate Gaussian EM

The eruptions at the Old Faithful geyser are actually very predictable, with
either short eruptions that occur relatively quickly after the previous
eruption, or longer waits leading to bigger eruptions. This motivates modelling
the data as a mixture of two bivariate normal distributions, where the variables
are the eruption duration and the waiting time to the next eruption (both in
minutes). `load_faithful_data()` in [data.py](../src/pyproblems/data.py) provides
them as (duration, waiting) pairs, and the [Old Faithful
notebook](../analysis/old_faithful.ipynb) describes the data in more detail.

Each standard deviation is now replaced by a covariance matrix, held in a
`MultivariateGaussianMixtureParameters` object. In
[mixture_models.py](../src/pyproblems/mixture_models.py), write multivariate
counterparts of the soft-EM functions:
`multivariate_mixture_log_likelihood`,
`multivariate_soft_expectation_step`, `multivariate_soft_maximization_step` and
`fit_multivariate_gaussian_mixture`. Finally, write
`fit_faithful_gaussian_mixture(initial_parameters)`, which fits the packaged Old
Faithful data.

Compare your fitted log-likelihood with the reference value in the tests (about
-1130.27). The [Old Faithful notebook](../analysis/old_faithful.ipynb) gives rough
starting values and asks you to plot the fit. EM is not guaranteed to find the
global maximum from every starting point.

This is the same dataset as the earlier regression exercise: the clusters should
help explain why a single straight line described it poorly. The notebook also
suggests an extension that revisits the prediction using the clusters.
