# The 100 prisoners 🔐

> **Difficulty:** 🌶️🌶️🌶️
>
> **Before you start:** basic Python. The investigation uses the
> [Against the Odds notebook](../../analysis/against_the_odds.ipynb), which needs
> the science packages (`uv sync --all-groups --extra science`).
>
> **Recommended first:** [The office party](office-party.md), for
> simulating with random numbers.
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

In [prisoners.py](../../src/pyproblems/prisoners.py), each prisoner is given a
`Room`, which is already written. They can only look at drawers by calling
`room.open(i)`, which returns the number inside. The room counts the drawers
opened, refuses more than `room.limit` by raising `TooManyDrawersError`, and notes
in `room.found` whether the prisoner has seen their own number. A prisoner's
plan is a *strategy*: a function `strategy(room)` that opens drawers. Because
functions can be passed as arguments, the same game can be played with any
strategy.

**Stage 1: no plan.** Implement `shuffled_drawers`, `random_strategy`,
`fixed_strategy`, `count_successes` and `estimate_survival`. A random prisoner
opens drawers at random. With `fixed_strategy` the prisoners instead agree in
advance that everyone opens the same drawers, such as the first half.
💡 There are hints.[^prisoners-random]
Once they work you can play the game in the notebook, below.

```bash
uv run pytest tests/test_prisoners.py -k "not clever and not cycle and not loop"
```

[^prisoners-random]: `random.shuffle` shuffles a list in place, and
    `random.sample(range(n), k)` picks `k` different values. Each prisoner needs a
    fresh `Room`, because the drawers are closed again between prisoners.

**Stage 2: use what you see.** The prisoners cannot talk, but they can react to
what they find. Implement `clever_strategy` so that the prisoners do much better
than random. 💡 There is a hint.[^prisoners-start]

```bash
uv run pytest tests/test_prisoners.py -k clever
```

[^prisoners-start]: Prisoner 7 must open *some* drawer first. Why not drawer 7?
    Then think about what the number inside is, and where a number could send
    them next.

**Investigation 🚀: alone and together.** In the
[notebook](../../analysis/against_the_odds.ipynb), compare the average number of
prisoners who find their number under each strategy. Then plot the distribution
ofExtension 🚀: why does it work?** Draw an arrangement of eight drawers as
arrows from each drawer to the drawer whose number it holds. Follow the arrows
from any drawer: where do you end up? Implement `cycle_lengths(arrangement)` to
split an arrangement into its closed loops and return their lengths. You will use
it in the notebook to explain the clever strategy.

```bash
uv run pytest tests/test_prisoners.py -k "cycle or loop"
```

## Investigation: over to the notebook 📓

The functions are done, so now use them. From here the work happens in the
[Against the Odds notebook](../../analysis/against_the_odds.ipynb#The-100-prisoners),
not in `prisoners.py`: open it, run the setup cell, and find the **The 100
prisoners** section. The plotting code is provided; your job is to fill in the
tables of results and explain what they show. There are no tests for this part,
so write down your prediction before you run each cell.

1. **Survival chance.** Build a table of the estimated survival chance with 10,
   20, 50 and 100 prisoners, each allowed to open half the drawers, for all
   three strategies, and plot it. Compare it with your prediction. How does the
   chance change as the number of prisoners grows? Is that what you expected? Why
   can you not simply simulate the random strategy with 100 prisoners and see?
   What is the chance, by pure calculation? Can you explain what happens with the
   fixed strategy?
2. **Alone and together 🚀.** Compare the average number of prisoners who find
   their number under each strategy. Then plot the distribution of that number
   across thousands of games. What do you notice about the averages, and what
   about the shapes? Which strategy makes the prisoners' fates depend on one
   another, and what does that buy them?
3. **Loops 🚀.** Compare `cycle_lengths` with `count_successes` in many games.
   Write down the rule linking the loops to the prisoners who succeed, and explain
   why a prisoner's own number is always somewhere in their chain. Then use that
   rule to estimate the survival chance without simulating any prisoners, which is
   much faster. Plot the length of the longest loop across many random
   arrangements of 100 drawers: how often is it longer than half the drawers?
   What does the chance approach as the number of prisoners grows to 1,000?

<details>
<summary>What did you discover?</summary>

With the random strategy the chance is about $2^{-n}$, effectively zero by
$n = 20$ (for 100 prisoners it is about $10^{-30}$, which is why you cannot
simulate it). The clever strategy starts at about 35% for 10 prisoners and
settles near 31% for 100. It does **not** shrink towards zero as the number of
prisoners grows. The fixed strategy is worse still: its chance is exactly zero
whenever the prisoners may not open every drawer, because the drawers they all
open hold only `limit` different numbers, so at most `limit` prisoners can ever
succeed.

Under all three strategies each prisoner has a 50% chance of finding their
number, so the average fraction who succeed is 0.50 either way. The shapes are
completely different. With the fixed strategy exactly half the prisoners succeed
in every game, a single bar. Random prisoners succeed independently, so the count
is bell-shaped around half the prisoners and every prisoner succeeding is
practically impossible. With the clever strategy the count is spread widely, with a spike at
"everyone": about a third of games free everyone. The clever strategy makes the
prisoners' fates **dependent**. Prisoners on the same loop of drawers all succeed
or all fail together, so successes come in large groups. The individual odds are
unchanged, but probability is pushed into the extremes, "everyone" and "almost
nobody", and "everyone" is the only outcome the director cares about.

A prisoner who starts at their own drawer follows the loop containing their
number, and reaches their number after exactly as many openings as that loop is
long. So a prisoner succeeds exactly when their loop has at most `limit` drawers,
and everyone on a loop succeeds or fails together. The number of prisoners who
succeed is the number of drawers on short loops, which is why your two columns
always agree.

Everybody survives exactly when no loop is longer than `limit`. In your
histogram, about a third of the arrangements of 100 drawers have a longest loop
of at most 50: that share is the survival chance. When `limit` is
half the drawers, at most one loop can be longer than that, and the chance of a
loop of exact length $k$ is $1/k$. The survival probability is therefore
$$1 - \sum_{k=n/2+1}^{n} \frac{1}{k},$$
which is 0.3118 for $n = 100$ and approaches $1 - \ln 2 \approx 0.3069$ as $n$
grows to 1,000 and beyond.

</details>
