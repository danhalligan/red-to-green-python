# Data Analysis

[← All problems](../README.md#index-of-problems)

> **Before you start:** basic Python and the
> optional scientific stack (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** exploring and plotting data, cleaning and summarising
> ordered categories, judging whether a relationship is convincing, and fitting
> and criticising a simple regression.
>
> **Check:** `uv run pytest tests/test_statistics.py -k summarize_xy -q`
> checks the functions; the notebook analyses are checked by your own plots and
> explanations.

**In this topic:** [Q1 Mysterious data](#q1-mysterious-data-) ·
[Q2 Steak, Tea, and Toast](#q2-categorical-data-steak-tea-and-toast) ·
[Q3 Old Faithful regression](#q3-linear-regression-predicting-the-next-old-faithful-eruption)

## Q1. Mysterious data 🤔

Thirteen coordinate datasets are packaged under neutral names. In the
[mysterious data notebook](../analysis/mysterious_data.ipynb), implement
`summarize_xy` and `summarize_xy_datasets` in
[statistics.py](../src/pyproblems/statistics.py), then compare their means,
sample standard deviations, and Pearson correlations.

Based only on those summaries, note which datasets seem interchangeable and
record your prediction.

Next, plot all 13 datasets with shared axis limits. Do the plots support your
prediction? Describe the patterns you observe and explain why you should inspect
data before choosing a model.

```bash
uv run pytest tests/test_statistics.py -k summarize_xy
```

**Next on Route 2:** [Scientific Python Q1](scientific-python.md#q1-how-uncertain-is-an-average)
and [Q3](scientific-python.md#q3-two-methods-two-answers), before returning to
[Q2](#q2-categorical-data-steak-tea-and-toast) and
[Q3](#q3-linear-regression-predicting-the-next-old-faithful-eruption) here.

## Q2. Categorical data: Steak, Tea, and Toast

Do people who burn their toast also like well-done steaks? Is there any
relationship between how people take their tea and their other preferences? A
simple dataset compiled from the results of a Facebook poll lets you find out.

![Steak, toast, and tea poll response scales](../assets/steak-toast-tea-poll.png)

The data are available in `src/pyproblems/datasets/steak_toast_tea.csv`. Each
row is one response and the three columns use the labels shown in the image:

- `Steak`: intended values 1 (rarest) to 5 (most well done)
- `Toast`: 1 (lightest) to 6 (most burnt)
- `Tea`: `a` (darkest) to `f` (milkiest)

Before you look at any data, write down your predictions. Then explore the data
and decide whether any apparent relationship is convincing.

First, though, real responses are messy. These are ordered categories, and the
source also contains some missing responses and several values outside the
displayed scales. Audit every column to find them all. Keep the raw data
unchanged, then make a cleaned copy, and explain any decision about these
observations instead of silently discarding or altering them. Several policies
are defensible;[^cleaning-policy] pick one but consider the implications.

[^cleaning-policy]: For example, treat them as missing, or keep half-step
    values as extra ordered levels. Either choice changes the denominators and
    the contingency tables, so make it explicit. The decision might depend
    on what analyses you plan to do.

Work through the [Steak, Tea, and Toast notebook](../analysis/steak_tea_toast.ipynb):
audit the data, make ordered categoricals, then investigate your questions with
whatever tables and plots help you judge. State the denominator of every
proportion, and whether you used all rows for each variable or only complete
pairs; select complete rows explicitly before cross-tabulating.

Finally, ask whether what you found is convincing. There are only 79 responses,
and you are comparing several pairs of questions at once. Did your predictions
survive?

<details>
<summary>💡 Hint 1: a nudge</summary>

The answers are ordered categories, so a way of measuring association should
respect the order. Which table or plot shows how two ordered questions go
together at a glance?

</details>

<details>
<summary>💡 Hint 2: a strategy</summary>

A rank correlation (`scipy.stats.spearmanr`) measures how consistently one
variable rises with another, and gives both a correlation and a p-value. A
chi-squared test of independence would ignore the ordering and, with tables as
large as 5 by 6, spread its power across many degrees of freedom. Because
Spearman uses only ranks, any increasing coding of the levels gives the same
answer.

</details>

<details>
<summary>💡 Hint 3: the risks of looking at everything</summary>

Since we test every pair of columns there is a risk of at least one false
positive, and we should probably adjust for the risk (for example, a Bonferroni
correction) or at least report it. You could also consider Kendall's $\tau_b$
(`scipy.stats.kendalltau`) and a permutation-test p-value
(`scipy.stats.permutation_test`), both of which deal with the many ties in these
data differently.

</details>

## Q3. Linear regression: predicting the next Old Faithful eruption

Visitors to Old Faithful geyser want to know how long they will wait for the
next eruption. `load_faithful_data()` in [data.py](../src/pyproblems/data.py)
provides each eruption's duration and the waiting time until the following one,
both in minutes.

In the [Old Faithful notebook](../analysis/old_faithful.ipynb), fit a straight
line predicting the waiting time from the eruption duration, for example with
`numpy.polyfit` or `scipy.stats.linregress`. Interpret the intercept and slope in
minutes, calculate $R^2$, and predict the wait after a 2-minute and a 4-minute
eruption. Plot the data with the fitted line, and plot the residuals against the
fitted values.

The line has a decent $R^2$, but is it a good model? Look at both plots and
think about what the residuals are telling you. What do you notice about the
data itself? Hold that thought: you can come back to this data in the
[multivariate Gaussian EM](statistical-modelling.md#multivariate-gaussian-em)
exercise.

## Where next?

- **Look into the structure:** [Statistical Modelling](statistical-modelling.md)
  fits mixtures to this same Old Faithful data. It is optional and challenging
  (😱), and needs
  [Scientific Python Q4](scientific-python.md#q4-recovering-the-parameters).
- **If you skipped them:** [Scientific Python](scientific-python.md) covers
  standard errors, the bootstrap and likelihood, which this topic uses.
- **Simulation:** [Models of Life](models-of-life.md).
- Return to the [routes](../README.md#choosing-a-route).
