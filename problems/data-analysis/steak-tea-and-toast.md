# Steak, Tea, and Toast

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** cleaning ordered categories, exploring associations,
> and judging evidence while accounting for multiple comparisons.
>
> **Check:** your notebook's plots, summaries and explanations; no automated tests.

Do people who burn their toast also like well-done steaks? Is there any
relationship between how people take their tea and their other preferences? A
simple dataset compiled from the results of a Facebook poll lets you find out.

![Steak, toast, and tea poll response scales](../../assets/steak-toast-tea-poll.png)

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

Work through the [Steak, Tea, and Toast notebook](../../analysis/steak_tea_toast.ipynb):
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
