# Test-first: 99 Bottles

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python. This is an optional test-first kata: a
> practice exercise in working one test at a time, not an algorithmic puzzle.
>
> **You’ll practise:** test-first development, string formatting, composing
> small functions, and writing your own tests.
>
> **Check:** `uv run pytest exercises/pythonic_python/ninety_nine_bottles/ -q`

The goal here is to write functions that generate the lyrics to "99 bottles".
We will do this following the principle of test-first development. The tests
for the functions are all provided; you now need to make them pass by filling
in the functions.

Implement `verse(number)`, `verses(start, end)`, and `bottles()` in
[bottles.py](bottles.py). The tests in
[test_bottles.py](test_bottles.py) are executable examples: make one
scenario pass at a time, then refactor without changing the lyrics. Preserve
singular and plural grammar, the zero-bottle wording, blank lines between
verses, and the final newline. The full song is available at
[99_bottles.txt](data/99_bottles.txt).

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
   [test_bottles.py](test_bottles.py) for the two verses above, for a
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
