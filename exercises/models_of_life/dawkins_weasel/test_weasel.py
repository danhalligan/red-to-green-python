import numpy as np
import pytest

from exercises.models_of_life.dawkins_weasel.weasel import (
    WEASEL_ALPHABET,
    WEASEL_TARGET,
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


def test_full_mutation_changes_every_position_to_an_allowed_symbol():
    message = "METHINKS IT IS"

    mutated = mutate_message(message, mutation_rate=1, rng=np.random.default_rng(3))

    assert len(mutated) == len(message)
    assert all(new != old for new, old in zip(mutated, message, strict=True))
    assert set(mutated) <= set(WEASEL_ALPHABET)


def test_partial_mutation_changes_some_but_not_all_positions():
    message = "A" * 400

    mutated = mutate_message(message, mutation_rate=0.5, rng=np.random.default_rng(5))

    changed = sum(new != old for new, old in zip(mutated, message, strict=True))
    assert 100 < changed < 300


def test_simulation_stops_at_the_generation_limit_when_nothing_can_change():
    result = evolve_weasel(
        population_size=10,
        mutation_rate=0,
        rng=np.random.default_rng(1),
        max_generations=7,
    )

    assert result["generations"] == 7
    assert len(result["match_history"]) == 8
    assert len(set(result["match_history"])) == 1
    assert result["candidate"] != WEASEL_TARGET


def test_simulation_reaches_a_custom_target_before_the_limit():
    result = evolve_weasel(
        target="HELLO",
        population_size=10,
        mutation_rate=0.05,
        rng=np.random.default_rng(11),
        max_generations=20_000,
    )

    assert result["candidate"] == "HELLO"
    assert result["match_history"][-1] == len("HELLO")
    assert result["generations"] < 20_000
    assert len(result["match_history"]) == result["generations"] + 1


def test_final_candidate_agrees_with_the_match_history():
    target = "SOMETHING"

    result = evolve_weasel(
        target=target,
        population_size=5,
        mutation_rate=0.05,
        rng=np.random.default_rng(9),
        max_generations=50,
    )

    assert len(result["candidate"]) == len(target)
    assert set(result["candidate"]) <= set(WEASEL_ALPHABET)
    assert result["match_history"][-1] == matching_characters(
        result["candidate"], target
    )
    assert all(0 <= score <= len(target) for score in result["match_history"])


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

    assert isinstance(first, dict)
    assert set(first) == {"candidate", "generations", "match_history"}
    assert isinstance(first["candidate"], str)
    assert isinstance(first["generations"], int)
    assert isinstance(first["match_history"], tuple)
    assert all(isinstance(score, int) for score in first["match_history"])
    assert first == second
    assert len(first["match_history"]) == first["generations"] + 1
    assert all(
        earlier <= later
        for earlier, later in zip(
            first["match_history"], first["match_history"][1:], strict=False
        )
    )


@pytest.mark.parametrize("mutation_rate", [-0.1, 1.1])
def test_simulation_rejects_invalid_mutation_rates(mutation_rate):
    with pytest.raises(ValueError):
        mutate_message(
            "HELLO", mutation_rate=mutation_rate, rng=np.random.default_rng(0)
        )
