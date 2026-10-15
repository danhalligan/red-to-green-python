# Data Analysis

[← All problems](../README.md#index-of-problems)

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md) and the
> optional scientific stack (`uv sync --all-groups --extra science`). Q3 also
> needs `ols_coefficients` from
> [Scientific Python Q2](scientific-python.md#q2-linear-models-and-ordinary-least-squares).
>
> **You’ll practise:** exploring and plotting data, cleaning and summarising
> ordered categories, testing for association, and fitting and criticising a
> simple regression.
>
> **Check:** `uv run pytest tests/test_statistics.py -k "summarize_xy or ols" -q`
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

**Next on Route 2:** [Scientific Python Q1](scientific-python.md#q1-sampling-variation-and-standard-error),
[Q2](scientific-python.md#q2-linear-models-and-ordinary-least-squares) and
[Q4](scientific-python.md#q4-bootstrap-standard-error), before returning to
[Q2](#q2-categorical-data-steak-tea-and-toast) and
[Q3](#q3-linear-regression-predicting-the-next-old-faithful-eruption) here.

## Q2. Categorical data: Steak, Tea, and Toast

This package includes a simple dataset compiled from the results of a
Facebook poll.

![Steak, toast, and tea poll response scales](../assets/steak-toast-tea-poll.png)

The data are available in `src/pyproblems/datasets/steak_toast_tea.csv`. Each
row is one response and the three columns use the labels shown in the image:

- `Steak`: intended values 1 (rarest) to 5 (most well done)
- `Toast`: 1 (lightest) to 6 (most burnt)
- `Tea`: `a` (darkest) to `f` (milkiest)

These are ordered categories. The source also contains some missing responses
and several values outside the displayed scales. Audit every column to find them
all. Keep the raw data unchanged, then make a cleaned copy, and explain any
decision about these observations instead of silently discarding or altering
them. Several policies are defensible;[^cleaning-policy] pick one but consider
the implications.

[^cleaning-policy]: For example, treat them as missing, or keep half-step
    values as extra ordered levels. Either choice changes the denominators and
    the contingency tables, so make it explicit. The decision might depend
    on what analyses you plan to do.

Complete the first investigation in the
[Steak, Tea, and Toast notebook](../analysis/steak_tea_toast.ipynb): inspect
row counts, column types, category levels, and missing counts; make ordered
categoricals; calculate frequency and proportion tables; and visualise
contingency tables for two pairs of questions. State the denominator of every
proportion, and whether you used all rows for each variable or only complete
pairs; select complete rows explicitly before cross-tabulating.

You can now try to test for any statistical associations between the questions.

💡 Hint if you're stuck [^association-hint]

[^association-hint]: To test for association between a pair of questions, you
    could use a Spearman rank correlation (`scipy.stats.spearmanr`), which gives
    both a correlation and a p-value. A chi-squared test of independence would
    ignore the ordering and, with tables as large as 5 by 6, spread its power
    across many degrees of freedom. Because Spearman uses only ranks, any
    increasing coding of the levels gives the same answer. Note that since we
    test every pair of columns there is a risk of at least one false positive,
    and we should probably adjust for the risk (for example, a Bonferroni
    correction) or at least report it. You could also consider Kendall's
    $\tau_b$ (`scipy.stats.kendalltau`) and with a permutation-test p-value
    (`scipy.stats.permutation_test`), both of which deal with the many ties in
    these data differently.

## Q3. Linear regression: predicting the next Old Faithful eruption

Visitors to Old Faithful geyser want to know how long they will wait for the
next eruption. `load_faithful_data()` in [data.py](../src/pyproblems/data.py)
provides each eruption's duration and the waiting time until the following one,
both in minutes.

In the [Old Faithful notebook](../analysis/old_faithful.ipynb), fit a straight line
predicting the waiting time from the eruption duration, using `ols_coefficients`
with an intercept column. Interpret the intercept and slope in minutes,
calculate $R^2$, and predict the wait after a 2-minute and a 4-minute eruption.
Plot the data with the fitted line, and plot the residuals against the fitted
values.

The line has a decent $R^2$, but is it a good model? Look at both plots and
think about what the residuals are telling you. We will come back to this data
in the
[multivariate Gaussian EM](statistical-modelling.md#multivariate-gaussian-em)
exercise, where a mixture of two clusters explains why a single straight line
describes it poorly.

## Where next?

- **Explain the poor fit:** [Statistical Modelling](statistical-modelling.md)
  fits mixtures to this same Old Faithful data. It is optional and challenging
  (😱), and needs
  [Scientific Python Q5](scientific-python.md#q5-likelihood-and-normal-maximum-likelihood-estimation).
- **If you skipped them:** [Scientific Python](scientific-python.md) covers
  standard errors, the bootstrap and likelihood, which this topic uses.
- **Simulation:** [Models of Life](models-of-life.md).
- Return to the [routes](../README.md#choosing-a-route).
