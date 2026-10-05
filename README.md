# Python Problems

## Introduction

This repository is a hands-on introduction to Python. Exercises live in
`src/pyproblems/`, and pytest provides executable examples of their expected
behaviour. Analysis exercises belong in `solutions.ipynb`.

Open the repository in its dev container or install the complete local
environment with:

```bash
uv sync --all-groups --extra science
```

Run the focused fundamentals tests with `uv run pytest tests/test_language.py`.
The exercise tests are expected to fail until you implement the starter
functions. Read one failure at a time, make a small change, and rerun that
focused command. The standard-library language exercises do not require the
optional scientific-Python packages.

Use [DEVELOPMENT.md](DEVELOPMENT.md) for environment and contribution
workflows. Python exercise implementations intentionally begin as stubs, so
focused exercise tests fail until you complete them.

## Python Fundamentals

> **Prerequisites:** none.
>
> **You’ll practice:** functions, sequences, comprehensions, iteration,
> dictionaries, generators, exceptions, text files, and readable tests.

### Q1. Exponentiating values

Implement `exponentiate(values)` in `src/pyproblems/language.py`. It should
return a list containing the exponential of every value in the input iterable.
Start with a `for` loop and `list.append`; once it works, rewrite the body as a
list comprehension. Explain which version you find easier to read. Later, the
scientific-Python section will compare these with a NumPy ufunc. Do not use
`numpy.vectorize` as a substitute for vectorized numerical computation.

Check this exercise with:

```bash
uv run pytest tests/test_language.py -k exponentiate
```

### Q2. Adjacent products

Implement `adjacent_elements_product(values)` to return the largest product
of neighbouring integers. For example, `[3, 6, -2, -5, 7, 3]` returns `21`.
Return `None` when there is no adjacent pair. The input may be any iterable,
including a one-shot iterator. Try `itertools.pairwise` rather than indexing
through positions.

```bash
uv run pytest tests/test_language.py -k adjacent
```

### Q3. FizzBuzz

Implement `fizzbuzz(n)` to return strings from 1 through `n`: use `Fizz` for
multiples of three, `Buzz` for multiples of five, and `FizzBuzz` for both.
`fizzbuzz(5)` returns `['1', '2', 'Fizz', '4', 'Buzz']`, and zero returns an
empty list. Raise `TypeError` for non-integer inputs and `ValueError` for a
negative integer.

```bash
uv run pytest tests/test_language.py -k fizzbuzz
```

### Q4. A clearer summary function

Refactor `summarize(values, *, method="mean")` into a pure function: it should
return a dictionary with `center` and `spread`, and should not print or mutate
its input. `None` and NaN values are missing and should be ignored. Raise
`ValueError` when no usable values remain, when a value is infinite, or when
the method is unknown; reject non-numeric values with `TypeError`.

The `mean` method uses sample standard deviation. The `median` method uses the
raw, unscaled median absolute deviation. A single observation has zero spread.
Return results rather than printing them so callers can compose the function.

```bash
uv run pytest tests/test_language.py -k summarize
```

### Q5. Fibonacci with a generator

Implement `fibonacci()` as an infinite generator beginning `0, 1, 1, 2, 3, 5`.
Use `yield` and local state; each call should return an independent iterator.
Try `next()` to request individual values and `itertools.islice` to take a
finite prefix without materialising the infinite sequence.

```python
from itertools import islice

list(islice(fibonacci(), 8))
```

```bash
uv run pytest tests/test_language.py -k fibonacci
```

### Q6. First non-repeating character

Implement `first_non_repeating_character(text)`. Return the first character
that occurs once, or `_` if no character qualifies. The search is
case-sensitive; spaces and punctuation are characters too. Use a dictionary
or `collections.Counter` to count, then scan in the original order.

```bash
uv run pytest tests/test_language.py -k non_repeating
```

### Q7. Read measurements from a file

Implement `parse_measurements(path)` using `pathlib.Path`, `with`, and
`enumerate`. Each non-empty line contains one finite number; return the values
as `list[float]`. A malformed or non-finite value should raise `ValueError`
that identifies its one-based line number. Do not catch unrelated file errors.
Use pytest's `tmp_path` fixture to create test files.

```bash
uv run pytest tests/test_language.py -k parse_measurements
```

### Q8. Python behaviour investigations

For each snippet, predict its behaviour, explain why, then rewrite it to make
the intended behaviour explicit.

#### a. A mutable default argument

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags


print(add_tag("first"))
print(add_tag("second"))
```

#### b. Equality and identity

```python
first = ["tea"]
second = ["tea"]
print(first == second)
print(first is second)
```

#### c. Aliasing through list multiplication

```python
rows = [[]] * 3
rows[0].append("changed")
print(rows)
```

#### d. Mutating a list while iterating

```python
values = [1, 2, 3, 4, 5, 6]
for value in values:
    if value % 2 == 0:
        values.remove(value)
print(values)
```

#### e. Floating-point representation

```python
print(0.1 + 0.2 == 0.3)
```

#### f. An exhausted iterator

```python
numbers = iter([1, 2, 3])
print(list(numbers))
print(list(numbers))
```

## Object-oriented Python

> **Prerequisites:** Python Fundamentals.
>
> **You’ll practice:** classes, instances, inheritance, method overriding,
> inherited behavior, and readable object representations.

Create an `Animal` base class in `src/pyproblems/oop.py`. Its initializer
should store an optional name. Its `speak()` method defines the interface and
raises `NotImplementedError`; subclasses provide their own sound by overriding
that method. Implement an inherited `lyric()` method that calls `self.speak()`
and formats a line such as `Dog goes "woof"`. Because this method calls the
overridden method, the same inherited code works for every subclass.

Start with `Dog` and `Cat`, then add `Bird`, `Mouse`, `Cow`, `Frog`, `Elephant`,
`Duck`, `Fish`, and `Seal`. Each class should inherit from `Animal` and
implement `speak()`. For example:

```python
dog = Dog("Milo")
print(dog.speak())
print(dog.lyric())
print(isinstance(dog, Animal))
```

Implement `__str__()` so `str(Dog("Milo"))` produces a useful description.
Then implement `zoo()` to create one instance of each animal, and
`render_animal_song(animals)` to combine their `lyric()` lines with the fixed
fox refrain. Return a string rather than printing it. The song tests compare
the complete text, including its final newline, with snapshots.

```bash
uv run pytest tests/test_oop.py -q
```

Notice that the song renderer does not need to ask what type each animal is.
It calls the same method on every object and lets the object's class choose
the behaviour. This is polymorphism through ordinary inheritance and method
overriding. Do not add a subclass solely to make the design more elaborate;
the Gilded Rose exercise later is a useful counterexample where helpers may be
clearer than a class hierarchy.

## Refactoring: The Gilded Rose Kata

> **Prerequisites:** Python Fundamentals and Object-oriented Python.
> **Check:** `uv run pytest tests/test_gilded_rose.py -q`

The mutable `Item` dataclass and deeply nested `update_quality` implementation
in [gilded_rose.py](src/pyproblems/gilded_rose.py) deliberately preserve the
original rules in a difficult-to-change form. Run the focused tests and read
the implementation before refactoring. The regular-item, Aged Brie, Sulfuras,
backstage-pass, quality-bound, and multiple-item tests characterize existing
behaviour. The Conjured Mana Cake cases are the new failing requirement: make
those pass while preserving every existing behaviour test.

Refactor in small steps, running the focused command after each change. Keep
the public data model as a mutable `Item` dataclass and the
`update_quality(items)` interface. You may choose helpers, subclasses, or
another design; the tests check behaviour rather than a particular hierarchy.

## Test-first Development: 99 Bottles

> **Prerequisites:** Python Fundamentals.
> **Check:** `uv run pytest tests/test_bottles.py -q`

Implement `verse(number)`, `verses(start, end)`, and `bottles()` in
[bottles.py](src/pyproblems/bottles.py). The tests in
[test_bottles.py](tests/test_bottles.py) are executable examples: make one
scenario pass at a time, then refactor without changing the lyrics. Preserve
singular and plural grammar, the zero-bottle wording, blank lines between
verses, and the final newline. The full song is compared with
[99_bottles.txt](tests/fixtures/99_bottles.txt).

After the original tests pass, extend `verse`, `verses`, and `bottles` to
accept a keyword-only `container="bottle"`. Before implementing it, add tests
for a regular plural verse, the one-container verse, and the zero case using
`container="can"`. Confirm those new tests fail, implement singular/plural
forms, then refactor while preserving the default lyrics. These extension
tests are intentionally left for you to write.

## Scientific Python and Data Analysis

> **Prerequisites:** Python Fundamentals and Object-oriented Python.
> **Dependencies:** install the optional scientific stack with
> `uv sync --all-groups --extra science`.

The functions in [statistics.py](src/pyproblems/statistics.py) are exercises:
their tests describe the expected behaviour, and their starter implementations
raise `NotImplementedError`. Work through them in dependency order:

1. Implement `standard_error` using the sample standard deviation. In
  [solutions.ipynb](solutions.ipynb), simulate samples for sizes 2 through 100
  and compare the estimates with the theoretical $1 / \sqrt{n}$ curve.
2. Implement `ols_coefficients` with `numpy.linalg.solve` on the normal
  equations. Compare it with `numpy.linalg.lstsq`, and explain why numerical
  libraries generally use more stable methods for real analyses.
3. Use `scipy.stats` to compare a binomial distribution with its normal
  approximation, including a continuity correction.
4. Implement `summarize_xy` and `summarize_xy_datasets`. Compare the 13 mystery
  datasets' summary statistics, then use shared axes and equal aspect ratio
  scatterplots to find what the summaries conceal.
5. Implement `bootstrap_standard_error` with explicit resampling and a
  keyword-only `numpy.random.Generator`. Compare it with the analytic standard
  error and report the simulation variability.
6. Implement `normal_log_likelihood`, `normal_likelihood`, and
  `fit_normal_mle`. Sum log densities directly, constrain the standard
  deviation through a log transform, and check optimizer success.

Use the notebook for the broader analyses: inspect the Steak/Tea/Toast
responses, preserve missing and invalid values in your reasoning, explore
categorical associations, and fit/diagnose linear models with statsmodels.
The original poll prompt shows the response scales used by the survey:

![Steak, toast, and tea poll response scales](assets/steak-toast-tea-poll.png)

The poll is self-selected and should not be treated as representative of a
population. Notebook code cells are intentionally empty learner workspaces.

Run the focused contracts with `uv run pytest tests/test_statistics.py -q`.
The tests are expected to fail until the exercise functions are implemented.

## Further Practice and Advanced Modelling

### Q1. Sudoku validity

Implement `sudoku(grid)` in [language.py](src/pyproblems/language.py). The
input is a 9 by 9 list of lists containing integers 1 through 9 or `None` for
blank cells. Return whether the supplied values are valid: no row, column, or
3 by 3 box may repeat a value. The puzzle need not be complete or solvable.
Use sets to check each group, and compare your result with the labelled puzzles
from `load_sudoku_data()`.

Check this exercise with `uv run pytest tests/test_sudoku.py -q`.

### Q2. Gaussian mixture models (advanced)

> **Prerequisites:** scientific-Python statistics and numerical optimization.
> **Dependencies:** the optional science extra.

In [statistics.py](src/pyproblems/statistics.py), implement
`gaussian_mixture_log_likelihood` and `fit_gaussian_mixture`. The likelihood
function takes named component means, positive standard deviations, a mixture
weight strictly between zero and one, and the observations. For each
observation, combine the weighted component densities in log space; avoid
underflow with stable log-sum-exp arithmetic.

The fitter returns a `GaussianMixtureFit` with named estimates for both means,
standard deviations, the first component's weight, and the log-likelihood.
Try several deterministic starting points, retain the best converged fit,
check optimizer status, and report the component with the smaller mean first.
Mixture fitting can have local optima, so do not rely on one arbitrary start.

Run the advanced contracts with `uv run pytest -m advanced -q`. The tests use a
fixed-seed sample and invariants rather than relying on global random state;
they are expected to fail until the advanced functions are implemented.

## Further Reading

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
