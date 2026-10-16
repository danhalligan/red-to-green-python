# Sudoku solver 🔢

[← All problems](../../README.md#index-of-problems)

> **Prerequisites:** [Python Fundamentals](../python-fundamentals.md), in
> particular the [Sudoku checker](../python-fundamentals.md#q7-sudoku-checker)
> (Q7), because your solver builds on `sudoku_checker` in the same file.
>
> **You’ll practise:** recursion, backtracking, and working on a copy instead
> of mutating the input.
>
> **Check:** `uv run pytest tests/test_sudoku_solver.py -q`

We are now going to build on our earlier Sudoku problem. We previously wrote a
function to check a Sudoku grid was valid
(the [Sudoku checker](../python-fundamentals.md#q7-sudoku-checker)), and now we
will write a new function to find a solution: given a puzzle with some cells
blank, fill in all of them, or report that no solution exists. Some puzzles have
more than one solution, and you only need to find one.

Build on `sudoku_checker` in [sudoku.py](../../src/pyproblems/sudoku.py) by
implementing `is_valid_placement(grid, row, column, value)` and
`sudoku_solver(grid)` in the same file. The docstrings
give the argument conventions and edge cases. Test a completed grid, an
unsolvable grid, and a puzzle with multiple valid solutions, as well as the
supplied puzzles.

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

## Where next?

- **Another search:** [Word ladder](word-ladder.md) uses breadth-first search.
- **Dynamic programming:** [...Try, try again](rugby.md) and then
  [Global sequence alignment](global-sequence-alignment.md).
- Back to [Algorithms and Search](../algorithms-and-search.md).
