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

**Stage 3: predict without simulating 😱.** Implement
`expected_waiting_time(pattern)`, the exact expected number of flips for any
pattern. The tests check every pattern up to length four, and a pattern of 20
heads, which is far too slow to simulate. Check your formula against your
simulated table.

This stage is a real step up in mathematics: you are not expected to invent the
method from scratch, so the 💡 hints build up to it gradually. Open them one at a
time. The Penney's game extension does not depend on this stage.

```bash
uv run pytest tests/test_coin_patterns.py -k expected
```

<details>
<summary>💡 Hint 1: think about progress</summary>

While you wait for a pattern, the useful thing to know is how much of the
*beginning* of the pattern matches your most recent flips. That is your
progress. For `HH`, you have made some progress when your latest flip is an `H`.
For `HT`, the same flip makes the same progress.

Now imagine the next flip. What happens to your progress after a head, and after
a tail? Is the answer the same for `HH` and `HT`? Try a few longer patterns by
hand.

</details>

<details>
<summary>💡 Hint 2: expected time from each state</summary>

Treat each amount of progress as a *state*: no progress, one flip matched, two
flips matched, and so on up to the whole pattern. Give each state a variable for
the expected number of *additional* flips needed from there.

From any state you flip once, which costs one unit of time. The state you land in
then depends on whether the flip was a head or a tail. Write down the equations
for a short pattern such as `HH` or `HT` first, and see whether you can solve
them.

</details>

<details>
<summary>💡 Hint 3: a mathematical strategy</summary>

Call the expected number of additional flips from state $s$ by $E_s$. A fair
coin gives each outcome probability one half, so

$$
E_s = 1 + \frac{E_{\text{next H}} + E_{\text{next T}}}{2},
$$

where $E_{\text{next H}}$ and $E_{\text{next T}}$ are the values for the states
you reach after a head and after a tail. The completed state has $E = 0$.

To find the next state, take the flips that match your progress so far, add the
new flip, and find the *longest suffix* of that text which is also a *prefix* of
the target pattern. Its length is your new progress. A pattern of length $n$
gives $n$ unknowns and $n$ equations, which you can solve with a little algebra
for a short pattern, or with a small linear solver (such as Gaussian elimination
in plain Python) for a long one.

Alternatively, once your equations work, look at the answers for different
patterns: how do the places where the start of a pattern is repeated at its end
show up in the waiting time? That route needs no equations at all.

</details>

**Extension 🚀: Penney's game.** Now you play against your friend. You choose a
pattern of three flips first, then your friend chooses a different one, and
whichever pattern shows up first wins. Does choosing second help? Use
`flips_until` on the *same* list of flips for both patterns, built from
`list(islice(coin_flips(rng), 200))`, to see who wins. In the
[notebook](../../analysis/against_the_odds.ipynb), play all 56 ordered pairs of
patterns many times. Is there a best pattern to choose first? What does that say
about the idea that one pattern is simply "better" than another?
