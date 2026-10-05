from pathlib import Path

import pytest

from pyproblems.alignment import (
    needleman_wunsch_alignment,
    needleman_wunsch_score,
)

FIXTURES = Path(__file__).parent / "fixtures"


def alignment_score(alignment: tuple[str, str]) -> int:
    return sum(
        1 if left == right else -1 for left, right in zip(*alignment, strict=True)
    )


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [("ATAGTCACAT", "AAATCGACAAA", 2)],
)
def test_needleman_wunsch_score(first, second, expected):
    assert needleman_wunsch_score(first, second) == expected


def test_dna_fixture_has_expected_optimal_score():
    first, second = (FIXTURES / "dna.txt").read_text().splitlines()
    assert needleman_wunsch_score(first, second) == 100


@pytest.mark.parametrize(
    "sequences",
    [("ATAGTCACAT", "AAATCGACAAA")],
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
