# Python Problems

## Introduction

Welcome! This is a hands-on collection of Python exercises, from small
programming puzzles to data analysis and statistical modelling. Start with
Python Fundamentals, then choose one of the routes below or jump to a topic that
interests you. The early exercises are bite-sized; later notebooks, the kata,
and mixture-model work can each take several sessions. If you complete all the
exercises you'll have touched on python fundamentals such as list
comprehensions, generators and object orientation, but also maximum likelihood,
expectation-maximisation, recursion, test first development, refactoring,
breadth-first search and even cellular automaton.

The purpose of this package is partially to help you learn Python, but is also a
collection of interesting and hopefully satisfying problems to solve. It is not
simply about collecting completed solutions. A coding agent could complete the
exercises for you, but that would bypass the practice and interest they are
designed to provide. Writing code, investigating failures, and explaining your
choices build an understanding of Python that remains useful in the age of
agentic coding: you need that understanding to specify requirements, assess
generated code, spot mistakes, and maintain the result. Agents can support your
learning with hints, explanations, or reviews of your own attempts. Try each
problem yourself first, and make sure you can explain and test any code you
adopt; passing tests alone is not the learning goal.

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

Most exercise functions start as stubs, so their tests will fail until you
implement them. Pick an exercise, read its prompt, and run its focused test
command; make one small change at a time and rerun the test. For your first
check, try `uv run pytest tests/test_language.py`. The early language exercises
use only the Python standard library; scientific exercises need the optional
science packages installed above.

## Choosing a route

Each route has its own test commands, and finishing one counts as completing a
useful course. The exercises that follow are in the order of the sections below,
not the order of the routes.

**Route 1: Python core.** Learn the language and practise writing tested code.

1. Python Fundamentals, Q1 to Q7:
   `uv run pytest tests/test_language.py tests/test_sudoku.py -q`
2. Object-oriented Python, from talking animals to the parrot:
   `uv run pytest tests/test_oop.py -q`
3. One kata from Refactoring and Test-First Development, either Gilded Rose
   (`tests/test_gilded_rose.py`) or 99 Bottles (`tests/test_bottles.py`). The
   other is optional.
4. Word ladder: `uv run pytest tests/test_word_ladder.py -q`

You have finished this route when the word ladder works.

**Route 2: Scientific Python.** Work with real data. Do Route 1 first, then:

1. Data Analysis Q1, Mysterious data.
2. Scientific Python Q1, Q2 and Q4 (standard error, least squares and the
   bootstrap): `uv run pytest tests/test_statistics.py -k "standard_error or ols"`
3. Data Analysis Q2 (Steak, Tea, and Toast) and Q3 (Old Faithful regression).
4. Optionally, Models of Life: Game of Life and Dawkins' weasel.

You have finished this route when you can explain why a single straight line is
not a good model for the Old Faithful data.

**Route 3: Advanced extensions.** Choose what interests you. The algorithm
projects (Sudoku solver, global sequence alignment) need only Route 1. The
modelling projects (Scientific Python Q3 and Q5, and Statistical Modelling)
need Route 2, and some comfort with probability densities, likelihood, logs,
basic linear algebra and covariance matrices.

You have finished this route when you have completed whichever extension you
chose, for example the expectation-maximisation fit of the Old Faithful data.

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

If you didn't already, try to implement this using `itertools.pairwise`
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

Given a string, find and return the first instance of a non-repeating character
in it. If there is no such character, return `"_"`.

For example, in `"abacabad"`, both `c` and `d` occur once, but `c` comes first;
in `"abacabaabacaba"`, every character repeats. The search is case-sensitive;
spaces and punctuation count too.

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
should store an optional name on the instance, so that `animal.name` returns
it (or `None` if none was given). Its `speak()` method defines the interface
and raises `NotImplementedError`; subclasses provide their own sound by
overriding that method.

Implement an inherited `lyric()` method that calls `self.speak()`
and formats a line such as `Dog goes "woof"`. Because this method calls the
overridden method, the same inherited code works for every subclass. This is
polymorphism: the renderer asks each object to perform the same operation
without branching on its concrete type.

Start with `Dog` and `Cat`, then add `Bird`, `Mouse`, `Cow`, `Frog`, `Elephant`,
`Duck`, `Fish`, and `Seal`. Each class should inherit from `Animal` and
implement `speak()`. For example:

```python
dog = Dog("Woofy Goldberg")
print(dog.speak())
print(dog.lyric())
print(dog.name)
print(isinstance(dog, Animal))
```

Implement `__str__()` so `str(Dog("Woofy Goldberg"))` produces
`Dog named Woofy Goldberg`, and `str(Cat())` (no name) is just `Cat`. Notice
what is shared and what is not: the sound and the class name belong to the
class, so every `Dog` goes "woof", but the name belongs to each instance, so two
`Dog` objects can have different names. `lyric()` uses the class name, not the
instance name.

### What Does the Fox Say?

Add a `Fox` class. Its `speak()` returns the refrain
`"Ring-ding-ding-ding-dingeringeding!"`, but the fox's verse is more than a
`goes` line, so `Fox` overrides `lyric()` to return the whole closing verse.

Now implement `zoo()` to create one instance of each of the ten animals above
(not the fox), each with a name of its own. Call the dog "Woofy Goldberg" and
the cat "Chairman Meow", and invent equally good names for the rest. Then
implement `wdtfs(animals)` to combine their `lyric()` lines with a
`Fox`'s `lyric()` and return as a string to generate the lyrics to
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

### A parrot that learns

So far each subclass only returns a fixed string. Subclasses become more
interesting when they have state. Add `Parrot(Bird)`, which repeats the last
sound it heard:

```python
polly = Parrot("Polly")
print(polly.speak())  # tweet
polly.hear("hello")
print(polly.speak())  # hello
print(polly.lyric())  # Parrot goes "hello"
```

Before it hears anything, a `Parrot` should behave like any other `Bird`, so
use `super()` rather than repeating `"tweet"`. You should not need to change
`lyric()`: it calls `self.speak()`, so it works for the parrot unchanged. A
lookup table of sounds could not do this.

## Refactoring and Test-First Development

### The Gilded Rose Kata

> **Prerequisites:** Python Fundamentals and Object-oriented Python.
> **Check:** `uv run pytest tests/test_gilded_rose.py -q`

Below you'll find instructions for a code kata. The job here is to implement a
new request in existing code. Handily, tests already exist that test the
functionality of the existing code, three of which fail (corresponding to the
new request that is not yet implemented). You can trust that the tests are
correct and capture every scenario (within reason): if the tests pass, your code
is working.

Unfortunately for you, the current implementation of `update_quality` in
[gilded_rose.py](src/pyproblems/gilded_rose.py) is deeply nested and difficult
to modify so you will need to refactor it.

The setting is an inn that updates each item's `sell_in` countdown and `quality`
once per day. Ordinary goods lose quality faster after their sell-by date; Aged
Brie improves with age; Sulfuras never changes; and backstage passes become more
valuable as a concert approaches, then become worthless afterward. Quality is
generally bounded between 0 and 50, except Sulfuras, whose legendary quality is
left unchanged.

Run the focused tests and read the implementation before refactoring. The
regular-item, Aged Brie, Sulfuras, backstage-pass, quality-bound, and
multiple-item tests characterize existing behaviour. The new requirement is to
implement a new item: "Conjured Mana Cake" that degrades twice as fast as an
ordinary item, including the faster post-expiration rate. 

Refactor in small steps, running the focussed tests after each change. Refactor
first to make it easy to add the new requirement. Keep the public data model as
a mutable `Item` dataclass and the `update_quality(items)` interface. You may
choose helpers, subclasses, or another design; the tests check behaviour rather
than a particular hierarchy.

The original instructions for this kata are provided in the source code.

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
resampling, to likelihood-based estimation. They use two notebooks: the
[Old Faithful notebook](analysis/old_faithful.ipynb) applies the functions to a
real dataset, and the [simulation studies notebook](analysis/simulation_studies.ipynb)
uses simulated data with known parameters, so you can check what the methods do.
Keep reusable calculations in `statistics.py`.

### Q1. Sampling variation and standard error

The standard error (SE) of the sample mean $\bar{x}$ measures how much $\bar{x}$
varies from one sample to the next. If the observations have true standard
deviation $\sigma$, the SE is $\sigma/\sqrt{n}$. We rarely know $\sigma$, so we
estimate the SE by replacing it with $s$, the standard deviation of the sample
we actually have (using $n-1$ in the denominator):
$\widehat{\mathrm{SE}}(\bar{x}) = s / \sqrt{n}$.

Implement `standard_error` using $s$. In the
[Old Faithful notebook](analysis/old_faithful.ipynb), use it to report the mean
waiting time between eruptions with its standard error. Then, in the
[simulation studies notebook](analysis/simulation_studies.ipynb), simulate 500
independent samples of standard normal data ($\sigma=1$) for each $n$ from 2
through 100. The true SE is then $1/\sqrt{n}$. Plot the mean of the estimated
standard errors against $n$ and compare it with that curve; explain the
sampling variation around it.

Note that the two will not match exactly due to Jensen's inequality![^se-bias]

[^se-bias]: Each estimate $s/\sqrt{n}$ is random because $s$ changes from sample
    to sample, which is the sampling variation. However, there is also a small
    systematic gap. The sample variance $s^2$ averages exactly $\sigma^2$ (it is
    unbiased), but taking a square root bends the average downwards, so $s$
    averages slightly less than $\sigma$ (this is an instance of [Jensen's
    inequality](https://en.wikipedia.org/wiki/Jensen%27s_inequality)). The
    effect is noticeable for small $n$: at $n=2$ the average estimate is about
    0.564, not 0.707. Running more repetitions smooths the random variation but
    does not remove this gap.

### Q2. Linear models and ordinary least squares

Ordinary least squares chooses coefficients that minimize the sum of
squared residuals. For a full-column-rank design matrix $X$ and outcome
vector $y$, the normal equations are
$X^\mathsf{T}X\hat{\beta}=X^\mathsf{T}y$.

Implement `ols_coefficients` by solving this system with `numpy.linalg.solve`,
not by explicitly computing an inverse. The function does not add an intercept:
include a column of ones when one is wanted. In the
[simulation studies notebook](analysis/simulation_studies.ipynb), simulate
outcomes from known coefficients and compare your estimates with the truth and
with `numpy.linalg.lstsq`. You will use `ols_coefficients` on real data later.

### Q3. The binomial and normal distributions

If $X\sim\mathrm{Binomial}(n,p)$, its mean is $np$ and its variance is
$np(1-p)$. When both expected counts $np$ and $n(1-p)$ are sufficiently
large, a normal distribution with that mean and variance can approximate
the binomial. Start with $n=100$ and $p=0.5$.

In the [simulation studies notebook](analysis/simulation_studies.ipynb), use
`scipy.stats` to plot the exact probability at each integer from 0 to 100
alongside the continuous normal density.

A density is not a probability: a continuous variable has probability zero of
equalling any single value, whereas $P(X=k)$ is a positive point mass. The
*continuity correction* bridges the two by treating each integer $k$ as
standing for the unit-width interval from $k-0.5$ to $k+0.5$. If
$Y\sim\mathcal{N}(np,np(1-p))$, then

$$
P(X=k)\approx P(k-0.5<Y<k+0.5),
\qquad
P(X\le k)\approx P(Y<k+0.5).
$$

The second approximation is the one that matters when summing over many values.
Without the $+0.5$, $P(Y<k)$ misses half of the bar at $k$ and is
systematically too small. Compare the exact probabilities with both the
corrected normal probabilities and the uncorrected ones, for example by plotting
the errors, and check the effect on a cumulative probability such as
$P(X\le 45)$. Investigate a value of $p$ nearer zero or one, where the
approximation becomes less reliable.

### Q4. Bootstrap standard error

A standard error describes how much a statistic, such as the sample mean,
would vary across repeated samples of the same size from a population. Since
we usually have only one sample, the bootstrap uses its observed values as a
stand-in for the population: repeatedly draw samples of size $n$ *with
replacement*, and calculate the statistic for each one. The standard deviation
of those bootstrap means estimates the standard error of the sample mean.

Implement `bootstrap_standard_error` by computing the mean of each of 10,000
resamples and returning the standard deviation of those means. Accept a
keyword-only `numpy.random.Generator` so the experiment is reproducible.

You should use the *sample* standard deviation (`ddof=1`) of the resample means;
at 10,000 resamples the convention matters little though. Compare the result
with the analytic standard error, which uses `ddof=1` on the original sample.
For a fixed sample, the exact bootstrap standard error of the mean is
$\mathrm{std}(x, \mathrm{ddof}=0)/\sqrt{n}$, so even infinitely many resamples
differ from the analytic value by the factor $\sqrt{(n-1)/n}$. What remains is
Monte Carlo error, which shrinks as the number of resamples grows. In the
[Old Faithful notebook](analysis/old_faithful.ipynb), apply it to the waiting
times, and try random subsamples of small and moderate size to see the two
effects separately.

### Q5. Likelihood and normal maximum likelihood estimation

For independent observations from a normal model, the joint likelihood is
$\mathcal{L}(\mu,\sigma\mid x)=\prod_i f(x_i\mid\mu,\sigma)$, where $f$ is the
normal density. This gives the
"probability density" for the observed data ($x$) as a function of the
parameters ($\mu,\sigma$).

Calculating this quantity can be difficult because products of small densities
can underflow. As a result, it is more convenient to consider the log
likelihood
$\ell(\mu,\sigma\mid x)=\log\mathcal{L}(\mu,\sigma\mid x)=\sum_i \log f(x_i\mid\mu,\sigma)$.
For the purposes of finding the parameter combinations that maximise
the likelihood (which we are about to come on to), considering the log
likelihood is suitable because it always increases/decreases when the
likelihood increases/decreases. Implement `normal_log_likelihood` as a sum of
log densities.

Implement `fit_normal_mle` by numerical optimization, constrain the positive
standard deviation (for example, optimize its logarithm), and check optimizer
success. As a validation, compare with the analytical estimates: the sample mean
and the population standard deviation. In the
[Old Faithful notebook](analysis/old_faithful.ipynb), fit a normal distribution
to the waiting times and judge how well it describes them. In the
[simulation studies notebook](analysis/simulation_studies.ipynb), investigate
the bias of these estimates across repeated samples.

Optimizers can fail, for example reporting "precision loss" on small samples or
on data far from zero or with a tiny spread. Start from a sensible guess based
on the data, check the optimizer's `success` and `message` instead of assuming
it worked, and if it fails try a different starting point. Your fit should work
across many seeded small samples and on shifted and rescaled data.

Run the tests with `uv run pytest tests/test_statistics.py -q`.

## Data Analysis

### Q1. Mysterious data

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

### Q2. Categorical data: Steak, Tea, and Toast

Included in this package is a simple dataset compiled from the results of a
Facebook poll.

![Steak, toast, and tea poll response scales](assets/steak-toast-tea-poll.png)

The data is available in `src/pyproblems/datasets/steak_toast_tea.csv`. Each row
is one response and the three columns use the labels shown in the image:

- `Steak`: intended values 1 (rarest) to 5 (most well done)
- `Toast`: 1 (lightest) to 6 (most burnt)
- `Tea`: `a` (darkest) to `f` (milkiest)

These are ordered categories. The source also contains some missing responses
and several values outside the displayed scales. Audit every column to find them
all. Keep the raw data unchanged, then make a cleaned copy, and explain any
decision about these observations instead of silently discarding or altering
them. More than one policy is defensible (for example, treat them as missing, or
keep half-step values as extra ordered levels); say which you chose and why.

Complete the first investigation in the
[Steak, Tea, and Toast notebook](analysis/steak_tea_toast.ipynb): inspect
row counts, column types, category levels, and missing counts; make ordered
categoricals; calculate frequency and proportion tables; and visualize
contingency tables for two pairs of questions. State the denominator of every
proportion, and whether you used all rows for each variable or only complete
pairs; select complete rows explicitly before cross-tabulating.

You can now try to test for any statistical associations between the questions.
If you get stuck, there is a hint.[^association-hint]

[^association-hint]: To test for association between a pair of questions, you
    could use a Spearman rank correlation (`scipy.stats.spearmanr`), which gives
    both a correlation and a p-value. A chi-squared test of independence would
    ignore the ordering and, with tables as large as 5 by 6, spread its power
    across many degrees of freedom. Because Spearman uses only ranks, any
    increasing coding of the levels gives the same answer. Note that it detects
    a consistent increasing or decreasing trend, not every possible kind of
    association.

    Testing every pair of columns means several p-values at once. Consider what
    that does to the chance of at least one false positive, and how you would
    adjust for it (for example, a Bonferroni correction) or at least report it.

    As an extension, compare Spearman with Kendall's $\tau_b$
    (`scipy.stats.kendalltau`) and with a permutation-test p-value
    (`scipy.stats.permutation_test`), both of which deal with the many ties in
    these data differently.

### Q3. Linear regression: predicting the next Old Faithful eruption

Visitors to Old Faithful geyser want to know how long they will wait for the
next eruption. `load_faithful_data()` in [data.py](src/pyproblems/data.py)
provides each eruption's duration and the waiting time until the following one,
both in minutes. In the
[Old Faithful notebook](analysis/old_faithful.ipynb), fit a
straight line predicting the waiting time from the eruption duration, using
`ols_coefficients` with an intercept column. Interpret the intercept and slope in
minutes, calculate $R^2$, and predict the wait after a 2-minute and a 4-minute
eruption. Plot the data with the fitted line, and plot the residuals against the
fitted values.

The line has a decent $R^2$, but is it a good model? Look at both plots and
think about what the residuals are telling you. We will come back to this data
in the mixture-modelling section.

## Statistical Modelling

### Gaussian-mixture

> **Prerequisites:** scientific-Python statistics and numerical optimization.
> **Dependencies:** the optional science extra.
>
> **Optional:** this direct-optimization exercise can be skipped. The
> expectation-maximization section that follows does not depend on it.

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

Optimizing a mixture is trickier than fitting a single normal, so there is a
hint for the optimization, including a minimum standard deviation that the tests
expect.[^mixture-hint]

[^mixture-hint]: For unconstrained optimization, represent each standard
    deviation as a floor plus the exponential of an unconstrained parameter, and
    represent `weight1` with the logistic transform so it stays between zero and
    one. Try several deterministic starting points, keep the best successful
    result, and report the component with the smaller mean first. Mixture
    fitting can have local optima, so do not rely on one arbitrary start. Derive
    the starting points from the location and spread of the data, so shifted or
    rescaled observations give correspondingly shifted or rescaled fits.

    There is one catch: the likelihood has no true maximum. If you centre one
    component on a single observation and shrink its standard deviation towards
    zero, its density at that point grows without bound (a very narrow normal
    curve is very tall), while the other component still explains the remaining
    points. An optimiser can therefore chase this spike forever. To stop that,
    keep each standard deviation at or above a floor of `1e-3` times the sample
    standard deviation of the observations, so the fit is always finite. The
    likelihood function itself should still accept any positive standard
    deviation.

Run the tests with `uv run pytest tests/test_advanced_models.py -q`.

### Gaussian-mixture EM

Recall from the likelihood question in Scientific Python that the ML estimates of
a normal distribution can be found by differentiating the log-likelihood and
solving: they are simply the sample mean and the *population* standard deviation,
so no optimiser is needed. ML estimation is harder for a mixture when we do not
know which distribution each observation came from. The direct-optimization
exercise above maximised the log-likelihood, which sums over the possible
distributions for each observation, with a general optimiser, but this becomes
less and less practical as the number of parameters grows.

#### The EM algorithm for Gaussian mixtures

A much more efficient approach is
[Expectation-Maximization](https://en.wikipedia.org/wiki/Expectation%E2%80%93maximization_algorithm)
(EM), which treats this as a *missing data* problem. We pretend that the labels,
which tell us which distribution each observation came from, are missing. This is
useful because, with the labels, estimation becomes easy again: the ML estimates
for each distribution are just its mean and population standard deviation, with
no optimisation.

The EM approach when the labels are missing is:

1. Guess the parameter values.
2. Use the parameter values to infer likely labels (the E-step).
3. Use the labels to obtain ML estimates of the parameters of each distribution
   in the mixture, and of the relative contribution of each (the M-step).
4. Iterate steps 2 and 3 until convergence.

Under iteration, EM typically converges to a local optimum, which we hope is the
global optimum and therefore gives the ML estimates.

#### E-step

How do we infer the labels? We can simply assign each observation to the
component it is most likely to have come from. Assigning labels this way is
called "hard" EM, because the labels are categorical.

The parameters of the mixture are held in a `GaussianMixtureParameters` object
with fields `mean1`, `standard_deviation1`, `mean2`, `standard_deviation2` and
`weight1`, where `weight1` is the probability that an observation comes from
component one. Work in [mixture_models.py](src/pyproblems/mixture_models.py) and
write `hard_expectation_step(observations, parameters)`. It returns a Boolean
array, the same length as the observations, saying whether each observation is
more likely to have come from component one, which means comparing the weighted
densities $\pi\,\phi(x\mid\mu_1,\sigma_1)$ and
$(1-\pi)\,\phi(x\mid\mu_2,\sigma_2)$. Break a tie in favour of component one.

#### M-step

Using these (imperfect) labels we can update our estimated parameters by maximum
likelihood. Write `hard_maximization_step(observations, labels)`, which takes the
observations and the Boolean labels and returns new `GaussianMixtureParameters`:
the mean and population standard deviation of the observations in each group,
and `weight1` as the fraction labelled as component one. Raise `ValueError`,
rather than returning invalid parameters, if a group is empty or has zero
variance.

#### Iteration

Write `expectation_maximization(observations, initial_parameters,
expectation_step, maximization_step, log_likelihood, *, tolerance=1e-10,
max_iterations=1000)`, which iterates the supplied E-step, M-step and
log-likelihood functions until there is no further improvement in log-likelihood.
It returns an `ExpectationMaximizationResult` with the fitted `parameters`, the
`log_likelihood`, the number of `iterations` and whether it `converged`. You will
also need `mixture_log_likelihood(observations, parameters)`: the sum over the
observations of the log of the weighted sum of the two component densities.
Compute it in log space (for example with `scipy.special.logsumexp`) so that a
point far from both components still gives a finite value.

The tests check these details:

- One iteration is one E-step followed by one M-step. Stop when the absolute
  change in log-likelihood between consecutive iterations is below `tolerance`,
  or when `max_iterations` is reached.
- Judge convergence only after an update, so `max_iterations=0` returns the
  initial parameters and log-likelihood, unconverged.
- Use the absolute change: hard EM optimises a different objective, so its
  log-likelihood can fall from one iteration to the next, whereas soft EM never
  decreases it (apart from rounding). A large decrease is not convergence.
- The component labels can be swapped without changing the model, so return the
  component with the lower mean first.

Then write `fit_hard_gaussian_mixture(observations, initial_parameters)`, which
calls `expectation_maximization` using the hard steps. Check that it gives a
reasonable fit to some sample data, for example:

```python
rng = np.random.default_rng(42)
x = np.concatenate((rng.normal(-3, 2, 100), rng.normal(3, 1, 200)))
initial = GaussianMixtureParameters(0, 2, 1, 2, 0.3)
fitted = fit_hard_gaussian_mixture(x, initial)
```

Plot a histogram of `x` with the fitted mixture density over the top. The data
came from a normal with mean -3 and standard deviation 2 (weight 1/3) and one
with mean 3 and standard deviation 1 (weight 2/3), so the fit should be close.

#### Soft EM

An alternative is to use the relative *probability* that an observation belongs
to each component, which is termed a "soft" EM algorithm. It is a slight tweak to
the approach above: instead of assigning each observation to its most probable
component, we *weight* its contribution to our ML estimates by the probability
that it came from that component. The more certain we are that an observation
belongs to component one, the more it contributes to the estimates for
component one.

For a univariate two-component mixture, let $r_i$ be the probability that
observation $x_i$ belongs to component one. The soft E-step computes

$$
r_i = \frac{\pi\,\phi(x_i\mid\mu_1,\sigma_1)}
{\pi\,\phi(x_i\mid\mu_1,\sigma_1)+(1-\pi)\,\phi(x_i\mid\mu_2,\sigma_2)}.
$$

For soft weights, the component-one updates illustrate the calculation:
$\mu_1=\sum_i r_i x_i/\sum_i r_i$ and
$\sigma_1^2=\sum_i r_i(x_i-\mu_1)^2/\sum_i r_i$; component two uses weights
$1-r_i$, and $\pi$ is the average of the $r_i$ values. These are population
standard deviations, as required for maximum-likelihood estimation.

Write `soft_expectation_step(observations, parameters)`, which takes the same
arguments as the hard step but returns a float array of the probabilities $r_i$,
and `soft_maximization_step(observations, weights)`, which takes the observations
and the weights $r_i$ and returns new `GaussianMixtureParameters`. The weighted
mean is available as `numpy.average(..., weights=...)`, but you will need to
write the weighted standard deviation yourself. Raise `ValueError` if a component
ends up with no weight or zero variance. The E-step must stay finite for
observations far from both components, so work in log space. Finally, write
`fit_soft_gaussian_mixture(observations, initial_parameters)` in the same way as
the hard fit, and check it on the same sample data.

#### Multivariate Gaussian EM

Old Faithful is a geyser in Yellowstone National Park which erupts in a very
predictable manner, with either short eruptions that occur relatively quickly
after the previous eruption, or longer waits leading to bigger eruptions. This
motivates modelling the data as a mixture of two bivariate normal distributions,
where the variables are the eruption duration and the waiting time to the next
eruption (both in minutes). `load_faithful_data()` in
[data.py](src/pyproblems/data.py) provides them as (duration, waiting) pairs, and
the [Old Faithful notebook](analysis/old_faithful.ipynb) describes the data in
more detail.

The parameters are held in a `MultivariateGaussianMixtureParameters` object. It
has the same fields as before, except that each mean is a length-2 array
(duration and waiting time) and each standard deviation is replaced by a 2 by 2
covariance matrix (`covariance1` and `covariance2`). In
[mixture_models.py](src/pyproblems/mixture_models.py), write multivariate
counterparts of the soft-EM functions:
`multivariate_gaussian_mixture_log_likelihood`,
`multivariate_soft_expectation_step`, `multivariate_soft_maximization_step` and
`fit_multivariate_gaussian_mixture`, all taking the observations as an $n$ by 2
array. The log-likelihood needs a bivariate normal density
(`scipy.stats.multivariate_normal` has a `logpdf`). The M-step uses weighted
means and weighted population covariance matrices (`numpy.cov` accepts
`aweights`, and `ddof=0` gives the population version) and raises `ValueError` if
a covariance matrix is singular. The fit returns the component with the smaller
first mean coordinate first. Finally, `fit_faithful_gaussian_mixture(initial_parameters)`
fits the packaged Old Faithful data.

Compare your fitted log-likelihood with the reference value in the tests (about
-1130.27). The [Old Faithful notebook](analysis/old_faithful.ipynb) gives rough
starting values and asks you to plot the fit. EM is not guaranteed to find the
global maximum from every starting point.

This is the same dataset as the earlier regression exercise: the clusters should
help explain why a single straight line described it poorly. The notebook also
suggests an extension that revisits the prediction using the clusters.

```bash
uv run pytest tests/test_mixture_models.py -m advanced -q
```

Hard EM is a stepping stone to soft EM. If you would rather skip it, run
`uv run pytest tests/test_mixture_models.py -m advanced -k "not hard"`, which
leaves out its tests (and one test that is shared with the soft M-step).

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
  if there are no missing positions:
    return success (the grid is solved)
  pick the first missing position
  for each valid choice for that position:
    assign choice
    if solve(grid) succeeds:
      return success
    unmake choice (backtrack)
  return failure (no choice led to a solution)
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
  that any of ten offspring does so? Beware that `1 - (1 - p) ** n` rounds to
  zero when $p$ is tiny; `-np.expm1(n * np.log1p(-p))` keeps the small
  positive value.
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
