# Office party 🎂

> **Difficulty:** 🌶️
>
> **Before you start:** basic Python. The investigation uses the
> [Against the Odds notebook](investigate.ipynb), which needs
> the science packages (`uv sync --all-groups --extra science`).
>
> **You’ll practise:** sets, seeding the `random` module for repeatable
> simulations, arithmetic with huge integers, and searching with `next` and
> `itertools.count`.
>
> **Check:** `uv run pytest exercises/office_party/ -q`, or the focused command at
> each stage.

You are at a party full of strangers when someone offers a bet: two people in
this room share a birthday. How many people must be in the room before that bet
is better than even odds? Write your guess down now, with a sentence about why.

This is the famous [birthday problem](https://en.wikipedia.org/wiki/Birthday_problem).
Resist looking up the answer: make Python tell you, then work out why. Assume
365 equally likely days (number them 0 to 364, and ignore leap years) and
independent birthdays.

**Stage 1: ask the crowd.** In [birthday.py](birthday.py),
implement `has_shared_birthday` and `estimate_shared_birthday_probability`.
The estimate uses the functions in the `random` module. Calling `random.seed(42)`
before it gives the same estimate every time, so results can be repeated, and
the tests check that you get this. 💡 There is a hint.[^birthday-set] Estimate
the chance for several group sizes and run it with different seeds. How much do
the answers wobble? How many trials do you need before the second decimal place
stops changing?

```bash
uv run pytest exercises/office_party/test_birthday.py -k "not exact and not smallest"
```

[^birthday-set]: A set holds each value once, so a group has a shared birthday
    exactly when turning it into a set makes it smaller. `random.choices(range(365),
    k=people)` draws a whole group in one call.

**Stage 2: do the sum.** A simulation can only estimate. Implement
`shared_birthday_probability(people, days)` to calculate the chance exactly, and
compare it with your estimates. 💡 There is a hint.[^birthday-opposite] Then
implement `smallest_group_with_probability(threshold)`, which finds the first
group size whose chance reaches the threshold,[^birthday-next] and use it to
answer the question you started with. How close was your guess?

```bash
uv run pytest exercises/office_party/test_birthday.py -k "exact or smallest"
```

[^birthday-opposite]: Counting every way that *somebody* shares is messy. Count
    the opposite instead: in how many ways can everyone have a *different*
    birthday? `math.perm` may help. Python integers never overflow, so you can
    let the intermediate numbers grow enormous and divide only at the end.

[^birthday-next]: `next(n for n in itertools.count() if ...)` returns the first
    value from an endless counter that passes a test, without building a list.

## Over to the notebook 📓

The functions are done, so now use them. From here the work happens in the
[Against the Odds notebook](investigate.ipynb#The-office-party),
not in `birthday.py`: open it, run the setup cell, and find the **The office
party** section. The plotting code is provided; your job is to fill in the
tables of results and explain what they show.

1. **Simulation against the sum.** Build a table of estimated and exact chances
   for group sizes from 2 to 60, then plot both. How many trials do you need
   before the simulated points hug the exact curve?
2. **Why so few? 🚀** A group of $n$ people contains $\binom{n}{2}$ pairs of
   people (`math.comb(n, 2)`). Compare the number of pairs at your answer with
   the number of days. What does that suggest? Then, for 10, 100, 1,000, 10,000
   and 100,000 days, find the group size for even odds and tabulate it with the
   number of pairs. Plot group size against days. What is the pattern, and does
   it fit the pairs argument?
3. **Uneven birthdays.** Real birthdays are not equally likely. Predict whether
   that makes a match more or less likely, then check by simulation.

<details>
<summary>What did you discover?</summary>

The chance passes one half at **23 people**, far fewer than the roughly 180 many
people guess by thinking of half the days in a year. With 10,000 trials per group
size the simulation tracks the exact curve to within about 0.01 (the standard
error of such an estimate is at most 0.005), and each extra decimal place of
agreement costs about 100 times as many trials.

The intuition fails because we compare the group with *ourselves*, which is only
$n - 1$ possible matches. Any two people can match, and there are
$\binom{n}{2}$ pairs.

For other numbers of days, the number of pairs at even odds stays close to $0.7$
times the number of days (it tends to $\ln 2 \approx 0.69$), so the group size
grows like $\sqrt{\text{days}}$, at about $1.18\sqrt{\text{days}}$. Each pair
matches with probability $1/\text{days}$, so the expected number of matching
pairs is about $\binom{n}{2}/\text{days}$. For small chances,
$P(\text{no match}) \approx e^{-n(n-1)/(2\,\text{days})}$. Setting that to
$1/2$ gives $n(n-1) \approx 2\ln 2 \times \text{days}$, so
$n \approx 1.18\sqrt{\text{days}}$. A group only needs to grow with the square
root of the number of days, not the number of days itself.

Uneven birthdays make a match **more** likely. In a busy-season example where 40
days are three times as popular as the other 325, the chance with 23 people
rises from about 0.51 to about 0.59. When some days are popular, two people are
more likely to land on the same one. Uniform birthdays are the *least*
favourable case for a match, so the standard answer of 23 is an upper bound for
any real population.

</details>
