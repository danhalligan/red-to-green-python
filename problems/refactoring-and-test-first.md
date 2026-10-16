# Refactoring and Test-First Development

[← All problems](../README.md#index-of-problems)

**In this topic:** [The Gilded Rose Kata](#the-gilded-rose-kata-) ·
[99 Bottles](#99-bottles). You only need to do one of them, but both are good
practice.

## The Gilded Rose Kata 🌹

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
>
> **Recommended first:** [Object-oriented Python](object-oriented-python.md), so
> that classes, inheritance and polymorphism are familiar. You will be working
> with a larger object-oriented codebase.
>
> **You’ll practise:** refactoring existing code safely, using tests as a
> specification, and adding a feature to code you did not write.
>
> **Check:** `uv run pytest tests/test_gilded_rose.py -q`

Below you'll find instructions for a "code kata". The job here is to implement a
new request in existing code. Handily, tests already exist that test the
functionality of the existing code, three of which fail (corresponding to the
new request that is not yet implemented). The existing tests are a good, though
not exhaustive, description of the behaviour to preserve: if they pass, you can
be fairly confident that your refactoring has not changed it. Unfortunately for
you, the current implementation of
`update_quality` in [gilded_rose.py](../src/pyproblems/gilded_rose.py) is deeply
nested and difficult to modify so you will need to refactor it first.

The setting is an inn that updates each item's `sell_in` countdown and `quality`
once per day. Ordinary goods lose quality faster after their sell-by date; Aged
Brie improves with age; Sulfuras never changes; and backstage passes become more
valuable as a concert approaches, then become worthless afterward. Quality is
generally bounded between 0 and 50, except Sulfuras, whose legendary quality is
left unchanged.

Run the focused tests and read the implementation before refactoring. The
regular-item, Aged Brie, Sulfuras, backstage-pass, quality-bound, and
multiple-item tests characterise existing behaviour. The new requirement is to
implement a new item: "Conjured Mana Cake" that degrades twice as fast as an
ordinary item, including the faster post-expiration rate.

Refactor in small steps, running the focused tests after each change. Refactor
first to make it easy to add the new requirement. Keep the public data model as
a mutable `Item` dataclass and the `update_quality(items)` interface. You may
choose helpers, subclasses, or another design; the tests check behaviour rather
than a particular hierarchy.

The original instructions for this kata are provided in the source code.

## 99 Bottles

> **Prerequisites:** [Python Fundamentals](python-fundamentals.md).
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

## Where next?

- **Search algorithms:** [Word ladder](algorithms/word-ladder.md) finishes the
  Python core route.
- **Real data:** after the core route, the
  [Scientific Python route](../README.md#choosing-a-route) starts with
  [Mysterious data](data-analysis.md#q1-mysterious-data-).
- **The other kata**, if you did only one: [Gilded Rose](#the-gilded-rose-kata-)
  or [99 Bottles](#99-bottles).
