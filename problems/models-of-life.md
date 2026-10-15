# Models of Life 🌿

[← All problems](../README.md)

These two small simulations explore how systems change over time. Game of Life
is deterministic: the board and rules determine each next generation. Dawkins'
weasel is stochastic: random mutation and selection mean repeated runs can
differ. Both are simplified models and are interesting in unique ways.

## Conway's Game of Life 🔫

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md) and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** NumPy arrays and slicing, neighbourhood calculations,
> and simulating a cellular automaton.
>
> **Check:** `uv run pytest tests/test_game_of_life.py -q`

Conway's Game of Life is a cellular automaton: a grid of live and dead cells
changes in discrete generations according to local rules. Despite the simple
rules, repeated updates can produce still lifes, oscillators, and patterns
that move across the board.

For each cell, inspect its eight neighbouring positions. A live cell survives
with two or three live neighbours; a dead cell becomes live with exactly three;
all other cells are dead in the next generation. This exercise uses finite,
bounded arrays rather than wrapping edges, so cells outside the board are not
counted.

In [game_of_life.py](../src/pyproblems/game_of_life.py), implement
`count_live_neighbors` and `step_game_of_life` with NumPy arrays; the docstrings
give the details. The glider, lightweight/middleweight/heavyweight
spaceships, and Gosper glider gun are provided as readable rows in
[game_of_life_shapes.yaml](../src/pyproblems/datasets/game_of_life_shapes.yaml);
`load_shape(name)` and `render_board` are already implemented. Rows use `O`
for live cells and `.` for empty cells. Focus on the
neighbour-count and generation-update algorithms. Consider shifted array slices
or padding to vectorise the local counts without accidentally wrapping edges.

In the [Game of Life notebook](../analysis/game_of_life.ipynb), place a pattern
inside a larger empty board, iterate many generations, and animate the frames.
The supplied patterns are starting
conditions, not additional implementation tasks.

## Dawkins' weasel 🦦

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md) and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** random number generators, stochastic simulation, and
> probability reasoning.
>
> **Check:** `uv run pytest tests/test_evolution.py -m advanced -q`

In *The Blind Watchmaker*, Richard Dawkins used a simple computer model to
illustrate cumulative selection. The target here is the 28-character phrase
`METHINKS IT IS LIKE A WEASEL`; each position is chosen from the 26 uppercase
letters and a space. Start with a uniformly random phrase. Make a population
of ten copies by independently leaving each character unchanged with
probability 0.99, or mutating it with probability 0.01 to one of the *other*
26 symbols. Score a phrase by the number of positions matching the target,
and choose a highest-scoring copy as the parent of the next generation. Break
ties at random. For reproducibility in this Python version, retain the best
candidate seen so far and inject a NumPy random generator.

Before simulating, work through the probability questions in the
[weasel simulation notebook](../analysis/weasel_simulation.ipynb):

1. How many possible 28-character phrases are there? What is the probability
  that a random phrase has at least one correct position, and exactly one?
2. If no position currently matches, use the complement rule to find the
  probability that at least one of ten offspring gains a correct position.
  For small $x$ and large $n$, the approximation
  $(1-x)^n\approx e^{-nx}$ can simplify the calculation.
3. Once 18 positions match, what must happen at each of the remaining ten
  positions for one offspring to match the entire target? What is the chance
  that any of ten offspring does so? Beware that `1 - (1 - p) ** n` rounds to
  zero when $p$ is tiny; `-np.expm1(n * np.log1p(-p))` keeps the small
  positive value.
4. Which assumptions make this a poor model of evolution in nature? Consider
  the known target, the simple mutation process, and selection based on one
  fixed score.

Then implement `matching_characters`, `mutate_message`, and `evolve_weasel` in
[evolution.py](../src/pyproblems/evolution.py). Each generation creates a fixed
number of mutated copies, keeps a highest-scoring candidate, and records the
best score. Use the [weasel simulation notebook](../analysis/weasel_simulation.ipynb)
to investigate time to target and how the mutation rate affects convergence
for a population of 100. Compare several
seeded runs rather than treating one random run as a universal answer.
