"""Stochastic simulation exercises inspired by Dawkins' weasel model."""

from dataclasses import dataclass

from numpy.random import Generator

WEASEL_TARGET = "METHINKS IT IS LIKE A WEASEL"
WEASEL_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "


@dataclass(frozen=True)
class EvolutionResult:
    """Best candidate and match history from a weasel simulation."""

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
    """Independently mutate message characters using the supplied generator."""
    raise NotImplementedError


def evolve_weasel(
    *,
    target: str = WEASEL_TARGET,
    population_size: int = 10,
    mutation_rate: float = 0.01,
    rng: Generator,
    max_generations: int = 100_000,
) -> EvolutionResult:
    """Select the best mutated candidate until target or generation limit."""
    raise NotImplementedError
