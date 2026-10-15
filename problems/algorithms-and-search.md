# Algorithms and Search

[← All problems](../README.md)

## Word ladder 🪜

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
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

Use `load_words()` from [data.py](../src/pyproblems/data.py) to load the
lowercase word set. Implement `word_ladder(start, target, words)` in
[word_ladder.py](../src/pyproblems/word_ladder.py) to return a shortest route, or
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

## ...Try, try again 🏉

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
>
> **You’ll practise:** breaking a problem into smaller ones, spotting repeated
> work, caching, and building an answer up from the bottom.
>
> **Check:** `uv run pytest tests/test_rugby.py -q`

A rugby match has finished, but the scoring record has been lost. All we have is
the final score. The commentator insists there must be dozens of ways the points
could have been scored. The referee isn't so sure. Your job is to reconstruct
what might have happened.

| Scotland | England |
| ---: | ---: |
| 8 | 0 |

Scotland scored eight points 🎉. How many different sequences of scoring
events could have produced that result? In rugby union a team can score in four
different ways:

| Event | Points |
| --- | --- |
| Penalty kick | 3 |
| Drop goal | 3 |
| Try | 5 |
| Conversion | 2 |

A conversion can only ever be taken straight after a try, and we will ignore
penalty tries (which are awarded as 7 points). Although they share the same
points, penalties and drop goals are separate events. The order matters, so a
try followed by a penalty is different from a penalty followed by a try.

For eight points there are four sequences: a penalty then a try, a drop goal
then a try, a try then a penalty, or a try then a drop goal. A few more:

- 0 points: one sequence, the empty one, since nothing has happened yet.
- 3 points: two sequences, a penalty or a drop goal.
- 5 points: one sequence, a try.
- 6 points: four sequences, any two of the three-point events in either order.
- 7 points: one sequence, a try then its conversion.
- 1, 2 and 4 points: no sequences at all.

### Stage 1: Reconstruct the match

Implement `count_scoring_sequences(points)` in
[rugby.py](../src/pyproblems/rugby.py); it should raise a `ValueError` for a
negative score. Work out 10 points by hand before you write any code, then check
it against your function. How you do it is up to you: any approach that gets the
right counts will do. Stuck? There are 💡 hints.[^try-hint][^try-hint2]

```bash
uv run pytest tests/test_rugby.py -k "scoring_sequences and not carried_away and not season"
```

[^try-hint]: Does the answer for a score of 5 help you with 7? What about 8?
    Think about what the *last* scoring event could have been, and what the
    score was before it. Could you perhaps call the score calculating function
    to get the result for a smaller score to help calculate the current score?

[^try-hint2]: Conversions are special types of event and might need special
    consideration because a conversion can only ever follow a try. Can you
    reframe the question slightly to make it easy to implement conversions?

### Stage 2: The commentator gets carried away

The commentator is sure Scotland won, but is so delirious they're not sure of
the score any more. Did they score 30 points? Or was it 50? Maybe it was 100! Try
these in your function. If it works for small scores but struggles with larger
ones, think about why. Is it repeating calculations that it has already
performed? Try drawing out which smaller scores your function needs for 12
points, or count how many times it is called for 20, 30 and 40 points. How does
the cost grow? The `carried_away` test gives up after five seconds and says so,
rather than hanging. 💡 There is a hint towards a fix.[^try-cache]

```bash
uv run pytest tests/test_rugby.py -k carried_away
```

[^try-cache]: *Caching* (also called memoisation) remembers each answer the
    first time it is computed, so that it is never computed twice. Python
    has a "decorator" that can help if you need it: `functools.cache`.

How fast do you think these sequences of scores grow? **What's the smallest
final score that can be reached in more than one million different sequences?**
Implement `smallest_score_with_more_sequences_than(count)`, which returns the
smallest score reachable in more than `count` sequences, and use it to answer
the question. Write down your answer: the tests check your function with other
thresholds, including a trillion, which is hopeless unless you stop repeating
work.

```bash
uv run pytest tests/test_rugby.py -k smallest
```

### Stage 3: The entire season

A whole season of rugby adds up to many points. Your function should now cope
with a score of 20,000. If you used a cached recursion, you may run into
Python's limit on how deeply functions can call themselves. Can you calculate
the answers in an order that avoids deep recursion altogether? 💡 There is a
hint.[^try-table] The answer has nearly 3,000 digits, but thankfully Python
integers do not overflow!

```bash
uv run pytest tests/test_rugby.py -k season
```

[^try-table]: Caching works from the answer down to the base cases. The
    alternative is to start from the base case and work up, filling in a table
    (a list) so that every entry only needs entries that already exist.
    Fibonacci that way:

    ```text
    table = [0, 1]
    for n from 2 up to the target:
        add table[n - 1] + table[n - 2] to the end of the table
    return the last entry of the table
    ```

    For rugby, what goes in the first entry, and what does each later entry
    need? Notice too that a cached function that is only ever called for
    1, 2, 3, ... in turn never recurses deeply: it is secretly working from the
    bottom up.

If you wrote more than one version, compare them at 100 and 20,000 points. Which
would you rather use, and why? Keep whichever you prefer as
`count_scoring_sequences`.

**Extension 🚀: does the order matter?** A reporter might not care in what
order the points arrived, only how many penalties, drop goals, tries and
conversions there were. Implement `count_scoring_combinations(points)`, which
counts these tallies. Penalties and drop goals are still counted separately,
and a tally cannot have more conversions than tries. Six points gives
four sequences but only three tallies. Find the two tallies for eight points,
and explain why there are four sequences for the same score. Compare the
number of sequences with the number of tallies for 6, 8, 9, 10 and 12 points:
why can you not get one from the other by dividing by a fixed number? 💡 The
code is very close to your bottom-up version.[^try-combinations] The extension's
tests are the ones that match `-k combinations`; use `-k "not combinations"` to
skip them.

[^try-combinations]: A bottom-up table can count either. With the outer loop over
    scores and the inner loop over events, every ordering is counted. With the
    outer loop over events and the inner loop over scores, each event type is
    added in a fixed order, so every combination is counted once.

**Investigation 🚀: how fast do the counts grow?** The ratio of consecutive
Fibonacci numbers tends to the golden ratio, about 1.618. Check this with your
`fibonacci()`. Then look at your scoring counts from about 50 points on: what
does `count(n) / count(n - 1)` tend to, and what is `count(n) / count(n - 10)`?
(Compare it with the growth you saw in Stage 2.) Now try the number of tallies
from the extension. What does all this tell you about how fast each count grows,
and about why order makes the problem so much harder? 💡 The golden ratio
solves $x^2 = x + 1$.[^try-growth]

[^try-growth]: Fibonacci satisfies $f_n = f_{n-1} + f_{n-2}$. Trying
    $f_n = x^n$ gives $x^n = x^{n-1} + x^{n-2}$, which simplifies to
    $x^2 = x + 1$. Do the same with the recurrence for your scoring counts.

## Global sequence alignment 🧬

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
>
> **You’ll practise:** generators and recursion, brute-force search, dynamic
> programming, two-dimensional tables, and tracing back through a table to
> recover a solution.
>
> **Check:** `uv run pytest tests/test_alignment.py -q`. For the brute-force
> part only, add `-k "score_alignment or all_alignments or brute_force_finds"`.

### Naive brute force

We're going to explore how to find an optimal "global" alignment (one that
aligns both sequences from beginning to end) of two DNA
sequences. Throughout this exercise, a matching pair scores +1, a mismatch
scores -1, and a character aligned with a gap scores -1. Our optimal alignment
is then defined as the arrangement of the two sequences with the highest score.
Our job is to find this.

For example:

```
ATAGTC-AC-AT
AAA-TCGACAAA
```

The score is the sum across columns: equal characters contribute +1 and every
other column contributes -1.

The simplest way to find the best alignment is to try them all. In
[alignment.py](../src/pyproblems/alignment.py), implement
`score_alignment(aligned_first, aligned_second)`, which scores a pair of
already-aligned strings, and `all_alignments(first, second)`, which yields every
possible alignment of two sequences.[^enumerate-hint] The best score is then the
maximum over all alignments.

[^enumerate-hint]: Think about the first character of each sequence. Either the
    first character of `first` is aligned with a gap, or the first character of
    `second` is aligned with a gap, or the two are aligned with each other.
    Whichever you choose, what remains is a smaller alignment problem, so a
    recursive generator is a natural fit. A column that is a gap in both rows is
    never allowed.

How far does this get you? Unfortunately, the number of possible alignments
grows **very** quickly: for two sequences of length $n = 3$ there are 63;
for $n = 7$ this grows to 48,639 and there are over eight million at $n=10$!

Time your function as the sequences get longer, then think about the 10 and 11
base example above. How long do you think it would take for two 1,000 base
sequences?

### Dynamic programming & Needleman-Wunsch 😱

Brute force repeats a great deal of work, because many alignments share the same
beginnings. *Dynamic programming* removes the repetition. It is a technique for
solving a big problem by solving smaller, overlapping subproblems once each and
storing the answers in a table so they can be reused rather than recomputed.
Here the subproblems are the best alignments of the beginnings (prefixes) of the
two sequences, and the table is filled in from short prefixes up to the full
sequences.

> [!NOTE]
> Despite the name, dynamic programming is not about changing data or code that
> adapts as it runs, and "programming" here means planning (as in "linear
> programming"), not writing code.

The Needleman-Wunsch algorithm is a dynamic-programming method for *global*
alignment: it aligns both sequences from beginning to end, inserting gaps
where useful. This models the idea that the sequences share an overall extent,
even if insertions or deletions have shifted later characters. It is used in
bioinformatics to compare DNA, RNA, or protein sequences.

Use a dynamic-programming table whose entry
$D_{i,j}$ is the best score for aligning the first $i$ characters of the first
sequence with the first $j$ characters of the second.
Initialise the first row and column with the cost of aligning that many
characters to gaps. Each later cell chooses the best of a match/mismatch
diagonal, a gap in the first sequence, or a gap in the second:

$$
D_{i,j}=\max\begin{cases}
D_{i-1,j-1}+s(a_i,b_j),\\
D_{i-1,j}-1,\\
D_{i,j-1}-1,
\end{cases}
\qquad
s(a_i,b_j)=\begin{cases}
+1 & a_i=b_j,\\ 
-1 & a_i\ne b_j.
\end{cases}
$$

Implement `needleman_wunsch_score(first, second)`, which needs only the best
score in the final cell, and `needleman_wunsch_alignment(first, second)`, which
traces back through the table to recover one optimal pair of strings. The
starter code shares a helper, `_alignment_table`, between these functions. It
allocates the table, initialises its boundaries, and supplies the traversal
loops. Your first task is to replace its scoring TODO. Think of each candidate
as "the best score for a smaller problem, plus the score for one new column".

Here is the structure in pseudocode; the scoring decisions are yours to fill in:

```text
create D with (length(first) + 1) rows and (length(second) + 1) columns
set D[0, 0] to zero
initialise the first column and first row with cumulative gap costs
for each row i from 1 to length(first):
  for each column j from 1 to length(second):
    consider ending with both characters, or with a gap in either sequence
    TODO: calculate the three candidate scores using already-filled cells
    TODO: store the best candidate in D[i, j]
return D
```

The extra row and column matter: `D[0, j]` aligns an empty first sequence with
`j` characters of the second. Table indices count characters, while Python
string indices start at zero, so the characters at cell `(i, j)` are
`first[i - 1]` and `second[j - 1]`. A diagonal move adds both characters, an
upward move adds a character from `first` against a gap, and a leftward move
adds a gap against a character from `second`. Row-by-row traversal ensures all
three neighbours have already been filled. Try drawing the table for `"A"`
and `"AA"` before tackling longer inputs.

Once the score tests pass, complete the traceback TODO:

```text
start at the bottom-right cell with two empty character lists
while either sequence still has characters left:
  if on the top row or left column, only a gap move is possible
  otherwise:
    TODO: choose a move whose neighbour score plus column score
        equals the current cell's score
    append that move's character/gap pair to the lists
    move to that neighbour
reverse both lists and join each into a string
```

Do not simply choose the neighbour with the largest stored score: the score
of the new alignment column matters too. If several moves explain the current
score, choose any one. Stop at the top-left cell, not as soon as one sequence
runs out; the remaining characters must be aligned with gaps. The skeleton
handles these boundary moves and reverses the output for you.

The docstrings give the details. Check both functions against your brute-force
version on short sequences. The longer DNA fixture checks that the same
algorithm scales beyond the small worked example.

## Sudoku solver 🔢

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md), in particular the Sudoku checker
> (Q7).
>
> **You’ll practise:** recursion, backtracking, and working on a copy instead
> of mutating the input.
>
> **Check:** `uv run pytest tests/test_sudoku_solver.py -q`

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

Build on `sudoku_checker` in [sudoku.py](../src/pyproblems/sudoku.py) by
implementing `is_valid_placement(grid, row, column, value)` and
`sudoku_solver(grid)` in the same file. The docstrings
give the argument conventions and edge cases. Test a completed grid, an
unsolvable grid, and a puzzle with multiple valid solutions, as well as the
supplied puzzles.

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
   valid digit is a forced move, so no guessing is needed there.[^sudoku-order]

[^sudoku-order]: The number of recursive calls, not the running time, is the
    fairest measure here, because choosing the best cell costs extra work per
    call. Expect a few puzzles to need tens of thousands of calls in the
    first-blank order but under a hundred with the most-constrained rule.
