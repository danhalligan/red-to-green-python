# Red to Green: Python problems from FizzBuzz to mixture models

## Introduction

Welcome! This is a hands-on collection of Python exercises that begin *red* and
end *green*. Most functions start as stubs whose tests fail, and your job is to
turn them green by implementing them one small step at a time. The problems run
from FizzBuzz-sized programming puzzles to data analysis and statistical
modelling. If you complete all the exercises you'll have touched on Python
fundamentals such as list comprehensions, generators, recursion and object
orientation, but also maximum likelihood, expectation-maximisation, test first
development, refactoring, graph search, probability puzzles that defy intuition
and even cellular automaton.

> [!TIP]
> **New here?** Follow [Start here](#start-here) below to install the tools and
> run your first failing test, in [Q1: Exponentiation](problems/python-fundamentals.md#q1-exponentiation).

Look out for these markers: 💡 a hint (in a footnote or a collapsible section,
sometimes in three levels that give away a little more each time), 😱 a
particularly challenging section, and 🚀 an optional extension. Some
investigations end with a collapsible **What did you discover?** section: read
it after you have formed your own view.

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
route below finishes at a sensible stopping point. The early exercises are
bite-sized; later notebooks, the kata, and mixture-model work can each take
several sessions. For an overview of the repository layout and development
setup, see [DEVELOPMENT.md](DEVELOPMENT.md).

## Start here

The dev container is ready to use. For a local setup with the notebooks and
scientific tools, install the complete environment with:

```bash
uv sync --all-groups --extra science
```

Then try your first exercise,
[Q1: Exponentiation](problems/python-fundamentals.md#q1-exponentiation):

1. Read the prompt, then run its test. It is **expected to fail** at first:

   ```bash
   uv run pytest tests/test_language.py -k exponentiate -q
   ```

2. Implement `exponentiate` in `src/pyproblems/language.py`.
3. Rerun the same command until it passes: that is red to green.
4. Carry on with [Q2](problems/python-fundamentals.md#q2-adjacent-products), or
   choose a [route](#choosing-a-route).

## How to complete an exercise

- Each topic has its own page, listed in the [index](#index-of-problems), which
  opens with its prerequisites and the test command that checks it.
- Use the focused test command for the exercise you are working on. Most
  exercises begin as stubs, so their tests are red until you implement them.
  Topic-level commands run every exercise in a topic and are more useful after
  you have completed several.
- Make one small change at a time and rerun the test.
- Look for 💡 hints only when you are stuck, opening one level at a time, and
  try the 🚀 extensions if you want more.
- Notebook analyses (in `analysis/`) have no pass or fail, so they are checked by
  your own plots and explanations.
- The early language exercises use only the Python standard library; scientific
  exercises need the optional science packages installed above.

## Index of problems

**Prerequisites** must be completed first. **Recommended first** exercises are
useful but not required. Each topic page links onwards to related exercises.

| Topic | Exercises | Needs |
| --- | --- | --- |
| [Python Fundamentals](problems/python-fundamentals.md) | [Q1 Exponentiation](problems/python-fundamentals.md#q1-exponentiation), [Q2 Adjacent products](problems/python-fundamentals.md#q2-adjacent-products), [Q3 FizzBuzz](problems/python-fundamentals.md#q3-fizzbuzz), [Q4 Fibonacci](problems/python-fundamentals.md#q4-fibonacci-sequence), [Q5 First non-repeating character](problems/python-fundamentals.md#q5-first-non-repeating-character), [Q6 Python gotchas](problems/python-fundamentals.md#q6-python-gotchas), [Q7 Sudoku checker](problems/python-fundamentals.md#q7-sudoku-checker) | Nothing |
| [Object-oriented Python](problems/object-oriented-python.md) | [Noisy animals](problems/object-oriented-python.md#noisy-animals-), [What Does the Fox Say?](problems/object-oriented-python.md#what-does-the-fox-say-), [A parrot that learns](problems/object-oriented-python.md#a-parrot-that-learns-), [The robot joins the band](problems/object-oriented-python.md#the-robot-joins-the-band-) | [Python Fundamentals](problems/python-fundamentals.md) |
| [Refactoring and Test-First Development](problems/refactoring-and-test-first.md) | [Gilded Rose kata](problems/refactoring-and-test-first.md#the-gilded-rose-kata-), [99 Bottles](problems/refactoring-and-test-first.md#99-bottles) | [Python Fundamentals](problems/python-fundamentals.md). Recommended first for Gilded Rose: [Object-oriented Python](problems/object-oriented-python.md) |
| [Scientific Python 🔬](problems/scientific-python.md) | [Q1 Standard error](problems/scientific-python.md#q1-how-uncertain-is-an-average), [Q2 Binomial and normal](problems/scientific-python.md#q2-when-does-the-normal-approximation-fail), [Q3 Bootstrap](problems/scientific-python.md#q3-two-methods-two-answers), [Q4 Likelihood](problems/scientific-python.md#q4-recovering-the-parameters), [Q5 Coverage 🚀](problems/scientific-python.md#q5-can-you-trust-a-95-interval-) | [Python Fundamentals](problems/python-fundamentals.md), [Object-oriented Python](problems/object-oriented-python.md), science packages |
| [Data Analysis](problems/data-analysis.md) | [Q1 Mysterious data](problems/data-analysis.md#q1-mysterious-data-), [Q2 Steak, Tea and Toast](problems/data-analysis.md#q2-categorical-data-steak-tea-and-toast), [Q3 Predicting Old Faithful](problems/data-analysis.md#q3-linear-regression-predicting-the-next-old-faithful-eruption) | [Python Fundamentals](problems/python-fundamentals.md), science packages |
| [Statistical Modelling](problems/statistical-modelling.md) | [Gaussian-mixture](problems/statistical-modelling.md#gaussian-mixture-) (optional), [Gaussian-mixture EM](problems/statistical-modelling.md#gaussian-mixture-em-) 😱 | [Scientific Python Q4](problems/scientific-python.md#q4-recovering-the-parameters). Recommended first for EM: [Data Analysis Q3](problems/data-analysis.md#q3-linear-regression-predicting-the-next-old-faithful-eruption) |
| [Algorithms and Search](problems/algorithms-and-search.md) | [Word ladder](problems/algorithms/word-ladder.md), [...Try, try again](problems/algorithms/rugby.md), [Global sequence alignment](problems/algorithms/global-sequence-alignment.md), [Sudoku solver](problems/algorithms/sudoku-solver.md) | [Python Fundamentals](problems/python-fundamentals.md). The Sudoku solver needs [Sudoku checker (Q7)](problems/python-fundamentals.md#q7-sudoku-checker). Recommended first: [Fibonacci (Q4)](problems/python-fundamentals.md#q4-fibonacci-sequence) for rugby, and rugby for alignment |
| [Against the Odds 🎲](problems/against-the-odds.md) | [The office party](problems/against-the-odds.md#the-office-party-), [Waiting for heads](problems/against-the-odds.md#waiting-for-heads-), [The 100 prisoners](problems/against-the-odds.md#the-100-prisoners-) | [Python Fundamentals](problems/python-fundamentals.md). Recommended first: [Fibonacci (Q4)](problems/python-fundamentals.md#q4-fibonacci-sequence) for the coin patterns, and [The office party](problems/against-the-odds.md#the-office-party-) for the prisoners. The investigations use the science packages |
| [Models of Life 🌿](problems/models-of-life.md) | [Conway's Game of Life](problems/models-of-life.md#conways-game-of-life-), [Dawkins' weasel](problems/models-of-life.md#dawkins-weasel-) | [Python Fundamentals](problems/python-fundamentals.md), science packages |

## Choosing a route

The index above lists the topics; the routes below pick a path through them.
Each route has its own test commands, and finishing one counts as completing a
useful course. You can branch between routes, and each page suggests where to go
next.

**Route 1: Python core.** Learn the language and practise writing tested code.

1. [Python Fundamentals](problems/python-fundamentals.md):
   [Q1](problems/python-fundamentals.md#q1-exponentiation),
   [Q2](problems/python-fundamentals.md#q2-adjacent-products),
   [Q3](problems/python-fundamentals.md#q3-fizzbuzz),
   [Q4](problems/python-fundamentals.md#q4-fibonacci-sequence),
   [Q5](problems/python-fundamentals.md#q5-first-non-repeating-character),
   [Q6](problems/python-fundamentals.md#q6-python-gotchas) and
   [Q7](problems/python-fundamentals.md#q7-sudoku-checker):
   `uv run pytest tests/test_language.py tests/test_sudoku.py -q`
2. [Object-oriented Python](problems/object-oriented-python.md), from
   [noisy animals](problems/object-oriented-python.md#noisy-animals-) through
   [the fox](problems/object-oriented-python.md#what-does-the-fox-say-) and
   [the parrot](problems/object-oriented-python.md#a-parrot-that-learns-) to
   [the robot](problems/object-oriented-python.md#the-robot-joins-the-band-):
   `uv run pytest tests/test_oop.py -q`
3. One kata from
   [Refactoring and Test-First Development](problems/refactoring-and-test-first.md),
   either [Gilded Rose](problems/refactoring-and-test-first.md#the-gilded-rose-kata-)
   (`tests/test_gilded_rose.py`) or
   [99 Bottles](problems/refactoring-and-test-first.md#99-bottles)
   (`tests/test_bottles.py`). The other is optional.
4. [Word ladder](problems/algorithms/word-ladder.md):
   `uv run pytest tests/test_word_ladder.py -q`

**Route 2: Scientific Python.** Work with real data. Do Route 1 first, then:

1. [Data Analysis Q1, Mysterious data](problems/data-analysis.md#q1-mysterious-data-).
2. [Scientific Python Q1](problems/scientific-python.md#q1-how-uncertain-is-an-average)
   and [Q3](problems/scientific-python.md#q3-two-methods-two-answers) (standard
   error and the bootstrap):
   `uv run pytest tests/test_statistics.py -k standard_error`
3. [Data Analysis Q2, Steak, Tea, and Toast](problems/data-analysis.md#q2-categorical-data-steak-tea-and-toast)
   and
   [Q3, Old Faithful regression](problems/data-analysis.md#q3-linear-regression-predicting-the-next-old-faithful-eruption).
4. Optionally, [Models of Life](problems/models-of-life.md):
   [Game of Life](problems/models-of-life.md#conways-game-of-life-) and
   [Dawkins' weasel](problems/models-of-life.md#dawkins-weasel-).

**Route 3: Advanced extensions.** Choose what interests you.

- The algorithm projects need only Route 1:
  [...Try, try again](problems/algorithms/rugby.md),
  [Sudoku solver](problems/algorithms/sudoku-solver.md) and
  [global sequence alignment](problems/algorithms/global-sequence-alignment.md).
- The probability puzzles in [Against the Odds](problems/against-the-odds.md)
  also need only Route 1, and are a good way to practise simulation:
  [the office party](problems/against-the-odds.md#the-office-party-),
  [waiting for heads](problems/against-the-odds.md#waiting-for-heads-) and
  [the 100 prisoners](problems/against-the-odds.md#the-100-prisoners-).
- The modelling projects need Route 2, and some comfort with probability
  densities, likelihood, logs, basic linear algebra and covariance matrices:
  [Scientific Python Q2](problems/scientific-python.md#q2-when-does-the-normal-approximation-fail),
  [Scientific Python Q4](problems/scientific-python.md#q4-recovering-the-parameters),
  [Gaussian-mixture](problems/statistical-modelling.md#gaussian-mixture-) and
  [Gaussian-mixture EM](problems/statistical-modelling.md#gaussian-mixture-em-).

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
