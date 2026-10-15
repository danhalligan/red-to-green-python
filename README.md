# Red to Green: Python problems from FizzBuzz to mixture models

## Introduction

Welcome! This is a hands-on collection of Python exercises that begin *red* and
end *green*. Most functions start as stubs whose tests fail, and your job is to
turn them green by implementing them one small step at a time. The problems run
from FizzBuzz-sized programming puzzles to data analysis and statistical
modelling. If you complete all the exercises you'll have touched on Python
fundamentals such as list comprehensions, generators and object orientation, but
also maximum likelihood, expectation-maximisation, recursion, test first
development, refactoring, graph search and even cellular automaton.

Start with [Python Fundamentals](problems/python-fundamentals.md), then choose
one of the [routes](#choosing-a-route) below or jump to a topic from the
[index of problems](#index-of-problems) that interests you. The early exercises
are bite-sized; later notebooks, the kata, and mixture-model work can each take
several sessions.

Look out for these markers: 💡 a hint (usually in a footnote), 😱 a
particularly challenging section, and 🚀 an optional extension.

> [!IMPORTANT]
> The purpose of this package is partially to help you learn Python, but is also a
> collection of interesting and hopefully satisfying problems to solve. It is not
> simply about collecting completed solutions. A coding agent could complete the
> exercises for you, but that would bypass the practice and interest they are
> designed to provide. Writing code, investigating failures, and explaining your
> choices build an understanding of Python that remains useful in the age of
> agentic coding: you need that understanding to specify requirements, assess
> generated code, spot mistakes, and maintain the result. Agents can support your
> learning with hints, explanations, or reviews of your own attempts. Try each
> problem yourself first, and make sure you can explain and test any code you
> adopt; passing tests alone is not the learning goal.

As a rough guide, allow 25 to 50 hours for a full pass, depending on your
experience and how deeply you explore the investigations. Treat that as a
provisional guide, not a deadline: you do not need to do everything, and each
route below finishes at a sensible stopping point. For an overview of the
repository layout and development setup, see [DEVELOPMENT.md](DEVELOPMENT.md).

The dev container is ready to use. For a local setup with the notebooks and
scientific tools, install the complete environment with:

```bash
uv sync --all-groups --extra science
```

## How to complete an exercise

Most exercise functions start as stubs, so their tests are red until you
implement them. Each topic has its own page, linked from the
[index](#index-of-problems), which opens with its prerequisites and the test
command that checks it.

1. Read the prompt for an exercise, then run its focused test command and watch
   it fail.
2. Implement the function named in the prompt, in its file under
   `src/pyproblems/`. Make one small change at a time and rerun the test until
   it turns green.
3. Look for 💡 hints (usually in footnotes) only when you are stuck, and try
   the 🚀 extensions if you want more.
4. Notebook analyses (in `analysis/`) have no pass or fail, so they are checked
   by your own plots and explanations.

For your first check, try `uv run pytest tests/test_language.py`. The early
language exercises use only the Python standard library; scientific exercises
need the optional science packages installed above.

## Index of problems

| Topic | What you will do | Needs |
| --- | --- | --- |
| [Python Fundamentals](problems/python-fundamentals.md) | Exponentiation, adjacent products, FizzBuzz, Fibonacci, first non-repeating character, Python gotchas, Sudoku checker | Nothing |
| [Object-oriented Python](problems/object-oriented-python.md) | Noisy animals, What Does the Fox Say?, a parrot that learns, the robot joins the band | Python Fundamentals |
| [Refactoring and Test-First Development](problems/refactoring-and-test-first.md) | Gilded Rose kata, 99 Bottles | Python Fundamentals (Gilded Rose also needs Object-oriented Python) |
| [Scientific Python 🔬](problems/scientific-python.md) | Standard error, least squares, binomial against normal, the bootstrap, maximum likelihood, confidence interval coverage | Python Fundamentals, Object-oriented Python, science packages |
| [Data Analysis](problems/data-analysis.md) | Mysterious data, Steak, Tea and Toast, predicting Old Faithful | Python Fundamentals, science packages, Scientific Python Q2 |
| [Statistical Modelling](problems/statistical-modelling.md) | Gaussian mixtures by numerical optimisation and by expectation-maximisation 😱 | Scientific Python Q5 |
| [Algorithms and Search](problems/algorithms-and-search.md) | Word ladder, ...Try, try again, global sequence alignment, Sudoku solver | Python Fundamentals |
| [Models of Life 🌿](problems/models-of-life.md) | Conway's Game of Life, Dawkins' weasel | Python Fundamentals, science packages |

## Choosing a route

Each route has its own test commands, and finishing one counts as completing a
useful course. The routes visit the topics above in a different order.

**Route 1: Python core.** Learn the language and practise writing tested code.

1. [Python Fundamentals](problems/python-fundamentals.md), Q1 to Q7:
   `uv run pytest tests/test_language.py tests/test_sudoku.py -q`
2. [Object-oriented Python](problems/object-oriented-python.md), from noisy
   animals to the robot: `uv run pytest tests/test_oop.py -q`
3. One kata from
   [Refactoring and Test-First Development](problems/refactoring-and-test-first.md),
   either Gilded Rose (`tests/test_gilded_rose.py`) or 99 Bottles
   (`tests/test_bottles.py`). The other is optional.
4. [Word ladder](problems/algorithms-and-search.md):
   `uv run pytest tests/test_word_ladder.py -q`

**Route 2: Scientific Python.** Work with real data. Do Route 1 first, then:

1. [Data Analysis](problems/data-analysis.md) Q1, Mysterious data.
2. [Scientific Python](problems/scientific-python.md) Q1, Q2 and Q4 (standard
   error, least squares and the bootstrap):
   `uv run pytest tests/test_statistics.py -k "standard_error or ols"`
3. [Data Analysis](problems/data-analysis.md) Q2 (Steak, Tea, and Toast) and Q3
   (Old Faithful regression).
4. Optionally, [Models of Life](problems/models-of-life.md): Game of Life and
   Dawkins' weasel.

**Route 3: Advanced extensions.** Choose what interests you. The algorithm
projects (Try, try again, Sudoku solver, global sequence alignment, all in
[Algorithms and Search](problems/algorithms-and-search.md)) need only Route 1.
The modelling projects ([Scientific Python](problems/scientific-python.md) Q3
and Q5, and [Statistical Modelling](problems/statistical-modelling.md)) need
Route 2, and some comfort with probability densities, likelihood, logs, basic
linear algebra and covariance matrices.

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
