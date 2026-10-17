# Predicting Old Faithful

> **Before you start:** basic Python and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** fitting and interpreting regression, prediction,
> and checking residuals.
>
> **Check:** your notebook's plots, predictions and explanations; no automated tests.

Visitors to Old Faithful geyser want to know how long they will wait for the
next eruption. `load_faithful_data()` in [data.py](../../src/pyproblems/data.py)
provides each eruption's duration and the waiting time until the following one,
both in minutes.

In the [Old Faithful notebook](../../analysis/old_faithful.ipynb#Waiting-time-prediction), fit a straight
line predicting the waiting time from the eruption duration, for example with
`numpy.polyfit` or `scipy.stats.linregress`. Interpret the intercept and slope in
minutes, calculate $R^2$, and predict the wait after a 2-minute and a 4-minute
eruption. Plot the data with the fitted line, and plot the residuals against the
fitted values.

The line has a decent $R^2$, but is it a good model? Look at both plots and
think about what the residuals are telling you. What do you notice about the
data itself? Hold that thought: you can come back to this data in the
[multivariate Gaussian EM](../statistical-modelling/expectation-maximisation.md#multivariate-gaussian-em)
exercise.
