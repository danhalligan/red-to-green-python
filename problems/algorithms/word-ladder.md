# Word ladder 🪜

[← All problems](../../README.md#index-of-problems)

> **Prerequisites:** [Python Fundamentals](../python-fundamentals.md).
>
> **You’ll practise:** sets and strings, searching a network of words, and
> reconstructing a path.
>
> **Check:** `uv run pytest tests/test_word_ladder.py -q`

A word ladder changes one letter at a time, and every word along the route must
appear in the packaged word list (common English words, derived from
[SCOWL](http://wordlist.aspell.net/)). Your job is to implement a
function to construct the shortest word ladder from a starting word to get to a
final word (or one such route if there are multiple).

Use `load_words()` from [data.py](../../src/pyproblems/data.py) to load the
lowercase word set. Implement `word_ladder(start, target, words)` in
[word_ladder.py](../../src/pyproblems/word_ladder.py) to return a shortest route, or
`None` if no route exists. The docstring gives the input requirements. The
number of moves is one less than the number of words in the returned route.
Stuck on the approach? There is a 💡 hint.[^ladder-hint]

[^ladder-hint]: Think of the words as a network in which two words are linked if
    they differ by one letter. Breadth-first search explores outward one move at
    a time, so the first time it reaches the target it has found a shortest
    route. Record each word's predecessor as you go, so you can reconstruct that
    route once the target is found.

For example, starting from `play`, we can find the following ladders:

- `plan` takes one move only (we just change "y" to "n").
- `snap` takes three moves (`play -> slay -> slap -> snap`)
- `pool` takes four (`play -> ploy -> plop -> poop -> pool`)
- `golf` takes six (`play -> clay -> clad -> glad -> goad -> gold -> golf`)
- `ball` takes seven (`play -> slay -> slam -> seam -> seal -> sell -> bell -> ball`)

How many moves does it take to get from `play` to `game`? Give one valid
shortest route.

**Extension 🚀:** Some pairs of four-letter words are much harder to connect than
others. Implement `longest_shortest_ladder(words, length=4)`, which finds the two
words of that length whose *shortest* ladder needs the most moves and returns one
such route. Which two words are they, and how many moves apart are they?
💡 Hint: you already have code that finds shortest routes from a start word; how
many times would you need to run it?[^longest-ladder] The extension's tests are the ones that match
`-k longest`; use `-k "not longest"` to skip them.

[^longest-ladder]: Be careful to answer this question and not a harder one. Asking
    for the longest ladder that never repeats a word, rather than the longest
    *shortest* ladder, is the longest simple path problem, which has no known
    efficient solution, so a brute-force search for it is hopeless on a
    dictionary this size.

## Where next?

- **Other searches:** the [Sudoku solver](sudoku-solver.md) uses backtracking
  rather than breadth-first search.
- **Counting and caching:** [...Try, try again](rugby.md) introduces dynamic
  programming.
- **Real data:** after the Python core route, the
  [Scientific Python route](../../README.md#choosing-a-route) starts with
  [Mysterious data](../data-analysis.md#q1-mysterious-data-).
- Back to [Algorithms and Search](../algorithms-and-search.md).
