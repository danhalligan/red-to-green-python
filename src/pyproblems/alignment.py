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


def _alignment_table(first: str, second: str) -> list[list[int]]:
    """Build the score table shared by both Needleman-Wunsch exercises.

    Row i represents first[:i]; column j represents second[:j]. The extra
    row and column represent empty prefixes. Their scores are just gap costs.
    Work left to right, top to bottom so each cell's neighbours are ready.

    Complete the inner loop: consider the diagonal, above, and left cells,
    add the score of each possible final alignment column, then store the
    best candidate in table[row][column]. Sequence indices are one less than
    table indices: compare first[row - 1] with second[column - 1].
    """
    table = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]

    for row in range(1, len(first) + 1):
        table[row][0] = -row
    for column in range(1, len(second) + 1):
        table[0][column] = -column

    for row in range(1, len(first) + 1):
        for column in range(1, len(second) + 1):
            raise NotImplementedError(
                "TODO: score each move and store the best score "
                f"in table[{row}][{column}]"
            )

    return table


def needleman_wunsch_score(first: str, second: str) -> int:
    """Return the optimal global alignment score using +1/-1 scoring.

    A match scores +1; a mismatch or a character aligned with a gap scores -1.
    Fill a dynamic-programming table `D[i][j]` holding the best score for
    aligning the first i characters of `first` with the first j of `second`.
    The answer is the final cell. Complete the scoring TODO in
    `_alignment_table`; this function then needs no further changes.
    """
    table = _alignment_table(first, second)
    return table[-1][-1]


def needleman_wunsch_alignment(first: str, second: str) -> tuple[str, str]:
    """Return one optimal global alignment, inserting hyphens for gaps.

    Use the same table as `needleman_wunsch_score`, then trace back from the
    final cell to recover the aligned strings. Both returned strings have equal
    length, and removing the hyphens must recover the original inputs. Ties can
    give different but equally optimal alignments; any one is acceptable.

    Complete `_alignment_table` first, then the traceback TODO below. A move
    must explain the current score: neighbour score plus column score equals
    the current cell. Diagonal consumes both characters; up consumes only
    `first` (gap in `second`); left consumes only `second` (gap in `first`).
    Append the chosen column and decrease the corresponding indices. You are
    building the alignment backwards, so reverse both lists at the end.
    """
    table = _alignment_table(first, second)
    row, column = len(first), len(second)
    aligned_first: list[str] = []
    aligned_second: list[str] = []

    while row > 0 or column > 0:
        if row == 0:
            aligned_first.append("-")
            aligned_second.append(second[column - 1])
            column -= 1
        elif column == 0:
            aligned_first.append(first[row - 1])
            aligned_second.append("-")
            row -= 1
        else:
            raise NotImplementedError(
                f"TODO: choose a move explaining score {table[row][column]} "
                f"at table[{row}][{column}], "
                "append its alignment column, and update row and/or column"
            )

    return "".join(reversed(aligned_first)), "".join(reversed(aligned_second))
