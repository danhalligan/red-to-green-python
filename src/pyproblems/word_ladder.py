"""Word-ladder exercises."""


def word_ladder(start: str, target: str, words: set[str]) -> list[str] | None:
    """Return a shortest valid word route, or None if no route exists.

    Each step changes exactly one letter and every word on the route must be in
    `words`. `start` and `target` must be lowercase words of the same length
    and both must appear in `words`.

    The route includes both endpoints, so the number of moves is one less than
    its length. If `start` equals `target` the route is just `[start]`.
    """
    raise NotImplementedError


def longest_shortest_ladder(words: set[str], length: int = 4) -> list[str]:
    """Return a shortest route between the two `length`-letter words furthest apart.

    Of all pairs of words in `words` with exactly `length` letters that are
    joined by a ladder, find the pair whose shortest ladder needs the most
    moves, and return one shortest route between them, including both
    endpoints. Words of other lengths are ignored. If there is only one word
    of that length, the route is just that word.

    Raise ValueError if `words` contains no word of that length.
    """
    raise NotImplementedError
