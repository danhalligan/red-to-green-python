"""Integrity checks for the shared English word list."""

from exercises._shared.loaders import load_words


def test_words_are_lowercase_and_include_word_ladder_examples():
    words = load_words()

    assert {"play", "game", "snap", "pool"}.issubset(words)
    assert "PLAY" not in words
    assert len(words) == 39_083
