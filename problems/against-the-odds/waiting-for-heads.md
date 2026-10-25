# Waiting for heads 🪙

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python. The investigation uses the
> [Against the Odds notebook](../../analysis/against_the_odds.ipynb), which needs
> the science packages (`uv sync --all-groups --extra science`).
>
> **Recommended first:** [Fibonacci](../../exercises/pythonic_python/python_fundamentals/README.md#q6-fibonacci-sequence)
> (Python Fundamentals Q4), for endless generators, and
> [The office party](office-party.md) for random numbers and seeding.
>
> **You’ll practise:** endless generators, reading an iterator lazily, a
> sliding window with `collections.deque`, slicing strings, and checking a
> simulation against exact reasoning.
>
> **Check:** `uv run pytest tests/test_coin_patterns.py -q`, or the focused
> command at each stage.

You and a friend each flip your own fair coin. You flip until you see `HH` (two
heads in a row); your friend flips until they see `HT` (a head, then a tail). At
any two flips in a row, the two patterns are equally likely. So on average, how
many flips does each of you wait? Predict both numbers before you start. Would
you bet that they are the same?

**Stage 1: a stream of flips.** In
[coin_patterns.py](../../src/pyproblems/coin_patterns.py), implement `coin_flips()`,
an endless generator of `"H"` and `"T"`, and `flips_until(pattern, flips)`, the
number of flips needed for the pattern to first appear. It must read flips lazily
and stop the instant the pattern appears, because the stream never ends and you
cannot call `list` on it. The tests pass a generator that raises an error if you
read a flip you did not need. 💡 There is a hint.[^coin-window]

```bash
uv run pytest tests/test_coin_patterns.py -k "coin_flips or flips_until"
```

[^coin-window]: Only the latest `len(pattern)` flips matter.
    `collections.deque(maxlen=len(pattern))` forgets older flips by itself, or
    you could slice the end off a string you keep growing. `enumerate(flips,
    start=1)` counts the flips for you.

**Stage 2: run the experiment.** Implement
`average_waiting_time(pattern, *, trials)`, the mean number of flips over
many trials, using `coin_flips` and `flips_until`. You will compare it with your
predictions in the notebook below.

```bash
uv run pytest tests/test_coin_patterns.py -k average
```

**Stage 3: predict without simulating.** Implement
`expected_waiting_time(pattern)`, the exact expected number of flips for any
pattern. The tests check every pattern up to length four, and a pattern of 20
heads, which is far too slow to simulate.

You are not expected to derive the maths. The expected waiting time for a
pattern of $n$ flips is

$$
E = \sum_{k=1}^{n} 2^k \, c_k,
$$

where $c_k = 1$ if the first $k$ flips of the pattern are the same as its last
$k$ flips, and $c_k = 0$ otherwise. This is the *autocorrelation* of the
pattern: see
[Autocorrelation (words)](https://en.wikipedia.org/wiki/Autocorrelation_%28words%29#First_occurrence_of_a_word_in_a_random_string)
on Wikipedia, which gives the same result for a fair coin as
$|A|^n c(1/|A|)$ with an alphabet of $|A| = 2$ letters. The whole pattern
always matches itself, so $k = n$ always counts. For example, `HT` only matches
at $k = 2$, giving $2^2 = 4$ flips, while `HH` matches at $k = 1$ and $k = 2$,
giving $2 + 4 = 6$.

Turning this into code is your task. 💡 There is a hint.[^coin-slices]

```bash
uv run pytest tests/test_coin_patterns.py -k expected
```

[^coin-slices]: `pattern[:k]` is the first `k` flips and `pattern[-k:]` is the
    last `k`, so `pattern[:k] == pattern[-k:]` tests whether they match.

## Investigation: over to the notebook 📓

The functions are done, so now use them. From here the work happens in the
[Against the Odds notebook](../../analysis/against_the_odds.ipynb#Waiting-for-heads): open it, run the setup cell, and find the **Waiting
for heads** section. The plotting code is provided; your job is to fill in the
tables of results and explain what they show. There are no tests for this part,
so write down your prediction before you run each cell.

1. **`HH` against `HT`.** Compare the simulated averages with your predictions
   and with `expected_waiting_time`.
2. **Patterns of three flips.** Build a table of simulated and exact waiting times
   for every pattern of three flips, and plot them. Which patterns are quickest,
   and which are slowest? What do the quick ones have in common, and how does the
   formula above explain it?
3. **Extension 🚀: Penney's game.** Now you play against your friend. You choose
   a pattern of three flips first, then your friend chooses a different one, and
   whichever pattern shows up first wins. Does choosing second help? Use
   `flips_until` on the *same* list of flips for both patterns, built from
   `list(islice(coin_flips(), 200))`, to see who wins. Play all 56 ordered
   pairs of patterns many times and build a table of how often the pattern
   chosen first wins. Is there a best pattern to choose first? What does that
   say about the idea that one pattern is simply "better" than another? This
   extension does not depend on Stage 3.

<details>
<summary>What did you discover?</summary>

On average `HH` needs 6 flips but `HT` needs only 4, even though both are
equally likely at any pair of flips. The difference is what a miss costs. Having
just seen an `H`, a failed attempt at `HT` (another `H`) still leaves you one
step in, because the latest `H` could start a new `HT`. A failed `HH` (a `T`)
throws all your progress away.

This is what the formula measures: the expected wait is the sum of $2^k$ over
every $k$ for which the first $k$ flips of the pattern equal its last $k$ flips.
The whole pattern always counts, so $\text{HT}$ gives $2^2 = 4$, while
$\text{HH}$ gives $2^1 + 2^2 = 6$. Of the patterns of three flips, those that
cannot overlap themselves (`HHT`, `HTT`, `THH` and `TTH`) are quickest, at 8
flips. `HTH` and `THT` take 10, and `HHH` and `TTT`, which overlap most, are
slowest, at 14. The simulated table matches this rule in every row.

In Penney's game, choosing second helps. Whichever pattern is chosen first,
there is a reply that appears first between about 66% and 88% of the time, so
**no pattern is a good first choice**. No pattern beats every other, because
"appears first" is not transitive: each pattern can be beaten by another, a bit
like rock, paper, scissors.

The best reply is easy to remember. Take the opposite of the middle flip of the
first pattern, then add its first two flips. For `HHT` that is `T` followed by
`HH`, giving `THH`, which matches your table.

</details>
