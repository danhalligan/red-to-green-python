from pathlib import Path

import pytest

from pyproblems.alignment import (
    needleman_wunsch_alignment,
    needleman_wunsch_score,
)

FIXTURES = Path(__file__).parent / "fixtures"


def alignment_score(alignment: tuple[str, str]) -> int:
    assert all(
        not (left == right == "-") for left, right in zip(*alignment, strict=True)
    ), "gap-gap columns are not valid alignment operations"
    return sum(
        1 if left == right else -1 for left, right in zip(*alignment, strict=True)
    )


def test_alignment_score_helper_rejects_gap_gap_columns():
    padded = ("ATAGTCACAT----", "AAATCGACAAA---")
    with pytest.raises(AssertionError, match="gap-gap"):
        alignment_score(padded)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ("ATAGTCACAT", "AAATCGACAAA", 2),
        ("", "", 0),
        ("", "AC", -2),
        ("A", "A", 1),
        ("A", "C", -1),
        ("A", "AA", 0),
    ],
)
def test_needleman_wunsch_score(first, second, expected):
    assert needleman_wunsch_score(first, second) == expected


def test_dna_fixture_has_expected_optimal_score():
    first, second = (FIXTURES / "dna.txt").read_text().splitlines()
    assert needleman_wunsch_score(first, second) == 100


@pytest.mark.parametrize(
    "sequences",
    [
        ("ATAGTCACAT", "AAATCGACAAA"),
        ("", ""),
        ("", "AC"),
        ("A", "A"),
        ("A", "C"),
        ("A", "AA"),
        ("GATTACAGATTACA", "GCATGCUGCATGCU"),
    ],
)
def test_alignment_preserves_sequences_and_achieves_optimal_score(sequences):
    first, second = sequences
    aligned_first, aligned_second = needleman_wunsch_alignment(first, second)

    assert len(aligned_first) == len(aligned_second)
    assert aligned_first.replace("-", "") == first
    assert aligned_second.replace("-", "") == second
    assert alignment_score((aligned_first, aligned_second)) == (
        needleman_wunsch_score(first, second)
    )
