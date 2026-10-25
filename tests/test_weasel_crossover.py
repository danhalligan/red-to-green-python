"""Optional weasel extension: one-point crossover in the population GA."""

import re

import numpy as np
import pytest

from pyproblems.weasel import (
    WEASEL_ALPHABET,
    WEASEL_TARGET,
    evolve_population,
    matching_characters,
    one_point_crossover,
)

pytestmark = pytest.mark.advanced


def test_crossover_builds_a_prefix_of_one_parent_and_a_suffix_of_the_other():
    rng = np.random.default_rng(8)

    children = [one_point_crossover("A" * 10, "B" * 10, rng=rng) for _ in range(300)]

    assert all(re.fullmatch(r"A+B+", child) for child in children)
    assert {child.count("A") for child in children} == set(range(1, 10))


def test_crossover_can_beat_both_parents():
    parent_a, parent_b = "AAAABBBB", "BBBBAAAA"
    rng = np.random.default_rng(9)

    best = max(
        matching_characters(
            one_point_crossover(parent_a, parent_b, rng=rng), "AAAAAAAA"
        )
        for _ in range(100)
    )

    assert best == 8


@pytest.mark.parametrize(
    ("parent_a", "parent_b"), [("ABC", "AB"), ("A", "B"), ("", "")]
)
def test_crossover_rejects_unusable_parents(parent_a, parent_b):
    with pytest.raises(ValueError):
        one_point_crossover(parent_a, parent_b, rng=np.random.default_rng(0))


def test_recombination_ga_starts_from_the_same_population_as_mutation_only():
    mutation_only = evolve_population(
        population_size=25,
        crossover=False,
        rng=np.random.default_rng(4),
        max_generations=0,
    )
    recombination = evolve_population(
        population_size=25,
        crossover=True,
        rng=np.random.default_rng(4),
        max_generations=0,
    )

    assert recombination["population"] == mutation_only["population"]
    assert recombination["match_history"] == mutation_only["match_history"]


def test_recombination_ga_keeps_its_population_size():
    result = evolve_population(
        population_size=30,
        crossover=True,
        rng=np.random.default_rng(2),
        max_generations=5,
    )

    assert len(result["population"]) == 30
    assert all(len(phrase) == len(WEASEL_TARGET) for phrase in result["population"])
    assert set("".join(result["population"])) <= set(WEASEL_ALPHABET)


def test_recombination_ga_reports_the_fittest_phrase_of_the_final_population():
    result = evolve_population(
        population_size=20,
        mutation_rate=1,
        crossover=True,
        rng=np.random.default_rng(3),
        max_generations=10,
    )
    best_score = max(matching_characters(phrase) for phrase in result["population"])

    assert result["candidate"] in result["population"]
    assert matching_characters(result["candidate"]) == best_score
    assert result["match_history"][-1] == best_score
    assert len(result["match_history"]) == 11


def test_recombination_ga_stops_at_the_generation_limit():
    result = evolve_population(
        population_size=10,
        mutation_rate=0,
        crossover=True,
        rng=np.random.default_rng(5),
        max_generations=7,
    )

    assert result["generations"] == 7
    assert len(result["match_history"]) == 8
    assert result["candidate"] != WEASEL_TARGET


def test_recombination_ga_reaches_a_custom_target_before_the_limit():
    result = evolve_population(
        target="HELLO",
        population_size=50,
        mutation_rate=0.05,
        crossover=True,
        rng=np.random.default_rng(6),
        max_generations=5_000,
    )

    assert result["candidate"] == "HELLO"
    assert result["match_history"][-1] == len("HELLO")
    assert result["generations"] < 5_000
    assert len(result["match_history"]) == result["generations"] + 1


def test_recombination_ga_is_reproducible_with_an_injected_generator():
    runs = [
        evolve_population(
            population_size=20,
            crossover=True,
            rng=np.random.default_rng(42),
            max_generations=30,
        )
        for _ in range(2)
    ]

    assert runs[0] == runs[1]
