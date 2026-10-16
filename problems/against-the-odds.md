# Against the Odds 🎲

[← All problems](../README.md#index-of-problems)

Probability puzzles where your gut is confidently wrong. Each has a short story,
a few small functions to write, and an investigation that shows why. They share a
routine: **predict** the answer and write it down, **simulate** it, **calculate**
it exactly, then **explain** the gap between your prediction and the result.

Everything here uses only the Python standard library, so you need nothing
beyond [Python Fundamentals](python-fundamentals.md). Random choices always
come from a `random.Random` passed in as `rng`, so a seeded run can be repeated.
The investigations use plots, so they live in the
[Against the Odds notebook](../analysis/against_the_odds.ipynb), which needs the
science packages (`uv sync --all-groups --extra science`).

**In this topic:** [The office party](#the-office-party-) ·
[Waiting for heads](#waiting-for-heads-) · [The 100 prisoners](#the-100-prisoners-).
They are roughly in order of difficulty, but each can be done on its own.

## The office party 🎂

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
>
> **You’ll practise:** sets, passing a seeded random generator as an argument,
> arithmetic with huge integers, and searching with `next` and
> `itertools.count`.
>
> **Check:** `uv run pytest tests/test_birthday.py -q`, or the focused command at
> each stage.

You are at a party full of strangers when someone offers a bet: two people in
this room share a birthday. How many people must be in the room before that bet
is better than even odds? Write your guess down now, with a sentence about why.

This is the famous [birthday problem](https://en.wikipedia.org/wiki/Birthday_problem).
Resist looking up the answer: make Python tell you, then work out why. Assume
365 equally likely days (number them 0 to 364, and ignore leap years) and
independent birthdays.

**Stage 1: ask the crowd.** In [birthday.py](../src/pyproblems/birthday.py),
implement `has_shared_birthday` and `estimate_shared_birthday_probability`.
The estimate takes a `random.Random` called `rng` rather than using the global
`random` functions: a generator seeded with `random.Random(42)` gives the same
answer every time, and the tests check that you only used the one you were
given. 💡 There is a hint.[^birthday-set] Estimate the chance for several group
sizes and run it with different seeds. How much do the answers wobble? How many
trials do you need before the second decimal place stops changing?

```bash
uv run pytest tests/test_birthday.py -k "not exact and not smallest"
```

[^birthday-set]: A set holds each value once, so a group has a shared birthday
    exactly when turning it into a set makes it smaller. `rng.choices(range(365),
    k=people)` draws a whole group in one call.

**Stage 2: do the sum.** A simulation can only estimate. Implement
`shared_birthday_probability(people, days)` to calculate the chance exactly, and
compare it with your estimates. 💡 There is a hint.[^birthday-opposite] Then
implement `smallest_group_with_probability(threshold)`, which finds the first
group size whose chance reaches the threshold,[^birthday-next] and use it to
answer the question you started with. How close was your guess?

```bash
uv run pytest tests/test_birthday.py -k "exact or smallest"
```

[^birthday-opposite]: Counting every way that *somebody* shares is messy. Count
    the opposite instead: in how many ways can everyone have a *different*
    birthday? `math.perm` may help. Python integers never overflow, so you can
    let the intermediate numbers grow enormous and divide only at the end.

[^birthday-next]: `next(n for n in itertools.count() if ...)` returns the first
    value from an endless counter that passes a test, without building a list.

**Investigation 🚀: why so few?** A group of $n$ people contains
$\binom{n}{2}$ pairs of people (`math.comb(n, 2)`). Compare the number of pairs
at your answer with the number of days. What does that suggest? In the
[notebook](../analysis/against_the_odds.ipynb), change the number of days to 10,
100, 1,000, 10,000 and 100,000, find the group size for even odds each time, and
plot it against the number of days. What is the pattern, and does it fit the
pairs argument?

## Waiting for heads 🪙

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
>
> **Recommended first:** [Fibonacci](python-fundamentals.md#q4-fibonacci-sequence)
> (Python Fundamentals Q4), for endless generators, and
> [The office party](#the-office-party-) for seeded generators.
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
[coin_patterns.py](../src/pyproblems/coin_patterns.py), implement `coin_flips(rng)`,
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
[notebook](../analysis/against_the_odds.ipynb), play all 56 ordered pairs of
patterns many times. Is there a best pattern to choose first? What does that say
about the idea that one pattern is simply "better" than another?

## The 100 prisoners 🔐

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
>
> **Recommended first:** [The office party](#the-office-party-), for
> simulating with a seeded generator.
>
> **You’ll practise:** passing functions as arguments, a class that controls
> what code can see, shuffling, following chains of references, and finding
> loops with a `set`.
>
> **Check:** `uv run pytest tests/test_prisoners.py -q`, or the focused command
> at each stage.

A prison director offers 100 prisoners, numbered 0 to 99, a last chance at
freedom. A room holds a cupboard with 100 closed drawers. The director puts each
prisoner's number into a different drawer, completely at random. The prisoners
enter one at a time, may open up to 50 drawers, and leave everything as they
found it. If every prisoner finds their own number, they all go free. If even one
does not, nobody does. The prisoners can agree a plan beforehand, but may not
communicate once the first one enters the room.

Before you read on, estimate the chance that all 100 succeed if every prisoner
opens 50 drawers at random. Is there any plan that could make freedom a
realistic hope? This is the famous
[100 prisoners problem](https://en.wikipedia.org/wiki/100_prisoners_problem),
and that page gives the solution away, so have a think on your own first if
you've not encountered this before.

In [prisoners.py](../src/pyproblems/prisoners.py), each prisoner is given a
`Room`, which is already written. They can only look at drawers by calling
`room.open(i)`, which returns the number inside. The room counts the drawers
opened, refuses more than `room.limit` by raising `TooManyDrawersError`, and notes
in `room.found` whether the prisoner has seen their own number. A prisoner's
plan is a *strategy*: a function `strategy(room, rng)` that opens drawers. Because
functions can be passed as arguments, the same game can be played with any
strategy.

**Stage 1: no plan.** Implement `shuffled_drawers`, `random_strategy`,
`count_successes` and `estimate_survival`. 💡 There are hints.[^prisoners-random]
Estimate the survival chance with 2, 4, 6 and 10 prisoners, each allowed to open
half the drawers, and compare it with your prediction. Why can you not simply
simulate 100 prisoners and see? What is the chance, by pure calculation?

```bash
uv run pytest tests/test_prisoners.py -k "not clever and not cycle and not loop"
```

[^prisoners-random]: `rng.shuffle` shuffles a list in place, and
    `rng.sample(range(n), k)` picks `k` different values. Each prisoner needs a
    fresh `Room`, because the drawers are closed again between prisoners.

**Stage 2: use what you see.** The prisoners cannot talk, but they can react to
what they find. Implement `clever_strategy` so that the prisoners do much better
than random. 💡 There is a hint.[^prisoners-start] Then estimate the survival
chance with 10, 20, 50 and 100 prisoners, each allowed half the drawers, with both
strategies. How does it change as the number of prisoners grows? Is that what you
expected?

```bash
uv run pytest tests/test_prisoners.py -k clever
```

[^prisoners-start]: Prisoner 7 must open *some* drawer first. Why not drawer 7?
    Then think about what the number inside is, and where a number could send
    them next.

**Investigation 🚀: alone and together.** In the
[notebook](../analysis/against_the_odds.ipynb), compare the average number of
prisoners who find their number under each strategy. Then plot the distribution
of that number across thousands of games. What do you notice about the averages,
and what about the shapes? Which strategy makes the prisoners' fates depend on
one another, and what does that buy them?

**Extension 🚀: why does it work?** Draw an arrangement of eight drawers as
arrows from each drawer to the drawer whose number it holds. Follow the arrows
from any drawer: where do you end up? Implement `cycle_lengths(arrangement)` to
split an arrangement into its closed loops and return their lengths. Compare them
with `count_successes` in a few games. Write down the rule linking the loops to
the prisoners who succeed, and explain why a prisoner's own number is always
somewhere in their chain. Then use that rule to estimate the survival chance
without simulating any prisoners, which is much faster. What does the chance
approach as the number of prisoners grows to 1,000?

```bash
uv run pytest tests/test_prisoners.py -k "cycle or loop"
```

## Where next?

- **More simulation:** [Scientific Python](scientific-python.md) turns simulation
  into a tool for checking statistics, and
  [Dawkins' weasel](models-of-life.md#dawkins-weasel-) simulates evolution.
- **Counting and search:** [Algorithms and Search](algorithms-and-search.md),
  including [...Try, try again](algorithms/rugby.md), which counts possibilities
  too many to list.
- Return to the [routes](../README.md#choosing-a-route).
