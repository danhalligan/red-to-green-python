from pathlib import Path

import pytest

from exercises.noisy_animals.animals import (
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
FIXTURES = Path(__file__).parent / "data"
REFRAIN = "Ring-ding-ding-ding-dingeringeding!"


class Says:
    """A minimal speaker (not an Animal) with a fixed sound."""

    def __init__(self, sound: str) -> None:
        self.sound = sound

    def speak(self) -> str:
        return self.sound


def mystery_verse(animal: str, guess: str) -> list[str]:
    return [
        "But there's one sound",
        "That no one knows",
        f"What does the {animal} say?",
        f'"{guess}"',
    ]


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


def test_unknown_sound_error_has_a_default_message():
    assert str(UnknownSoundError()) == "Who Knows!"
    assert str(UnknownSoundError("Wa-pa-pa-pa-pa-pa-pow!")) == "Wa-pa-pa-pa-pa-pa-pow!"


def test_fox_is_an_animal_whose_sound_is_unknown():
    fox = Fox()

    assert isinstance(fox, Animal)
    with pytest.raises(UnknownSoundError):
        fox.speak()


def test_fox_offers_the_refrain_as_its_guess():
    with pytest.raises(UnknownSoundError) as error:
        Fox().speak()

    assert str(error.value) == REFRAIN


def test_lyric_does_not_hide_an_unknown_sound():
    with pytest.raises(UnknownSoundError):
        lyric(Fox())


def test_sing_gives_one_line_per_animal():
    assert sing([Dog(), Duck()]) == ['Dog goes "woof"', 'Duck goes "quack"']


def test_sing_turns_an_unknown_sound_into_a_question():
    assert sing([Cat(), Fox()]) == [
        'Cat goes "meow"',
        *mystery_verse("fox", REFRAIN),
    ]


def test_sing_uses_the_error_message_as_the_answer():
    class Wolf(Animal):
        def speak(self) -> str:
            raise UnknownSoundError("Wa-pa-pa-pa-pa-pa-pow!")

    assert sing([Wolf()]) == mystery_verse("wolf", "Wa-pa-pa-pa-pa-pa-pow!")


def test_sing_names_whichever_animal_is_unknown():
    class Yeti(Animal):
        def speak(self) -> str:
            raise UnknownSoundError

    assert sing([Yeti()]) == mystery_verse("yeti", "Who Knows!")


def test_sing_does_not_swallow_other_errors():
    with pytest.raises(NotImplementedError):
        sing([Animal()])


def test_wdtfs_matches_short_snapshot():
    expected = (FIXTURES / "animal_song_short.txt").read_text(encoding="utf-8")

    assert wdtfs([Bird(), Cat(), Mouse()]) == expected.splitlines()


def test_wdtfs_matches_full_snapshot():
    expected = (FIXTURES / "animal_song_full.txt").read_text(encoding="utf-8")

    assert wdtfs([animal_type() for animal_type in FULL_CAST]) == expected.splitlines()


def test_parrot_tweets_until_it_hears_something():
    parrot = Parrot("Polly Morphism")

    assert isinstance(parrot, Bird)
    assert parrot.speak() == "tweet"
    assert lyric(parrot) == 'Parrot goes "tweet"'


def test_parrot_repeats_the_last_sound_it_heard():
    parrot = Parrot()

    parrot.listen_to(Dog())
    parrot.listen_to(Says("hello"))

    assert parrot.speak() == "hello"
    assert lyric(parrot) == 'Parrot goes "hello"'


def test_parrots_remember_independently():
    polly, percy = Parrot(), Parrot()

    polly.listen_to(Says("hello"))

    assert percy.speak() == "tweet"


def test_parrot_keeps_name_handling_from_animal():
    assert str(Parrot("Polly Morphism")) == "Parrot named Polly Morphism"


def test_parrot_learns_by_listening_to_another_animal():
    parrot = Parrot()

    parrot.listen_to(Cow())

    assert parrot.speak() == "moo"


def test_parrot_can_listen_to_another_parrot():
    polly, percy = Parrot(), Parrot()
    polly.listen_to(Says("hello"))

    percy.listen_to(polly)

    assert percy.speak() == "hello"


def test_parrot_does_not_learn_from_an_unknown_sound():
    parrot = Parrot()
    parrot.listen_to(Says("hello"))

    with pytest.raises(UnknownSoundError):
        parrot.listen_to(Fox())

    assert parrot.speak() == "hello"


def test_parrot_ends_the_song_with_its_answer_to_the_fox_mystery():
    parrot = Parrot("Polly Morphism")
    parrot.listen_to(Says(REFRAIN))

    song = sing([Dog(), Fox(), parrot])

    assert song[-1] == f'Parrot goes "{REFRAIN}"'


def test_robot_is_not_an_animal():
    assert not isinstance(Robot("Marvin the Paranoid Android"), Animal)


def test_robot_has_a_name():
    assert Robot("Marvin the Paranoid Android").name == "Marvin the Paranoid Android"


def test_robot_with_an_empty_memory_does_not_know_what_to_say():
    robot = Robot("Marvin the Paranoid Android")

    with pytest.raises(UnknownSoundError, match="Beep boop"):
        robot.speak()


def test_robot_speaks_what_it_learned_in_order_then_runs_out():
    robot = Robot("Marvin the Paranoid Android")
    robot.program_with(Says("Here I am"))
    robot.program_with(Says("Brain the size of a planet"))

    assert robot.speak() == "Here I am"
    assert robot.speak() == "Brain the size of a planet"
    for _ in range(2):
        with pytest.raises(UnknownSoundError, match="Beep boop"):
            robot.speak()


def test_robot_remembers_what_the_speaker_says_when_programmed():
    parrot = Parrot()
    parrot.listen_to(Says("hello"))
    robot = Robot("Marvin")

    robot.program_with(parrot)
    parrot.listen_to(Says("goodbye"))

    assert robot.speak() == "hello"


def test_programming_adds_to_what_the_robot_remembers():
    robot = Robot("Marvin")
    robot.program_with(Dog())
    robot.program_with(Cat())
    robot.speak()

    robot.program_with(Cow())

    assert [robot.speak(), robot.speak()] == ["meow", "moo"]


def test_an_exhausted_robot_can_be_programmed_again():
    robot = Robot("Marvin")
    robot.program_with(Dog())
    robot.speak()

    robot.program_with(Cat())

    assert robot.speak() == "meow"


def test_robots_keep_independent_memories():
    marvin, robbie = Robot("Marvin"), Robot("Robbie")
    marvin.program_with(Dog())
    marvin.program_with(Cat())
    robbie.program_with(Cow())

    marvin.speak()

    assert robbie.speak() == "moo"
    assert marvin.speak() == "meow"


def test_robot_cannot_learn_an_unknown_sound():
    robot = Robot("Marvin")

    with pytest.raises(UnknownSoundError):
        robot.program_with(Fox())

    with pytest.raises(UnknownSoundError, match="Beep boop"):
        robot.speak()


def test_lyric_works_for_a_robot_too():
    robot = Robot("Marvin")
    robot.program_with(Says("Hello"))

    assert lyric(robot) == 'Robot goes "Hello"'


def test_lyric_does_not_hide_an_empty_robots_unknown_sound():
    with pytest.raises(UnknownSoundError, match="Beep boop"):
        lyric(Robot("Marvin"))


def test_parrot_can_learn_from_a_robot():
    robot = Robot("Marvin")
    robot.program_with(Says("Life, don't talk to me about life"))
    parrot = Parrot()

    parrot.listen_to(robot)

    assert parrot.speak() == "Life, don't talk to me about life"
    with pytest.raises(UnknownSoundError, match="Beep boop"):
        robot.speak()


def test_a_programmed_robot_can_stand_in_for_a_duck():
    robo_duck = Robot("RoboDuck")
    robo_duck.program_with(Duck())

    assert not isinstance(robo_duck, Duck)
    assert lyric(robo_duck) == 'Robot goes "quack"'


def test_lyric_and_sing_work_for_any_object_that_can_speak():
    class Doorbell:
        def speak(self) -> str:
            return "ding dong"

    assert lyric(Doorbell()) == 'Doorbell goes "ding dong"'
    assert sing([Doorbell(), Dog()]) == ['Doorbell goes "ding dong"', 'Dog goes "woof"']


def test_robot_is_asked_only_once_per_line():
    robot = Robot("Marvin")
    robot.program_with(Dog())
    robot.program_with(Cat())

    assert sing([robot]) == ['Robot goes "woof"']
    assert robot.speak() == "meow"


def test_sing_gives_an_empty_robot_the_mystery_verse():
    assert sing([Robot("Marvin")]) == mystery_verse("robot", "Beep boop")


def test_cover_replaces_every_animal_with_the_robot():
    robot = Robot("Marvin the Paranoid Android")

    assert cover([Bird(), Cat(), Mouse()], robot) == [
        'Robot goes "tweet"',
        'Robot goes "meow"',
        'Robot goes "squeek"',
        "But there's one sound",
        "That no one knows",
        "What does the robot say?",
        '"Beep boop"',
    ]


def test_cover_sings_the_whole_song_in_the_same_order():
    expected = (FIXTURES / "animal_song_full.txt").read_text(encoding="utf-8")
    band = [animal_type() for animal_type in FULL_CAST]

    covered = cover(band, Robot("Marvin"))

    sounds = [line.split('"')[1] for line in covered[:10]]
    assert sounds == [animal.speak() for animal in band]
    assert len(covered) == len(expected.splitlines())


def test_cover_uses_what_each_animal_says_now():
    parrot = Parrot()
    parrot.listen_to(Says("hello"))

    assert cover([parrot, Dog()], Robot("Marvin"))[:2] == [
        'Robot goes "hello"',
        'Robot goes "woof"',
    ]


def test_cover_can_be_repeated_with_the_same_robot():
    robot = Robot("Marvin")

    assert cover([Dog(), Cat()], robot) == cover([Dog(), Cat()], robot)


def test_cover_with_an_empty_band_is_just_the_mystery_verse():
    assert cover([], Robot("Marvin")) == mystery_verse("robot", "Beep boop")


def test_cover_does_not_change_the_animals():
    parrot = Parrot()
    parrot.listen_to(Says("hello"))

    cover([parrot], Robot("Marvin"))

    assert parrot.speak() == "hello"
