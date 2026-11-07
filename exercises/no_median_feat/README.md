# No median feat

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python and NumPy, and the optional scientific stack
> (`uv sync --all-groups --extra science`). The idea of a standard error from
> [Known unknowns](../known_unknowns/README.md) is useful, but not required.
>
> **You’ll practise:** robust summaries (trimmed mean, median, MAD), flagging
> outliers, Theil–Sen regression, and using simulation to measure the trade-off
> between resisting outliers and efficiency on clean data.
>
> **Check:** `uv run pytest exercises/no_median_feat/ -q` checks the functions you
> write. Your notebook's plots and explanations check the investigation.

One bad number can ruin an average. A single mistyped weight, a sensor glitch or
a data-entry slip can drag the mean, the standard deviation and a fitted line
anywhere it likes. The median is famous for shrugging these off, so why not use
it for everything?

Because protection has a price. In this exercise you will find out how much one
wild value can hurt, what each defence costs when the data are well behaved, and
build up from the median to a regression line that is hard to fool. Use
simulated data throughout, so that you always know the truth. Work through the
[notebook](simulation.ipynb) alongside the stages below, using seeded random
generators so that your results are reproducible.

## Stage 1: From mean to median

> **Check:** `uv run pytest exercises/no_median_feat/test_robust.py -k trimmed_mean -q`

The mean uses every value fully. The median uses only the middle one. Between
them lies a whole family: the **trimmed mean** sorts the values, discards a
proportion from each end, and averages what is left.

Implement `trimmed_mean(values, proportion)` in [robust.py](robust.py). A
proportion of 0 is the ordinary mean; as the proportion approaches 0.5 the
result approaches the median.

In [notebook section 1](simulation.ipynb#1.-One-bad-number), glitch clean
normal data by knocking an increasing fraction of the values far off course. The
supplied `glitch` helper in [simulation.py](simulation.py) does this, and lets
you choose how big the glitches are, which way they go and where they land. Plot
the error of the mean, two trimmed means and the median against the fraction
glitched. Predict the plot first. Roughly how much contamination can each
estimator take before it is dragged away? Then, in [section
2](simulation.ipynb#2.-The-price-of-protection), compare the estimators on
samples from several kinds of data. The supplied `sample` helper in
[simulation.py](simulation.py) yields normal, skewed (exponential) or
heavy-tailed (`t`) samples, with or without glitches, and `simulate` (used in
Stage 3) shares its noise options. Start with *clean* normal data and compare
how much each estimator varies from sample to sample. Who wins when nothing goes
wrong? Then change the data and see whether the answer, and the standard error
alone, still tells you what you need to know.

<details>
<summary>💡 Hint: measuring “how much it varies”</summary>

Draw a few thousand samples, compute each estimator on every sample, and take
the standard deviation of those estimates. That is the standard error from
[Known unknowns](../known_unknowns/README.md), found by brute force.

</details>

<details>
<summary>What did you discover?</summary>

Each estimator has a **breakdown point**: the fraction of wild values it can
survive. The mean has a breakdown point of 0, because one wild value is enough.
A trimmed mean survives up to the fraction it trims, and the median, at 50%, is
as robust as an estimator can be.

On clean normal data the ranking reverses. The mean has the smallest standard
error, and the median's is about 25% larger: you would need roughly 57% more
data (a factor of $\pi/2$) for the median to match the mean. A trimmed mean sits
in between. Robustness is insurance, and insurance costs a premium.

Change the data and the picture changes with it. With heavy-tailed data the
premium disappears: the mean becomes the least precise estimator, and the robust
ones win outright. With skewed data the robust estimators are more precise but
*biased*, because the median and trimmed means estimate the typical value, not
the average. And with a few glitches pushing the same way, the standard errors
barely change at all while the mean is shifted by the average size of the
glitches. A standard error measures how much an estimate varies, not how far
off it is, so look at the bias as well.

</details>

## Stage 2: A robust spread

> **Check:** `uv run pytest exercises/no_median_feat/test_robust.py -k "mad or outliers" -q`

The standard deviation has the same weakness as the mean. A robust alternative
is the **median absolute deviation** (MAD): the median of
$|x_i - \mathrm{median}(x)|$.

Implement `mad(values, scale=True)`. With `scale=True`, multiply the result by a
constant so that, for normal data, it estimates the same quantity as the
standard deviation. Work out what that constant must be (a normal distribution's
MAD is $\Phi^{-1}(0.75)\,\sigma$, where $\Phi^{-1}$ is the normal quantile
function) and check it against the tests.

Then implement `flag_outliers(values, threshold=3.5)`, which marks values more
than `threshold` scaled MADs from the median.

A caveat the tests do not cover: if more than half of the values are identical
(a sensor stuck on one reading, or counts with many ties), the MAD is 0, and
every value that differs from the median, however slightly, is more than
`threshold` MADs away. Try it. What would you want `flag_outliers` to do in that
case, and what would you report to the person who gave you the data?

In [notebook section
3](simulation.ipynb#3.-Can-the-three-sigma-rule-see-outliers?),
take a sample of ten sensible measurements and then add a couple of absurd
ones. The familiar rule says to distrust anything more than three standard
deviations from the mean. Does it catch your absurd values? Try a few sample
sizes and positions for the outliers, then compare with `flag_outliers`.

<details>
<summary>💡 Hint: if the rule misses something</summary>

Look at the standard deviation you divided by. Where did the outliers go when
you calculated it?

</details>

<details>
<summary>What did you discover?</summary>

The outliers **mask** themselves. They inflate the mean and, much more, the
standard deviation, so the very values that should stand out sit comfortably
inside "3σ". There is even a hard limit: in a sample of $n$ values, no value can
lie more than $(n-1)/\sqrt{n}$ sample standard deviations from the mean, which
is about 2.85 when $n = 10$. With ten values, the 3σ rule *cannot* flag
anything.

The median and MAD barely notice the outliers, so the robust rule measures
everyone against an honest yardstick. The threshold of 3.5 is the value
suggested by Iglewicz and Hoaglin for their “modified z-score”, which is the
same calculation written with a different constant.

</details>

## Stage 3: A robust line

> **Check:** `uv run pytest exercises/no_median_feat/test_robust.py -k theil_sen -q`

A least-squares line is a kind of mean, so it inherits the mean's weakness. The
**Theil–Sen** estimator applies the median idea to regression:

- the slope is the median of the slopes between *every pair* of points;
- the intercept is the median of $y_i - \text{slope}\cdot x_i$.

Implement `theil_sen(x, y)`, returning a `LineFit`. It needs no optimiser and no
probability model, just medians.

In [notebook section 4](simulation.ipynb#4.-A-robust-line), simulate a
noisy straight line, glitch a few points and fit it with least squares
(`numpy.polyfit`) and with `theil_sen`. The supplied `simulate` helper in
[simulation.py](simulation.py) yields as many noisy datasets as you ask for,
with normal or skewed noise and optional glitches. Use repeated simulation to
compare the *slope* estimates under three kinds of data: clean normal noise,
normal noise with glitches, and skewed noise. Look at the *intercept* too when
the noise is skewed (but has mean zero), and predict what each method will
estimate before you check.

In [section 5](simulation.ipynb#5.-Where-it-breaks), find out where Theil–Sen
breaks. Glitch a growing fraction of the points and plot the slope error. How
much contamination can it take, and does it matter where the glitches are?

<details>
<summary>💡 Hint: all the pairs</summary>

For $n$ points there are $n(n-1)/2$ pairs. A Python loop is fine for 30 points.
For a faster version, `numpy.triu_indices(n, k=1)` gives the indices of every
pair at once. Think about what should happen to a pair of points with the same
$x$.

</details>

<details>
<summary>What did you discover?</summary>

With glitches, the least-squares slope is dragged around while the Theil–Sen
slope barely moves: a glitch spoils only the pairs it belongs to, so the median
of all the pairs is untouched until a large fraction are spoiled. The breakdown
point is about 29% of the points, $1 - 1/\sqrt{2}$, but that is a *worst case*:
all the glitches at one end, all pushing the same way, so that every pair mixing
a glitch with a good point is wrong in the same direction, and half the pairs
are mixed when 29% are glitched. Glitches at random positions are far less
harmful, because the wrong slopes fall on both sides of the true one and
largely cancel in the median.

On clean normal data Theil–Sen gives up a little: its slope varies somewhat
more than least squares (about 5% more variance for large samples), a small
premium compared with the median's.

With skewed noise both slopes are unbiased, and Theil–Sen is actually *more*
precise, because the long tail of large errors hurts a method built on means
more than one built on medians. The Theil–Sen intercept, however, is biased. The
median of skewed errors is not their mean, so Theil–Sen estimates a line through
the *typical* point, while least squares estimates one through the *average*
point. Neither is wrong, but they answer different questions, and you should
know which one you want.

This also connects to [A likely story](../a_likely_story/README.md), where
Student-$t$ noise gave a robust fit by describing the glitches with a
probability model. Theil–Sen resists them without a model at all.

</details>

## Extensions 🚀

- Vectorise `theil_sen` with `numpy.triu_indices`, and time it against a loop as
  the number of points grows. How does the cost scale?
- Put a bootstrap confidence interval on the Theil–Sen slope (see [Known
  unknowns](../known_unknowns/README.md)). Does the interval keep its promise
  under glitches?
- Compare your results with `scipy.stats.theilslopes` and with the Student-$t$
  fit from [A likely story](../a_likely_story/README.md).
- Explore the other glitch settings in `simulate`: `where="end"` and
  `direction="down"` or `"both"`. When are glitches least harmful, and why?
- Glitch the *x* values instead of the *y* values (apply `glitch` to `x`). Which
  method copes?
- Implement Siegel's repeated medians, which has a breakdown point of about 50%.

## Further reading

- [Theil–Sen estimator](https://en.wikipedia.org/wiki/Theil%E2%80%93Sen_estimator)
  on Wikipedia, which also covers its breakdown point and efficiency.
- [Median absolute deviation](https://en.wikipedia.org/wiki/Median_absolute_deviation)
  on Wikipedia, including the scale constant.
- [Robust statistics](https://en.wikipedia.org/wiki/Robust_statistics) on
  Wikipedia, for breakdown points and efficiency.
