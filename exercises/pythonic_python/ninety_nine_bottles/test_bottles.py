from pathlib import Path

from exercises.pythonic_python.ninety_nine_bottles.bottles import (
    bottles,
    verse,
    verses,
)

FIXTURE = Path(__file__).parent / "data" / "99_bottles.txt"


def test_first_verse():
    assert verse(99) == (
        "99 bottles of beer on the wall, 99 bottles of beer.\n"
        "Take one down and pass it around, 98 bottles of beer on the wall.\n"
    )


def test_another_verse():
    assert verse(98) == (
        "98 bottles of beer on the wall, 98 bottles of beer.\n"
        "Take one down and pass it around, 97 bottles of beer on the wall.\n"
    )


def test_a_couple_of_verses_are_separated_by_one_blank_line():
    assert verses(99, 98) == verse(99) + "\n" + verse(98)


def test_final_verses_use_singular_and_zero_forms():
    assert verses(2, 0) == (
        "2 bottles of beer on the wall, 2 bottles of beer.\n"
        "Take one down and pass it around, 1 bottle of beer on the wall.\n"
        "\n"
        "1 bottle of beer on the wall, 1 bottle of beer.\n"
        "Take it down and pass it around, no more bottles of beer on the wall.\n"
        "\n"
        "No more bottles of beer on the wall, no more bottles of beer.\n"
        "Go to the store and buy some more, 99 bottles of beer on the wall.\n"
    )


def test_complete_song_matches_fixture():
    assert bottles() == FIXTURE.read_text(encoding="utf-8")
