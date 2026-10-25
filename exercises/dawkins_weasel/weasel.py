"""Stochastic simulation exercises inspired by Dawkins' weasel model."""

from collections.abc import Sequence

from numpy.random import Generator

WEASEL_TARGET = "METHINKS IT IS LIKE A WEASEL"
WEASEL_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ "


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
) -> dict[str, str | int | tuple[int, ...]]:
    """Select the best mutated candidate until target or generation limit.

    Start from a uniformly random phrase over `WEASEL_ALPHABET`. Each
    generation, make `population_size` mutated copies of the current parent,
    score them with `matching_characters`, and choose a highest-scoring copy as
    the next parent, breaking ties at random. Retain the best candidate seen so
    far, so the best score never decreases. Use only the injected `rng` so runs
    are reproducible.

    Stop when the target is matched or after `max_generations`. Return a
    dictionary with keys `candidate` (the best phrase, a str), `generations`
    (the number of generations run, an int), and `match_history` (a tuple of
    best scores, each an int). The history starts with the initial random
    phrase's score, so it has `generations + 1` entries.
    """
    raise NotImplementedError


def fittest(phrases: Sequence[str], target: str = WEASEL_TARGET) -> str:
    """Return a phrase with the most `matching_characters`; ties may go either way.

    Raise ValueError if `phrases` is empty.
    """
    raise NotImplementedError


def tournament_select(
    population: Sequence[str],
    target: str = WEASEL_TARGET,
    *,
    tournament_size: int = 3,
    rng: Generator,
) -> str:
    """Pick a parent: the `fittest` of `tournament_size` distinct random phrases.

    Raise ValueError if `tournament_size` is below 1 or above the population
    size. Use only the injected `rng`.
    """
    raise NotImplementedError


def one_point_crossover(parent_a: str, parent_b: str, *, rng: Generator) -> str:
    """Join a prefix of `parent_a` to the matching suffix of `parent_b`.

    The cut falls at a uniformly random position strictly inside the phrase, so
    the child always inherits at least one character from each parent. Raise
    ValueError if the parents differ in length or have fewer than two
    characters. Use only the injected `rng`.
    """
    raise NotImplementedError


def evolve_population(
    *,
    target: str = WEASEL_TARGET,
    population_size: int = 100,
    tournament_size: int = 3,
    mutation_rate: float = 0.02,
    crossover: bool = False,
    rng: Generator,
    max_generations: int = 10_000,
) -> dict[str, str | int | tuple[int, ...] | tuple[str, ...]]:
    """Evolve a population by tournament selection until target or limit.

    Start from `population_size` identical copies of one uniformly random
    phrase over `WEASEL_ALPHABET`, drawn first from `rng`, so every difference
    in the population arises by mutation (and crossover). Each generation
    replaces the whole population with `population_size` new offspring, each
    with one parent chosen by `tournament_select` from the old population, or
    two joined by `one_point_crossover` when `crossover` is true, and then
    mutated with `mutate_message`. Nothing is carried over unchanged, so the
    best score can fall.

    Stop when some phrase matches the target or after `max_generations`. Return
    a dictionary with keys `candidate` (the fittest phrase in the final
    population), `generations` (the number run), `match_history` (the best score
    in each population, starting with the initial one, so `generations + 1`
    entries) and `population` (the final phrases, a tuple of `population_size`
    strings). Use only the injected `rng` so runs are reproducible.
    """
    raise NotImplementedError
