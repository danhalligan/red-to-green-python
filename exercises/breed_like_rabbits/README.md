# Breed like rabbits 🐇

> **Difficulty:** 🌶️
>
> **Before you start:** basic Python and NumPy, and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** iterating a function, NumPy arrays and broadcasting, and
> plotting many simulations at once.
>
> **Check:** `uv run pytest exercises/breed_like_rabbits/ -q`

A few rabbits are let loose in a field. Each spring they breed, so the more
rabbits there are, the more there will be next year. But the field is only so
big: the more crowded it gets, the more rabbits starve.

We can model each generation using two numbers: `x`, the fraction of the field's
carrying capacity that is filled, from 0 (no rabbits) to 1 (a full field), and
`r`, the breeding rate. The population next season is:

```text
x_next = r * x * (1 - x)
```

In this model `r * x` gives us more rabbits in the next generation depending on
the breeding rate (`r`), and `(1 - x)` stops the field getting too crowded.

The rule is a single line, so you'll probably expect the population to behave
simply. Your job is to simulate it, then find out.

## Stage 1: One season at a time

> **Check:** `uv run pytest exercises/breed_like_rabbits/test_rabbits.py -k "test_breed or empty_and_full" -q`

In [rabbits.py](rabbits.py), implement `breed` for one breeding season. It
should also work on whole arrays of populations and breeding rates at once. The
docstring gives the details, and the tests check known cases.

Then open the [rabbit notebook](investigate.ipynb) and work through section 1.
Don't just run it: predict, then experiment. Start from 0.5 and apply `breed`
over and over for a few breeding rates. What do the rabbits settle into, and how
does that depend on `r`?

## Stage 2: Skipping to the long run

> **Check:** `uv run pytest exercises/breed_like_rabbits/test_rabbits.py -k "not test_breed and not empty_and_full" -q`

The early seasons are just the rabbits finding their feet. To compare breeding
rates we want the settled population size, so implement `simulate_seasons` to
follow the rabbits for many seasons. It should use NumPy to simulate many
breeding rates at once. Its `discard` option runs some seasons first without
recording them, so only the settled populations are returned.

<details>
<summary>Hint 1: nudge</summary>

`simulate_seasons` can take an array of breeding rates. If `breed` works
elementwise, one call can advance the population for every rate for one season.

</details>

<details>
<summary>Hint 2: strategy</summary>

Keep one array holding the current population for every breeding rate. Loop over
seasons, updating that array each season. Run the discarded seasons first,
without storing them, then start recording.

</details>

<details>
<summary>Hint 3: implementation guidance</summary>

Make a preallocated array of shape `(seasons + 1, *rates.shape)` with
`np.empty`, set its first row to `start`, then fill each later row from the one
before: `population[season + 1] = breed(population[season], rates)`. A single
breeding rate has shape `()`, so this also gives `(seasons + 1,)`.

</details>

Check your function against your plots in section 2 of the notebook.

## Investigate

With both functions working, return to the notebook (sections 3 to 5). Predict,
then experiment.

1. Simulate thousands of breeding rates between 2.5 and 4, discard the early
   seasons while the population settles, and plot what is left against `r`. How
   does the settled population change as the breeding rate changes?
2. Start two fields with populations that differ by one part in a billion. How
   do they compare after a while? Does the answer depend on `r`?
3. Zoom in on anything interesting in your plot from the first question.

When you have an explanation, compare it with the one below.

<details>
<summary>What did you discover?</summary>

For small `r` the rabbits die out. Above `r = 1` they settle at a steady
population, which rises with `r`. Around `r = 3` the steady population splits
into a two-year cycle, then a four-year cycle, then eight, with each doubling
arriving sooner than the last. Past `r ≈ 3.57` the pattern never repeats and the
population looks random, even though the rule is simple and has no randomness in
it. This is deterministic chaos.

In the chaotic regime, tiny differences in the starting population are amplified
every season, so two nearly identical fields soon diverge completely. That is
why forecasting such systems is hard beyond a few seasons. The plot is not
merely noise, though: it has clear structure and repeats itself at smaller
scales. Chaos is interrupted by "windows" of order, such as the period-three
window near `r ≈ 3.83`, and each window contains its own period-doubling route
back into chaos.

This plot is closely related to a one-dimensional slice of the Mandelbrot set.
Replace `x` by a suitably scaled and shifted version and the rabbit rule becomes
`z → z² + c`, the iteration that defines the Mandelbrot set. The bifurcation
diagram is what you see along the real axis of the Mandelbrot set, from its tip
at `c = 1/4` to `c = -2`.

</details>
