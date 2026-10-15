# Python Fundamentals

[← All problems](../README.md)

> **Prerequisites:** none.
>
> **You’ll practise:** functions, sequences, comprehensions, iteration,
> dictionaries, generators, exceptions, and readable tests.
>
> **Check:** `uv run pytest tests/test_language.py tests/test_sudoku.py -q`, or
> each question's own command below.

## Q1. Exponentiation

Write a function to take numbers $x$ and return $e^x$ as `exponentiate(values)`
in `src/pyproblems/language.py`. Note that the input can be any iterable, not
just a list.

Begin with a `for` loop and `list.append`. Once it works, try rewriting the
function as a list comprehension. Compare the two versions for readability.

Check this exercise with:

```bash
uv run pytest tests/test_language.py -k exponentiate
```

## Q2. Adjacent products

Given a sequence of integers, write a function to find the pair of adjacent
elements that has the largest product and return that product. Return `None`
when fewer than two values are supplied. The input may be any iterable.

For example, for the list `[3, 6, -2, -5, 7, 3]` you should return `21`, since
7 and 3 produce the largest product.

Implement `adjacent_elements_product(values)` in `language.py`.

💡 **Hint:** `itertools.pairwise` could be useful here.

```bash
uv run pytest tests/test_language.py -k adjacent
```

## Q3. FizzBuzz

FizzBuzz is a classic programming exercise. The goal is to count through the
integers, replacing multiples of three with `Fizz`, multiples of five with
`Buzz`, and multiples of both with `FizzBuzz`.

Implement `fizzbuzz(n)` to return strings from 1 through `n`, inclusive. For
example, `fizzbuzz(5)` should return `['1', '2', 'Fizz', '4', 'Buzz']`.

```bash
uv run pytest tests/test_language.py -k fizzbuzz
```

## Q4. Fibonacci sequence

The Fibonacci sequence starts as 0, 1, 1, 2, 3, 5. After the starting values
0 and 1, each new value is the sum of the two before it.

Implement `fibonacci()` as a generator that yields the Fibonacci sequence
indefinitely. Each call to `fibonacci()` should return an independent iterator.
Try `next()` to request individual values and `itertools.islice` to take a
finite prefix without materialising the infinite sequence.

```python
from itertools import islice

list(islice(fibonacci(), 8))
```

```bash
uv run pytest tests/test_language.py -k fibonacci
```

## Q5. First non-repeating character

Given a string, find and return the first instance of a non-repeating character
in it. If there is no such character, return `_`.

For example, in `abacabad`, both `c` and `d` occur once, but `c` comes first;
in `abacabaabacaba`, every character repeats. The search is case-sensitive;
spaces and punctuation count too.

Implement `first_non_repeating_character(text)`.

```bash
uv run pytest tests/test_language.py -k non_repeating
```

## Q6. Python gotchas

These short examples expose behaviour that can be surprising when translating
habits from other languages or when reading unfamiliar Python. Before running
each snippet, write down its output and explain the mechanism. Then write a
correct version as a function in `language.py`, where the tests check that the
intended behaviour holds.

```bash
uv run pytest tests/test_language.py -k gotcha
```

### a. A mutable default argument

```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags


print(add_tag("first"))
print(add_tag("second"))
```

Implement `add_tag(tag, tags=None)`, which appends `tag` to `tags` and returns
the list. When no list is given it should start a new one, so separate calls
never share state.

### b. Equality and identity

```python
first = ["tea"]
second = ["tea"]
print(first == second)
print(first is second)
```

Implement `copy_grid(grid)`, which returns a grid that is *equal* to a list of
lists but is not the same object, and shares none of its inner lists with the
original, so changing the copy never changes the original.

### c. Aliasing through list multiplication

```python
rows = [[]] * 3
rows[0].append("changed")
print(rows)
```

Implement `make_grid(rows, columns, fill=0)`, which returns a list of `rows`
independent lists, each holding `columns` copies of `fill`.

### d. Mutating a list while iterating

The goal is to keep only the odd values.

```python
values = [1, 2, 4, 6, 7]
for value in values:
    if value % 2 == 0:
        values.remove(value)
print(values)
```

Implement `keep_odd(values)`, which returns a *new* list of the odd values and
leaves its input unchanged.

### e. Floating-point representation

```python
print(0.1 + 0.2 == 0.3)
```

Implement `approximately_equal(first, second)`, which treats numbers that differ
only by floating-point rounding as equal. 💡 `math.isclose` is worth a look.

### f. An exhausted iterator

```python
numbers = iter([1, 2, 3])
print(list(numbers))
print(list(numbers))
```

Implement `average(values)`, which returns the mean of any iterable of numbers,
including a one-shot iterator or generator that can only be read once.

## Q7. Sudoku checker

Sudoku asks you to fill a 9 by 9 grid so each row, column, and 3 by 3 box
contains the digits 1 through 9 exactly once. A partially filled grid is
*valid* when none of its supplied digits conflicts with those rules.

Implement `sudoku_checker(grid)` in [sudoku.py](../src/pyproblems/sudoku.py).
The input is a list of nine rows containing integers 1 through 9 or `None` for
blanks.

Compare the result with the labelled puzzles from `load_sudoku_data()` and try
an empty grid, a valid completed grid, and a duplicate in each kind of
constraint group.

```bash
uv run pytest tests/test_sudoku.py -q
```
