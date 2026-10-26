# A likely story

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python, NumPy and probability, and the optional
> scientific stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** likelihood, working in log space, numerical
> optimisation, parameter transformations, and fitting several kinds of model
> with the same tool.
>
> **Check:** `uv run pytest exercises/a_likely_story/ -q`

Every model in this exercise answers the same question: *if these parameter
values were true, how probable is the data I actually saw?* Write that down for
one observation, and you can estimate the parameters of almost any model,
whether a coin, a bell curve, a straight line or something with no textbook
formula at all. By the end you will fit all of these with one function you
wrote yourself, and see a case where it beats a method you probably already
know.

All the data here are simulated, so you know the true parameters and can check
whether your estimates find them. Work through the [notebook](investigate.ipynb)
alongside the stages below, using seeded random generators.

## Stage 1: Is this coin fair?

> **Check:** `uv run pytest exercises/a_likely_story/test_likelihood.py -k bernoulli -q`

You flip a coin 10 times and see 7 heads. Each flip is heads with some unknown
probability $p$, independently of the others, so the probability of one flip
$x_i$ (1 for heads, 0 for tails) is $p$ if it is heads and $1-p$ if it is tails.
The probability of the whole sequence is the product of these terms.

The *likelihood* is that same quantity viewed the other way round. The data are
now fixed, because we have observed them, and we ask how the probability changes
as we vary the parameter: $\mathcal{L}(p\mid x)=\prod_i P(x_i\mid p)$.
Parameter values under which the observed data are more probable have a higher
likelihood, and are better supported by the data. *Maximum likelihood
estimation* (MLE) chooses the parameter values that maximise it.

Products of many probabilities quickly underflow to zero, so we work with the
log-likelihood instead, which turns the product into a sum:
$\ell(p\mid x)=\sum_i \log P(x_i\mid p)$. The logarithm is increasing, so
whatever maximises $\ell$ also maximises $\mathcal{L}$.

Implement `bernoulli_log_likelihood` in [likelihood.py](likelihood.py). Think
about what should happen when $p$ is exactly 0 or 1.

In [notebook section 1](investigate.ipynb#1.-Is-this-coin-fair?), plot
$\ell(p)$ for 7 heads in 10 flips, and again for 70 heads in 100. Where is the
peak in each case, and how does its shape differ? How many times more likely is
the data under the best $p$ than under a fair coin ($p=0.5$)? Which data set
would make you more suspicious of the coin, and why, given that both show 70%
heads?

<details>
<summary>What did you discover?</summary>

Both curves peak at $\hat p = k/n = 0.7$: for a coin, the MLE is simply the
proportion of heads, which you can confirm by differentiating $\ell$. The
difference is the shape. With 100 flips the curve is far more sharply peaked,
because each extra flip adds another term to the sum, so moving away from the
best value is penalised more heavily.

Seven heads in ten is only about 2.3 times more likely under $p=0.7$ than under
a fair coin, which is weak evidence. Seventy in a hundred is about 3,700 times
more likely, which is strong. The same proportion carries very different
evidence depending on how much data stands behind it: the width of the peak is a
measure of uncertainty, the same idea you met as the standard error in
[Known unknowns](../known_unknowns/README.md).

</details>

## Stage 2: A likelihood surface

> **Check:** `uv run pytest exercises/a_likely_story/test_likelihood.py -k "normal or fit_mle" -q`

Now suppose the observations are measurements that come from a normal
distribution with unknown mean $\mu$ and standard deviation $\sigma$. The
probability of a single continuous observation is replaced by its density,
$\phi(x_i\mid\mu,\sigma)$, but the recipe is the same:
$\ell(\mu,\sigma\mid x)=\sum_i \log \phi(x_i\mid\mu,\sigma)$. Implement
`normal_log_likelihood`.

With two parameters you could still search a grid, but that does not scale.
Instead, implement `fit_mle`, a general-purpose fitter that takes *any*
log-likelihood, written as a function of a parameter vector, and a starting
point, and maximises it numerically (for example with
`scipy.optimize.minimize`, which minimises, so give it the negative). Check the
optimiser's `success` and raise a `RuntimeError` if it fails rather than
returning a wrong answer.

Optimisers search over all real numbers, but $\sigma$ must be positive and
$p$ must lie between 0 and 1. The standard trick is to optimise a transformed
parameter that can take any value: fit $\log\sigma$ and use
$\sigma=e^{\theta}$, or fit the log-odds of $p$ and use
$p=1/(1+e^{-\theta})$ (`scipy.special.expit`). Use `fit_mle` with the log trick
to implement `fit_normal_mle`. It should work across many small samples, and on
data far from zero or with a tiny or enormous spread.

<details>
<summary>💡 Hint: when the optimiser fails</summary>

Optimisers can fail, for example reporting "precision loss" on data far from
zero or with a tiny spread. Start from a sensible guess based on the data, or
standardise the data first (subtract a centre and divide by a spread), fit, and
transform the estimates back.

</details>

In [notebook section 2](investigate.ipynb#2.-A-likelihood-surface), simulate 20
observations from a normal distribution with known parameters and draw the
log-likelihood as a contour plot over a grid of $\mu$ and $\sigma$. Mark the
true values and your fitted estimate. Repeat with 200 observations. Compare the
estimates with the sample mean and the *population* standard deviation (divisor
$n$).

Then, in [notebook section 3](investigate.ipynb#3.-Is-the-MLE-right-on-average?),
fit many repeated samples at several sample sizes, including small ones. Do the
estimates recover the true parameters on average? Does that depend on $n$?

<details>
<summary>What did you discover?</summary>

The surface is a single hill whose peak sits at the sample mean and the
population standard deviation: for the normal model those are the ML estimates,
which you can show by setting the derivatives of $\ell$ to zero. With more data
the hill becomes narrower, just as the coin's curve did. It is also not
symmetric in $\sigma$: small values are penalised more steeply than large ones.

The MLE of $\mu$ is unbiased, but $\hat\sigma$ is too small on average. Its
square divides by $n$ rather than $n-1$, so it averages
$\frac{n-1}{n}\sigma^2$: the spread is measured around $\bar{x}$, which was
fitted to the same data and so sits closer to the observations than the true
mean does. This is the same factor that separated the bootstrap from
$s/\sqrt{n}$ in [Known unknowns](../known_unknowns/README.md#stage-2-bootstrapping).
Taking the square root adds a further downward bend, as in
[Known unknowns](../known_unknowns/README.md#stage-1-standard-error). Both
effects shrink as $n$ grows, so the MLE is still a sensible estimator, but small
samples need care.

</details>

## Stage 3: Regression is a likelihood too

> **Check:** `uv run pytest exercises/a_likely_story/test_likelihood.py -k regression -q`

A straight-line regression is just another model for how the data were
generated: each $y_i$ is normal with mean $a + b x_i$ and standard deviation
$\sigma$. The parameters are now $(a, b, \sigma)$, but nothing else changes.
Implement `linear_regression_log_likelihood`, then, in [notebook section
4](investigate.ipynb#4.-Regression-is-a-likelihood-too), simulate 30 points from
a line you choose, fit it with `fit_mle`, and compare the result with
least squares (`np.polyfit(x, y, 1)`). What do you notice, and can you explain
it by looking at the normal log-density?

### When the data misbehave

Now corrupt your data: move three of the points well away from the line, as if a
sensor glitched. In [notebook section
5](investigate.ipynb#5.-When-the-data-misbehave), fit the line again, by least
squares and by your normal likelihood, and plot both against the true line.

Then change *one thing*: instead of a normal distribution for the noise, use a
Student-$t$ distribution with 3 degrees of freedom, whose tails are much
heavier, so large errors are rare but not astronomically so. You only need a new
log-likelihood, using `scipy.stats.t.logpdf(y, 3, loc=a + b * x, scale=sigma)`
in place of the normal log-density; `fit_mle` does the rest. Plot this fit too.
Which line would you trust, and why?

<details>
<summary>What did you discover?</summary>

On clean data the likelihood fit and least squares agree to many decimal
places. They are the same method: the normal log-density is
$-\frac{(y_i - a - b x_i)^2}{2\sigma^2}$ plus terms that do not involve $a$ or
$b$, so maximising the likelihood over the line is exactly minimising the sum of
squared residuals. Least squares *is* maximum likelihood with normal errors,
and $\hat\sigma$ comes along for free.

That also explains what goes wrong with the glitches. Under a normal model a
point 12 standard deviations from the line costs 72 units of log-likelihood, so
the fit drags the whole line towards the outliers to reduce that penalty; three
glitches near one end can flatten the slope or even reverse it. Under the
Student-$t$ model the same point costs only about 8, so the fit can afford to
treat it as a rare event and follow the other 27 points, and the slope barely
moves. You did not write a special "robust regression" algorithm. You described
a different probability for one data point, and maximum likelihood did the
rest.

</details>

**Extension 🚀:** try a model for a *yes/no* outcome. In logistic regression,
$P(y_i=1)=1/(1+e^{-(a+bx_i)})$, so each observation is a coin flip whose
probability depends on $x_i$. Write its log-likelihood (your
`bernoulli_log_likelihood` is nearly there), simulate data from known $a$ and
$b$, and fit it with `fit_mle`. This is what scikit-learn's `LogisticRegression`
does in [Titanic disaster](../titanic_disaster/README.md), apart from a small
penalty it adds by default.

This exercise prepares you for [Fitting a
mixture](../fitting_a_mixture/README.md), where the likelihood has no
closed-form maximum and a cleverer algorithm takes over.
