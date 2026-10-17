# Try, try again 🏉

> **Before you start:** basic Python.
>
> **Recommended first:** [Fibonacci](../pythonic-python/python-fundamentals.md#q4-fibonacci-sequence)
> (Python Fundamentals Q4), which introduces recurrence relationships.
>
> **You’ll practise:** breaking a problem into smaller ones, spotting repeated
> work, caching, and building an answer up from the bottom.
>
> **Check:** `uv run pytest tests/test_rugby.py -q`, or the focused command at
> each stage.

**In this exercise:** [Stage 1](#stage-1-reconstruct-the-match) ·
[Stage 2](#stage-2-the-commentator-gets-carried-away) ·
[Stage 3](#stage-3-the-entire-season), then an optional extension and
investigation (🚀).

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

## Stage 1: Reconstruct the match

Implement `count_scoring_sequences(points)` in
[rugby.py](../../src/pyproblems/rugby.py); it should raise a `ValueError` for a
negative score. Work out 10 points by hand before you write any code, then check
it against your function. How you do it is up to you: any approach that gets the
right counts will do. Stuck? There are 💡 hints.

```bash
uv run pytest tests/test_rugby.py -k "scoring_sequences and not carried_away and not season"
```

<details>
<summary>💡 Hint 1: a nudge</summary>

Does the answer for a score of 5 help you with 7? What about 8? Think about what
the *last* scoring event could have been, and what the score was before it. Could
you perhaps call the score calculating function to get the result for a smaller
score to help calculate the current score?

</details>

<details>
<summary>💡 Hint 2: conversions</summary>

Conversions are special types of event and might need special consideration
because a conversion can only ever follow a try. Can you reframe the question
slightly to make it easy to implement conversions?

</details>

## Stage 2: The commentator gets carried away

The commentator is sure Scotland won, but is so delirious they're not sure of
the score any more. Did they score 30 points? Or was it 50? Maybe it was 100! Try
these in your function. If it works for small scores but struggles with larger
ones, think about why. Is it repeating calculations that it has already
performed? Try drawing out which smaller scores your function needs for 12
points, or count how many times it is called for 20, 30 and 40 points. How does
the cost grow? The `carried_away` test gives up after five seconds and says so,
rather than hanging. 💡 There are hints towards a fix.

```bash
uv run pytest tests/test_rugby.py -k carried_away
```

<details>
<summary>💡 Hint 1: a nudge</summary>

When your function works out the answer for 12 points, which smaller scores does it
ask about, and do any of them come up more than once? What if it could remember
an answer it had already worked out?

</details>

<details>
<summary>💡 Hint 2: a strategy</summary>

*Caching* (also called memoisation) remembers each answer the first time it is
computed, so that it is never computed twice. Python has a "decorator" that can
help if you need it: `functools.cache`.

</details>

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

## Stage 3: The entire season

A whole season of rugby adds up to many points. Your function should now cope
with a score of 20,000. If you used a cached recursion, you may run into
Python's limit on how deeply functions can call themselves. Can you calculate
the answers in an order that avoids deep recursion altogether? 💡 There are
hints. The answer has nearly 3,000 digits, but thankfully Python
integers do not overflow!

```bash
uv run pytest tests/test_rugby.py -k season
```

<details>
<summary>💡 Hint 1: a nudge</summary>

Caching works from the answer down to the base cases. What would it look like to
work the other way, starting from the base case?

</details>

<details>
<summary>💡 Hint 2: a strategy</summary>

Start from the base case and work up, filling in a table (a list) so that every
entry only needs entries that already exist. Notice too that a cached function
that is only ever called for 1, 2, 3, ... in turn never recurses deeply: it is
secretly working from the bottom up.

</details>

<details>
<summary>💡 Hint 3: the shape of the loop</summary>

Fibonacci that way:

```text
table = [0, 1]
for n from 2 up to the target:
    add table[n - 1] + table[n - 2] to the end of the table
return the last entry of the table
```

For rugby, what goes in the first entry, and what does each later entry need?

</details>

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
why can you not get one from the other by dividing by a fixed number? 💡 There
are hints.
The extension's tests are the ones that match `-k combinations`; use
`-k "not combinations"` to skip them.

<details>
<summary>💡 Hint 1: a nudge</summary>

Your sequence counter treats every ordering as different. Work out six points by
hand: which sequences should now count as the same thing? Which of your
function's calculations would no longer be needed, or would need to change?

</details>

<details>
<summary>💡 Hint 2: a strategy</summary>

A bottom-up table can count either sequences or combinations. The two versions
come from the same two loops, one over the scores and one over the events, and
differ only in which loop is on the outside. Think about what the table holds at
the moment each event type is added.

</details>

<details>
<summary>💡 Hint 3: which loop goes first</summary>

With the outer loop over scores and the inner loop over events, every ordering
is counted. With the outer loop over events and the inner loop over scores, each
event type is added in a fixed order, so every combination is counted once.

</details>

**Investigation 🚀: how fast do the counts grow?** The ratio of consecutive
Fibonacci numbers tends to the golden ratio, about 1.618. Check this with your
[`fibonacci()`](../pythonic-python/python-fundamentals.md#q4-fibonacci-sequence). Then look at
your scoring counts from about 50 points on: what
does `count(n) / count(n - 1)` tend to, and what is `count(n) / count(n - 10)`?
(Compare it with the growth you saw in Stage 2.) Now try the number of tallies
from the extension. What does all this tell you about how fast each count grows,
and about why order makes the problem so much harder? 💡 The golden ratio
solves $x^2 = x + 1$.[^try-growth]

[^try-growth]: Fibonacci satisfies $f_n = f_{n-1} + f_{n-2}$. Trying
    $f_n = x^n$ gives $x^n = x^{n-1} + x^{n-2}$, which simplifies to
    $x^2 = x + 1$. Do the same with the recurrence for your scoring counts.
