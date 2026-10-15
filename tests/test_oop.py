from pathlib import Path

import pytest

from pyproblems.oop import (
    REFRAIN,
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
    Robot,
    Seal,
    UnknownSoundError,
    cover,
    lyric,
    sing,
    wdtfs,
)

FULL_CAST = [Dog, Cat, Bird, Mouse, Cow, Frog, Elephant, Duck, Fish, Seal]
FIXTURES = Path(__file__).parent / "fixtures"


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


def test_animals_do_not_write_song_lyrics():
    assert not hasattr(Animal, "lyric")


def test_lyric_asks_the_animal_for_its_sound():
    assert lyric(Duck("Quackers")) == 'Duck goes "quack"'
    assert lyric(Dog()) == 'Dog goes "woof"'


def test_lyric_uses_the_class_name_not_the_instance_name():
    assert lyric(Cat("Chairman Meow")) == 'Cat goes "meow"'


def test_fox_is_an_animal_whose_sound_is_unknown():
    fox = Fox()

    assert isinstance(fox, Animal)
    with pytest.raises(UnknownSoundError):
        fox.speak()


def test_lyric_does_not_hide_an_unknown_sound():
    with pytest.raises(UnknownSoundError):
        lyric(Fox())


def test_sing_gives_one_line_per_animal():
    assert sing([Dog(), Duck()]) == 'Dog goes "woof"\nDuck goes "quack"\n'


def test_sing_turns_an_unknown_sound_into_a_question():
    assert sing([Cat(), Fox()]) == (
        'Cat goes "meow"\n'
        "But there's one sound\n"
        "That no one knows\n"
        "What does the fox say?\n"
        f'"{REFRAIN}"\n'
    )


def test_sing_accepts_a_different_guess():
    assert sing([Fox()], guess="Wa-pa-pa-pa-pa-pa-pow!").endswith(
        '"Wa-pa-pa-pa-pa-pa-pow!"\n'
    )


def test_sing_names_whichever_animal_is_unknown():
    class Yeti(Animal):
        def speak(self) -> str:
            raise UnknownSoundError

    assert "What does the yeti say?" in sing([Yeti()])


def test_sing_does_not_swallow_other_errors():
    with pytest.raises(NotImplementedError):
        sing([Animal()])


def test_wdtfs_matches_short_snapshot():
    expected = (FIXTURES / "animal_song_short.txt").read_text(encoding="utf-8")

    assert wdtfs([Bird(), Cat(), Mouse()]) == expected


def test_wdtfs_matches_full_snapshot():
    expected = (FIXTURES / "animal_song_full.txt").read_text(encoding="utf-8")

    assert wdtfs([animal_type() for animal_type in FULL_CAST]) == expected


def test_parrot_tweets_until_it_hears_something():
    parrot = Parrot("Polly Morphism")

    assert isinstance(parrot, Bird)
    assert parrot.speak() == "tweet"
    assert lyric(parrot) == 'Parrot goes "tweet"'


def test_parrot_repeats_the_last_sound_it_heard():
    parrot = Parrot()

    parrot.hear("woof")
    parrot.hear("hello")

    assert parrot.speak() == "hello"
    assert lyric(parrot) == 'Parrot goes "hello"'


def test_parrots_remember_independently():
    polly, percy = Parrot(), Parrot()

    polly.hear("hello")

    assert percy.speak() == "tweet"


def test_parrot_keeps_name_handling_from_animal():
    assert str(Parrot("Polly Morphism")) == "Parrot named Polly Morphism"


def test_parrot_learns_by_listening_to_another_animal():
    parrot = Parrot()

    parrot.listen_to(Cow())

    assert parrot.speak() == "moo"


def test_parrot_can_listen_to_another_parrot():
    polly, percy = Parrot(), Parrot()
    polly.hear("hello")

    percy.listen_to(polly)

    assert percy.speak() == "hello"


def test_parrot_does_not_learn_from_an_unknown_sound():
    parrot = Parrot()
    parrot.hear("hello")

    with pytest.raises(UnknownSoundError):
        parrot.listen_to(Fox())

    assert parrot.speak() == "hello"


def test_parrot_ends_the_song_with_its_answer_to_the_fox_mystery():
    parrot = Parrot("Polly Morphism")
    parrot.hear(REFRAIN)

    song = sing([Dog(), Fox(), parrot])

    assert song.splitlines()[-1] == f'Parrot goes "{REFRAIN}"'


def test_robot_is_not_an_animal():
    assert not isinstance(Robot("Marvin the Paranoid Android"), Animal)


def test_robot_beeps_until_it_is_programmed():
    robot = Robot("Marvin the Paranoid Android")

    assert robot.name == "Marvin the Paranoid Android"
    assert robot.speak() == "Beep boop"


def test_robot_speaks_its_program_in_order_then_beeps():
    robot = Robot("Marvin the Paranoid Android")
    robot.program_speech(["Here I am", "Brain the size of a planet"])

    assert robot.speak() == "Here I am"
    assert robot.speak() == "Brain the size of a planet"
    assert robot.speak() == "Beep boop"
    assert robot.speak() == "Beep boop"


def test_reprogramming_a_robot_starts_the_sequence_again():
    robot = Robot("Marvin the Paranoid Android")
    robot.program_speech(["one", "two"])
    robot.speak()

    robot.program_speech(["alpha", "beta"])

    assert [robot.speak(), robot.speak()] == ["alpha", "beta"]


def test_reprogramming_an_exhausted_robot_makes_it_speak_again():
    robot = Robot("Marvin the Paranoid Android")
    robot.program_speech(["one"])
    robot.speak()
    robot.speak()

    robot.program_speech(["two"])

    assert robot.speak() == "two"


def test_robots_keep_independent_programs_and_positions():
    marvin, robbie = Robot("Marvin"), Robot("Robbie")
    marvin.program_speech(["one", "two"])
    robbie.program_speech(["alpha", "beta"])

    marvin.speak()

    assert robbie.speak() == "alpha"
    assert marvin.speak() == "two"


def test_robot_program_is_not_changed_by_later_edits_to_the_list():
    lines = ["one", "two"]
    robot = Robot("Marvin")
    robot.program_speech(lines)

    lines.append("three")
    lines[0] = "changed"

    assert [robot.speak(), robot.speak(), robot.speak()] == ["one", "two", "Beep boop"]


def test_robot_program_can_be_any_iterable():
    robot = Robot("Marvin")
    robot.program_speech(line for line in ["one", "two"])

    assert [robot.speak(), robot.speak()] == ["one", "two"]


def test_lyric_works_for_a_robot_too():
    robot = Robot("Marvin")
    robot.program_speech(["Hello"])

    assert lyric(robot) == 'Robot goes "Hello"'


def test_parrot_can_learn_from_a_robot():
    robot = Robot("Marvin")
    robot.program_speech(["Life, don't talk to me about life"])
    parrot = Parrot()

    parrot.listen_to(robot)

    assert parrot.speak() == "Life, don't talk to me about life"
    assert robot.speak() == "Beep boop"


def test_a_programmed_robot_can_stand_in_for_a_duck():
    robo_duck = Robot("RoboDuck")
    robo_duck.program_speech(["quack"])

    assert not isinstance(robo_duck, Duck)
    assert lyric(robo_duck) == 'Robot goes "quack"'


def test_lyric_and_sing_work_for_any_object_that_can_speak():
    class Doorbell:
        def speak(self) -> str:
            return "ding dong"

    assert lyric(Doorbell()) == 'Doorbell goes "ding dong"'
    assert sing([Doorbell(), Dog()]) == 'Doorbell goes "ding dong"\nDog goes "woof"\n'


def test_cover_replaces_every_animal_with_the_robot():
    robot = Robot("Marvin the Paranoid Android")

    assert cover([Bird(), Cat(), Mouse()], robot) == (
        'Robot goes "tweet"\n'
        'Robot goes "meow"\n'
        'Robot goes "squeek"\n'
        "But there's one sound\n"
        "That no one knows\n"
        "What does the fox say?\n"
        '"Beep boop"\n'
    )


def test_cover_sings_the_whole_song_in_the_same_order():
    expected = (FIXTURES / "animal_song_full.txt").read_text(encoding="utf-8")
    band = [animal_type() for animal_type in FULL_CAST]

    covered = cover(band, Robot("Marvin")).splitlines()

    sounds = [line.split('"')[1] for line in covered[:10]]
    assert sounds == [animal.speak() for animal in band]
    assert len(covered) == len(expected.splitlines())


def test_cover_uses_what_each_animal_says_now():
    parrot = Parrot()
    parrot.hear("hello")

    assert cover([parrot, Dog()], Robot("Marvin")).splitlines()[:2] == [
        'Robot goes "hello"',
        'Robot goes "woof"',
    ]


def test_cover_replaces_the_robots_earlier_program():
    robot = Robot("Marvin")
    robot.program_speech(["old", "program", "here"])

    assert cover([Cow()], robot).splitlines()[0] == 'Robot goes "moo"'


def test_cover_can_be_repeated_with_the_same_robot():
    robot = Robot("Marvin")

    assert cover([Dog(), Cat()], robot) == cover([Dog(), Cat()], robot)


def test_cover_accepts_any_iterable_of_animals():
    covered = cover((animal for animal in [Dog(), Cat()]), Robot("Marvin"))

    assert covered.splitlines()[:2] == ['Robot goes "woof"', 'Robot goes "meow"']


def test_cover_with_an_empty_band_is_just_the_mystery_verse():
    assert cover([], Robot("Marvin")) == sing([Fox()], guess="Beep boop")


def test_cover_does_not_change_the_animals():
    parrot = Parrot()
    parrot.hear("hello")

    cover([parrot], Robot("Marvin"))

    assert parrot.speak() == "hello"
