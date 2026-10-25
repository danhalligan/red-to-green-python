# Known unknowns

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python and NumPy, and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** estimating uncertainty, repeated sampling, bootstrap
> resampling, confidence intervals, and measuring coverage with Monte Carlo
> uncertainty.
>
> **Check:** `uv run pytest exercises/known_unknowns/ -q`
> for the code, and your notebook's plots and explanations for the rest.

You measure something 30 times and report the mean. How far might that mean be
from the truth? You cannot repeat the experiment to find out, but you can
*estimate* the uncertainty from the one sample you have. And if you simulate the
data yourself, you know the truth and can test whether those estimates, and the
claims built on them, are right.

Work through the three stages below, using the [simulation
notebook](investigate.ipynb) throughout. Use seeded random generators so your
results are reproducible.

## Stage 1: Standard error

> **Check:** `uv run pytest exercises/known_unknowns/test_uncertainty.py -k "standard_error and not bootstrap" -q`

The standard error (SE) of a statistic is its standard deviation across repeated
samples: it measures how much a statistic would vary if we could redraw the
data. 

For the sample mean $\bar{x}$ we could, in principle, draw many samples, compute
$\bar{x}$ for each and take the standard deviation of those means. In practice
we have only one sample, so that spread cannot be observed directly.

For the standard error of the mean, theory provides a shortcut: if the
observations are independent with true standard deviation $\sigma$, the SE is
$\sigma/\sqrt{n}$. We rarely know $\sigma$, but can estimate SE by replacing
it with $s$, the standard deviation of the sample we actually have (using $n-1$
in the denominator): $\widehat{\mathrm{SE}}(\bar{x}) = s / \sqrt{n}$.

Implement `standard_error` using $s$ in [uncertainty.py](uncertainty.py).

Is the formula honest? In the
[notebook](investigate.ipynb#1.-Is-the-standard-error-right-on-average?), we'll
investigate how well it performs by simulating samples from a normal
distribution. Simulate 500 independent samples of standard normal data
($\sigma=1$) for each $n$ from 2 through 100. The true SE is then $1/\sqrt{n}$.
Plot the mean of your estimated standard errors against $n$ and compare it with
the truth. Predict what you will see first: does the estimator get the right
answer on average? Then look at how the individual estimates scatter, and at how
both the scatter and any gap from the true curve change as $n$ grows and as you
add repetitions.

<details>
<summary>💡 Hint: telling two kinds of difference apart</summary>

Rerun with 5,000 repetitions instead of 500. Which differences between your
average and the true curve shrink, and which stay put?

</details>

<details>
<summary>What did you discover?</summary>

Each estimate $s/\sqrt{n}$ is random because $s$ changes from sample to sample.
That is the sampling variation, and averaging over more repetitions smooths it
out. There is also a small systematic gap. The sample variance $s^2$ averages
exactly $\sigma^2$ (it is unbiased), but taking a square root bends the average
downwards, so $s$ averages slightly less than $\sigma$ (this is an instance of
[Jensen's inequality](https://en.wikipedia.org/wiki/Jensen%27s_inequality)). The
effect is noticeable for small $n$: at $n=2$ the average estimate is about
0.564, not 0.707. More repetitions do not remove this gap, but larger samples
shrink it.

</details>

## Stage 2: Bootstrapping

> **Check:** `uv run pytest exercises/known_unknowns/test_uncertainty.py -k bootstrap_standard_error -q`

*Bootstrapping* is an alternative way to estimate the same standard error. It
mimics repeated samples from the population by using the *observed values* as a
stand-in for the population. We repeatedly draw samples of size $n$ *with
replacement* and calculate the statistic of each. These *resample* statistics
play the role of repeated *sample* statistics, and as such, their standard
deviation estimates the standard error.

Implement `bootstrap_standard_error` in [uncertainty.py](uncertainty.py) by
computing the statistic of each of 10,000 resamples and returning the standard
deviation of those values [^bs-sd]. The statistic defaults to the mean, but any
function that works like `np.mean` and `np.median` is accepted (it is called as
`statistic(resamples, axis=1)` on an array with one resample per row). Accept a
keyword-only `numpy.random.Generator` so the experiment is reproducible.

[^bs-sd]: You should use the *sample* standard deviation (`ddof=1`) of the
    resample statistics (at 10,000 resamples the convention matters little 
    though).

### Does it agree with the formula?

For the mean, the bootstrap and $s/\sqrt{n}$ claim to estimate the same
quantity. In [notebook section 2](investigate.ipynb#2.-Does-the-bootstrap-agree-with-the-formula?),
extend your stage 1 simulation to $n = 10, 30$ and $100$ and add the bootstrap
estimate. Do they agree? Compare each with the true SE $1/\sqrt{n}$, and then
with each other. Change the number of resamples. What changes as you use more
resamples, and what does not? How does the gap between the two methods depend on
the sample size?

<details>
<summary>💡 Hint: comparing on the same sample</summary>

Averages of noisy estimates make a small gap hard to see. Calculate the ratio of
the bootstrap to the analytic estimate *for each sample*, and look at how that
ratio behaves.

</details>

<details>
<summary>What did you discover?</summary>

There are two reasons the estimates differ. The first is Monte Carlo error: we
use a finite number of resamples, so the estimate wanders around its limiting
value, and settles towards it as the number of resamples grows. The second is a
systematic difference: the limiting value is
$\mathrm{std}(x, \mathrm{ddof}=0)/\sqrt{n}$, which differs from the analytic
estimate by the factor $\sqrt{(n-1)/n}$.

That limiting value is what you would get by averaging over every possible
resample, so there is no Monte Carlo error. Resampling with replacement draws
each observation with probability $1/n$, so the bootstrap treats the sample *as
if it were the whole population*. The variance of that population is
$\frac{1}{n}\sum_i (x_i-\bar{x})^2$, with divisor $n$ (`ddof=0`), because
$\bar{x}$ is its known true mean. The variance of the mean of $n$ draws is then
this divided by $n$. The analytic estimate $s$ instead uses divisor $n-1$ to
correct for the fact that the sample mean was estimated from the same data,
which makes $s^2$ unbiased for the true $\sigma^2$. The bootstrap has no such
correction, so it is slightly smaller: by 5% at $n=10$, but only 0.5% at
$n=100$.

</details>

### Where the bootstrap earns its place

For the mean we already have a formula, so the bootstrap is only a check. The
median has no such formula, but `bootstrap_standard_error(values,
statistic=np.median)` works the same way. Is it any good? In [notebook section
3](investigate.ipynb#3.-When-there-is-no-formula:-the-median), use simulation to
find the *true* standard error of the median: draw many samples, take the median
of each and calculate the standard deviation of those medians. Then, for $n =
10, 30$ and $100$ and for both normal and skewed (exponential) data, compare
that truth with the bootstrap estimates from single samples. Is the bootstrap
right on average? How much do the individual estimates scatter, compared with
the bootstrap estimates for the mean? Which statistic is more precise for each
population?

<details>
<summary>What did you discover?</summary>

On average the bootstrap standard error of the median is close to the truth, a
little too high at small $n$ (by a few percent, and by as much as 10% for
exponential data at $n=10$). But a single estimate is much noisier than for the
mean: at $n=100$ the estimates scatter by around 20–25% of their value, compared
with about 7% (normal) or 15% (exponential) for the mean. The median depends on
the few observations in the middle of the sample, and the bootstrap needs more
data to describe its variability. It also has no formula to fall back on. For
normal data the median is less precise than the mean (its SE is about
$1.25\sigma/\sqrt{n}$), while for exponential data the two are about equally
precise, so which one to prefer depends on the population.

There are caveats. The bootstrap assumes independent observations that represent
the population, and it can perform poorly for very small samples or for extreme
statistics such as the maximum.

</details>

## Stage 3: Confidence intervals

> **Check:** `uv run pytest exercises/known_unknowns/test_uncertainty.py -k interval -q`

A standard error becomes most useful as an interval. Two common intervals are:

- the *normal interval*, $\hat\theta \pm c\,\widehat{\mathrm{SE}}$, where
  $\hat\theta$ is the estimate and $c$ is a critical value: 1.96 for 95% from the
  normal distribution, or the larger $t$ critical value for $d$ degrees of
  freedom, which allows for the standard error itself being uncertain;
- the *percentile bootstrap* interval, which runs from the 2.5th to the 97.5th
  percentile of the bootstrap resample statistics.

Implement both in [uncertainty.py](uncertainty.py). `normal_interval` takes an
estimate and its standard error, so it works for any statistic: pass `df` to use
the $t$ critical value (`scipy.stats.t.ppf`) instead of the normal one
(`scipy.stats.norm.ppf`). `bootstrap_interval` takes the data and a `statistic`
like `bootstrap_standard_error` does. Both accept a `level` (default 0.95).

A 95% interval is meant to contain the true value in about 95% of repeated
samples. That is a claim about the procedure, and a simulation can test it,
because there we know the truth.

### Coverage for the mean

In [notebook section 4](investigate.ipynb#4.-Confidence-interval-coverage-for-the-mean),
draw samples of size 5, 10, 30 and 100 from a normal population and from a
skewed one (an exponential distribution), with the true mean known. For each
sample calculate three intervals: the normal interval with the normal critical
value, the same with the $t$ critical value (`df = n - 1`), and the percentile
bootstrap interval. Predict which methods will keep their promise, then record
the proportion of intervals that contain the truth (the *coverage*) and plot
coverage against $n$ for each method, with its Monte Carlo uncertainty.

<details>
<summary>💡 Hint: how precise is a coverage estimate?</summary>

The Monte Carlo uncertainty of a coverage estimate from $B$ repetitions is about
$\sqrt{p(1-p)/B}$, so use enough repetitions that you can tell 93% from 95%.

</details>

<details>
<summary>What did you discover?</summary>

With $n=5$ the estimated $s$ is very uncertain and is often too small, which
makes 1.96 too optimistic. The $t$ distribution corrects for this when the data
are normal. The percentile bootstrap resamples only from the data you have, so it
inherits the same problem for small samples. With skewed data, the sample mean is
itself skewed at small $n$, and no interval of this symmetric kind has exactly
95% coverage until $n$ is larger.

</details>

### Intervals for the median

The same tools work for a statistic with no standard-error formula. In
[notebook section 5](investigate.ipynb#5.-Confidence-intervals-for-the-median),
repeat the study for the *median*, using the true median of each population. Use
two intervals: the normal interval centred on the sample median with the
*bootstrap* standard error, and the percentile bootstrap interval. How does
their coverage compare with the mean's? Coverage alone can be bought with very
wide intervals, so also compare how wide the intervals are.

<details>
<summary>What did you discover?</summary>

Neither interval shows the collapse in coverage the mean's intervals have at
$n=5$: both stay within about three percentage points of 95% from $n=10$, with
the percentile interval slightly closer. The cost is width. The median is a less
precise statistic than the mean for normal data, and its bootstrap standard
error is itself very noisy, so the intervals are wide and vary a lot from sample
to sample. Coverage is only one half of the story, so look at both coverage and
width when judging an interval.

</details>
