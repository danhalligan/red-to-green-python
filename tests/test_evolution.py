import numpy as np
import pytest

from pyproblems.evolution import (
    WEASEL_TARGET,
    EvolutionResult,
    evolve_weasel,
    matching_characters,
    mutate_message,
)

pytestmark = pytest.mark.advanced


def test_matching_characters_counts_matching_positions():
    assert matching_characters("ABC", "ADC") == 2
    assert matching_characters(WEASEL_TARGET) == len(WEASEL_TARGET)


def test_zero_mutation_rate_preserves_message():
    generator = np.random.default_rng(17)

    assert mutate_message("HELLO", mutation_rate=0, rng=generator) == "HELLO"


def test_simulation_is_reproducible_with_an_injected_generator():
    first = evolve_weasel(
        population_size=10,
        mutation_rate=0.08,
        rng=np.random.default_rng(42),
        max_generations=500,
    )
    second = evolve_weasel(
        population_size=10,
        mutation_rate=0.08,
        rng=np.random.default_rng(42),
        max_generations=500,
    )

    assert isinstance(first, EvolutionResult)
    assert first == second
    assert len(first.match_history) == first.generations + 1
    assert all(
        earlier <= later
        for earlier, later in zip(
            first.match_history, first.match_history[1:], strict=False
        )
    )


@pytest.mark.parametrize("mutation_rate", [-0.1, 1.1])
def test_simulation_rejects_invalid_mutation_rates(mutation_rate):
    with pytest.raises(ValueError):
        mutate_message(
            "HELLO", mutation_rate=mutation_rate, rng=np.random.default_rng(0)
        )
