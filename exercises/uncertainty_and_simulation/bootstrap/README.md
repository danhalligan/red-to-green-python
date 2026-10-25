# Two methods, two answers

> **Difficulty:** 🌶️
>
> **Before you start:** [How uncertain is an average?](../standard_error/README.md) and the
> optional scientific stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** resampling with a seeded NumPy generator and comparing
> bootstrap and analytic uncertainty estimates.
>
> **Check:** `uv run pytest exercises/uncertainty_and_simulation/test_uncertainty.py -k bootstrap -q`

Two methods claim to estimate the uncertainty in the same measurement. Why don't
they give exactly the same answer?

The standard error (of the mean) is the standard deviation
of the sample mean across repeated samples. We estimated this from a single
sample using the sample standard deviation.

An alternative is a bootstrap approach. The idea here is to mimic repeated
samples from a population using the *observed values* as a stand-in for the
population. We repeatedly draw samples of size $n$ *with replacement* and
calculate the mean of each. These *resample* means play the role of repeated
*sample* means, and as such, their standard deviation estimates the standard error.

Implement `bootstrap_standard_error` by computing the mean of each of 10,000
resamples and returning the standard deviation of those means [^bs-sd]. Accept a
keyword-only `numpy.random.Generator` so the experiment is reproducible.

[^bs-sd]: You should use the *sample* standard deviation (`ddof=1`) of the
    resample means (at 10,000 resamples the convention matters little though).

In the [Old Faithful notebook](investigate.ipynb#Bootstrap-standard-error-of-the-mean-waiting-time), apply it to the
waiting times and compare it with $s/\sqrt{n}$. Do they agree exactly? Then try
random subsamples of small and moderate size, and change the number of
resamples. What changes as you use more resamples, and what does not? How does
the gap between the two methods depend on the sample size?

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
correct for the fact that the sample mean was estimated from the same data, which
makes $s^2$ unbiased for the true $\sigma^2$. The bootstrap has no such
correction, so it is slightly smaller: by 5% at $n=10$, but only 0.5% at
$n=100$.

</details>

The bootstrap concept is not specific to the mean. The standard deviation of any
statistic computed over the resamples estimates that statistic's standard error,
which is useful when no simple formula like $s/\sqrt{n}$ exists. For example,
the median has no such formula. There are caveats: the bootstrap assumes
independent observations that represent the population, and it can perform
poorly for very small samples or for extreme statistics such as the maximum.

**Extension 🚀:** adapt the same resampling loop to estimate the standard error
of the median waiting time and compare it with that of the mean.
