# Standard error

> **Difficulty:** 🌶️
>
> **Before you start:** basic Python and NumPy, and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** estimating uncertainty, repeated sampling, and
> distinguishing sampling variation from bias.
>
> **Check:** `uv run pytest exercises/uncertainty_and_simulation/test_uncertainty.py -k "standard_error and not bootstrap" -q`

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
[uncertainty.py](../uncertainty.py).

Old Faithful is a geyser in Yellowstone National Park, and its eruption waiting
times are a commonly used dataset in statistics. In the [Old Faithful
notebook](investigate.ipynb#Standard-error-of-the-mean-waiting-time), report the mean waiting time between
eruptions with its standard error.

Is the formula honest? Real data cannot tell you, because you never know the
truth. So, in the [simulation studies notebook](investigate.ipynb#1.-Is-the-standard-error-right-on-average?),
simulate 500 independent samples of standard normal data ($\sigma=1$) for each
$n$ from 2 through 100. The true SE is then $1/\sqrt{n}$. Plot the mean of your
estimated standard errors against $n$ and compare it with the truth. Predict what
you will see first: does the estimator get the right answer on average? Then look
at how the individual estimates scatter, and at how both the scatter and any gap
from the true curve change as $n$ grows and as you add repetitions.

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
