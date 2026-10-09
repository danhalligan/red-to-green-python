"""Breadth-first word-ladder exercise."""


def word_ladder(start: str, target: str, words: set[str]) -> list[str] | None:
    """Return a shortest valid word route, or None if no route exists.

    Each step changes exactly one letter and every word on the route must be in
    `words`. `start` and `target` must be lowercase words of the same length
    and both must appear in `words`.

    The route includes both endpoints, so the number of moves is one less than
    its length. If `start` equals `target` the route is just `[start]`.
    """
    raise NotImplementedError
