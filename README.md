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
[Q1: Exponentiation](problems/python-fundamentals.md#q1-exponentiation):

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
related exercises in the same file stay together here too. The algorithms have
separate files under `problems/algorithms/`.

Difficulty is a rough guide: 🌶️ gentle, 🌶️🌶️ takes some thought,
🌶️🌶️🌶️ challenging. A page may start gently and build up.

If you are new to Python, start with the fundamentals. Otherwise, dip in
wherever you like; the notes below flag useful background, not a required order.

### [Python Fundamentals](problems/python-fundamentals.md) 🌶️

Short language exercises: exponentiation, adjacent products, FizzBuzz,
Fibonacci generators, the first non-repeating character, and Python gotchas.

### [Object-oriented Python](problems/object-oriented-python.md) 🌶️🌶️

Build a cast of talking animals, from noisy animals and a silent fox to a
parrot that learns and a robot. Practise classes, inheritance and polymorphism.

### [Refactoring and Test-First Development](problems/refactoring-and-test-first.md) 🌶️🌶️🌶️

Two katas: tame an inherited codebase in Gilded Rose, or build 99 Bottles one
test at a time. Familiarity with classes helps with Gilded Rose.

### [Algorithms and Search](problems/algorithms-and-search.md)

- [Word ladder](problems/algorithms/word-ladder.md) 🌶️🌶️:
  turn `play` into `game` one letter at a time.
- [...Try, try again](problems/algorithms/rugby.md) 🌶️🌶️:
  count the ways a rugby score could have happened, from recursion to dynamic
  programming. The Fibonacci exercise is useful background.
- [Sudoku solver](problems/algorithms/sudoku-solver.md) 🌶️🌶️🌶️:
  warm up with a checker, then backtrack your way to a solution.
- [Global sequence alignment](problems/algorithms/global-sequence-alignment.md)
  🌶️🌶️🌶️: align two DNA sequences and discover why brute force cannot scale.
  The rugby problem introduces the dynamic programming ideas used here.

### [Data Analysis](problems/data-analysis.md) 🌶️🌶️

Explore thirteen mysterious datasets, investigate preferences for steak, tea
and toast, and predict Old Faithful eruptions. Notebook-based work with
plots, summaries and regression.

### [Scientific Python](problems/scientific-python.md) 🌶️🌶️🌶️

Investigate uncertainty in an average, the normal approximation, the bootstrap,
maximum likelihood and confidence intervals. Basic probability and statistics
help; the later exercises build on the earlier ones.

### [Statistical Modelling](problems/statistical-modelling.md) 🌶️🌶️🌶️

Fit Gaussian mixtures by numerical optimisation and expectation-maximisation.
These optional challenges assume likelihood (introduced in Scientific Python),
probability densities, basic linear algebra and covariance matrices.

### [Against the Odds](problems/against-the-odds.md) 🌶️🌶️🌶️

Three probability puzzles: the office party, waiting for heads, and the
100 prisoners. Predict, simulate, calculate and explain, using only the Python
standard library. They start gently and get harder.

### [Models of Life](problems/models-of-life.md) 🌶️🌶️

Simulate Conway's Game of Life and Dawkins' weasel: cellular automata and
evolution from simple rules.

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
