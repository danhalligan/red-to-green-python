from pathlib import Path

import pytest

from pyproblems.alignment import (
    all_alignments,
    needleman_wunsch_alignment,
    needleman_wunsch_score,
    score_alignment,
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


@pytest.mark.parametrize(
    ("aligned_first", "aligned_second", "expected"),
    [
        ("ATAGTC-AC-AT", "AAA-TCGACAAA", 2),
        ("", "", 0),
        ("A", "A", 1),
        ("A", "C", -1),
        ("A-", "-A", -2),
    ],
)
def test_score_alignment_scores_matches_mismatches_and_gaps(
    aligned_first, aligned_second, expected
):
    assert score_alignment(aligned_first, aligned_second) == expected


@pytest.mark.parametrize(
    ("aligned_first", "aligned_second"),
    [("AC", "A"), ("A-C", "A-C"), ("A-", "A-")],
)
def test_score_alignment_rejects_invalid_alignments(aligned_first, aligned_second):
    with pytest.raises(ValueError):
        score_alignment(aligned_first, aligned_second)


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ("", "", 1),
        ("A", "", 1),
        ("", "AC", 1),
        ("A", "C", 3),
        ("AC", "C", 5),
        ("AC", "GT", 13),
        ("ACG", "TGA", 63),
        ("ACGT", "TGAC", 321),
        ("ACGTA", "TGACT", 1683),
    ],
)
def test_all_alignments_yields_every_alignment_exactly_once(first, second, expected):
    alignments = list(all_alignments(first, second))

    assert len(alignments) == expected
    assert len(set(alignments)) == expected


def test_all_alignments_are_valid_alignments():
    first, second = "GATTA", "GCAT"

    for aligned_first, aligned_second in all_alignments(first, second):
        assert len(aligned_first) == len(aligned_second)
        assert aligned_first.replace("-", "") == first
        assert aligned_second.replace("-", "") == second
        alignment_score((aligned_first, aligned_second))  # rejects gap-gap columns


@pytest.mark.parametrize(
    ("first", "second", "expected"),
    [
        ("", "", 0),
        ("", "AC", -2),
        ("A", "A", 1),
        ("A", "C", -1),
        ("A", "AA", 0),
        ("ACGT", "AGT", 2),
    ],
)
def test_brute_force_finds_the_best_score(first, second, expected):
    scores = (score_alignment(*pair) for pair in all_alignments(first, second))

    assert max(scores) == expected


@pytest.mark.parametrize(
    ("first", "second"),
    [
        ("ATAGT", "AAATC"),
        ("GATTACA", "GCATGC"),
        ("", "ACG"),
        ("AAAA", "TTTT"),
        ("ACGTAC", "ACGTAC"),
    ],
)
def test_needleman_wunsch_matches_brute_force_on_short_sequences(first, second):
    scores = (score_alignment(*pair) for pair in all_alignments(first, second))

    assert needleman_wunsch_score(first, second) == max(scores)
