# Mysterious data 🤔

> **Difficulty:** 🌶️
>
> **Before you start:** basic Python and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** summary statistics, correlation, and plotting data
> before choosing a model.
>
> **Check:** `uv run pytest tests/test_statistics.py -k summarize_xy -q`

Thirteen coordinate datasets are packaged under neutral names. In the
[mysterious data notebook](../../analysis/mysterious_data.ipynb), implement
`summarize_xy` and `summarize_xy_datasets` in
[statistics.py](../../src/pyproblems/statistics.py), then compare their means,
sample standard deviations, and Pearson correlations.

Based only on those summaries, note which datasets seem interchangeable and
record your prediction.

Next, plot all 13 datasets with shared axis limits. Do the plots support your
prediction? Describe the patterns you observe and explain why you should inspect
data before choosing a model.

```bash
uv run pytest tests/test_statistics.py -k summarize_xy
```
