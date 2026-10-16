# Red to Green: Python problems from FizzBuzz to mixture models

## Introduction

Welcome! This is a collection of Python puzzles that begin *red* and end
*green*. Most functions start as stubs whose tests fail, and your job is to turn
them green. It is **not a course**: browse the [catalogue](#index-of-problems),
pick something that looks fun, struggle with it productively, use the hints when
you need them, and learn Python by solving it. The problems run from
FizzBuzz-sized warm-ups to data analysis, simulation, algorithms and statistical
modelling, and along the way you will meet list comprehensions, generators,
recursion, object orientation, test-first development, refactoring, graph
search, maximum likelihood, expectation-maximisation, probability puzzles that
defy intuition and even a cellular automaton.

> [!TIP]
> **Not sure where to begin?** Pick any problem from the
> [catalogue](#index-of-problems), or follow [Start here](#start-here) to
> install the tools and run your first failing test.

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

You do not need to do everything, or to do things in order. Problems range from
a few minutes to several sessions (the size in the catalogue is a rough guide),
and the optional [routes](#choosing-a-route) below are only suggestions. For an
overview of the repository layout and development setup, see
[DEVELOPMENT.md](DEVELOPMENT.md).

## Start here

The dev container is ready to use. For a local setup with the notebooks and
scientific tools, install the complete environment with:

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
4. Then pick anything else from the [catalogue](#index-of-problems), or follow a
   [route](#choosing-a-route).

## How to complete an exercise

- Each topic has its own page, linked from the [catalogue](#index-of-problems),
  which opens with anything you need beforehand and the test command that checks
  it.
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

Browse by what looks interesting. **Size** is a rough guide to how hot a problem
is: ☕ is mild and quick, ☕☕ takes some thought, ☕☕☕ is a substantial
challenge and ☕☕☕☕ is a project.
Nothing has to be done in order. **Try first** only suggests a problem that makes
this one easier or richer, and the one real dependency is marked **needs**.

| Problem | Size | Style | The hook | Try first |
| --- | --- | --- | --- | --- |
| [Python warm-ups](problems/python-fundamentals.md) | ☕ | Warm-up | Quick ones: [exponentiation](problems/python-fundamentals.md#q1-exponentiation), [adjacent products](problems/python-fundamentals.md#q2-adjacent-products), [FizzBuzz](problems/python-fundamentals.md#q3-fizzbuzz), [Fibonacci generators](problems/python-fundamentals.md#q4-fibonacci-sequence) and the [first non-repeating character](problems/python-fundamentals.md#q5-first-non-repeating-character) | |
| [Python gotchas](problems/python-fundamentals.md#q6-python-gotchas) | ☕ | Language puzzle | Predict what surprising snippets print, then fix them | |
| [Sudoku checker](problems/python-fundamentals.md#q7-sudoku-checker) | ☕☕ | Algorithm | Is this grid a valid Sudoku? | |
| [Talking animals](problems/object-oriented-python.md) | ☕☕ | Object-oriented | [Noisy animals](problems/object-oriented-python.md#noisy-animals-), a [fox nobody can hear](problems/object-oriented-python.md#what-does-the-fox-say-), [a parrot that learns](problems/object-oriented-python.md#a-parrot-that-learns-) and [a robot](problems/object-oriented-python.md#the-robot-joins-the-band-) | |
| [Gilded Rose](problems/refactoring-and-test-first.md#the-gilded-rose-kata-) | ☕☕☕ | Refactoring | Tame an inherited tangle of nested conditions without breaking it | [Talking animals](problems/object-oriented-python.md) |
| [99 Bottles](problems/refactoring-and-test-first.md#99-bottles) | ☕ | Test-first kata (optional) | Sing the song one test at a time, then write tests of your own | |
| [Word ladder](problems/algorithms/word-ladder.md) | ☕☕ | Algorithm | Turn `play` into `game` one letter at a time | |
| [...Try, try again](problems/algorithms/rugby.md) | ☕☕ | Algorithm | How many ways could a rugby score have happened? | [Fibonacci](problems/python-fundamentals.md#q4-fibonacci-sequence) |
| [Sudoku solver](problems/algorithms/sudoku-solver.md) | ☕☕☕ | Algorithm | Backtrack your way to a solution. **Needs** the [Sudoku checker](problems/python-fundamentals.md#q7-sudoku-checker) | |
| [Global sequence alignment](problems/algorithms/global-sequence-alignment.md) | ☕☕☕☕| Algorithm | Align two DNA sequences, and find out why trying every alignment cannot work | [...Try, try again](problems/algorithms/rugby.md) |
| [Mysterious data](problems/data-analysis.md#q1-mysterious-data-) | ☕ | Data investigation | Thirteen mystery datasets: which of them are the same? | |
| [Steak, tea and toast](problems/data-analysis.md#q2-categorical-data-steak-tea-and-toast) | ☕☕ | Data investigation | Do people who burn their toast also like well-done steak? | |
| [Predicting Old Faithful](problems/data-analysis.md#q3-linear-regression-predicting-the-next-old-faithful-eruption) | ☕☕ | Data investigation | When will the geyser erupt next, and is your model any good? | |
| [How uncertain is an average?](problems/scientific-python.md#q1-how-uncertain-is-an-average) | ☕☕ | Scientific investigation | Does the textbook standard-error formula tell the truth? | |
| [When does the normal approximation fail?](problems/scientific-python.md#q2-when-does-the-normal-approximation-fail) | ☕ | Scientific investigation | Find where a famous shortcut breaks | |
| [Two methods, two answers](problems/scientific-python.md#q3-two-methods-two-answers) | ☕☕ | Scientific investigation | Two estimates of the same uncertainty disagree. Why? | |
| [Recovering the parameters](problems/scientific-python.md#q4-recovering-the-parameters) | ☕☕☕ | Statistical modelling | Work out the process behind the data by maximum likelihood | |
| [Can you trust a 95% interval?](problems/scientific-python.md#q5-can-you-trust-a-95-interval-) | ☕☕☕ | Scientific investigation | Test the claim, and find when it fails | |
| [Gaussian mixture](problems/statistical-modelling.md#gaussian-mixture-) | ☕☕☕☕| Statistical modelling | Fit two hidden populations at once (optional) | [Recovering the parameters](problems/scientific-python.md#q4-recovering-the-parameters) |
| [Gaussian-mixture EM](problems/statistical-modelling.md#gaussian-mixture-em-) | ☕☕☕☕| Statistical modelling | Expectation-maximisation, from hard labels to the Old Faithful geyser | [Recovering the parameters](problems/scientific-python.md#q4-recovering-the-parameters), [Predicting Old Faithful](problems/data-analysis.md#q3-linear-regression-predicting-the-next-old-faithful-eruption) |
| [The office party](problems/against-the-odds.md#the-office-party-) | ☕ | Probability puzzle | How many people before a shared birthday is more likely than not? | |
| [Waiting for heads](problems/against-the-odds.md#waiting-for-heads-) | ☕☕ | Probability puzzle | Why is waiting for `HH` different from waiting for `HT`? | [Fibonacci](problems/python-fundamentals.md#q4-fibonacci-sequence) |
| [The 100 prisoners](problems/against-the-odds.md#the-100-prisoners-) | ☕☕☕ | Probability puzzle | A hopeless-looking last chance at freedom | [The office party](problems/against-the-odds.md#the-office-party-) |
| [Conway's Game of Life](problems/models-of-life.md#conways-game-of-life-) | ☕☕ | Simulation | Can you build a machine that makes more machines? | |
| [Dawkins' weasel](problems/models-of-life.md#dawkins-weasel-) | ☕☕ | Simulation | Can a sentence evolve out of gibberish? | |

Each topic also has an overview page: [Python Fundamentals](problems/python-fundamentals.md),
[Object-oriented Python](problems/object-oriented-python.md),
[Refactoring and Test-First Development](problems/refactoring-and-test-first.md),
[Algorithms and Search](problems/algorithms-and-search.md),
[Data Analysis](problems/data-analysis.md),
[Scientific Python](problems/scientific-python.md),
[Statistical Modelling](problems/statistical-modelling.md),
[Against the Odds](problems/against-the-odds.md) and
[Models of Life](problems/models-of-life.md).

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
   [Q7](problems/python-fundamentals.md#q7-sudoku-checker)
2. [Object-oriented Python](problems/object-oriented-python.md), from
   [noisy animals](problems/object-oriented-python.md#noisy-animals-) through
   [the fox](problems/object-oriented-python.md#what-does-the-fox-say-) and
   [the parrot](problems/object-oriented-python.md#a-parrot-that-learns-) to
   [the robot](problems/object-oriented-python.md#the-robot-joins-the-band-)
3. One kata from
   [Refactoring and Test-First Development](problems/refactoring-and-test-first.md),
   either [Gilded Rose](problems/refactoring-and-test-first.md#the-gilded-rose-kata-)
   or
   [99 Bottles](problems/refactoring-and-test-first.md#99-bottles). The other is optional.
4. [Word ladder](problems/algorithms/word-ladder.md).

**Route 2: Scientific Python.** Work with real data. Do Route 1 first, then:

1. [Data Analysis Q1, Mysterious data](problems/data-analysis.md#q1-mysterious-data-).
2. [Scientific Python Q1](problems/scientific-python.md#q1-how-uncertain-is-an-average)
   and [Q3](problems/scientific-python.md#q3-two-methods-two-answers) (standard
   error and the bootstrap)
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
