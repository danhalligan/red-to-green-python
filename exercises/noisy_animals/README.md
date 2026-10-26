# Noisy animals 📣

> **Difficulty:** 🌶️🌶️
>
> **Before you start:** basic Python.
>
> **You’ll practise:** classes, instances, inheritance, method overriding,
> polymorphism, exceptions, mutable instance state, and duck typing.
>
> **Check:** `uv run pytest exercises/noisy_animals/ -q`, or the command at the end of
> each exercise below.

**In this topic:** [Noisy animals](#noisy-animals-) ·
[What Does the Fox Say?](#what-does-the-fox-say-) ·
[A parrot that learns](#a-parrot-that-learns-) ·
[The robot joins the band](#the-robot-joins-the-band-) ·
[Looking back](#looking-back)

This exercise is about object-orientation, an approach that structures code around
*objects*: units that combine _data_ (attributes) and _functions_ (methods).

Complete the `Animal` base class `__init__` method in [animals.py](animals.py). This initialiser
should store an optional name on the instance, so that `animal.name` returns it
(or `None` if none was given). Note you can leave the `speak()` method alone:
subclasses will provide their own sound by overriding that method.

Implement `Dog`, `Cat` and `Bird`. The seven other animals (`Mouse`, `Cow`,
`Frog`, `Elephant`, `Duck`, `Fish` and `Seal`) are already written, so you can
see what a finished subclass looks like. Each class inherits from `Animal` and
implements `speak()`. The sound each animal makes is listed in the tests: read
`test_animal_subclasses_override_speak` in [test_animals.py](test_animals.py) to
see what `speak()` should return for `Dog`, `Cat` and `Bird`. For example:

```python
dog = Dog("Woofy Goldberg")
print(dog.speak())
print(dog.name)
print(isinstance(dog, Animal))

animals = [Dog("Woofy Goldberg"), Cat("Chairman Meow"), Fish("Gill Bates")]
print(", ".join(x.name for x in animals))
```

Implement `__str__()` so `str(Dog("Woofy Goldberg"))` produces
`Dog named Woofy Goldberg`, and `str(Cat())` (no name) is just `Cat`. You
should be able to do this by just editing the Animal base class! To do this
though, you'll need to look up the class name of each animal instance.

For example:

```python
dog = Dog("Woofy Goldberg")
type(dog).__name__
```

Notice what is shared and what is not: the sound and the class name belong to
the class, so every `Dog` goes "woof", but the name belongs to each instance, so
two `Dog` objects can have different names.

A dictionary mapping animal names to sounds would do the job so far, and for
simple lookups that is a perfectly good design. Classes start to pay off when
objects gain state and behaviour of their own, as the rest of this section
shows.

The tests for the later exercises fail until you reach them, so check this
exercise on its own with:

```bash
uv run pytest exercises/noisy_animals/test_animals.py -k "not (lyric or fox or sing or wdtfs or parrot or robot or cover)" -q
```

## What Does the Fox Say? 🦊

Implement `lyric(animal)`, which returns a line such as `Duck goes "quack"`
using the animal's class name and `animal.speak()`. It needs only those two
things from the object and never checks which kind of animal it has been given,
so the same code gives a different result for each object. This is polymorphism.

Nobody knows what the fox says, so make `Fox` an `Animal` whose `speak()` raises
`UnknownSoundError` (already defined for you) instead of returning a sound. The
error carries a message: the best guess at the sound. Give the fox's error the
message `"Ring-ding-ding-ding-dingeringeding!"`. (An `UnknownSoundError` created
without a message defaults to `"Who Knows!"`.)

Now implement `sing(animals)`, which returns a list of lines, one `lyric()` per
animal. If an animal's sound is unknown, `sing` should catch the error and add
a question instead, using the animal's lower-case class name and the error's
message as the answer. This verse is four lines long:

```text
But there's one sound
That no one knows
What does the fox say?
"Ring-ding-ding-ding-dingeringeding!"
```

Catch `UnknownSoundError` specifically, not every exception, so that a real bug
is still reported. Note not all animals with unknown sound errors are 
necessarily foxes, and the lyric should cope with other cases!

`wdtfs(animals)` is written for you. It runs through animals you give it and
then adds a fox at the end, reusing `sing` rather than repeating it. Create one
instance of each of the ten animals above (not the fox) in a list, in that
order, and pass it in.

You should now have the lyrics to
[The Fox (What Does the Fox Say?)](https://www.youtube.com/watch?v=jofNR_WkoCE).
The complete expected song is in
[animal_song_full.txt](data/animal_song_full.txt), one line of
the file per item in your list.

Open the [Animal playground notebook](investigate.ipynb) to
meet the band by name and hear the song for yourself. Its later sections use the
parrot and the robot, so come back to it as you finish each exercise.

```bash
uv run pytest exercises/noisy_animals/test_animals.py -k "(lyric or fox or sing or wdtfs) and not (parrot or robot or cover)" -q
```

## A parrot that learns 🦜

So far each subclass only returns a fixed string. Subclasses become more
interesting when they have state. Add `Parrot(Bird)`, which repeats the last
sound it heard:

```python
polly = Parrot("Polly Morphism")
print(polly.speak())  # tweet
polly.listen_to(Duck())
print(polly.speak())  # quack
print(lyric(polly))  # Parrot goes "quack"
```

Before it hears anything, a `Parrot` should behave like any other `Bird`, so
use `super()` rather than repeating `"tweet"`. You should not need to change
`lyric()`: it calls `animal.speak()`, so it works for the parrot unchanged. Two
parrots must remember independently of each other.

`listen_to(animal)` learns whatever sound `animal.speak()` returns. If the
animal's sound is unknown, the error should reach the caller and the parrot
should keep what it already knew.

Finally, give the parrot the last word. Have a parrot listen to a `Duck`, then
call `sing([Fox(), polly])`: the song ends with the parrot repeating what it
heard.

```bash
uv run pytest exercises/noisy_animals/test_animals.py -k "parrot and not (robot or cover)" -q
```

## The robot joins the band 🤖

A `Robot` can speak, but a robot is not an animal, so it should **not** inherit
from `Animal`. Inheritance should model a real relationship, not just share a
method name. 

Write a `Robot(name)` class with:

- `program_with(speaker)`, which adds whatever `speaker.speak()` says right
  now to the end of the robot's memory.
- `speak()`, which returns the oldest sound in the robot's memory and forgets
  it. When the memory is empty, the robot is as stumped as the fox: it raises
  `UnknownSoundError("Beep boop")`.

Each robot keeps its own memory, and a robot that has not been programmed has
nothing to say.

```bash
uv run pytest exercises/noisy_animals/test_animals.py -k "robot and not cover" -q
```

Now the surprise. `lyric()` and `sing()` were written before `Robot` existed,
yet they work for it, because all they need from an object is a `speak()` method
and a class name, and every Python object has a class name. Program a robot
with a duck and compare them:

```python
robo_duck = Robot("RoboDuck")
robo_duck.program_with(Duck())

print(lyric(Duck()))  # Duck goes "quack"
print(lyric(robo_duck))  # Robot goes "quack"
print(isinstance(robo_duck, Duck))  # False
```

If it quacks like a duck, `lyric()` is happy: it never checks what the object
is, and the line says `Robot` because that is the class name it asks for. This
is *duck typing*: code needs only the methods an object provides, not its place
in a class hierarchy, so unrelated classes can take part in the same code
without a shared base class. The same goes for `listen_to()`, so you can even
teach a parrot to repeat a robot.

An empty robot raises `UnknownSoundError`, just like the fox, so `sing` already
knows what to do with one: `sing([Robot("Marvin")])` asks what the *robot* says
and answers `"Beep boop"`.

Now put the robot to work. Write `cover(band, robot)`, which makes a cover
version of the song in which one robot replaces every animal. Teach the robot
what each animal in `band` says, in order, then sing one line per animal using
the robot itself, then ask the exhausted robot what it says. Its memory has run
out by then, so it answers with the usual `"Beep boop"`.

<details>
<summary>💡 Hint: how many lines?</summary>

Sing one line for each animal in the band, plus one more for the question the
robot cannot answer. `sing` asks each speaker once per line, so you can pass it
the same robot repeatedly.

</details>

```python
band = [Bird(), Cat(), Mouse()]
robot = Robot("Marvin the Paranoid Android")
print("\n".join(cover(band, robot)))
```

```text
Robot goes "tweet"
Robot goes "meow"
Robot goes "squeak"
But there's one sound
That no one knows
What does the robot say?
"Beep boop"
```

The same robot object appears on every line yet says something different each
time, because it remembers what it has been taught and forgets each sound once
it is spoken. `sing` needed no changes. After `cover` returns, call
`robot.speak()`: what happens, and why?

```bash
uv run pytest exercises/noisy_animals/test_animals.py -k cover -q
```

With everything finished, return to the
[Animal playground notebook](investigate.ipynb) and work 
through the parrot and robot sections.

## Looking back

Ten animal classes that differ only in the string that `speak()` returns is a
lot of effort.

- Could `Dog`, `Cat` and `Bird` have been one `Animal` class with a `sound`
  attribute? What would you have lost?
- What changed with the `Parrot` and the `Robot`? Why do objects, which bundle
  state with behaviour, earn their keep there?
- The robot never inherited from `Animal`, yet `lyric()` and `sing()` worked
  with it. What does Python need for polymorphism? When is inheritance still the
  right tool?

<details>
<summary>Some thoughts</summary>

Yes, for the first three a single class with a `sound` attribute would do, and
it would be simpler. You would lose the class name that `lyric()` and `str()`
use, and would need an explicit attribute for it. The classes here are a
teaching device. Objects pay for themselves when they carry state that changes
(the parrot's memory, the robot's memory of what it was taught) together with
the behaviour that uses it.

Python does not need a shared superclass for polymorphism: any object with a
`speak()` method will do. Inheritance is useful when subclasses really share
implementation (`Parrot` reuses `Bird`'s `"tweet"` through `super()`) or when
you want `isinstance` checks to group related types. Sharing a method name alone
is not a reason to inherit.

</details>
