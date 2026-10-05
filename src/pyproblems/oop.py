"""Introductory object-oriented programming exercises."""

from collections.abc import Iterable


class Animal:
    """Base class for animals in the song exercise."""

    def __init__(self, name: str | None = None) -> None:
        self.name = name

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
        raise NotImplementedError


class Cow(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Frog(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Elephant(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Duck(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Fish(Animal):
    def speak(self) -> str:
        raise NotImplementedError


class Seal(Animal):
    def speak(self) -> str:
        raise NotImplementedError


def zoo() -> list[Animal]:
    """Create the standard group of animals for the song exercise."""
    raise NotImplementedError


def wdtfs(animals: Iterable[Animal]) -> str:
    """Return song lyrics for animals, ending with the fixed fox refrain."""
    raise NotImplementedError
