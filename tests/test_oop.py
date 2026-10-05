from pathlib import Path

import pytest

from pyproblems.oop import (
    Animal,
    Bird,
    Cat,
    Cow,
    Dog,
    Duck,
    Elephant,
    Fish,
    Frog,
    Mouse,
    Seal,
    wdtfs,
    zoo,
)


@pytest.mark.parametrize(
    ("animal_type", "sound"),
    [
        (Dog, "woof"),
        (Cat, "meow"),
        (Bird, "tweet"),
        (Mouse, "squeek"),
        (Cow, "moo"),
        (Frog, "croak"),
        (Elephant, "toot"),
        (Duck, "quack"),
        (Fish, "blub"),
        (Seal, "ow ow ow"),
    ],
)
def test_animal_subclasses_override_speak(animal_type, sound):
    animal = animal_type("Milo")

    assert isinstance(animal, Animal)
    assert animal.speak() == sound
    assert animal.lyric() == f'{animal_type.__name__} goes "{sound}"'


def test_base_animal_requires_a_speak_implementation():
    with pytest.raises(NotImplementedError, match="subclasses"):
        Animal().speak()


def test_animal_string_representation_uses_instance_name():
    assert str(Dog("Milo")) == "Dog named Milo"
    assert str(Cat()) == "Cat"


def test_zoo_creates_the_default_roster():
    animals = zoo()

    assert [type(animal) for animal in animals] == [
        Dog,
        Cat,
        Bird,
        Mouse,
        Cow,
        Frog,
        Elephant,
        Duck,
        Fish,
        Seal,
    ]


def test_wdtfs_matches_short_snapshot():
    animals = [Bird(), Cat(), Mouse()]
    expected = (Path(__file__).parent / "fixtures" / "animal_song_short.txt").read_text(
        encoding="utf-8"
    )

    assert wdtfs(animals) == expected


def test_wdtfs_matches_full_snapshot():
    expected = (Path(__file__).parent / "fixtures" / "animal_song_full.txt").read_text(
        encoding="utf-8"
    )

    assert wdtfs(zoo()) == expected
