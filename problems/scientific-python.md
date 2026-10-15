# Scientific Python 🔬

[← All problems](../README.md)

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md) and [Object-oriented Python](object-oriented-python.md), and the
> optional scientific stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** NumPy and SciPy, sampling variation and standard errors,
> least squares, the bootstrap, and likelihood-based estimation.
>
> **Check:** `uv run pytest tests/test_statistics.py -q`

These exercises move from sampling variation, through linear models and
resampling, to likelihood-based estimation.

The reusable calculations are stub functions in
[statistics.py](../src/pyproblems/statistics.py) that you complete; their tests
check them. You will use the functions in two notebooks:

- The [Old Faithful notebook](../analysis/old_faithful.ipynb) applies them to a
  real dataset.
- The [simulation studies notebook](../analysis/simulation_studies.ipynb) uses
  simulated data with known parameters, so you can check what the methods do.

## Q1. Sampling variation and standard error

The standard error (SE) of a statistic is its standard deviation across
repeated samples: how much it would vary if we could redraw the data. For the
sample mean $\bar{x}$ we could, in principle, draw many samples, compute
$\bar{x}$ for each and take the standard deviation of those means. In practice
we have only one sample, so that spread cannot be observed directly.

For the standard error of the mean, theory provides a shortcut: if the
observations are independent with true standard deviation $\sigma$, the SE is
$\sigma/\sqrt{n}$. We rarely know $\sigma$, but can estimate SE by replacing
it with $s$, the standard deviation of the sample we actually have (using $n-1$
in the denominator): $\widehat{\mathrm{SE}}(\bar{x}) = s / \sqrt{n}$.

Implement `standard_error` using $s$ in
[statistics.py](../src/pyproblems/statistics.py).  

Old Faithful is a geyser in Yellowstone National Park. Data on eruption waiting
times is a commonly used dataset for statistics. In the [Old Faithful
notebook](../analysis/old_faithful.ipynb), report the mean waiting time between
eruptions with its standard error. 

Then, in the [simulation studies notebook](../analysis/simulation_studies.ipynb),
simulate 500 independent samples of standard normal data ($\sigma=1$) for each
$n$ from 2 through 100. The true SE is then $1/\sqrt{n}$. Plot the mean of the
estimated standard errors against $n$ and compare it with true SE
($1/\sqrt{n}$); explain the sampling variation and bias you see.

💡 Hint in the footnote [^se-bias].

[^se-bias]: Each estimate $s/\sqrt{n}$ is random because $s$ changes from sample
    to sample, which is the sampling variation. However, there is also a small
    systematic gap. The sample variance $s^2$ averages exactly $\sigma^2$ (it is
    unbiased), but taking a square root bends the average downwards, so $s$
    averages slightly less than $\sigma$ (this is an instance of [Jensen's
    inequality](https://en.wikipedia.org/wiki/Jensen%27s_inequality)). The
    effect is noticeable for small $n$: at $n=2$ the average estimate is about
    0.564, not 0.707. Running more repetitions smooths the random variation but
    does not remove this gap.

## Q2. Linear models and ordinary least squares

Ordinary least squares chooses coefficients that minimise the sum of
squared residuals. For a full-column-rank design matrix $X$ and outcome
vector $y$, the normal equations are $X^\mathsf{T}X\hat{\beta}=X^\mathsf{T}y$.

Implement `ols_coefficients` in [statistics.py](../src/pyproblems/statistics.py) by
solving this system with `numpy.linalg.solve`, not by explicitly computing an
inverse. The function does not add an intercept: include a column of ones when
one is wanted. 

In the [simulation studies notebook](../analysis/simulation_studies.ipynb),
simulate outcomes from known coefficients and compare your estimates with the
truth and with `numpy.linalg.lstsq`. You will use `ols_coefficients` on real
data later.

## Q3. The binomial and normal distributions

If $X\sim\mathrm{Binomial}(n,p)$, its mean is $np$ and its variance is
$np(1-p)$. When both expected counts $np$ and $n(1-p)$ are sufficiently
large, a normal distribution with that mean and variance can approximate
the binomial. Start with $n=100$ and $p=0.5$.

In the [simulation studies notebook](../analysis/simulation_studies.ipynb), use
`scipy.stats` to plot the exact probability at each integer from 0 to 100
alongside the continuous normal density.

Note you should consider the continuity correction [^continuity-correction] 
when calculating the normal probabilities.

[^continuity-correction]: A density is not a probability (a continuous variable
    has probability zero of equalling any single value), whereas $P(X=k)$ is a
    positive point mass. The *continuity correction* bridges the two by treating
    each integer $k$ as standing for the unit-width interval from $k-0.5$ to
    $k+0.5$. If $Y\sim\mathcal{N}(np,np(1-p))$, then 
    $$P(X\le k)\approx P(Y<k+0.5)$$.
    Without the $+0.5$, $P(Y<k)$ misses half of the bar at $k$ and is
    systematically too small.
    
Compare the exact probabilities with the normal probabilities, for example by
plotting the errors. Investigate a value of $p$ nearer zero or one, where the
approximation becomes less reliable.

## Q4. Bootstrap standard error

In Q1 we noted that the standard error (of the mean) is the standard deviation
of the sample mean across repeated samples. We estimated this from a single
sample using the sample standard deviation. 

An alternative, is a bootstrap approach. The idea here is to mimic repeated
samples from a population using the *observed values* as a stand-in for the
population. We repeatedly draw samples of size $n$ *with replacement* and
calculate the mean of each. These *resample* means play the role of repeated
*sample* means, and as such, their standard deviation estimates the standard error.

Implement `bootstrap_standard_error` by computing the mean of each of 10,000
resamples and returning the standard deviation of those means [^bs-sd]. Accept a
keyword-only `numpy.random.Generator` so the experiment is reproducible.

[^bs-sd]: You should use the *sample* standard deviation (`ddof=1`) of the
    resample means (at 10,000 resamples the convention matters little though). 

Your bootstrap estimate will not match $s/\sqrt{n}$ exactly, for two reasons.
The first is Monte Carlo error: we use a finite number of resamples, so the
estimate shrinks towards its limiting value as the number of resamples grows.
The second is a systematic difference: the limiting value is $\mathrm{std}(x,
\mathrm{ddof}=0)/\sqrt{n}$, which differs from the analytic estimate by the
factor $\sqrt{(n-1)/n}$.[^bs-exact]

[^bs-exact]: "Exact" here means the value you would get by averaging over every
    possible resample, so there is no Monte Carlo error. Resampling with
    replacement draws each observation with probability $1/n$, so the bootstrap
    treats the sample *as if it were the whole population*. The variance of
    that population is $\frac{1}{n}\sum_i (x_i-\bar{x})^2$, with divisor $n$
    (`ddof=0`), because $\bar{x}$ is its known true mean. The variance of the
    mean of $n$ draws is then this divided by $n$. The analytic estimate $s$
    instead uses divisor $n-1$ to correct for the fact that the sample mean
    was estimated from the same data, which makes $s^2$ unbiased for the true
    $\sigma^2$. The bootstrap has no such correction, so it is slightly
    smaller: by 5% at $n=10$, but only 0.5% at $n=100$.

In the [Old Faithful notebook](../analysis/old_faithful.ipynb), apply it to the
waiting times, and try random subsamples of small and moderate size to see the
two effects separately.

The bootstrap concept is not specific to the mean. The standard deviation of any
statistic computed over the resamples estimates that statistic's standard error,
which is useful when no simple formula like $s/\sqrt{n}$ exists. For example,
the median has no such formula. There are caveats: the bootstrap assumes
independent observations that represent the population, and it can perform
poorly for very small samples or for extreme statistics such as the maximum. 

**Extension 🚀:** adapt the same resampling loop to estimate the standard error
of the median waiting time and compare it with that of the mean.

## Q5. Likelihood and normal maximum likelihood estimation

Statistical models assume that data were generated by a process with unknown
parameters. In this question, we are going to work with a set of observations
that we assume are drawn independently from a normal distribution with mean
$\mu$ and standard deviation $\sigma$. 

For any chosen values of $\mu$ and $\sigma$, we can calculate the probability
density of an observation $x_i$ *conditional on those parameter values*, written
$\phi(x_i\mid\mu,\sigma)$, where $\phi$ denotes the Gaussian (normal) density
function. Because the observations are independent, the density of the whole
data set $x$ is the product of these terms.

The *likelihood* is that same quantity viewed the other way round. The data are
now fixed, because we have observed them, and we ask how the density changes as
we vary the parameters:
$\mathcal{L}(\mu,\sigma\mid x)=\prod_i \phi(x_i\mid\mu,\sigma)$. Parameter values
under which the observed data are more probable have a higher likelihood, and
are better supported by the data. *Maximum likelihood estimation* chooses the
parameter values that maximise it.

Calculating this quantity can be difficult because products of small densities
can underflow. As a result, it is more convenient to consider the log likelihood
$\ell(\mu,\sigma\mid x)=\log\mathcal{L}(\mu,\sigma\mid x)=\sum_i \log
\phi(x_i\mid\mu,\sigma)$. Maximising the log-likelihood will also maximise the
likelihood (as the log function is monotonic) and we don't have the issue of
handling very small values. Implement `normal_log_likelihood` as a sum of log
densities.

Implement `fit_normal_mle` by *numerical optimisation*. In other words, find the
combination of parameter values that maximises the value of
`normal_log_likelihood` numerically. Constrain the positive standard deviation
(for example, optimise its logarithm), and check optimiser success. Your fit
should work across many seeded small samples and on shifted and rescaled data.
Optimisers can fail, so there is a 💡 hint.[^optimiser-hint]

[^optimiser-hint]: Optimisers can fail, for example reporting "precision loss"
    on small samples or on data far from zero or with a tiny spread. Start from
    a sensible guess based on the data, check the optimiser's `success` and
    `message` instead of assuming it worked, and if it fails try a different
    starting point.

As a validation, compare with the analytical estimates: the sample mean and the
population standard deviation. In the [Old Faithful
notebook](../analysis/old_faithful.ipynb), fit a normal distribution to the waiting
times and judge how well it describes them. In the [simulation studies
notebook](../analysis/simulation_studies.ipynb), investigate the bias of these
estimates across repeated samples (💡 hint in the footnote).[^mle-bias]

[^mle-bias]: Compare the average of each estimate with the true value as $n$
    changes. The MLE of $\mu$ is the sample mean, which is unbiased. The MLE of
    $\sigma^2$ divides by $n$ rather than $n-1$, so on average it equals
    $\frac{n-1}{n}\sigma^2$, which is too small. This is the same factor that
    separated the bootstrap from $s/\sqrt{n}$ in Q4, for the same reason: the
    spread is measured around $\bar{x}$, which was fitted to the same data and
    so sits closer to the observations than the true mean does. Taking the
    square root to get $\hat\sigma$ adds the downward bend from Q1 (Jensen's
    inequality), so $\hat\sigma$ is biased low for TWO reasons! Both effects
    shrink as $n$ grows, so the MLE is still a sensible estimator; the bias is
    largest for small samples.

> [!NOTE]
> For the normal model the optimiser is not strictly needed. Differentiating the
> log-likelihood with respect to $\mu$ and $\sigma$, setting the derivatives to
> zero and solving shows analytically that the ML estimates are the sample mean,
> $\hat\mu=\bar{x}$, and the *population* standard deviation (divisor $n$),
> $\hat\sigma=\sqrt{\tfrac{1}{n}\sum_i(x_i-\bar{x})^2}$. Numerical optimisation
> earns its keep for models, such as the mixtures later on, where no such closed
> form exists.

## Q6. Confidence intervals and coverage 🚀

A standard error becomes most useful as an interval. Two common intervals for
a mean are the normal interval, $\bar{x} \pm 1.96\,\widehat{\mathrm{SE}}$,
and the *percentile bootstrap* interval, which runs from the 2.5th to the 97.5th
percentile of the resample means from Q4. A 95% interval is meant to contain the
true mean in about 95% of repeated samples. That is a claim about the procedure,
and a simulation can test it, because there we know the truth.

This question has no new function to write. In the [simulation studies
notebook](../analysis/simulation_studies.ipynb), use `standard_error` and your own
resampling loop. Draw samples of size 5, 10, 30 and 100 from a normal population
and from a skewed one (an exponential distribution), with the true mean known.
For each sample calculate three intervals: the normal interval above, the same
interval using the $t$ critical value instead of 1.96, and the percentile
bootstrap interval. Record the proportion of intervals that contain the truth
(the *coverage*) and plot coverage against $n$ for each method, with its Monte
Carlo uncertainty.

Which intervals fall short of 95%, when, and why? What does the skewed
population change? 💡 Hint in the footnote.[^coverage-hint]

[^coverage-hint]: With $n=5$ the estimated $s$ is very uncertain and is often too
    small, which makes 1.96 too optimistic. The $t$ distribution corrects for
    this when the data are normal, using `scipy.stats.t.ppf(0.975, n - 1)`. The
    percentile bootstrap resamples only from the data you have, so it inherits
    the same problem for small samples. With skewed data, the sample mean is
    itself skewed at small $n$, and no interval of this symmetric kind has
    exactly 95% coverage until $n$ is larger. The Monte Carlo uncertainty of a
    coverage estimate from $B$ repetitions is about $\sqrt{p(1-p)/B}$.
