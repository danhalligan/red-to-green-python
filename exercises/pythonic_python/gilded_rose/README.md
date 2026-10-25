# Refactoring: The Gilded Rose Kata 🌹

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python.
>
> **Recommended first:** [Object-oriented Python](../object_oriented_python/README.md), so
> that classes, inheritance and polymorphism are familiar. You will be working
> with a larger object-oriented codebase.
>
> **You’ll practise:** refactoring existing code safely, using tests as a
> specification, and adding a feature to code you did not write.
>
> **Check:** `uv run pytest exercises/pythonic_python/gilded_rose/ -q`

You have inherited the inventory system of the Gilded Rose, a small inn that buys
and sells fine goods. It works. Nobody dares touch it. The innkeeper, Allison,
wants to start selling a new kind of item, and Leeroy, who wrote the code, has
moved on to new adventures.

Open `update_quality` in [gilded_rose.py](gilded_rose.py). It
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

## Looking back

Now that the code is refactored and the new item works:

- How many places would you have to edit to add another kind of item, compared
  with the original thicket of `if` statements?
- Does `update_quality` now read like a description of what the inn does? Could a
  newcomer find the rule for one kind of item quickly?
- Did your design need classes? Would a table of rules, or a few small
  functions, have done as well? Which would you rather maintain?

Did the refactoring genuinely make future changes simpler? If the honest answer
is "not much", what would you change?
