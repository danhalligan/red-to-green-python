# Can you trust a 95% interval? 🚀

> **Before you start:** [How uncertain is an average?](standard-error.md),
> [Two methods, two answers](bootstrap.md), and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** confidence intervals, simulation studies, and measuring
> coverage with Monte Carlo uncertainty.
>
> **Check:** your notebook's coverage plots and explanations; no automated tests.

A method claims to capture the true parameter 95% of the time. Can you test that
claim, and when does it fail?

A standard error becomes most useful as an interval. Two common intervals for
a mean are the normal interval, $\bar{x} \pm 1.96\,\widehat{\mathrm{SE}}$,
and the *percentile bootstrap* interval, which runs from the 2.5th to the 97.5th
percentile of the bootstrap resample means. A 95% interval is meant to contain the
true mean in about 95% of repeated samples. That is a claim about the procedure,
and a simulation can test it, because there we know the truth.

This question has no new function to write. In the [simulation studies
notebook](../../analysis/simulation_studies.ipynb#3.-Confidence-interval-coverage), use `standard_error` and your own
resampling loop. Draw samples of size 5, 10, 30 and 100 from a normal population
and from a skewed one (an exponential distribution), with the true mean known.
For each sample calculate three intervals: the normal interval above, the same
interval using the $t$ critical value instead of 1.96, and the percentile
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

With $n=5$ the estimated $s$ is very uncertain and is often too small, which makes
1.96 too optimistic. The $t$ distribution corrects for this when the data are
normal, using `scipy.stats.t.ppf(0.975, n - 1)`. The percentile bootstrap
resamples only from the data you have, so it inherits the same problem for small
samples. With skewed data, the sample mean is itself skewed at small $n$, and no
interval of this symmetric kind has exactly 95% coverage until $n$ is larger.

</details>
