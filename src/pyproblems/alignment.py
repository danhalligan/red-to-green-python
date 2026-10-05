"""Dynamic-programming sequence-alignment exercises."""


def needleman_wunsch_score(first: str, second: str) -> int:
    """Return the optimal global alignment score using +1/-1 scoring."""
    raise NotImplementedError


def needleman_wunsch_alignment(first: str, second: str) -> tuple[str, str]:
    """Return one optimal global alignment, inserting hyphens for gaps."""
    raise NotImplementedError
