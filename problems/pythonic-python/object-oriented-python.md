# Object-oriented Python

> **Before you start:** basic Python.
>
> **You’ll practise:** classes, instances, inheritance, method overriding,
> polymorphism, exceptions, mutable instance state, and duck typing.
>
> **Check:** `uv run pytest tests/test_oop.py -q`, or the command at the end of
> each exercise below.

**In this topic:** [Noisy animals](#noisy-animals-) ·
[What Does the Fox Say?](#what-does-the-fox-say-) ·
[A parrot that learns](#a-parrot-that-learns-) ·
[The robot joins the band](#the-robot-joins-the-band-)

Work through the exercises in order: each builds on the code you wrote in the
last. All of the code goes in [oop.py](../../src/pyproblems/oop.py).

## Noisy animals 📣

Create an `Animal` base class in `oop.py`. Its initialiser
should store an optional name on the instance, so that `animal.name` returns
it (or `None` if none was given). Its `speak()` method defines the interface
and raises `NotImplementedError`; subclasses provide their own sound by
overriding that method.

Implement `Dog`, `Cat` and `Bird`. The seven other animals (`Mouse`, `Cow`,
`Frog`, `Elephant`, `Duck`, `Fish` and `Seal`) are already written, so you can
see what a finished subclass looks like. Each class inherits from `Animal` and
implements `speak()`. For example:

```python
dog = Dog("Woofy Goldberg")
print(dog.speak())
print(dog.name)
print(isinstance(dog, Animal))

animals = [Dog("Woofy Goldberg"), Cat("Chairman Meow"), Fish("Gill Bates")]
print(", ".join(x.name for x in animals))
```

The sound each animal makes is listed in the tests: read
`test_animal_subclasses_override_speak` in [test_oop.py](../../tests/test_oop.py) to
see what `speak()` should return for `Dog`, `Cat` and `Bird`.

Implement `__str__()` so `str(Dog("Woofy Goldberg"))` produces
`Dog named Woofy Goldberg`, and `str(Cat())` (no name) is just `Cat`. Notice
what is shared and what is not: the sound and the class name belong to the
class, so every `Dog` goes "woof", but the name belongs to each instance, so two
`Dog` objects can have different names.

A dictionary mapping animal names to sounds would do the job so far, and for
simple lookups that is a perfectly good design. Classes start to pay off when
objects gain state and behaviour of their own, as the rest of this section
shows.

The tests for the later exercises fail until you reach them, so check this
exercise on its own with:

```bash
uv run pytest tests/test_oop.py -k "not (lyric or fox or sing or wdtfs or parrot or robot or cover)" -q
```

## What Does the Fox Say? 🦊

*Builds on [Noisy animals](#noisy-animals-): you need `Animal` and its
subclasses.*

Generating song lyrics is not an animal's job, so write it as a separate
function. Implement `lyric(animal)`, which returns a line such as
`Duck goes "quack"` using the animal's class name and `animal.speak()`. It
asks the animal for its sound and never checks which kind of animal it has been
given, so it works for every `Animal`: the same code gives a different result
for each object. This is polymorphism.

Nobody knows what the fox says, so make `Fox` an `Animal` whose `speak()` raises
`UnknownSoundError` (already defined for you) instead of returning a sound. Now
implement `sing(animals, guess=REFRAIN)`, which returns one `lyric()` line per
animal, each followed by a newline. If an animal's sound is unknown, `sing`
should catch the error and write a question instead, using the animal's
lower-case class name and the `guess` as the answer:

```text
But there's one sound
That no one knows
What does the fox say?
"Ring-ding-ding-ding-dingeringeding!"
```

Catch `UnknownSoundError` specifically, not every exception, so that a real bug
is still reported.

`wdtfs(animals)` is written for you. It sings the animals you give it and then
the fox, reusing `sing` rather than repeating it. Create one instance of each of
the ten animals above (not the fox) in a list, in that order, and pass it in.
You should now have the lyrics to
[The Fox (What Does the Fox Say?)](https://www.youtube.com/watch?v=jofNR_WkoCE).
The complete expected song is in
[animal_song_full.txt](../../tests/fixtures/animal_song_full.txt).

```bash
uv run pytest tests/test_oop.py -k "(lyric or fox or sing or wdtfs) and not (parrot or robot or cover)" -q
```

## A parrot that learns 🦜

*Builds on [What Does the Fox Say?](#what-does-the-fox-say-): you need `lyric`,
`sing` and `Fox`.*

So far each subclass only returns a fixed string. Subclasses become more
interesting when they have state. Add `Parrot(Bird)`, which repeats the last
sound it heard:

```python
polly = Parrot("Polly Morphism")
print(polly.speak())  # tweet
polly.hear("hello")
print(polly.speak())  # hello
print(lyric(polly))  # Parrot goes "hello"
```

Before it hears anything, a `Parrot` should behave like any other `Bird`, so
use `super()` rather than repeating `"tweet"`. You should not need to change
`lyric()`: it calls `animal.speak()`, so it works for the parrot unchanged. Two
parrots must remember independently of each other.

Add `listen_to(animal)`, which learns whatever sound `animal.speak()` returns.
If the animal's sound is unknown, the error should reach the caller and the
parrot should keep what it already knew.

Finally, give the parrot the last word. Have a parrot hear a guess for the fox
and call `sing([..., Fox(), polly], guess)`: the song now ends with the parrot
repeating the answer.

```bash
uv run pytest tests/test_oop.py -k "parrot and not (robot or cover)" -q
```

## The robot joins the band 🤖

*Builds on the earlier exercises: you need `lyric`, `sing` and `Fox` from
[What Does the Fox Say?](#what-does-the-fox-say-), and `Parrot` from
[A parrot that learns](#a-parrot-that-learns-).*

A `Robot` can speak, but a robot is not an animal, so it should **not** inherit
from `Animal`. Inheritance should model a real relationship, not just share a
method name. Write a `Robot(name)` class with:

- `program_speech(lines)`, which gives the robot a sequence of phrases to say
  and starts it again from the first one. The robot should keep its own copy,
  so editing your list later does not change it.
- `speak()`, which returns the next programmed phrase each time it is called.
  Once the program runs out, it returns `"Beep boop"`.

Each robot keeps its own program and its own position in it. A robot that has
not been programmed just says `"Beep boop"`.

```bash
uv run pytest tests/test_oop.py -k "robot and not cover" -q
```

Now the surprise. `lyric()` and `sing()` were written before `Robot` existed,
yet they work for it, because they only ever call `speak()`. Program a robot
to say `"quack"` and compare it with a real duck:

```python
robo_duck = Robot("RoboDuck")
robo_duck.program_speech(["quack"])

print(lyric(Duck()))  # Duck goes "quack"
print(lyric(robo_duck))  # Robot goes "quack"
print(isinstance(robo_duck, Duck))  # False
```

If it quacks like a duck, `lyric()` treats it as a duck. This is *duck typing*:
code needs only the methods an object provides, not its place in a class
hierarchy, so unrelated classes can take part in the same code without a
shared base class. The same goes for `listen_to()`, so you can even teach a
parrot to repeat a robot.

Now put the robot to work. Write `cover(band, robot)`, which makes a cover
version of the song in which one robot replaces every animal. Program the robot
with what each animal in `band` says, in order, and sing one line per animal
using the robot itself, then ask the exhausted robot what the fox says. The
robot has run out of program by then, so its answer is the usual `"Beep boop"`:

```python
band = [Bird(), Cat(), Mouse()]
print(cover(band, Robot("Marvin the Paranoid Android")))
```

```text
Robot goes "tweet"
Robot goes "meow"
Robot goes "squeek"
But there's one sound
That no one knows
What does the fox say?
"Beep boop"
```

The same robot object appears on every line yet says something different each
time, because it remembers where it is in its program. `sing` needed no changes.

```bash
uv run pytest tests/test_oop.py -k cover -q
```
