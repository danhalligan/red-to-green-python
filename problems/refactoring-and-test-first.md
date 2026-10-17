# Refactoring and Test-First Development

**In this topic:** [The Gilded Rose Kata](#the-gilded-rose-kata-) ·
[99 Bottles](#99-bottles). Both are optional katas and independent of each
other: pick whichever appeals, or do both for practice.

## The Gilded Rose Kata 🌹

> **Before you start:** basic Python.
>
> **Recommended first:** [Object-oriented Python](object-oriented-python.md), so
> that classes, inheritance and polymorphism are familiar. You will be working
> with a larger object-oriented codebase.
>
> **You’ll practise:** refactoring existing code safely, using tests as a
> specification, and adding a feature to code you did not write.
>
> **Check:** `uv run pytest tests/test_gilded_rose.py -q`

You have inherited the inventory system of the Gilded Rose, a small inn that buys
and sells fine goods. It works. Nobody dares touch it. The innkeeper, Allison,
wants to start selling a new kind of item, and Leeroy, who wrote the code, has
moved on to new adventures.

Open `update_quality` in [gilded_rose.py](../src/pyproblems/gilded_rose.py). It
is a thicket of nested `if` statements, and adding a new kind of item means
weaving yet another special case through all of them and hoping nothing else
breaks. Your real challenge is not the new item. It is making this code easy to
change.

Somewhere inside that tangle is a neat, clear picture of what the inn actually
does. If you refactor well, the rules should read like the problem, and a new
kind of item should be a small, obvious addition rather than one more branch.
Your goal is to find that structure and save us from impenetrable nested
conditions and deep indentation.

The setting is an inn that updates each item's `sell_in` countdown and `quality`
once per day. Ordinary goods lose quality faster after their sell-by date; Aged
Brie improves with age; Sulfuras never changes; and backstage passes become more
valuable as a concert approaches, then become worthless afterward. Quality is
generally bounded between 0 and 50, except Sulfuras, whose legendary quality is
left unchanged. The original instructions for this kata are in the source code.

**What must not change.** Everything the system does today, and its interface:

- The mutable `Item` dataclass and the `update_quality(items)` function.
- The behaviour for every existing kind of item, including the quality limits.
  The regular-item, Aged Brie, Sulfuras, backstage-pass, quality-bound and
  multiple-item tests describe it. They pass now, and must still pass after every
  change you make: that is how you know you have not broken anything.

**What is new.** The inn has a supplier of "Conjured Mana Cake", which degrades
twice as fast as an ordinary item, including the faster rate after its sell-by
date. The tests for it fail until you add the feature.

Run the focused tests and read the implementation before you change anything.
Refactor in small steps, running the tests after each one, and refactor *first*,
so that adding the new item is easy. You choose the design: helpers, classes, a
table of rules or something else. The tests check behaviour, not structure.

<details>
<summary>💡 Hint 1: a nudge</summary>

Describe in plain English what happens to each kind of item in a single day. What
do the descriptions have in common, and where do they differ? How many places in
the current code would you have to edit to add a new kind of item?

</details>

<details>
<summary>💡 Hint 2: a way to look at it</summary>

Look for what changes from item to item, and separate it from what is the same for
every item (such as the countdown of `sell_in`). If each kind of item's rule were
in one place, what would `update_quality` itself need to do?

</details>

## 99 Bottles

> **Before you start:** basic Python. This is an optional test-first kata: a
> practice exercise in working one test at a time, not an algorithmic puzzle.
>
> **You’ll practise:** test-first development, string formatting, composing
> small functions, and writing your own tests.
>
> **Check:** `uv run pytest tests/test_bottles.py -q`

The goal here is to write functions that generate the lyrics to "99 bottles".
We will do this following the principle of test-first development. The tests
for the functions are all provided; you now need to make them pass by filling
in the functions.

Implement `verse(number)`, `verses(start, end)`, and `bottles()` in
[bottles.py](../src/pyproblems/bottles.py). The tests in
[test_bottles.py](../tests/test_bottles.py) are executable examples: make one
scenario pass at a time, then refactor without changing the lyrics. Preserve
singular and plural grammar, the zero-bottle wording, blank lines between
verses, and the final newline. The full song is available at
[99_bottles.txt](../tests/fixtures/99_bottles.txt).

The exercise is deliberately test-first rather than a specification to solve
all at once. Start with one verse, then a range of verses, then the complete
song. Keep formatting decisions at the boundary where they belong: `verse`
creates one stanza, while `verses` and `bottles` compose those stanzas.

**Extension 🚀: write your own tests.** So far the tests have been written for you.
In this extension you write them to add a new requirement. You should write
tests that would actually catch a wrong implementation. No tests are supplied
for it, so yours are the check.

The new requirement is a six-pack. Extend `verse`, `verses`, and `bottles` to
accept a keyword-only `six_packs=False`. When it is `True`, a count of exactly
6 is called "1 six-pack" wherever it appears. Every other count, and the
default behaviour, stays the same. For example, `verse(7, six_packs=True)` and
`verse(6, six_packs=True)` are:

```text
7 bottles of beer on the wall, 7 bottles of beer.
Take one down and pass it around, 1 six-pack of beer on the wall.

1 six-pack of beer on the wall, 1 six-pack of beer.
Take one down and pass it around, 5 bottles of beer on the wall.
```

1. Before changing any code, add tests to
   [test_bottles.py](../tests/test_bottles.py) for the two verses above, for a
   verse the option should not affect, for the default lyrics of `verse(6)`,
   and for `verses` passing the option through.
2. Run them and confirm they fail for the right reason (the option does not
   exist yet), not because of a mistake in the test.
3. Make them pass, then refactor with every test still green. If you are
   adding the same `if` in several places, put the wording of a count in one
   place.
4. Check your tests. Break your implementation on purpose, for example by
   treating 5 as a six-pack or by changing only the first half of the verse,
   and confirm that at least one test fails each time. A test that cannot fail
   tells you nothing.
