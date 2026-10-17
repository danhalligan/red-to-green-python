# Red to Green: Python problems from FizzBuzz to mixture models

## Introduction

Welcome! This is a collection of Python puzzles that begin *red* and end
*green*. Most functions start as stubs whose tests fail, and your job is to turn
them green ✅.

Problems run from FizzBuzz-sized warm-ups to data analysis, simulation,
algorithms and statistical modelling, and along the way you will meet list
comprehensions, generators, recursion, object orientation, test-first
development, refactoring, graph search, maximum likelihood,
expectation-maximisation, probabilities that defy intuition and even a cellular
automaton.

> [!IMPORTANT]
> The purpose of this package is partially to help you learn Python, but is also
> a collection of interesting and hopefully satisfying problems to solve. It is
> not simply about collecting completed solutions. A coding agent could complete
> the exercises for you, but that would miss the point entirely. Writing code,
> investigating failures, and explaining your choices build an understanding of
> Python, statistics and algorithms that remain useful in the age of agentic
> coding. You'll need this understanding to specify requirements, assess
> generated code, spot mistakes, and maintain the result. Consider using agents
> to support your learning with hints, explanations, or reviews of your own
> attempts. Try each problem yourself first, and make sure you can explain and
> test any code you adopt; passing tests alone is not the learning goal.

When working through the problems, look out for these markers:

- 💡 a hint (in a footnote or a collapsible section, sometimes in three levels
  that give away a little more each time)
- 😱 a tricky section
- 🚀 an optional extension.

Some investigations also end with a collapsible **What did you discover?**
section: read it after you have formed your own view.

You do not need to do everything, or to do things in order. Problems range from
a few minutes to several sessions.

For an overview of the repository layout and development setup, see
[DEVELOPMENT.md](DEVELOPMENT.md).

## Getting started

The dev container is ready to use, but not required. For a local setup with the
notebooks and scientific tools, install the complete environment with:

```bash
uv sync --all-groups --extra science
```

Then try a first exercise, for example the quick warm-up
[Q1: Exponentiation](problems/pythonic-python/python-fundamentals.md#q1-exponentiation):

1. Read the prompt, then run its test. It is **expected to fail** at first:

   ```bash
   uv run pytest tests/test_language.py -k exponentiate -q
   ```

2. Implement `exponentiate` in `src/pyproblems/language.py`.
3. Rerun the same command until it passes: that is red to green.
4. Keep going with the Python language problems, or pick any other!

## How to complete an exercise

- Each problem page, linked from the [index](#index-of-problems), opens with
  anything you need beforehand and the test command that checks it. Some pages
  group several related exercises.
- Use the focused test command for the exercise you are working on. Most
  exercises begin as stubs, so their tests are red until you implement them.
  Topic-level commands run every exercise in a topic and are more useful after
  you have completed several.
- Aim to make one small change at a time and rerun the test.
- Look for 💡 hints only when you are stuck, opening one level at a time, and
  try the 🚀 extensions if you want more.
- Notebook analyses (in `analysis/`) have no pass or fail, so they are checked
  by your own plots and explanations.
- The early language exercises use only the Python standard library; scientific
  exercises need the optional science packages installed above.

## Index of problems

Pick a topic that interests you. Each link opens a file under `problems/`;
related exercises in the same file stay together here too. Pythonic Python pages
are under `problems/pythonic-python/`, and algorithms under `problems/algorithms/`.

Difficulty is a rough guide: 🌶️ gentle, 🌶️🌶️ takes some thought,
🌶️🌶️🌶️ challenging. A page may start gently and build up.

If you are new to Python, start with the fundamentals. Otherwise, dip in
wherever you like; the notes below flag useful background, not a required order.

### Pythonic Python

Practise writing clear Python, organising it with classes, and improving it
through tests and refactoring.

- [Python Fundamentals](problems/pythonic-python/python-fundamentals.md) 🌶️:
  short language exercises covering exponentiation, adjacent products, FizzBuzz,
  Fibonacci generators, the first non-repeating character, and Python gotchas.
- [Object-oriented Python](problems/pythonic-python/object-oriented-python.md) 🌶️🌶️:
  build a cast of talking animals, from noisy animals and a silent fox to a
  parrot that learns and a robot. Practise classes, inheritance and polymorphism.
- [Refactoring (Gilded Rose)](problems/pythonic-python/gilded-rose.md) 🌶️🌶️🌶️:
  tame an inherited codebase without breaking its existing behaviour.
  Familiarity with classes helps.
- [Test-first (99 Bottles)](problems/pythonic-python/99-bottles.md) 🌶️🌶️:
  build 99 Bottles one test at a time, then write tests of your own.

### Algorithms and Search

Four self-contained exercises, each with its own page, starter code and tests.
You can start with any of them, but some build on earlier ideas, as shown below.

- [Word ladder](problems/algorithms/word-ladder.md) 🌶️🌶️:
  turn `play` into `game` one letter at a time.
- [...Try, try again](problems/algorithms/rugby.md) 🌶️🌶️:
  count the ways a rugby score could have happened, from recursion to dynamic
  programming. The Fibonacci exercise is useful background.
- [Sudoku solver](problems/algorithms/sudoku-solver.md) 🌶️🌶️🌶️:
  warm up with a checker, then backtrack your way to a solution.
- [Global sequence alignment](problems/algorithms/sequence-alignment.md)
  🌶️🌶️🌶️: align two DNA sequences and discover why brute force cannot scale.
  The rugby problem introduces the dynamic programming ideas used here.

### Data Analysis

Explore data, look for relationships, and question what summaries hide.
These notebook-based exercises use the optional scientific stack.

- [Mysterious data](problems/data-analysis/mysterious-data.md) 🌶️:
  thirteen datasets with matching summaries. What do their plots reveal?
- [Steak, Tea, and Toast](problems/data-analysis/steak-tea-and-toast.md) 🌶️🌶️:
  clean messy survey responses and investigate associations between preferences.
- [Predicting Old Faithful](problems/data-analysis/predicting-old-faithful.md) 🌶️🌶️:
  predict the next eruption with regression, then ask what the line misses.

### Uncertainty and Simulation

Use repeated experiments to find out how much you can trust an estimate.
Basic NumPy, probability and statistics help; the bootstrap and confidence
interval exercises build on standard error.

- [How uncertain is an average?](problems/uncertainty-and-simulation/standard-error.md)
  🌶️🌶️: estimate standard error and test its behaviour across repeated samples.
- [Two methods, two answers](problems/uncertainty-and-simulation/bootstrap.md)
  🌶️🌶️: compare bootstrap and analytic estimates of the same uncertainty.
- [Can you trust a 95% interval?](problems/uncertainty-and-simulation/confidence-intervals.md)
  🌶️🌶️🌶️: measure how often confidence intervals keep their promise.
- [When does the normal approximation fail?](problems/uncertainty-and-simulation/normal-approximation.md)
  🌶️: find when a continuous approximation to a discrete distribution breaks down.

### Statistical Modelling

Choose a model, estimate its parameters, and examine what it misses.
Start with likelihood for a single normal distribution; the mixture exercises
build on it, with covariance matrices needed for multivariate EM.

- [Recovering the parameters](problems/statistical-modelling/recovering-the-parameters.md)
  🌶️🌶️🌶️: fit a normal distribution by maximum likelihood and investigate bias.
- [Fitting a Gaussian mixture](problems/statistical-modelling/gaussian-mixture.md)
  🌶️🌶️🌶️: fit two hidden populations by direct numerical optimisation (optional).
- [Expectation-maximisation](problems/statistical-modelling/expectation-maximisation.md)
  🌶️🌶️🌶️: build hard and soft EM, then fit a bivariate mixture to Old Faithful.

The [Old Faithful notebook](analysis/old_faithful.ipynb) is shared across these
topics: the same data supports questions about uncertainty, prediction and
model choice. Each exercise links to its relevant section.

### Against the Odds

Probability puzzles where your gut is confidently wrong. Predict, simulate,
calculate and explain, using only the Python standard library; the investigations
share a notebook and use the science packages for plots.

- [The office party](problems/against-the-odds/office-party.md) 🌶️:
  how many people before a shared birthday is more likely than not?
- [Waiting for heads](problems/against-the-odds/waiting-for-heads.md) 🌶️🌶️:
  why is waiting for `HH` different from waiting for `HT`?
- [The 100 prisoners](problems/against-the-odds/100-prisoners.md) 🌶️🌶️🌶️:
  find a strategy for a hopeless-looking last chance at freedom.

### Models of Life

Explore how simple rules produce complex behaviour: deterministic cellular
automata and stochastic evolution. Both exercises use NumPy.

- [Conway's Game of Life](problems/models-of-life/game-of-life.md) 🌶️🌶️:
  build a cellular automaton and watch patterns grow and move.
- [Dawkins' weasel](problems/models-of-life/weasel.md) 🌶️🌶️:
  can a sentence evolve out of gibberish through mutation and selection?

## Further Reading 📚

- [The Python Tutorial](https://docs.python.org/3/tutorial/)
- [Python Standard Library](https://docs.python.org/3/library/)
- [pytest documentation](https://docs.pytest.org/)
- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [pandas getting started](https://pandas.pydata.org/docs/getting_started/)
- [SciPy statistics](https://docs.scipy.org/doc/scipy/tutorial/stats.html)
- [statsmodels User Guide](https://www.statsmodels.org/stable/user-guide.html)
- [Refactoring](https://en.wikipedia.org/wiki/Code_refactoring)
- [Test-driven development](https://en.wikipedia.org/wiki/Test-driven_development)
- [99 Bottles of OOP](https://www.sandimetz.com/99bottles/)
- [Needleman-Wunsch algorithm](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm)
- [Sudoku solving algorithms](https://en.wikipedia.org/wiki/Sudoku_solving_algorithms)
- [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [Expectation-Maximisation](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)
- [Dawkins' weasel program](https://en.wikipedia.org/wiki/Weasel_program)
- [Birthday problem](https://en.wikipedia.org/wiki/Birthday_problem)
- [Penney's game](https://en.wikipedia.org/wiki/Penney%27s_game) and the
  [100 prisoners problem](https://en.wikipedia.org/wiki/100_prisoners_problem),
  which give away the solutions to the puzzles in Against the Odds
