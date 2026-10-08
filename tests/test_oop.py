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
    Fox,
    Frog,
    Mouse,
    Parrot,
    Seal,
    wdtfs,
)

FULL_CAST = [Dog, Cat, Bird, Mouse, Cow, Frog, Elephant, Duck, Fish, Seal]


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
    animal = animal_type("Woofy Goldberg")

    assert isinstance(animal, Animal)
    assert animal.speak() == sound
    assert animal.lyric() == f'{animal_type.__name__} goes "{sound}"'


def test_fox_speaks_the_refrain():
    fox = Fox()

    assert isinstance(fox, Animal)
    assert fox.speak() == "Ring-ding-ding-ding-dingeringeding!"


def test_fox_lyric_is_the_closing_verse():
    assert Fox().lyric() == (
        "But there's one sound\n"
        "That no one knows\n"
        "What does the fox say?\n"
        '"Ring-ding-ding-ding-dingeringeding!"'
    )


def test_parrot_tweets_until_it_hears_something():
    parrot = Parrot("Polly Morphism")

    assert isinstance(parrot, Bird)
    assert parrot.speak() == "tweet"
    assert parrot.lyric() == 'Parrot goes "tweet"'


def test_parrot_repeats_the_last_sound_it_heard():
    parrot = Parrot()

    parrot.hear("woof")
    parrot.hear("hello")

    assert parrot.speak() == "hello"
    assert parrot.lyric() == 'Parrot goes "hello"'


def test_parrots_remember_independently():
    polly, percy = Parrot(), Parrot()

    polly.hear("hello")

    assert percy.speak() == "tweet"


def test_parrot_keeps_name_handling_from_animal():
    assert str(Parrot("Polly Morphism")) == "Parrot named Polly Morphism"


def test_base_animal_requires_a_speak_implementation():
    with pytest.raises(NotImplementedError, match="subclasses"):
        Animal().speak()


def test_animal_stores_its_name_on_the_instance():
    dog = Dog("Woofy Goldberg")

    assert dog.name == "Woofy Goldberg"
    assert Dog().name is None


def test_instances_of_one_class_have_separate_names():
    woofy, rex = Dog("Woofy Goldberg"), Dog("Rex")

    assert woofy.name == "Woofy Goldberg"
    assert rex.name == "Rex"
    assert type(woofy) is type(rex)


def test_animal_string_representation_uses_instance_name():
    assert str(Dog("Woofy Goldberg")) == "Dog named Woofy Goldberg"
    assert str(Cat("Chairman Meow")) == "Cat named Chairman Meow"
    assert str(Cat()) == "Cat"


def test_lyric_uses_the_class_name_not_the_instance_name():
    assert Cat("Chairman Meow").lyric() == 'Cat goes "meow"'


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

    assert wdtfs([animal_type() for animal_type in FULL_CAST]) == expected


def test_wdtfs_works_with_a_parrot_that_has_learned_something():
    parrot = Parrot()
    parrot.hear("hello")

    assert wdtfs([parrot]).splitlines()[0] == 'Parrot goes "hello"'
