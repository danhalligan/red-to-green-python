# The office party 🎂

> **Before you start:** basic Python. The investigation uses the
> [Against the Odds notebook](../../analysis/against_the_odds.ipynb), which needs
> the science packages (`uv sync --all-groups --extra science`).
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

**Stage 1: ask the crowd.** In [birthday.py](../../src/pyproblems/birthday.py),
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
[notebook](../../analysis/against_the_odds.ipynb), change the number of days to 10,
100, 1,000, 10,000 and 100,000, find the group size for even odds each time, and
plot it against the number of days. What is the pattern, and does it fit the
pairs argument?
