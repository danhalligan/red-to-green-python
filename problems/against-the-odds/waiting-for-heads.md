# Waiting for heads 🪙

> **Before you start:** basic Python. The extension uses the
> [Against the Odds notebook](../../analysis/against_the_odds.ipynb), which needs
> the science packages (`uv sync --all-groups --extra science`).
>
> **Recommended first:** [Fibonacci](../pythonic-python/python-fundamentals.md#q4-fibonacci-sequence)
> (Python Fundamentals Q4), for endless generators, and
> [The office party](office-party.md) for seeded generators.
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
[coin_patterns.py](../../src/pyproblems/coin_patterns.py), implement `coin_flips(rng)`,
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
`average_waiting_time(pattern, *, trials, rng)`, the mean number of flips over
many trials. Compare `HH` and `HT` with your predictions. Then tabulate every
pattern of three flips, and of four (`itertools.product("HT", repeat=3)`). Which
patterns are quickest, and which are slowest? What do the quick ones have in
common?

```bash
uv run pytest tests/test_coin_patterns.py -k average
```

**Stage 3: predict without simulating.** Implement
`expected_waiting_time(pattern)`, the exact expected number of flips for any
pattern. The tests check every pattern up to length four, and a pattern of 20
heads, which is far too slow to simulate. 💡 There is a hint.[^coin-progress]
Check your formula against your simulated table.

```bash
uv run pytest tests/test_coin_patterns.py -k expected
```

[^coin-progress]: Think about *progress*. You are partway through `HH` when you
    have just seen an `H`. If the next flip is wrong, how much of that progress
    survives? Compare `HT` in the same position. You could model the progress as
    a chain of states and solve equations for the expected number of flips from
    each, or look for what the start and the end of a pattern have in common.

**Extension 🚀: Penney's game.** Now you play against your friend. You choose a
pattern of three flips first, then your friend chooses a different one, and
whichever pattern shows up first wins. Does choosing second help? Use
`flips_until` on the *same* list of flips for both patterns, built from
`list(islice(coin_flips(rng), 200))`, to see who wins. In the
[notebook](../../analysis/against_the_odds.ipynb), play all 56 ordered pairs of
patterns many times. Is there a best pattern to choose first? What does that say
about the idea that one pattern is simply "better" than another?
