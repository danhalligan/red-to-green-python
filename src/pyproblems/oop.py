"""Introductory object-oriented programming exercises."""

from collections.abc import Iterable
from typing import Any

REFRAIN = "Ring-ding-ding-ding-dingeringeding!"


class UnknownSoundError(Exception):
    """Raised by speak() when nobody knows what an animal says."""


class Animal:
    """Base class for animals in the song exercise."""

    def __init__(self, name: str | None = None) -> None:
        """Store the animal's optional name as the instance attribute `name`."""
        raise NotImplementedError

    def speak(self) -> str:
        """Return this animal's sound; subclasses provide the sound."""
        raise NotImplementedError("Animal subclasses must implement speak()")

    def __str__(self) -> str:
        """Return a readable description of this animal."""
        raise NotImplementedError


class Dog(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Cat(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Bird(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Mouse(Animal):
    def speak(self) -> str:
        return "squeek"


class Cow(Animal):
    def speak(self) -> str:
        return "moo"


class Frog(Animal):
    def speak(self) -> str:
        return "croak"


class Elephant(Animal):
    def speak(self) -> str:
        return "toot"


class Duck(Animal):
    def speak(self) -> str:
        return "quack"


class Fish(Animal):
    def speak(self) -> str:
        return "blub"


class Seal(Animal):
    def speak(self) -> str:
        return "ow ow ow"


def lyric(animal: Any) -> str:
    """Return a song line such as `Duck goes "quack"` for anything that can speak()."""
    raise NotImplementedError


class Fox(Animal):
    """An animal whose sound nobody knows."""

    def speak(self) -> str:
        """Raise UnknownSoundError: nobody knows what the fox says."""
        raise NotImplementedError


def sing(animals: Iterable[Any], guess: str = REFRAIN) -> str:
    """Return one lyric line per animal, each followed by a newline.

    An animal whose sound is unknown gets the mystery verse instead, with
    `guess` as the answer and the animal's lower-case class name in the question:

        But there's one sound
        That no one knows
        What does the fox say?
        "Ring-ding-ding-ding-dingeringeding!"
    """
    raise NotImplementedError


def wdtfs(animals: Iterable[Animal]) -> str:
    """Return the song "What Does the Fox Say?": the animals, then the fox."""
    return sing([*animals, Fox()])


class Parrot(Bird):
    """A bird that repeats the last sound it heard, else tweets."""

    def __init__(self, name: str | None = None) -> None:
        raise NotImplementedError

    def hear(self, sound: str) -> None:
        """Remember sound so that speak() repeats it."""
        raise NotImplementedError

    def listen_to(self, animal: Any) -> None:
        """Learn whatever sound `animal.speak()` returns."""
        raise NotImplementedError

    def speak(self) -> str:
        raise NotImplementedError


class Robot:
    """A speaker that is not an Animal: it recites a programmed sequence."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError

    def program_speech(self, lines: Iterable[str]) -> None:
        """Replace the program with `lines` and start again from the first."""
        raise NotImplementedError

    def speak(self) -> str:
        """Return the next programmed line, or "Beep boop" once they run out."""
        raise NotImplementedError


def cover(band: Iterable[Animal], robot: Robot) -> str:
    """Return the song with `robot` standing in for every animal in `band`.

    Program the robot with the sounds of the band, in order, and sing one line
    for each. Then ask the exhausted robot what the fox says.
    """
    raise NotImplementedError
