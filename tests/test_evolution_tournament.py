"""Optional weasel extension: a mutation-only GA with tournament selection."""

from collections import Counter

import numpy as np
import pytest

from pyproblems.evolution import (
    WEASEL_ALPHABET,
    WEASEL_TARGET,
    evolve_population,
    fittest,
    matching_characters,
    tournament_select,
)

pytestmark = pytest.mark.advanced


def test_fittest_returns_a_phrase_with_the_most_matches():
    assert fittest(["BBBB", "AABB", "AAAB", "ABBB"], "AAAA") == "AAAB"
    assert fittest(["ABAB", "BABA"], "AAAA") in {"ABAB", "BABA"}
    assert fittest([WEASEL_TARGET, "A" * 28]) == WEASEL_TARGET


def test_fittest_rejects_an_empty_collection():
    with pytest.raises(ValueError):
        fittest([], "AAAA")


def test_tournament_returns_a_member_of_the_population():
    population = ["AAAA", "AAAB", "AABB", "BBBB"]
    rng = np.random.default_rng(0)

    for _ in range(20):
        assert tournament_select(population, "AAAA", rng=rng) in population


def test_tournament_over_the_whole_population_picks_the_fittest():
    population = ["BBBB", "AABB", "AAAB", "AAAA", "ABBB"]

    for seed in range(10):
        winner = tournament_select(
            population, "AAAA", tournament_size=5, rng=np.random.default_rng(seed)
        )
        assert winner == "AAAA"


def test_tournament_favours_fitter_individuals_but_not_exclusively():
    population = ["AAAA", "AAAB", "AABB", "BBBB"]
    rng = np.random.default_rng(1)

    wins = Counter(
        tournament_select(population, "AAAA", tournament_size=2, rng=rng)
        for _ in range(2000)
    )

    assert wins["AAAA"] > wins["AAAB"] > wins["AABB"] > wins["BBBB"]
    assert wins["AAAB"] > 0


@pytest.mark.parametrize("tournament_size", [0, 5])
def test_tournament_rejects_impossible_sizes(tournament_size):
    population = ["AAAA", "AAAB", "AABB", "BBBB"]

    with pytest.raises(ValueError):
        tournament_select(
            population,
            "AAAA",
            tournament_size=tournament_size,
            rng=np.random.default_rng(0),
        )


def test_mutation_only_ga_starts_from_identical_copies_of_one_phrase():
    result = evolve_population(
        population_size=25, rng=np.random.default_rng(4), max_generations=0
    )

    assert result["generations"] == 0
    assert len(result["population"]) == 25
    assert len(set(result["population"])) == 1
    assert result["candidate"] == result["population"][0]
    assert result["match_history"] == (matching_characters(result["candidate"]),)


def test_mutation_only_ga_keeps_its_population_size():
    result = evolve_population(
        population_size=30, rng=np.random.default_rng(2), max_generations=5
    )

    assert len(result["population"]) == 30
    assert all(len(phrase) == len(WEASEL_TARGET) for phrase in result["population"])
    assert set("".join(result["population"])) <= set(WEASEL_ALPHABET)


def test_mutation_only_ga_without_mutation_stays_identical():
    result = evolve_population(
        population_size=20,
        mutation_rate=0,
        rng=np.random.default_rng(7),
        max_generations=15,
    )

    assert len(set(result["population"])) == 1


def test_mutation_only_ga_reports_the_fittest_phrase_of_the_final_population():
    result = evolve_population(
        population_size=20,
        mutation_rate=1,
        rng=np.random.default_rng(3),
        max_generations=10,
    )
    best_score = max(matching_characters(phrase) for phrase in result["population"])

    assert result["candidate"] in result["population"]
    assert matching_characters(result["candidate"]) == best_score
    assert result["match_history"][-1] == best_score
    assert len(result["match_history"]) == 11


def test_mutation_only_ga_stops_at_the_generation_limit():
    result = evolve_population(
        population_size=10,
        mutation_rate=0,
        rng=np.random.default_rng(5),
        max_generations=7,
    )

    assert result["generations"] == 7
    assert len(result["match_history"]) == 8
    assert result["candidate"] != WEASEL_TARGET


def test_mutation_only_ga_reaches_a_custom_target_before_the_limit():
    result = evolve_population(
        target="HELLO",
        population_size=50,
        mutation_rate=0.05,
        rng=np.random.default_rng(6),
        max_generations=5_000,
    )

    assert result["candidate"] == "HELLO"
    assert result["match_history"][-1] == len("HELLO")
    assert result["generations"] < 5_000
    assert len(result["match_history"]) == result["generations"] + 1


def test_mutation_only_ga_is_reproducible_with_an_injected_generator():
    runs = [
        evolve_population(
            population_size=20, rng=np.random.default_rng(42), max_generations=30
        )
        for _ in range(2)
    ]

    assert runs[0] == runs[1]
