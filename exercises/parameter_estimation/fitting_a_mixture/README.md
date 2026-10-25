# Fitting a mixture

> **Difficulty:** 🌶️🌶️🌶️
>
> **Before you start:** the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **Recommended first:**
> [Recovering the parameters](../recovering_the_parameters/README.md)
> (likelihood and maximum likelihood). The final part introduces Old Faithful
> with a short regression diagnostic before fitting a mixture.
>
> **You’ll practise:** the mixture likelihood, working in log space, hidden
> labels, expectation-maximisation (EM), hard and soft assignment, weighted
> estimates, and fitting a bivariate mixture to real data.
>
> **Check:** `uv run pytest exercises/parameter_estimation/fitting_a_mixture/test_mixture_models.py -k gaussian_mixture_log_likelihood -q`
> for the likelihood, then `uv run pytest exercises/parameter_estimation/fitting_a_mixture/test_mixture_models.py -m advanced -q`
> for EM.

Suppose observations come from one of two Gaussian distributed populations, but
we do not know which population produced each observation. If the first
population has weight $\pi$, the density for one observation is

$$
f(x\mid\theta) = \pi \phi(x\mid\mu_1,\sigma_1) + (1-\pi) \phi(x\mid\mu_2,\sigma_2),
$$

where $\phi$ is the Gaussian density function and
$\theta=(\mu_1,\sigma_1,\mu_2,\sigma_2,\pi)$. How can we estimate $\theta$ from
the observations alone?

Recall from the likelihood question in
[Recovering the parameters](../recovering_the_parameters/README.md)
that the ML estimates of a normal distribution are simply the sample mean and
the *population* standard deviation. For a mixture, the sum inside the
logarithm of the log-likelihood means there is no such closed form.

## Calculating the log-likelihood

In [mixture_models.py](mixture_models.py), implement
`gaussian_mixture_log_likelihood`. It takes named component means, positive
standard deviations, a mixture weight (strictly between zero and one), and the
observations. Remember, the likelihood is the product of mixture densities
across observations and the log-likelihood is the sum of the log mixture
densities across observations. Work in log space so that observations far in
the tails do not underflow.

## Finding the maximum

We could maximise this log-likelihood over all five parameters numerically
(equivalent to our approach in
[Recovering the parameters](../recovering_the_parameters/README.md)). That can work, but
it is tricky: the parameters are constrained, there are local optima, and the
likelihood is unbounded if a component collapses onto a single observation. To
see the last point, evaluate your function with `mean1` equal to one of the
observations and a shrinking `standard_deviation1`. The difficulties grow with
every extra component.

There is a neat way round this. Imagine each observation came with a *hidden
label* saying which population produced it. With the labels, estimation becomes
easy again: the ML estimates for each population are just the mean and
population standard deviation of its own observations, and the weight is the
fraction of observations with each label. No optimisation is needed.

We do not have the labels, but we can *guess* them from our current parameter
estimates, and then use the guessed labels to improve the estimates. Treating
the labels as missing data in this way is called
[Expectation-Maximisation](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)
(EM):

1. Guess the parameter values.
2. Use the parameter values to infer likely labels (the E-step).
3. Use the labels to obtain ML estimates of the parameters of each distribution
   in the mixture, and of the relative contribution of each (the M-step).
4. Iterate steps 2 and 3 until convergence.

Under iteration, EM typically converges to a local optimum, which we hope is the
global optimum and therefore gives the ML estimates.

## E-step

How do we infer the labels? We can simply assign each observation to the
component it is most likely to have come from. Assigning labels this way is
called "hard" EM, because the labels are categorical.

Work in [mixture_models.py](mixture_models.py), where the
mixture parameters are held in a `GaussianMixtureParameters` object. Write
`hard_expectation_step(observations, parameters)`, which says whether each
observation is more likely to have come from component one, by comparing the
weighted densities $\pi\,\phi(x\mid\mu_1,\sigma_1)$ and
$(1-\pi)\,\phi(x\mid\mu_2,\sigma_2)$.

## M-step

Using these (imperfect) labels we can update our estimated parameters by maximum
likelihood: the mean and population standard deviation within each group, and
the fraction of observations in component one. Write
`hard_maximization_step(observations, labels)`.

## Iteration

Write `em_steps`, a generator that yields the parameters after each iteration
(first the initial values, then the result of an E-step followed by an M-step,
and so on, endlessly). 

Then write `expectation_maximization`, which takes values from `em_steps` until
the log-likelihood stops changing, and `mixture_log_likelihood`, which
calculates the sum of the log mixture densities across observations. Stop on the
*absolute* change in log-likelihood.[^abs-change] The docstrings give the exact
signatures, stopping rule and return values, and the tests check them. Neither
function needs to know what the parameters are, so they should work for any
model with an E-step and an M-step.

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

## Soft EM

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

## Multivariate Gaussian EM

Start with a diagnostic in the
[Old Faithful notebook](investigate.ipynb#Waiting-time-prediction).
Plot every eruption's duration against the waiting time that followed it.
Fit a straight line with `numpy.polyfit` or `scipy.stats.linregress`, interpret
its slope and intercept in minutes, and plot residuals against fitted values.
Calculate $R^2$: does a respectable value mean the model captures the structure?
This is a short model check, not an evaluation of out-of-sample prediction.

Do the points look like one cloud, or something else? Suppose they come from a
mixture of two bivariate normal distributions, where the variables are the
eruption duration and the waiting time to the next eruption (both in minutes).
`load_faithful_data()` in [loaders.py](../../_shared/loaders.py) provides them as
(duration, waiting) pairs, and the [Old Faithful
notebook](investigate.ipynb#The-data) describes the data in more detail.

Each standard deviation is now replaced by a covariance matrix, held in a
`MultivariateGaussianMixtureParameters` object. In
[mixture_models.py](mixture_models.py), write multivariate
counterparts of the soft-EM functions:
`multivariate_mixture_log_likelihood`,
`multivariate_soft_expectation_step`, `multivariate_soft_maximization_step` and
`fit_multivariate_gaussian_mixture`. Reuse your `expectation_maximization` for
the last of these: the loop shouldn't need to change. Finally, write
`fit_faithful_gaussian_mixture(initial_parameters)`, which fits the packaged Old
Faithful data. The two components are interchangeable (swapping them gives the
same likelihood), so a fit keeps the labels of your starting values.

Compare your fitted log-likelihood with the reference value in the tests (about
-1130.27). The [Old Faithful notebook](investigate.ipynb#Gaussian-mixture) gives rough
starting values and asks you to plot the fit. EM is not guaranteed to find the
global maximum from every starting point.

Because the fit is held in a `MultivariateGaussianMixtureParameters` object,
[mixture_models.py](mixture_models.py) can supply plotting
helpers that work with it. `plot_faithful_mixture(parameters)` draws the
Old Faithful data with each component in its own colour (mean and ellipses one
and two standard deviations out), and colours each eruption by the component
that most likely produced it, using your `multivariate_soft_expectation_step`.
Plot your starting values and your fitted result to check that the clusters look
sensible.

If you want to watch EM at work, `animate_faithful_mixtures(history)` animates a
list of parameter objects. Your `em_steps` yields the parameters after each
iteration, so `list(islice(em_steps(...), 40))` makes a ready-made history. Try
different starting values and see how the animation changes.

What do your fitted clusters say about the straight line, and about what it
was missing? The notebook also suggests an extension that revisits the
prediction using the clusters.
