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

In this model `r * x` gives us more rabbits in the next generation, and
`(1 - x)` stops the field getting too crowded.

The rule is a single line, so you'll probably expect the population to behave
simply. Your job is to simulate it, then find out.

In [rabbits.py](rabbits.py), implement:

1. `next_population` for one breeding season. It should also work on a whole
   array of populations at once.
2. `simulate_population` to follow the rabbits for many seasons.
3. `long_run_population` to find where the rabbits end up for many breeding
   rates at the same time.

The docstrings give the details, and the tests check known cases.

<details>
<summary>Hint 1: nudge</summary>

`long_run_population` takes an array of breeding rates. If `next_population`
works elementwise, one call can advance the population for every rate for one
season.

</details>

<details>
<summary>Hint 2: strategy</summary>

Keep one array holding the current population for every breeding rate. Loop over
seasons, not over rates. Update that array each season, throw away the burn-in,
then store the next `keep` seasons.

</details>

<details>
<summary>Hint 3: implementation guidance</summary>

Start with `np.full(rates.shape, start)`. For the seasons you keep, write each new
population array into one column of a preallocated array of shape
`(*rates.shape, keep)` using `kept[..., season] = population`. That also gives
`(keep,)` for a single breeding rate.

</details>

## Investigate

When the tests pass, open the [rabbit notebook](investigate.ipynb). Don't just
run it: predict, then experiment.

1. Simulate a few breeding rates and plot the populations against season. What
   do the rabbits settle into, and how does that depend on `r`?
2. Start two fields with populations that differ by one part in a billion. How
   do they compare after a while? Does the answer depend on `r`?
3. Plot the long-run population against the breeding rate for `r` between 2.5
   and 4. Then zoom in on anything interesting.

When you have an explanation, compare it with the one below.

<details>
<summary>What did you discover?</summary>

For small `r` the rabbits die out. Above `r = 1` they settle at a steady
population, which rises with `r`. Around `r = 3` the steady population splits into
a two-year cycle, then a four-year cycle, then eight, with each doubling arriving
sooner than the last. Past `r ≈ 3.57` the pattern never repeats and the population
looks random, even though the rule is simple and has no randomness in it. This is
deterministic chaos.

In the chaotic regime, tiny differences in the starting population are amplified
every season, so two nearly identical fields soon diverge completely. That is why
forecasting such systems is hard beyond a few seasons. The plot is not merely
noise, though: it has clear structure and repeats itself at smaller scales.
Chaos is interrupted by "windows" of order, such as the period-three window near
`r ≈ 3.83`, and each window contains its own period-doubling route back into
chaos.

This plot is closely related to a one-dimensional slice of the Mandelbrot set.
Replace `x` by a suitably scaled and shifted version and the rabbit rule becomes
`z → z² + c`, the iteration that defines the Mandelbrot set. The bifurcation
diagram is what you see along the real axis of the Mandelbrot set, from its tip
at `c = 1/4` to `c = -2`.

</details>
