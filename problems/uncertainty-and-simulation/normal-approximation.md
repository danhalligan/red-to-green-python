# When does the normal approximation fail?

> **Before you start:** basic Python, NumPy and probability, and the optional
> scientific stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** comparing discrete probabilities with a continuous
> approximation and finding when that approximation breaks down.
>
> **Check:** your notebook's plots and explanations; no automated tests.

If $X\sim\mathrm{Binomial}(n,p)$, its mean is $np$ and its variance is
$np(1-p)$. A normal distribution with that mean and variance is often used as a
stand-in for the binomial. Is it a good one? Start with $n=100$ and $p=0.5$.

In the [simulation studies notebook](../../analysis/simulation_studies.ipynb#2.-Binomial-and-normal-distributions), use
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
plotting the errors. Now find where the stand-in breaks down. Vary $n$ and $p$,
and predict which combinations will be worst before you run them. Can you
describe, in terms of $n$ and $p$, when you would trust the approximation and
when you would not?

<details>
<summary>What did you discover?</summary>

The approximation is poor when $np$ or $n(1-p)$ is small. The binomial is then
visibly skewed, with skewness $(1-2p)/\sqrt{np(1-p)}$, whereas a normal
distribution is symmetric, and the binomial cannot go below 0 or above $n$
whereas the normal can. A common rule of thumb is to trust the approximation when
both $np$ and $n(1-p)$ are at least about 10 (some texts use 5). For a fixed $p$
the approximation improves as $n$ grows, but for $p$ near 0 or 1 it needs a much
larger $n$.

</details>
