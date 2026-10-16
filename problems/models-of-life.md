# Models of Life 🌿

[← All problems](../README.md#index-of-problems)

These two small simulations explore how systems change over time. Game of Life
is deterministic: the board and rules determine each next generation. Dawkins'
weasel is stochastic: random mutation and selection mean repeated runs can
differ. Both are simplified models and are interesting in unique ways.

**In this topic:** [Conway's Game of Life](#conways-game-of-life-) ·
[Dawkins' weasel](#dawkins-weasel-). The two exercises are independent.

## Conway's Game of Life 🔫

> **Before you start:** basic Python and NumPy, and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** NumPy arrays and slicing, neighbourhood calculations,
> and simulating a cellular automaton.
>
> **Check:** `uv run pytest tests/test_game_of_life.py -q`

Conway's Game of Life is a cellular automaton: a grid of live and dead cells
changes in discrete generations according to local rules. The rules fit in a
paragraph. What they produce does not. Your job is to write the engine; the
reward is watching what it does.

For each cell, inspect its eight neighbouring positions. Follow these rules:
1. A live cell survives with two or three live neighbours
2. A dead cell becomes live with exactly three;
3. All other cells are dead in the next generation. 

This exercise uses finite, bounded arrays rather than wrapping edges, so cells
outside the board are not counted.

In [game_of_life.py](../src/pyproblems/game_of_life.py), implement
`count_live_neighbors` and `step_game_of_life` with NumPy arrays; the docstrings
give the details. Consider shifted array slices or padding to vectorise the local
counts without accidentally wrapping edges. Everything else is provided:
readable patterns in
[game_of_life_shapes.yaml](../src/pyproblems/datasets/game_of_life_shapes.yaml)
(`O` for live cells, `.` for empty ones), `load_shape` and `place_shape` to put
one on a board, `render_board` to print it, and `animate_boards` to watch it
move, so you can focus on the algorithm.

When the tests pass, open the [Game of Life notebook](../analysis/game_of_life.ipynb).
Start with the glider, then try the "Gosper Glider Gun". The last test, which
counts how a 36-cell pattern grows over time, is the check that you have built
it.

## Dawkins' weasel 🦦

> **Before you start:** basic Python and NumPy, and the optional scientific stack
> (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** random number generators, stochastic simulation, and
> investigating a model by experiment.
>
> **Check:** `uv run pytest tests/test_evolution.py -m advanced -q`

Start with 28 random characters. Copy them with the odd typo, keep the best copy,
and repeat. Can a sentence evolve out of gibberish? In *The Blind Watchmaker*,
Richard Dawkins used a simple computer model like this to show how cumulative
selection can build something that looks designed. The target here is the
28-character
phrase `METHINKS IT IS LIKE A WEASEL`; each position is chosen from the 26
uppercase letters and a space. Start with a uniformly random phrase. Make a
population of ten copies by independently leaving each character unchanged with
probability 0.99, or mutating it with probability 0.01 to one of the *other*
26 symbols. Score a phrase by the number of positions matching the target,
and choose a highest-scoring copy as the parent of the next generation. Break
ties at random. For reproducibility in this Python version, retain the best
candidate seen so far and inject a NumPy random generator.

Implement `matching_characters`, `mutate_message`, and `evolve_weasel` in
[evolution.py](../src/pyproblems/evolution.py). Each generation creates a fixed
number of mutated copies, keeps a highest-scoring candidate, and records the
best score. Then watch it evolve.

Use the [weasel simulation notebook](../analysis/weasel_simulation.ipynb) to
investigate. How many generations does it take to reach the target? Compare
several seeded runs rather than treating one random run as a universal answer,
and ask why they differ. Then try a population of 100, and several mutation
rates. What happens if the mutation rate is very low, or very high? Which is
best, and why?

**Comparison 🚀: evolution versus guessing.** Give a baseline the same budget.
If an evolving run scored `population_size * generations` phrases, generate that
many completely independent random phrases and keep the best score so far. Predict
the outcome first, then plot both best-score-so-far curves against the number of
phrases scored. Which gets closer to the target, and by how much?

> [!NOTE]
> The weasel is a deliberately simplified model. It has a fixed target that
> real evolution never has, a score that rewards each correct letter separately,
> and no recombination or changing environment. It shows that selection that
> *keeps* partial progress is far more powerful than chance alone; it does not
> show that evolution is aiming at anything.

How good a model of evolution in nature is this? Consider the known target, the
simple mutation process, and selection based on one fixed score.

**Extension 🚀: why does cumulative selection work?** Explain what you saw with
probability, in the notebook's optional final section:

1. How many possible 28-character phrases are there? What is the probability
   that a random phrase has at least one correct position, and exactly one?
2. If no position currently matches, what is the probability that at least one
   of ten offspring gains a correct position?
3. Once 18 positions match, what must happen at each of the remaining ten
   positions for one offspring to match the entire target? What is the chance
   that any of ten offspring does so?
4. Use your answers to explain the gap you saw in the comparison with
   independent random guessing.

<details>
<summary>💡 Hint: a useful trick for question 2</summary>

Use the complement rule: it is easier to find the probability that *none* of the
ten offspring gains a correct position. For small $x$ and large $n$, the
approximation $(1-x)^n\approx e^{-nx}$ can simplify the calculation.

</details>

<details>
<summary>💡 Hint: tiny probabilities in question 3</summary>

Beware that `1 - (1 - p) ** n` rounds to zero when $p$ is tiny;
`-np.expm1(n * np.log1p(-p))` keeps the small positive value.

</details>

## Where next?

- **Analyse real data:** [Data Analysis](data-analysis.md) and
  [Scientific Python](scientific-python.md) use the same scientific stack.
- **Fit models to data:** [Statistical Modelling](statistical-modelling.md)
  is the most advanced topic.
- **Algorithms:** [Algorithms and Search](algorithms-and-search.md).
- **More simulation:** [Against the Odds](against-the-odds.md) uses simulation to
  test your intuition about probability.
- Return to the [routes](../README.md#choosing-a-route).
