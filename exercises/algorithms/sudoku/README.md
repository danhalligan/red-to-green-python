# Sudoku solver 🔢

> **Difficulty:** 🌶️🌶️🌶️
>
> **Before you start:** [Python Fundamentals](../../pythonic_python/python_fundamentals/README.md).
> Start with the checker warm-up below, then build on it to write a solver.
>
> **You’ll practise:** checking rows, columns and boxes, recursion, backtracking,
> and working on a copy instead of mutating the input.
>
> **Check:** `uv run pytest exercises/algorithms/sudoku/ -q`

## Warm-up: Sudoku checker

Sudoku asks you to fill a 9 by 9 grid so each row, column, and 3 by 3 box
contains the digits 1 through 9 exactly once. A partially filled grid is
*valid* when none of its supplied digits conflicts with those rules.

Implement `sudoku_checker(grid)` in [sudoku.py](sudoku.py).
The input is a list of nine rows containing integers 1 through 9 or `None` for
blanks.

Compare the result with the labelled puzzles from `load_sudoku_data()` and try
an empty grid, a valid completed grid, and a duplicate in each kind of
constraint group.

```bash
uv run pytest exercises/algorithms/sudoku/test_sudoku.py -q
```

## Sudoku solver

Now build on your checker to find a solution: given a puzzle with some cells
blank, fill in all of them, or report that no solution exists. Some puzzles
have more than one solution, and you only need to find one.

Build on `sudoku_checker` in [sudoku.py](sudoku.py) by
implementing `is_valid_placement(grid, row, column, value)` and
`sudoku_solver(grid)` in the same file. The docstrings
give the argument conventions and edge cases. Test a completed grid, an
unsolvable grid, and a puzzle with multiple valid solutions, as well as the
supplied puzzles.

```bash
uv run pytest exercises/algorithms/sudoku/test_sudoku_solver.py -q
```

Stuck? There are three 💡 hints, each giving a little more away.

<details>
<summary>💡 Hint 1: a nudge</summary>

How do you solve a Sudoku by hand when no cell is forced? You pick a digit, carry
on, and sometimes discover later that it was a mistake. What do you do then, and
what does your program need to remember in order to do the same?

</details>

<details>
<summary>💡 Hint 2: a strategy</summary>

One approach is a recursive backtracking algorithm. Try a valid digit in an
empty cell, then continue from the resulting partial grid. If that choice leads
to a dead end, undo it and try the next digit. Stop when you find one complete
solution; there is no need to enumerate every possible completion.

</details>

<details>
<summary>💡 Hint 3: an outline</summary>

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

</details>

**Extension 🚀: does the order of the search matter?** Your solver fills the
*first* blank cell. A search that does the same work in a different order can
be far faster or slower, and you can measure it. This extension has no
tests; your own counts are the check.

1. Count how many times your recursive function is called while solving each
   packaged puzzle from `load_sudoku_data()` whose `answer` is `True` (one has
   no solution and is quickly shown to be a dead end). Stop a run after a fixed
   limit (say 50,000 calls) and record that it did not finish.
2. Change the search to fill the blank cell with the *fewest* valid digits
   instead of the first blank. If some blank has no valid digit, you can give
   up on that branch immediately.
3. Compare the counts, puzzle by puzzle. Which puzzles benefit most, and why
   does choosing the most constrained cell help? 💡 A cell with exactly one
   valid digit is a forced move, so no guessing is needed there.

<details>
<summary>What did you discover?</summary>

The number of recursive calls, not the running time, is the fairest measure here,
because choosing the best cell costs extra work per call. Expect a few puzzles to
need tens of thousands of calls in the first-blank order but under a hundred with
the most-constrained rule.

</details>
