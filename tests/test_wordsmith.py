import random
from collections import Counter

import pytest

from pyproblems.data import load_words
from pyproblems.wordsmith import END, START, generate_word, train_model

TINY = {"cat", "car", "dog"}


def draw(model, seed, count, **options):
    rng = random.Random(seed)
    return [generate_word(model, rng, **options) for _ in range(count)]


def test_train_model_counts_start_of_word_transitions():
    model = train_model(TINY)

    assert model[START] == Counter({"c": 2, "d": 1})


def test_train_model_counts_character_pairs_inside_words():
    model = train_model(TINY)

    assert model["c"] == Counter({"a": 2})
    assert model["a"] == Counter({"t": 1, "r": 1})
    assert model["d"] == Counter({"o": 1})
    assert model["o"] == Counter({"g": 1})


def test_train_model_counts_end_of_word_transitions():
    model = train_model(TINY)

    assert model["t"] == Counter({END: 1})
    assert model["r"] == Counter({END: 1})
    assert model["g"] == Counter({END: 1})


def test_train_model_learns_nothing_beyond_the_training_words():
    model = train_model(TINY)

    assert set(model) == {START, "c", "a", "t", "r", "d", "o", "g"}


def test_train_model_accumulates_repeated_transitions():
    model = train_model({"banana"})

    assert model[START] == Counter({"b": 1})
    assert model["b"] == Counter({"a": 1})
    assert model["a"] == Counter({"n": 2, END: 1})
    assert model["n"] == Counter({"a": 2})


def test_train_model_counts_every_word_independently():
    together = train_model({"cat", "cot", "dog"})

    assert together[START] == Counter({"c": 2, "d": 1})
    assert together["a"] == Counter({"t": 1})
    assert together["o"] == Counter({"t": 1, "g": 1})
    assert together["t"] == Counter({END: 2})


def test_train_model_does_not_depend_on_the_order_of_the_words():
    words = ["tea", "ten", "tan", "ant", "net"]

    assert train_model(words) == train_model(reversed(words))
    assert train_model(words) == train_model(set(words))


def test_train_model_lowercases_words():
    assert train_model({"Cat"}) == train_model({"cat"})


@pytest.mark.parametrize(
    "unsuitable", ["it's", "café", "x-ray", "r2d2", "two words", ""]
)
def test_train_model_skips_unsuitable_words(unsuitable):
    assert train_model({"cat", unsuitable}) == train_model({"cat"})


def test_train_model_with_no_usable_words_is_empty():
    assert train_model(set()) == {}
    assert train_model({"it's", ""}) == {}


@pytest.mark.parametrize("context_size", [0, -1])
def test_train_model_rejects_a_context_size_below_one(context_size):
    with pytest.raises(ValueError):
        train_model(TINY, context_size)


def test_generate_word_follows_only_transitions_the_model_has_seen():
    words = {"cat", "car", "dog", "cargo", "tag"}
    model = train_model(words)

    for word in draw(model, seed=1, count=200):
        assert word is not None
        padded = START + word + END
        for before, after in zip(padded, padded[1:], strict=False):
            assert after in model[before]


def test_generate_word_leaves_out_the_boundary_markers():
    model = train_model(TINY)

    for word in draw(model, seed=2, count=100):
        assert word
        assert word.isalpha()
        assert START not in word
        assert END not in word


def test_a_model_with_one_continuation_each_gives_a_predictable_word():
    model = train_model({"wizard"})

    assert draw(model, seed=3, count=5) == ["wizard"] * 5


def test_generate_word_stops_at_the_end_marker():
    model = {START: Counter({"a": 1}), "a": Counter({"b": 1}), "b": Counter({END: 1})}

    assert generate_word(model, random.Random(0)) == "ab"


def test_generate_word_respects_the_weights():
    model = {
        START: Counter({"a": 1_000, "b": 1}),
        "a": Counter({END: 1}),
        "b": Counter({END: 1}),
    }

    words = draw(model, seed=4, count=300)

    assert words.count("a") > 280
    assert words.count("b") < 20


def test_generate_word_can_choose_rare_transitions():
    model = {
        START: Counter({"a": 1, "b": 1}),
        "a": Counter({END: 1}),
        "b": Counter({END: 1}),
    }

    assert set(draw(model, seed=5, count=100)) == {"a", "b"}


def test_generate_word_gives_up_on_words_that_are_too_long():
    loop = {START: Counter({"a": 1}), "a": Counter({"a": 1})}

    assert generate_word(loop, random.Random(0), max_length=10) is None


def test_max_length_limits_the_letters_in_a_word():
    model = train_model({"abc"})

    assert generate_word(model, random.Random(0), max_length=3) == "abc"
    assert generate_word(model, random.Random(0), max_length=2) is None


def test_generate_word_gives_up_when_a_context_has_no_continuation():
    model = {START: Counter({"a": 1})}

    assert generate_word(model, random.Random(0)) is None


def test_generate_word_never_returns_an_empty_word():
    model = {START: Counter({END: 1})}

    assert generate_word(model, random.Random(0)) is None


def test_generate_word_rejects_an_empty_model_and_a_bad_length():
    with pytest.raises(ValueError):
        generate_word({}, random.Random(0))
    with pytest.raises(ValueError):
        generate_word(train_model(TINY), random.Random(0), max_length=0)


def test_generation_is_reproducible_with_a_seeded_generator():
    model = train_model({"cat", "car", "cart", "dog", "dot", "cargo", "tag", "gator"})

    first = draw(model, seed=7, count=30)
    second = draw(model, seed=7, count=30)
    other = draw(model, seed=8, count=30)

    assert first == second
    assert first != other


def test_generation_does_not_depend_on_the_order_counts_were_added():
    forward = {
        START: Counter({"a": 1, "b": 2, "c": 3}),
        "a": Counter({END: 1}),
        "b": Counter({END: 1}),
        "c": Counter({END: 1}),
    }
    backward = {
        START: Counter({"c": 3, "b": 2, "a": 1}),
        "c": Counter({END: 1}),
        "b": Counter({END: 1}),
        "a": Counter({END: 1}),
    }

    assert draw(forward, seed=9, count=50) == draw(backward, seed=9, count=50)


def test_a_model_trained_on_the_packaged_words_invents_words():
    model = train_model(load_words())

    words = [word for word in draw(model, seed=10, count=100) if word]

    assert len(words) > 80
    assert all(word.isalpha() and word.islower() and len(word) <= 20 for word in words)


def test_trigram_model_uses_two_character_contexts():
    model = train_model(TINY, context_size=2)

    assert set(model) == {"^^", "^c", "^d", "ca", "at", "ar", "do", "og"}
    assert all(len(context) == 2 for context in model)


def test_trigram_model_counts_contexts_and_continuations():
    model = train_model(TINY, context_size=2)

    assert model["^^"] == Counter({"c": 2, "d": 1})
    assert model["^c"] == Counter({"a": 2})
    assert model["ca"] == Counter({"t": 1, "r": 1})
    assert model["at"] == Counter({END: 1})
    assert model["ar"] == Counter({END: 1})
    assert model["^d"] == Counter({"o": 1})
    assert model["do"] == Counter({"g": 1})
    assert model["og"] == Counter({END: 1})


def test_trigram_model_handles_words_shorter_than_the_context():
    model = train_model({"a"}, context_size=2)

    assert model == {"^^": Counter({"a": 1}), "^a": Counter({END: 1})}


def test_trigram_model_distinguishes_contexts_that_a_bigram_model_merges():
    model = train_model({"the", "tho", "tax"}, context_size=2)

    assert model["th"] == Counter({"e": 1, "o": 1})
    assert model["ta"] == Counter({"x": 1})


def test_trigram_generation_follows_the_two_character_context():
    # Each two-character context has exactly one continuation.
    model = {
        "^^": Counter({"a": 1}),
        "^a": Counter({"b": 1}),
        "ab": Counter({"c": 1}),
        "bc": Counter({END: 1}),
    }

    assert generate_word(model, random.Random(0)) == "abc"


def test_trigram_models_generate_from_the_packaged_words():
    model = train_model(load_words(), context_size=2)

    words = [word for word in draw(model, seed=11, count=100) if word]

    assert len(words) > 80
    assert all(word.isalpha() and word.islower() for word in words)
