# Red to Green: Python problems from FizzBuzz to mixture models

[Get started](#getting-started-) ·
[Choose a problem](#the-problems-) ·
[How to](#how-to-work-through-the-problems-) ·
[Notebooks](#working-with-notebooks-) · [Further reading](#further-reading-)

## Introduction

Welcome! This is a collection of Python problems to solve. You solve them by
writing functions that start as stubs and whose tests fail and are *red* 🔴.
If you complete them correctly the tests will turn *green* 🟢!

Problems run from FizzBuzz-sized warm-ups to data analysis, simulation,
algorithms and statistical modelling, and along the way you will meet list
comprehensions, generators, recursion, object orientation, refactoring,
graph search, maximum likelihood,
expectation-maximisation, probabilities that defy intuition and even a cellular
automaton.

## Getting started 🚦

The dev container is ready to use, but not required. For a local setup with the
notebooks and scientific tools, install the complete environment with:

```bash
uv sync --all-groups --extra science
```

Then try a first exercise, for example the quick warm-up
[Q1: Exponentiation](exercises/python_fundamentals/README.md#q1-exponentiation):

1. Read the prompt, then run its test. It is **expected to fail** at first:

   ```bash
   uv run pytest exercises/python_fundamentals/test_fundamentals.py -k exponentiate -q
   ```

2. Implement `exponentiate` in
   `exercises/python_fundamentals/fundamentals.py`.
3. Rerun the same command until it passes: that is red to green.
4. Keep going with the Python language problems, or pick any other!

New to VS Code, environments or reading test failures? Follow
[Getting going in VS Code](GETTING_STARTED.md) for a step-by-step walkthrough,
including how to use the Testing panel and keep the output manageable.

For an overview of the repository layout and development setup, see
[DEVELOPMENT.md](DEVELOPMENT.md).

## The problems 🚨

Pick a topic that interests you. Each link opens an exercise folder under
`exercises/` that holds everything for that problem: its instructions (the
README), starter code, tests, and any notebook or data. The index groups
exercises by topic, and each is marked with its difficulty (🌶️ gentle, 🌶️🌶️ takes some
thought, 🌶️🌶️🌶️ challenging) so you can see at a glance which are easy and
which are hard.

If you are new to Python, start with the fundamentals. Otherwise, dip in
wherever you like; the notes below flag useful background, not a required order.
Not sure how to work through a problem, or what the 💡 and 🚀 markers mean? See
[How to work through the problems](#how-to-work-through-the-problems-) below.

If you would like a guided path, here are two suggested routes. Each starts with
the fundamentals and builds on the one before:

- **Python for experimental scientists:**
  [Python Fundamentals](exercises/python_fundamentals/README.md) →
  [Steak, Tea, and Toast](exercises/steak_tea_toast/README.md) →
  [Penguin parade](exercises/penguin_parade/README.md) →
  [Spinning plates](exercises/spinning_plates/README.md) →
  [Titanic disaster](exercises/titanic_disaster/README.md).
- **Programming and problem-solving:**
  [Python Fundamentals](exercises/python_fundamentals/README.md) →
  [Wordsmith](exercises/wordsmith/README.md) →
  [Word ladder](exercises/word_ladder/README.md) →
  [Try, try again](exercises/try_try_again/README.md) →
  [Sequence alignment](exercises/sequence_alignment/README.md).

### Pythonic Python

Practise writing clear Python, organising it with classes, and improving it
through tests and refactoring.

- [Python Fundamentals](exercises/python_fundamentals/README.md) 🌶️:
  short language exercises covering exponentiation, adjacent products, FizzBuzz,
  Fibonacci and look-and-say generators, the first non-repeating character, and
  Python gotchas.
- [Noisy animals](exercises/noisy_animals/README.md) 🌶️🌶️:
  build a cast of talking animals, from noisy animals and a silent fox to a
  parrot that learns and a robot. Practise classes, inheritance and polymorphism.
- [Gilded Rose](exercises/gilded_rose/README.md) 🌶️🌶️:
  tame an inherited codebase without breaking its existing behaviour.
  Familiarity with classes helps.

### Algorithms and Search

Four self-contained exercises, each with its own page, starter code and tests.
You can start with any of them, but some build on earlier ideas, as shown below.

- [Word ladder](exercises/word_ladder/README.md) 🌶️🌶️:
  turn `play` into `game` one letter at a time.
- [Try, try again](exercises/try_try_again/README.md) 🌶️🌶️:
  count the ways a rugby score could have happened, from recursion to dynamic
  programming. The Fibonacci exercise is useful background.
- [Sudoku solver](exercises/sudoku_solver/README.md) 🌶️🌶️🌶️:
  warm up with a checker, then backtrack your way to a solution.
- [Sequence alignment](exercises/sequence_alignment/README.md)
  🌶️🌶️🌶️: align two DNA sequences and discover why brute force cannot scale.
  The rugby problem introduces the dynamic programming ideas used here.

### Data Analysis

Explore data, look for relationships, and evaluate predictions on unseen data.
These notebook-based exercises use the optional scientific stack.

- [Mysterious data](exercises/mysterious_data/README.md) 🌶️:
  thirteen datasets with matching summaries. What do their plots reveal?
- [Penguin parade](exercises/penguin_parade/README.md) 🌶️: a field team counted
  344 penguins and your data join found rather more. Reconcile real biological
  measurements, investigate missing lab results and see what blood isotopes
  reveal.
- [Steak, Tea, and Toast](exercises/steak_tea_toast/README.md) 🌶️🌶️:
  clean messy survey responses and investigate associations between preferences.
- [Titanic disaster](exercises/titanic_disaster/README.md) 🌶️🌶️🌶️:
  build a prediction pipeline, beat a baseline, and test it on unseen passengers.
- [Spinning plates](exercises/spinning_plates/README.md) 🌶️🌶️: rescue a
  seemingly failed laboratory experiment performed on a 96 well plate: parse
  plate-reader files, reconstruct the sample mapping, build a tidy DataFrame
  pipeline and decide whether the results can be trusted.

### Uncertainty and Simulation

Use repeated experiments to find out how much you can trust an estimate.
Basic NumPy, probability and statistics help.

- [Known unknowns](exercises/known_unknowns/README.md)
  🌶️🌶️: estimate uncertainty with standard errors, the bootstrap and confidence
  intervals, then use simulation to test whether each method keeps its promise.

### Parameter Estimation

Estimate model parameters using likelihood, numerical optimisation and
mixture models fitted by expectation-maximisation, or weigh the evidence in real
trial data with Bayesian inference.
Start with likelihood for coins, normals and straight lines; the Bayesian and
mixture exercises build on it, with covariance matrices needed for multivariate
mixtures.

- [A likely story](exercises/a_likely_story/README.md)
  🌶️🌶️: write down the probability of one data point and fit any model with it,
  from a coin to a regression that shrugs off outliers.
- [Beyond reasonable doubt](exercises/beyond_reasonable_doubt/README.md)
  🌶️🌶️: a clinical trial misses the conventional significance threshold despite
  promising results. Use real trial data and Bayesian inference to decide what
  the evidence actually tells us. [A likely story](exercises/a_likely_story/README.md)
  is useful background.
- [Fitting a mixture](exercises/fitting_a_mixture/README.md)
  🌶️🌶️🌶️: write the mixture likelihood, then use hidden labels to fit hard and
  soft mixtures and a bivariate mixture to Old Faithful.

### Against the Odds

Probability puzzles where your gut is confidently wrong. Predict, simulate,
calculate and explain, using only the Python standard library; the investigations
use the science packages for plots.

- [Office party](exercises/office_party/README.md) 🌶️:
  how many people are required before a shared birthday is more likely than not?
- [Waiting for heads](exercises/waiting_for_heads/README.md) 🌶️🌶️:
  why is waiting for `HH` different from waiting for `HT`?
- [The 100 prisoners](exercises/one_hundred_prisoners/README.md) 🌶️🌶️🌶️:
  find a strategy for a hopeless-looking last chance at freedom.

### Models of Life

Explore how simple rules produce complex behaviour: deterministic cellular
automata and stochastic evolution. Both exercises use NumPy.

- [Game of Life](exercises/game_of_life/README.md) 🌶️🌶️:
  build a cellular automaton and watch patterns grow and move.
- [Dawkins' weasel](exercises/dawkins_weasel/README.md) 🌶️🌶️:
  can a sentence evolve out of gibberish through mutation and selection? Optional
  extensions add a tournament-selection genetic algorithm, then recombination.

### Generative Models

- [Wordsmith](exercises/wordsmith/README.md)
  🌶️🌶️: train a tiny probabilistic language model on English words, invent new
  ones, and investigate whether remembering more characters makes a better
  wordsmith.

## How to work through the problems 🧭

You do not need to do everything, or to do things in order. Problems range from
a few minutes to several sessions.

### The basic workflow

- Each exercise's README, linked from the [index](#the-problems-), opens with
  anything you need beforehand and the test command that checks it. The same
  folder holds the starter code, the tests and any notebook or data. Some
  READMEs group several related exercises.
- Use the focused test command for the exercise you are working on. Most
  exercises begin as stubs, so their tests are red until you implement them.
  Run several exercises together by listing their folders, for example
  `uv run pytest exercises/word_ladder/ exercises/sudoku_solver/ -q`;
  that is more useful after you have completed several exercises.
- Aim to make one small change at a time and rerun the test.
- The early language exercises use only the Python standard library; scientific
  exercises need the optional science packages installed above.

### Hints, difficulty and extensions 💡

Difficulty is a rough guide, shown at the top of each exercise README as well as
in the index: 🌶️ gentle, 🌶️🌶️ takes some thought, 🌶️🌶️🌶️ challenging. A page
may start gently and build up.

When working through the problems, look out for these markers:

- 💡 a hint (in a footnote or a collapsible section, sometimes in three levels
  that give away a little more each time)
- 🚀 an optional extension.

Look for hints only when you are stuck, opening one level at a time, and try
the extensions if you want more. Click a collapsible section's heading to open
it. Some investigations also end with a collapsible **What did you discover?**
section: read it after you have formed your own view.

### Using coding agents 🤖

> [!TIP]
> Try each problem yourself first. Use coding agents for hints, explanations
> and reviews of your attempts.

<details>
<summary>Using coding agents while learning</summary>

The purpose of this package is partially to help you learn Python, but is also
a collection of interesting and hopefully satisfying problems to solve. It is
not simply about collecting completed solutions. A coding agent could complete
the exercises for you, but that would miss the point entirely. Writing code,
investigating failures, and explaining your choices build an understanding of
Python, statistics and algorithms that remain useful in the age of agentic
coding. You'll need this understanding to specify requirements, assess
generated code, spot mistakes, and maintain the result. Consider using agents
to support your learning with hints, explanations, or reviews of your own
attempts. Try each problem yourself first, and make sure you can explain and
test any code you adopt; passing tests alone is not the learning goal.

[AGENTS.md](AGENTS.md) gives compatible coding agents learning-first guidance:
offer hints before solutions and ask before editing your exercise code.
Support varies by tool; if yours does not load it automatically, ask it to
read the guide first.

</details>

### Working with notebooks 📓

Each exercise's notebook is called `investigate.ipynb` and sits in its exercise
folder next to the instructions. It is a workspace for your investigation,
not a completed example. Open it in VS Code with Jupyter support, or run
`uv run jupyter lab` from the repository root. Use the project's `.venv` as
the kernel, with the notebook and science packages installed as described above.

Several statistics notebooks use the Old Faithful geyser data (in
`exercises/_shared/data/`) to explore uncertainty, prediction and model choice,
and some also check statistical methods against simulated data with known
answers. Each problem has its own notebook, so you only need the one in your
exercise folder.
The [Titanic notebook](exercises/titanic_disaster/investigate.ipynb)
is a staged machine-learning
investigation. Its setup reserves a test set: keep exploration and model
selection on the training rows, then open the test set only for the final
evaluation.

Run the setup cells first, then fill the `TODO` cells for your investigation,
running any earlier cells that section depends on. Implement reusable functions
in the source module named by the problem and check them with its tests; use
the notebook to call those functions, run experiments and make plots. Add code
cells as needed, and Markdown cells for your predictions, observations and
explanations. Use seeded random generators so experiments can be repeated.

Notebook investigations have no automatic pass or fail: your plots, numerical
checks and explanations are the result.

## Further Reading 📚

Use these when you need background or want to go beyond an exercise; none is
required reading before you start.

### Python and testing

- [The Python Tutorial](https://docs.python.org/3/tutorial/) explains core
  language features, including generators and classes. Use it alongside the
  Pythonic Python exercises when a concept is unfamiliar.
- [Python Standard Library](https://docs.python.org/3/library/) is the reference
  for built-in tools. Look up `itertools`, `collections` and `random` for the
  language exercises and probability simulations.
- [pytest documentation](https://docs.pytest.org/) explains assertions,
  parametrisation and fixtures. Use it to understand the supplied tests.

### Working with scientific data

- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) introduces
  arrays, axes and broadcasting: useful foundations for the simulations,
  cellular automaton and mixture models.
- [pandas getting started](https://pandas.pydata.org/docs/getting_started/)
  covers selecting, cleaning, grouping and plotting tabular data. These are the
  main tools used in the data-analysis notebooks.
- [SciPy statistics tutorial](https://docs.scipy.org/doc/scipy/tutorial/stats.html)
  explains probability distributions, sampling and distribution functions.
  Consult it for the uncertainty investigations and likelihood calculations.
- [SciPy optimisation tutorial](https://docs.scipy.org/doc/scipy/tutorial/optimize.html)
  explains numerical minimisation and constraints. It provides background for
  fitting coins, normals, regressions and mixtures by maximising their
  log-likelihoods.

### Prediction and model fitting

- [scikit-learn getting started](https://scikit-learn.org/stable/getting_started.html)
  introduces fitting, prediction, preprocessing and pipelines. It is a useful
  companion to the Titanic exercise's unfamiliar library calls.
- [scikit-learn cross-validation guide](https://scikit-learn.org/stable/modules/cross_validation.html)
  explains validation strategies and their relationship to a separate test set.
  Read it to understand or extend the Titanic evaluation workflow.
- [Expectation-maximisation](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)
  gives the broader latent-variable interpretation of EM. Read it after the
  mixture exercise to connect its alternating steps to the general method.
