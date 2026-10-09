"""Stochastic simulation exercises inspired by Dawkins' weasel model."""

from dataclasses import dataclass

from numpy.random import Generator

WEASEL_TARGET = "METHINKS IT IS LIKE A WEASEL"
WEASEL_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "


@dataclass(frozen=True)
class EvolutionResult:
    """Best candidate and match history from a weasel simulation.

    `match_history` holds the best score so far, starting with the initial
    random phrase, so it has `generations + 1` entries.
    """

    candidate: str
    generations: int
    match_history: tuple[int, ...]


def matching_characters(candidate: str, target: str = WEASEL_TARGET) -> int:
    """Count positions matching between equal-length strings."""
    raise NotImplementedError


def mutate_message(
    message: str,
    *,
    mutation_rate: float,
    rng: Generator,
) -> str:
    """Independently mutate message characters using the supplied generator.

    Each character is left unchanged with probability `1 - mutation_rate`;
    otherwise it becomes one of the *other* symbols in `WEASEL_ALPHABET`.
    Raise ValueError if `mutation_rate` is outside 0 to 1.
    """
    raise NotImplementedError


def evolve_weasel(
    *,
    target: str = WEASEL_TARGET,
    population_size: int = 10,
    mutation_rate: float = 0.01,
    rng: Generator,
    max_generations: int = 100_000,
) -> EvolutionResult:
    """Select the best mutated candidate until target or generation limit.

    Start from a uniformly random phrase over `WEASEL_ALPHABET`. Each
    generation, make `population_size` mutated copies of the current parent,
    score them with `matching_characters`, and choose a highest-scoring copy as
    the next parent, breaking ties at random. Retain the best candidate seen so
    far, so the best score never decreases. Use only the injected `rng` so runs
    are reproducible.

    Stop when the target is matched or after `max_generations`. Return an
    `EvolutionResult` with the best candidate, the number of generations run and
    the match history.
    """
    raise NotImplementedError
