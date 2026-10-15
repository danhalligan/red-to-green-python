"""Rugby union scoring exercises: "...Try, try again"."""


def count_scoring_sequences(points: int) -> int:
    """Return how many ordered sequences of scoring events total `points`.

    The events are a penalty (3 points), a drop goal (3), a try (5) and a
    conversion (2). A conversion can only happen immediately after a try.
    Order matters, and a penalty and a drop goal count as different events.
    Zero points has exactly one sequence: no events at all.

    Raise ValueError if `points` is negative.
    """
    raise NotImplementedError


def smallest_score_with_more_sequences_than(count: int) -> int:
    """Return the smallest score reachable by more than `count` sequences.

    Sequences are counted as in `count_scoring_sequences`. For example, 3 is
    the smallest score with more than one sequence (a penalty or a drop goal).
    """
    raise NotImplementedError


def count_scoring_combinations(points: int) -> int:
    """Return how many different tallies of events total `points`, ignoring order.

    A tally records how many penalties, drop goals, tries and conversions there
    were. Each conversion still needs its own try, so no tally has more
    conversions than tries. Penalties and drop goals are still counted separately.

    Raise ValueError if `points` is negative.
    """
    raise NotImplementedError
