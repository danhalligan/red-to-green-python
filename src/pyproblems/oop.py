"""Introductory object-oriented programming exercises."""

from collections.abc import Iterable
from typing import Any


class UnknownSoundError(Exception):
    """Raised by speak() when nobody knows what an animal says.

    The message is the best guess at the sound.
    """

    def __init__(self, message: str = "Who Knows!") -> None:
        super().__init__(message)


class Animal:
    """Base class for animals in the song exercise."""

    def __init__(self, name: str | None = None) -> None:
        """Store the animal's optional name as the instance attribute `name`."""
        # TODO: store the animal's name
        raise NotImplementedError

    def speak(self) -> str:
        """Return this animal's sound; subclasses provide the sound."""
        raise NotImplementedError("Animal subclasses must implement speak()")

    def __str__(self) -> str:
        """Return a readable description of this animal."""
        # TODO: return the readable description
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
        """Raise UnknownSoundError, with the fox's best guess as its message."""
        raise NotImplementedError


def sing(animals: Iterable[Any]) -> list[str]:
    """Return a list of song lines: one lyric per animal.

    An animal whose sound is unknown gets the mystery verse instead (four
    lines), using the lower-case class name in the question and the
    UnknownSoundError message as the answer:

        But there's one sound
        That no one knows
        What does the [class] say?
        "[message]"
    """
    raise NotImplementedError


def wdtfs(animals: Iterable[Animal]) -> list[str]:
    """Return the song "What Does the Fox Say?": the animals, then the fox."""
    return sing([*animals, Fox()])


class Parrot(Bird):
    """A bird that repeats the last sound it heard, else tweets."""

    def __init__(self, name: str | None = None) -> None:
        raise NotImplementedError

    def listen_to(self, animal: Any) -> None:
        """Learn whatever sound `animal.speak()` returns; speak() repeats it."""
        raise NotImplementedError

    def speak(self) -> str:
        raise NotImplementedError


class Robot:
    """A speaker that is not an Animal: it remembers sounds and replays them."""

    def __init__(self, name: str) -> None:
        raise NotImplementedError

    def program_with(self, speaker: Any) -> None:
        """Remember what `speaker.speak()` says now, after anything already learned."""
        raise NotImplementedError

    def speak(self) -> str:
        """Return the oldest unspoken sound, forgetting it.

        Raise UnknownSoundError("Beep boop") once the memory is empty.
        """
        raise NotImplementedError


def cover(band: list[Animal], robot: Robot) -> list[str]:
    """Return the song with `robot` standing in for every animal in `band`.

    Teach the robot what each animal says, in order, then sing one line for
    each, followed by the mystery verse for the exhausted robot.
    """
    raise NotImplementedError
