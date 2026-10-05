# Python Problems

## Introduction

Welcome! This is a hands-on collection of Python exercises, from small
programming puzzles to data analysis and statistical modelling. Start with
Python Fundamentals, then follow the sections in order or jump to a topic that
interests you. The early exercises are bite-sized; later notebooks, the kata,
and mixture-model work can each take several sessions.

The purpose of this package is to help you learn Python, not simply to collect
completed solutions. A coding agent could complete the exercises for you, but
that would bypass the practice they are designed to provide. Writing code,
investigating failures, and explaining your choices build an understanding of
Python that remains useful in the age of agentic coding: you need that
understanding to specify requirements, assess generated code, spot mistakes,
and maintain the result. Agents can support your learning with hints,
explanations, or reviews of your own attempts. Try each problem yourself first,
and make sure you can explain and test any code you adopt; passing tests alone
is not the learning goal.

As a rough guide, allow 25 to 50 hours for a full pass, depending on your
experience and how deeply you explore the investigations. Treat that as a
guide, not a deadline. For an overview of the repository layout and development
setup, see [DEVELOPMENT.md](DEVELOPMENT.md).

The dev container is ready to use. For a local setup with the notebooks and
scientific tools, install the complete environment with:

```bash
uv sync --all-groups --extra science
```

Most exercise functions start as stubs, so their tests will fail until you
implement them. Pick an exercise, read its prompt, and run its focused test
command; make one small change at a time and rerun the test. For your first
check, try `uv run pytest tests/test_language.py`. The early language exercises
use only the Python standard library; scientific exercises need the optional
science packages installed above.

## Python Fundamentals

> **Prerequisites:** none.
>
> **You’ll practice:** functions, sequences, comprehensions, iteration,
> dictionaries, generators, exceptions, and readable tests.

### Q1. Exponentiation

Write a function to take numbers $x$ and return $e^x$ as `exponentiate(values)`
in `src/pyproblems/language.py`. Note that the input can be any iterable, not
just a list.

Begin with a `for` loop and `list.append`. Once it works, try rewriting the
function as a list comprehension. Compare the two versions for readability.

Check this exercise with:

```bash
uv run pytest tests/test_language.py -k exponentiate
```

### Q2. Adjacent products

For a sequence of integers, consider every neighbouring pair and multiply its
two values. Return the largest of those products; pairs overlap, so
`[3, 6, -2, -5, 7, 3]` produces `18, -12, 10, -35, 21`, and the answer is
`21`. A negative pair can still be the maximum when every product is negative,
so do not assume the answer is at least zero.

Implement `adjacent_elements_product(values)` in `language.py`. Return `None`
when fewer than two values are supplied. The input may be any iterable.

If you didn't already, try now to implement this using `itertools.pairwise`
rather than indexing through positions.

```bash
uv run pytest tests/test_language.py -k adjacent
```

### Q3. FizzBuzz

FizzBuzz is a classic programming exercise. The goal is to visit each integer in
order, replace multiples of three with `Fizz`, multiples of five with `Buzz`,
and multiples of both with `FizzBuzz`.

Implement `fizzbuzz(n)` to return strings from 1 through `n`, inclusive.
`fizzbuzz(5)` returns `['1', '2', 'Fizz', '4', 'Buzz']`, and zero returns an
empty list.

You will need to raise `TypeError` for non-integer inputs and `ValueError` for a
negative integer to get all tests to pass.

```bash
uv run pytest tests/test_language.py -k fizzbuzz
```

### Q4. Fibonacci sequence

The Fibonacci sequence starts with $0, 1$; each later value is the sum of the
two before it. We can implement this neatly using
[generators](https://wiki.python.org/moin/Generators) in Python. A generator
suspends at each `yield`, keeping its local state until the next value is
requested. This gives callers a stream of values without constructing an
infinite list, and each generator call should own its own state.

Implement `fibonacci()` as a generator beginning `0, 1, 1, 2, 3, 5`. Each call
to `fibonacci()` should return an independent iterator. Try `next()` to request
individual values and `itertools.islice` to take a finite prefix without
materialising the infinite sequence.

```python
from itertools import islice

list(islice(fibonacci(), 8))
```

```bash
uv run pytest tests/test_language.py -k fibonacci
```

### Q5. First non-repeating character

Given a string, find the earliest character whose total count is exactly one.
For example, in `"abacabad"`, both `c` and `d` occur once, but `c` comes first;
in `"abacabaabacaba"`, every character repeats. Return `_` when no character
qualifies. The search is case-sensitive; spaces and punctuation count too.

Implement `first_non_repeating_character(text)`.

```bash
uv run pytest tests/test_language.py -k non_repeating
```

### Q6. Python gotchas

These short examples expose behaviour that can be surprising when translating
habits from other languages or when reading unfamiliar Python. Before running
each snippet, write down its output and explain the mechanism. Then rewrite it
so that the intended behaviour is explicit.

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

The goal is to keep only the odd values.

```python
values = [1, 2, 4, 6, 7]
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

### Q7. Sudoku checker

Sudoku asks you to fill a 9 by 9 grid so each row, column, and 3 by 3 box
contains the digits 1 through 9 exactly once. A partially filled grid is
*valid* when none of its supplied digits conflicts with those rules.

Implement `sudoku_checker(grid)` in [language.py](src/pyproblems/language.py).
The input is a list of nine rows containing integers 1 through 9 or `None` for
blanks.

Compare the result with the labelled puzzles from `load_sudoku_data()` and try
an empty grid, a valid completed grid, and a duplicate in each kind of
constraint group.

```bash
uv run pytest tests/test_sudoku.py -q
```

## Object-oriented Python

> **Prerequisites:** Python Fundamentals.
>
> **You’ll practice:** classes, instances, inheritance, method overriding,
> inherited behaviour, and readable object representations.

### Talking animals

Create an `Animal` base class in `src/pyproblems/oop.py`. Its initializer
should store an optional name. Its `speak()` method defines the interface and
raises `NotImplementedError`; subclasses provide their own sound by overriding
that method.

Implement an inherited `lyric()` method that calls `self.speak()`
and formats a line such as `Dog goes "woof"`. Because this method calls the
overridden method, the same inherited code works for every subclass. This is
polymorphism: the renderer asks each object to perform the same operation
without branching on its concrete type.

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

### What Does the Fox Say?

Now implement `zoo()` to create one instance of each animal, and
`wdtfs(animals)` to combine their `lyric()` lines with the fixed
fox refrain and return as a string to generate the lyrics to
[The Fox (What Does the Fox Say?)](https://www.youtube.com/watch?v=jofNR_WkoCE).

> Dog goes "woof"
> Cat goes "meow"
> Bird goes "tweet"
> Mouse goes "squeek"
> Cow goes "moo"
> Frog goes "croak"
> Elephant goes "toot"
> Duck goes "quack"
> Fish goes "blub"
> Seal goes "ow ow ow"
> But there's one sound
> That no one knows
> What does the fox say?
> "Ring-ding-ding-ding-dingeringeding!"

You can test your functions with

```bash
uv run pytest tests/test_oop.py -q
```

If this is implemented using object-orientation, you should notice that the
`wdtfs` function does not need to ask what type each animal is. It calls the
same method on every object and lets the object's class return the lyric line
appropriate for that animal. This is polymorphism through ordinary inheritance
and method overriding.

## Refactoring and Test-First Development

### The Gilded Rose Kata

> **Prerequisites:** Python Fundamentals and Object-oriented Python.
> **Check:** `uv run pytest tests/test_gilded_rose.py -q`

Below you'll find instructions for a code kata. The job here is to
implement a new request in existing code. Handily, tests already exist that
fully test the functionality of the existing code, three of which fail
(corresponding to the new request that is not yet implemented). You can trust
that the tests are correct and capture every scenario (within reason): if the
tests pass, your code is working.

Unfortunately for you, the current implementation of `update_quality` in [gilded_rose.py](src/pyproblems/gilded_rose.py) is deeply nested and difficult to modify so you will need to refactor it.

The setting is an inn that updates each item's `sell_in` countdown and `quality`
once per day. Ordinary goods lose quality faster after their sell-by date; Aged
Brie improves with age; Sulfuras never changes; and backstage passes become more
valuable as a concert approaches, then become worthless afterward. Quality is
generally bounded between 0 and 50, except Sulfuras, whose legendary quality is
left unchanged.

Run the focused tests and read the implementation before refactoring. The
regular-item, Aged Brie, Sulfuras, backstage-pass, quality-bound, and
multiple-item tests characterize existing behaviour. The new requirement is
that Conjured Mana Cake degrades twice as fast as an ordinary item, including
the faster post-expiration rate. Add that behaviour while preserving every
existing rule; use the tests to distinguish the boundary cases.

Refactor in small steps, running the focussed tests after each change. Keep
the public data model as a mutable `Item` dataclass and the
`update_quality(items)` interface. You may choose helpers, subclasses, or
another design; the tests check behaviour rather than a particular hierarchy.

#### Instructions

Hi and welcome to team Gilded Rose! As you know, we are a small inn with a
prime location in a prominent city ran by a friendly innkeeper named Allison.
We also buy and sell only the finest goods. Unfortunately, our goods are
constantly degrading in quality as they approach their sell by date. We have a
system in place that updates our inventory for us. It was developed by a
no-nonsense type named Leeroy, who has moved on to new adventures. Your task is
to add the new feature to our system so that we can begin selling a new
category of items. First an introduction to our system:

- All items have a "sell_in" value which denotes the number of days we have
  to sell the item.
- All items have a "quality" value which denotes how valuable the item is.
- At the end of each day our system lowers both values for every item.

Pretty simple, right? Well this is where it gets interesting:

- Once the sell by date has passed, quality degrades twice as fast.
- The quality of an item is never negative.
- "Aged Brie" actually increases in quality the older it gets.
- The quality of an item is never more than 50.
- "Sulfuras", being a legendary item, never has to be sold or decreases in
  quality.
- "Backstage passes", like aged brie, increases in quality as its sell_in
  value approaches; quality increases by 2 when there are 10 days or less
  and by 3 when there are 5 days or less but quality drops to 0 after the
  concert.

We have recently signed a supplier of "conjured" items. This requires an update
to our system:

- "Conjured" items degrade in quality twice as fast as normal items.

Refactor the internals and add helpers as needed, while preserving the mutable
`Item` dataclass and the `update_quality(items)` interface. Keep all existing
behaviour intact while adding the new requirement.

### 99 Bottles

> **Prerequisites:** Python Fundamentals.
> **Check:** `uv run pytest tests/test_bottles.py -q`

Implement `verse(number)`, `verses(start, end)`, and `bottles()` in
[bottles.py](src/pyproblems/bottles.py). The tests in
[test_bottles.py](tests/test_bottles.py) are executable examples: make one
scenario pass at a time, then refactor without changing the lyrics. Preserve
singular and plural grammar, the zero-bottle wording, blank lines between
verses, and the final newline. The full song is compared with
[99_bottles.txt](tests/fixtures/99_bottles.txt).

The exercise is deliberately test-first rather than a specification to solve
all at once. Start with one verse, then a range of verses, then the complete
song. Keep formatting decisions at the boundary where they belong: `verse`
creates one stanza, while `verses` and `bottles` compose those stanzas.

After the original tests pass, extend `verse`, `verses`, and `bottles` to
accept a keyword-only `container="bottle"`. Before implementing it, add tests
for a regular plural verse, the one-container verse, and the zero case using
`container="can"`. Confirm those new tests fail, implement singular/plural
forms, then refactor while preserving the default lyrics. These extension
tests are intentionally left for you to write.

## Scientific Python

> **Prerequisites:** Python Fundamentals and Object-oriented Python.
> **Dependencies:** install the optional scientific stack with
> `uv sync --all-groups --extra science`.

The functions in [statistics.py](src/pyproblems/statistics.py) are exercises:
their tests describe the expected behaviour, and their starter implementations
raise `NotImplementedError`. Work through them in dependency order, starting
with the questions below.

These exercises move from sampling variation, through linear models and
resampling, to likelihood-based estimation. Use the [statistical methods
notebook](analysis/statistical_methods.ipynb) for simulations, numerical
comparisons, and model visualizations; keep reusable calculations in
`statistics.py`.

### Q1. Sampling variation and standard error

The sample standard deviation describes variation among observations. The
standard error estimates variation in the sample mean across repeated
samples: $\widehat{\mathrm{SE}}(\bar{x}) = s / \sqrt{n}$.

Implement `standard_error` using the sample standard deviation. In the
[statistical methods notebook](analysis/statistical_methods.ipynb), simulate 500
independent samples for each $n$ from 2 through 100. Plot the mean of the
estimated standard errors against $n$ and compare it with the theoretical $1 /
\sqrt{n}$ curve; explain the sampling variation around that curve.

### Q2. Linear models and ordinary least squares

Ordinary least squares chooses coefficients that minimize the sum of
squared residuals. For a full-column-rank design matrix $X$ and outcome
vector $y$, the normal equations are
$X^\mathsf{T}X\hat{\beta}=X^\mathsf{T}y$.

Implement `ols_coefficients` by solving this system with `numpy.linalg.solve`,
not by explicitly computing an inverse. The function does not add an intercept:
include a column of ones when one is wanted. Compare with `numpy.linalg.lstsq`
in the [statistical methods notebook](analysis/statistical_methods.ipynb).

### Q3. The binomial and normal distributions

If $X\sim\mathrm{Binomial}(n,p)$, its mean is $np$ and its variance is
$np(1-p)$. When both expected counts $np$ and $n(1-p)$ are sufficiently
large, a normal distribution with that mean and variance can approximate
the binomial. Start with $n=100$ and $p=0.5$.

In the [statistical methods notebook](analysis/statistical_methods.ipynb), use
`scipy.stats` to plot the exact probability at each integer from 0 to 100
alongside the continuous normal density. Since a density is not a point
probability, also use a continuity correction. If
$Y\sim\mathcal{N}(np,np(1-p))$, compare $P(X=k)$ with $P(k-0.5<Y<k+0.5)$.
Investigate a value of $p$ nearer zero or one, where the approximation becomes
less reliable.

### Q4. Bootstrap standard error

A standard error describes how much a statistic, such as the sample mean,
would vary across repeated samples of the same size from a population. Since
we usually have only one sample, the bootstrap uses its observed values as a
stand-in for the population: repeatedly draw samples of size $n$ *with
replacement*, and calculate the statistic for each one. The standard deviation
of those bootstrap means estimates the standard error of the sample mean.

Implement `bootstrap_standard_error` by computing the mean of each of 1,000
resamples and returning the standard deviation of those means. Accept a
keyword-only `numpy.random.Generator` so the experiment is reproducible.

Compare the result with the analytic standard error; their difference is Monte
Carlo variation, not necessarily an implementation error.

### Q5. Likelihood and normal maximum likelihood estimation

For independent observations from a normal model, the joint likelihood is
$\mathcal{L}(\mu,\sigma\mid x)=\prod_i f(x_i\mid\mu,\sigma)$. This gives the
"density" for the observed data as a function of the parameters.

Calculating this quantity can be difficult because products of small densities
can underflow. As a result, it is more convenient to consider the log
likelihood. For the purposes of finding the parameter combinations that maximise
the likelihood (which we are about to come on to), considering the log
likelihood instead is suitable because it always increases/decreases when the
likelihood increases/decreases. Implement `normal_log_likelihood` as a sum of
log densities.

Implement `fit_normal_mle` by numerical optimization, constrain the positive
standard deviation (for example, optimize its logarithm), and check optimizer
success. As a validation, compare with the analytical estimates: the sample mean
and the population standard deviation. In the
[statistical methods notebook](analysis/statistical_methods.ipynb), investigate
the bias of these estimates across repeated samples.

Run the tests with `uv run pytest tests/test_statistics.py -q`.

## Data Analysis

### 1. Mysterious data

Thirteen coordinate datasets are packaged under neutral names. In the
[mysterious data notebook](analysis/mysterious_data.ipynb), implement
`summarize_xy` and `summarize_xy_datasets` in
[statistics.py](src/pyproblems/statistics.py), then compare their means,
sample standard deviations, and Pearson correlations. Based only on those
summaries, note which datasets seem interchangeable and record your
prediction.

Next, plot all 13 datasets with shared axis limits and equal aspect ratio.
Do the plots support your prediction? Describe the patterns you observe and
explain why you should inspect data before choosing a model.

```bash
uv run pytest tests/test_statistics.py -k summarize_xy
```

### 2. Categorical data: Steak, Tea, and Toast

Included in this package is a simple dataset compiled from the results of a
Facebook poll (in
[steak_toast_tea.csv](src/pyproblems/datasets/steak_toast_tea.csv)).

![Steak, toast, and tea poll response scales](assets/steak-toast-tea-poll.png)

Each row is one response
and the three columns use the labels shown in the image:

- `Steak`: intended values 1 (rarest) to 5 (most well done)
- `Toast`: 1 (lightest) to 6 (most burnt)
- `Tea`: `a` (darkest) to `f` (milkiest)

These are ordered categories, not continuous measurements. The source also
contains some missing responses and a steak value of `0` that is not among the
displayed choices. Keep the raw data unchanged, make a cleaned copy, and
explain any decision about those observations instead of silently discarding
them.

Complete the first investigation in the
[Steak, Tea, and Toast notebook](analysis/steak_tea_toast.ipynb): inspect
row counts, column types, category levels, and missing counts; make ordered
categoricals; calculate frequency and proportion tables; and visualize
contingency tables for two pairs of questions. If you test for association,
inspect expected cell counts before using a chi-squared approximation. Sparse
tables may call for Fisher's exact test or a simulated reference distribution.

Finish with two findings and two limitations.

### 3. Linear regression and diagnostics

For the final investigation in the
[mysterious data notebook](analysis/mysterious_data.ipynb), return to the 13
coordinate datasets. Fit a line to the first dataset, interpret its
intercept, slope, and $R^2$, then compare
confidence intervals for the mean response with prediction intervals for an
individual observation. Plot the fit and inspect residuals and a normal Q-Q
plot. Repeat the fit and plots for all 13 datasets. Finally, construct a
design matrix with an intercept and compare statsmodels with
`ols_coefficients`. A fitted line and a compact model summary do not replace
looking at the data and checking model assumptions.

## Statistical Modelling

### Gaussian-mixture

> **Prerequisites:** scientific-Python statistics and numerical optimization.
> **Dependencies:** the optional science extra.

Suppose observations come from one of two Gaussian distributed populations, but
we do not know which population produced each observation. If the first
population has weight $\pi$, the density for one observation is

$$
f(x\mid\theta) = \pi \phi(x\mid\mu_1,\sigma_1)
 + (1-\pi) \phi(x\mid\mu_2,\sigma_2),
$$

where $\phi$ is the Gaussian density function and
$\theta=(\mu_1,\sigma_1,\mu_2,\sigma_2,\pi)$. The likelihood is the product
of these mixture densities across observations.

In [statistics.py](src/pyproblems/statistics.py), implement
`gaussian_mixture_log_likelihood` and `fit_gaussian_mixture`. The likelihood
function takes named component means, positive standard deviations, a mixture
weight (strictly between zero and one), and the observations. For each
observation, combine the weighted component densities in log space.

`fit_gaussian_mixture` should return a dictionary (with keys `mean1`,
`standard_deviation1`, `mean2`, `standard_deviation2`, `weight1`, and
`log_likelihood`). You can use `scipy.optimize.minimize` to maximize the
log-likelihood by minimizing its negative.

For unconstrained optimization,
represent each standard deviation as the exponential of an unconstrained
parameter, and represent `weight1` with the logistic transform so it stays
between zero and one. Try several deterministic starting points, keep the best
successful result, and report the component with the smaller mean first. Mixture
fitting can have local optima, so do not rely on one arbitrary start.

Run the tests with `uv run pytest tests/test_advanced_models.py -q`.

### Gaussian-mixture EM

The direct-optimization exercise above estimates mixture parameters by
optimizing the likelihood. Expectation-Maximization (EM) uses a different
view: imagine that every observation has an unobserved component label. If
those labels were known, fitting each normal distribution would be
straightforward. EM alternates between estimating the missing labels from the
current parameters (the E-step) and re-estimating the parameters using those
labels (the M-step).

For a univariate two-component mixture, let $r_i$ be the probability that
observation $x_i$ belongs to component one. The soft E-step computes

$$
r_i = \frac{\pi\,\phi(x_i\mid\mu_1,\sigma_1)}
{\pi\,\phi(x_i\mid\mu_1,\sigma_1)+(1-\pi)\,\phi(x_i\mid\mu_2,\sigma_2)}.
$$

The hard E-step instead assigns each observation to whichever weighted
component density is larger. In the M-step, update each component's mean and
population standard deviation from its hard labels or soft weights; update
$\pi$ from the fraction or average responsibility assigned to component one.
Hard EM makes a definite assignment, while soft EM preserves uncertainty.
Both can converge to a local optimum, so the starting parameters matter.

For soft weights, the component-one updates illustrate the calculation:
$\mu_1=\sum_i r_i x_i/\sum_i r_i$ and
$\sigma_1^2=\sum_i r_i(x_i-\mu_1)^2/\sum_i r_i$; component two uses weights
$1-r_i$, and $\pi$ is the average of the $r_i$ values. These are population
standard deviations, as required for maximum-likelihood estimation.

Work in [mixture_models.py](src/pyproblems/mixture_models.py) to implement
hard and soft expectation/maximization steps, the generic
`expectation_maximization` loop, and univariate and multivariate fitting.
Pass the E-step, M-step, and log-likelihood callables to the generic loop.
Represent parameter sets with the supplied dataclasses. The log-likelihood
must sum log mixture densities stably. Stop when the likelihood improvement
is below the tolerance or the iteration limit is reached; report whether the
fit converged. Handle an empty hard-assignment component and singular
covariance matrices deliberately rather than allowing invalid parameters to
silently propagate. Since the component labels can be swapped without
changing the model, return the lower-mean component first.

`load_faithful_data()` in [data.py](src/pyproblems/data.py) provides eruption
duration and waiting-time values from the R `datasets` package, in that
column order. The two measurements form clusters: shorter eruptions tend to
be followed by shorter waits, while longer eruptions tend to precede longer
waits. The bivariate model replaces each standard deviation with a covariance
matrix so it can represent the relationship between the measurements.
`fit_faithful_gaussian_mixture()` applies the multivariate model to this
dataset. In the [statistical methods notebook](analysis/statistical_methods.ipynb),
plot the starting contours and fitted clusters, and
compare the result with the reference likelihood in the tests. EM is not
guaranteed to find the global maximum from every starting point.

```bash
uv run pytest tests/test_mixture_models.py -m advanced -q
```

## Algorithms and Search

### Word ladder

A word ladder changes one letter at a time, and every word along the route must
appear in the packaged word list (common English words, derived from
[SCOWL](http://wordlist.aspell.net/)). Your job is to implement a
function to construct the shortest word ladder from a starting word to get to a
final word (or one such route if there are multiple).

Use `load_words()` from [data.py](src/pyproblems/data.py) to load the
lowercase word set. Implement `word_ladder(start, target, words)` in
[word_ladder.py](src/pyproblems/word_ladder.py) to return a shortest route,
including both endpoints, or `None` if no route exists. The number of moves is
one less than the number of words in the returned route. The start and target
must be lowercase words of the same length and both must appear in `words`.

Breadth-first search is a natural fit for this problem. Record each word's
predecessor so you can reconstruct a shortest route once the target is found.

For example, starting from `play`, we can find the following ladders:

- `plan` takes one move only (we just change "y" to "n").
- `snap` takes three moves (`play -> slay -> slap -> snap`)
- `pool` takes four (`play -> ploy -> plop -> poop -> pool`)
- `golf` takes six (`play -> clay -> clad -> glad -> goad -> gold -> golf`)
- `ball` takes seven (`play -> slay -> slam -> seam -> seal -> sell -> bell -> ball`)

How many moves does it take to get from `play` to `game`? Give one valid
shortest route.

```bash
uv run pytest tests/test_word_ladder.py -q
```

### Global sequence alignment

The Needleman-Wunsch algorithm is a dynamic-programming method for *global*
alignment: it aligns both sequences from beginning to end, inserting gaps
where useful. This models the idea that the sequences share an overall extent,
even if insertions or deletions have shifted later characters. It is used in
bioinformatics to compare DNA, RNA, or protein sequences.

For this exercise, a matching pair scores +1, a mismatch scores -1, and a
character aligned with a gap scores -1. For example:

```
ATAGTC-AC-AT
AAA-TCGACAAA
```

The score is the sum across columns: equal characters contribute +1 and every
other column contributes -1. Use a dynamic-programming table whose entry
$D_{i,j}$ is the best score for aligning the first $i$ and $j$ characters.
Initialize the first row and column with the cost of aligning that many
characters to gaps. Each later cell chooses the best of a match/mismatch
diagonal, a gap in the first sequence, or a gap in the second:

$$
D_{i,j}=\max\begin{cases}
D_{i-1,j-1}+s(a_i,b_j),\\
D_{i-1,j}-1,\\
D_{i,j-1}-1,
\end{cases}
\qquad
s(a_i,b_j)=\begin{cases}+1 & a_i=b_j,\\-1 & a_i\ne b_j.\end{cases}
$$

Implement
`needleman_wunsch_score(first, second)` and
`needleman_wunsch_alignment(first, second)`. Use dynamic programming with a
score of +1 for a match and -1 for a mismatch or gap. The score function needs
only the best score in the final cell. The alignment function traces back
through the table to recover one optimal pair of strings. Ties can produce
different but equally valid alignments; removing gaps must recover the original
inputs. The longer DNA fixture checks that the same algorithm scales beyond
the small worked example.

```bash
uv run pytest tests/test_alignment.py -q
```

### Sudoku solver

We are now going to build on our earlier Sudoku problem. We previously wrote a
function to check a Sudoku grid was valid, and now we will write a new function
to find a solution.

One approach is a recursive backtracking algorithm. Try a valid digit in an
empty cell, then continue from the resulting partial grid. If that choice leads
to a dead end, undo it and try the next digit. Stop when you find one complete
solution; there is no need to enumerate every possible completion.

Use this outline:

```text
solve(grid):
  find an empty cell
  if there is no empty cell:
    return a copy of the completed grid
  for each digit from 1 through 9:
    if the digit is legal in this cell:
      place the digit
      solution = solve(grid)
      if solution was found:
        return solution
      clear the cell to backtrack
  return no solution
```

Reject a starting grid that already contains conflicting clues. Work on a copy
of the input so the original grid is unchanged.

Build on `sudoku_checker` in [language.py](src/pyproblems/language.py) by
implementing `is_valid_placement(grid, row, column, value)` and
`sudoku_solver(grid)` in [sudoku.py](src/pyproblems/sudoku.py). Coordinates
are zero-based and blank cells are `None`. Return one solved grid, or `None` if
the clues are inconsistent or no solution exists. Do not mutate the input;
raise `ValueError` for a malformed grid. Test a completed grid, an unsolvable
grid, and a puzzle with multiple valid solutions, as well as the supplied
puzzles.

```bash
uv run pytest tests/test_sudoku_solver.py -q
```

## Models of Life

These two small simulations explore how systems change over time. Game of Life
is deterministic: the board and rules determine each next generation. Dawkins'
weasel is stochastic: random mutation and selection mean repeated runs can
differ. Both are simplified models and are interesting in unique ways.

### Conway's Game of Life

Conway's Game of Life is a cellular automaton: a grid of live and dead cells
changes in discrete generations according to local rules. Despite the simple
rules, repeated updates can produce still lifes, oscillators, and patterns
that move across the board.

For each cell, inspect its eight neighboring positions. A live cell survives
with two or three live neighbors; a dead cell becomes live with exactly three;
all other cells are dead in the next generation. This exercise uses finite,
bounded arrays rather than wrapping edges: a corner has only three available
neighbors, and cells outside the board are not counted. A step returns a new
board of the same dimensions.

In [game_of_life.py](src/pyproblems/game_of_life.py), implement
`count_live_neighbors` and `step_game_of_life` with NumPy arrays. Boards are
bounded as described above. The glider, lightweight/middleweight/heavyweight
spaceships, and Gosper glider gun are provided as readable rows in
[game_of_life_shapes.yaml](src/pyproblems/datasets/game_of_life_shapes.yaml);
`load_shape(name)` and `render_board` are already implemented. Rows use `O`
for live cells and `.` for empty cells. Focus on the
neighbor-count and generation-update algorithms. Consider shifted array slices
or padding to vectorize the local counts without accidentally wrapping edges.

In the [Game of Life notebook](analysis/game_of_life.ipynb), place a pattern
inside a larger empty board, iterate many generations, and animate the frames.
The supplied patterns are starting
conditions, not additional implementation tasks.

```bash
uv run pytest tests/test_game_of_life.py -q
```

### Dawkins' weasel

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
[weasel simulation notebook](analysis/weasel_simulation.ipynb):

1. How many possible 28-character phrases are there? What is the probability
  that a random phrase has at least one correct position, and exactly one?
2. If no position currently matches, use the complement rule to find the
  probability that at least one of ten offspring gains a correct position.
  For small $x$ and large $n$, the approximation
  $(1-x)^n\approx e^{-nx}$ can simplify the calculation.
3. Once 18 positions match, what must happen at each of the remaining ten
  positions for one offspring to match the entire target? What is the chance
  that any of ten offspring does so?
4. Which assumptions make this a poor model of evolution in nature? Consider
  the known target, the simple mutation process, and selection based on one
  fixed score.

Then implement `matching_characters`, `mutate_message`, and `evolve_weasel` in
[evolution.py](src/pyproblems/evolution.py). Each generation creates a fixed
number of mutated copies, keeps a highest-scoring candidate, and records the
best score. Use the [weasel simulation notebook](analysis/weasel_simulation.ipynb)
to investigate time to target and how the mutation rate affects convergence
for a population of 100. Compare several
seeded runs rather than treating one random run as a universal answer.

```bash
uv run pytest tests/test_evolution.py -m advanced -q
```

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
- [Needleman-Wunsch algorithm](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm)
- [Sudoku solving algorithms](https://en.wikipedia.org/wiki/Sudoku_solving_algorithms)
- [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [Expectation-Maximization](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)
- [Dawkins' weasel program](https://en.wikipedia.org/wiki/Weasel_program)
