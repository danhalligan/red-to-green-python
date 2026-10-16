# Algorithms and Search

[← All problems](../README.md#index-of-problems)

Four self-contained exercises, each with its own page, starter code and tests.
You can start with any of them, but some build on earlier ideas, as shown below.

| Exercise | What you will do | Prerequisites | Check |
| --- | --- | --- | --- |
| [Word ladder 🪜](algorithms/word-ladder.md) | Find the shortest route between two words, changing one letter at a time | [Python Fundamentals](python-fundamentals.md) | `uv run pytest tests/test_word_ladder.py -q` |
| [...Try, try again 🏉](algorithms/rugby.md) | Count the ways a rugby score could have been reached, and discover why caching and tabulation matter | [Python Fundamentals](python-fundamentals.md). Recommended first: [Fibonacci](python-fundamentals.md#q4-fibonacci-sequence) | `uv run pytest tests/test_rugby.py -q` |
| [Global sequence alignment 🧬](algorithms/global-sequence-alignment.md) | Align two DNA sequences, first by brute force and then with Needleman-Wunsch | [Python Fundamentals](python-fundamentals.md). Recommended first: [...Try, try again](algorithms/rugby.md) | `uv run pytest tests/test_alignment.py -q` |
| [Sudoku solver 🔢](algorithms/sudoku-solver.md) | Solve a Sudoku by backtracking search | [Sudoku checker](python-fundamentals.md#q7-sudoku-checker) (Python Fundamentals Q7) | `uv run pytest tests/test_sudoku_solver.py -q` |

## How these connect

- **Dynamic programming:** [Fibonacci](python-fundamentals.md#q4-fibonacci-sequence)
  introduces a recurrence relationship, [...Try, try again](algorithms/rugby.md)
  applies it to counting in one dimension, and
  [Global sequence alignment](algorithms/global-sequence-alignment.md#dynamic-programming--needleman-wunsch-)
  extends it to two dimensions and to finding an optimal answer.
- **Search:** the [Sudoku checker](python-fundamentals.md#q7-sudoku-checker) is
  reused inside the [Sudoku solver](algorithms/sudoku-solver.md), and
  [Word ladder](algorithms/word-ladder.md) searches a network of words.

## Where next?

- Put the algorithms to work on data in
  [Scientific Python](scientific-python.md), or simulate with
  [Models of Life](models-of-life.md).
- Return to the [routes](../README.md#choosing-a-route) to pick another topic.
