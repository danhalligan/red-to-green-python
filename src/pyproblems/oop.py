"""Introductory object-oriented programming exercises."""

from collections.abc import Iterable


class Animal:
    """Base class for animals in the song exercise."""

    def __init__(self, name: str | None = None) -> None:
        """Store the animal's optional name as the instance attribute `name`."""
        raise NotImplementedError

    def speak(self) -> str:
        """Return this animal's sound; subclasses provide the sound."""
        raise NotImplementedError("Animal subclasses must implement speak()")

    def lyric(self) -> str:
        """Return a song line using this animal's name and sound."""
        return f'{type(self).__name__} goes "{self.speak()}"'

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


class Fox(Animal):
    def speak(self) -> str:
        """Return the refrain: "Ring-ding-ding-ding-dingeringeding!"."""
        raise NotImplementedError

    def lyric(self) -> str:
        """Return the whole fox verse, not just a "goes" line."""
        raise NotImplementedError


class Parrot(Bird):
    """A bird that repeats the last sound it heard, else tweets."""

    def __init__(self, name: str | None = None) -> None:
        raise NotImplementedError

    def hear(self, sound: str) -> None:
        """Remember sound so that speak() repeats it."""
        raise NotImplementedError

    def speak(self) -> str:
        raise NotImplementedError


def wdtfs(animals: Iterable[Animal]) -> str:
    """Return song lyrics for animals, ending with the verse from a Fox."""
    raise NotImplementedError
