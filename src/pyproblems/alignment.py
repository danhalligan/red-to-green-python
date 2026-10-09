"""Sequence-alignment exercises: brute force, then dynamic programming."""

from collections.abc import Iterator


def score_alignment(aligned_first: str, aligned_second: str) -> int:
    """Score an existing alignment: +1 per match, -1 per mismatch or gap.

    The two strings must have equal length, with `-` marking gaps. Raise
    ValueError if the lengths differ or if any column has a gap in both rows,
    which is not a valid alignment column.
    """
    raise NotImplementedError


def all_alignments(first: str, second: str) -> Iterator[tuple[str, str]]:
    """Yield every global alignment of two sequences, each exactly once.

    An alignment is a pair of equal-length strings that give `first` and
    `second` back when the `-` gap characters are removed, with no column that
    is a gap in both rows. The order of the alignments does not matter.

    The number of alignments grows very quickly with length (over eight million
    for two sequences of ten characters), so use this only for short inputs.
    """
    raise NotImplementedError


def needleman_wunsch_score(first: str, second: str) -> int:
    """Return the optimal global alignment score using +1/-1 scoring.

    A match scores +1; a mismatch or a character aligned with a gap scores -1.
    Fill a dynamic-programming table `D[i][j]` holding the best score for
    aligning the first i characters of `first` with the first j of `second`.
    The answer is the final cell.
    """
    raise NotImplementedError


def needleman_wunsch_alignment(first: str, second: str) -> tuple[str, str]:
    """Return one optimal global alignment, inserting hyphens for gaps.

    Use the same table as `needleman_wunsch_score`, then trace back from the
    final cell to recover the aligned strings. Both returned strings have equal
    length, and removing the hyphens must recover the original inputs. Ties can
    give different but equally optimal alignments; any one is acceptable.
    """
    raise NotImplementedError
