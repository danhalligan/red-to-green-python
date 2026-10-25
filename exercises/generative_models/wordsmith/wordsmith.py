"""A tiny character-level language model that invents words."""

from collections import Counter
from collections.abc import Iterable

START = "^"
END = "$"


def train_model(
    words: Iterable[str],
    context_size: int = 1,
) -> dict[str, Counter[str]]:
    """Learn next-character frequencies from `words`.

    Return a dictionary from a context (the previous `context_size` characters)
    to a `Counter` of the characters that followed it, counting every
    occurrence. Pad each word with `context_size` copies of `START` at the front
    and one `END` at the back, so the model also learns how words begin and end.
    For `cat` and a context size of 1, the transitions are `^ -> c`, `c -> a`,
    `a -> t` and `t -> $`; with a context size of 2 they are `^^ -> c`, `^c ->
    a`, `ca -> t` and `at -> $`.

    Convert each word to lowercase and skip any that is empty or contains
    anything but the letters `a` to `z`. Count every entry of `words`
    separately, and iterate over `sorted(words)` so the result does not depend
    on set order. Return an empty dictionary if no word is usable. Raise
    ValueError if `context_size` is less than 1.
    """
    raise NotImplementedError


def generate_word(
    model: dict[str, Counter[str]],
    max_length: int = 20,
) -> str | None:
    """Sample a word from a model made by `train_model`.

    Start from a context of `START` characters (as many as the model's context
    size, which is the length of its keys). Repeatedly sample the next
    character, with probability proportional to its count, and slide the context
    along, until `END` is sampled. Return the letters generated, without any
    markers.

    Use the `random` module, and sample from the characters in sorted order, so
    that `random.seed` gives the same word whatever order the model's counts
    were added in. Return None for an unsuccessful attempt: if the word would
    have more than `max_length` letters, if a context has no recorded
    continuation, or if the word would be empty. Raise ValueError if `model` is
    empty or `max_length` is less than 1.
    """
    raise NotImplementedError
