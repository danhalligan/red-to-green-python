import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from exercises.breed_like_rabbits.rabbits import (
    long_run_population,
    next_population,
    simulate_population,
)


def test_next_population_applies_breeding_and_overcrowding():
    assert_allclose(next_population(0.5, 2), 0.5)
    assert_allclose(next_population(0.2, 3), 0.48)


def test_empty_and_full_fields_have_no_rabbits_next_season():
    assert_allclose(next_population([0.0, 1.0], 3.7), [0.0, 0.0])


def test_next_population_works_elementwise_without_changing_the_input():
    populations = np.array([0.1, 0.5, 0.9])

    result = next_population(populations, 2)

    assert_allclose(result, [0.18, 0.5, 0.18])
    assert_array_equal(populations, [0.1, 0.5, 0.9])


def test_simulation_starts_at_start_and_has_one_value_per_season():
    population = simulate_population(2.5, start=0.3, seasons=10)

    assert population.shape == (11,)
    assert population[0] == pytest.approx(0.3)


def test_simulation_applies_next_population_each_season():
    population = simulate_population(3.1, start=0.4, seasons=5)

    for before, after in zip(population[:-1], population[1:], strict=True):
        assert after == pytest.approx(next_population(before, 3.1))


def test_a_low_breeding_rate_dies_out():
    population = simulate_population(0.5, start=0.8, seasons=50)

    assert population[-1] < 1e-6
    assert np.all(np.diff(population) < 0)


def test_a_moderate_breeding_rate_settles_to_a_steady_population():
    population = simulate_population(2.5, seasons=100)

    assert population[-1] == pytest.approx(0.6)
    assert next_population(population[-1], 2.5) == pytest.approx(population[-1])


def test_long_run_of_one_rate_returns_the_kept_seasons():
    result = long_run_population(3.3, start=0.2, burn_in=40, keep=7)
    expected = simulate_population(3.3, start=0.2, seasons=47)[-7:]

    assert result.shape == (7,)
    assert_allclose(result, expected)


def test_long_run_of_many_rates_has_one_row_per_rate():
    rates = np.array([2.5, 3.2, 3.5, 3.9])

    result = long_run_population(rates, burn_in=60, keep=12)

    assert result.shape == (4, 12)
    for row, rate in zip(result, rates, strict=True):
        assert_allclose(row, long_run_population(rate, burn_in=60, keep=12))


def test_long_run_does_not_modify_the_rates():
    rates = np.linspace(2.5, 3.5, 5)
    original = rates.copy()

    long_run_population(rates, burn_in=10, keep=5)

    assert_array_equal(rates, original)


def test_long_run_handles_thousands_of_rates():
    rates = np.linspace(2.5, 4.0, 2000)

    result = long_run_population(rates)

    assert result.shape == (2000, 100)
    assert np.all((result >= 0) & (result <= 1))


def test_long_run_of_a_moderate_rate_is_a_single_steady_value():
    assert_allclose(long_run_population(2.5), 0.6)


def test_long_run_of_a_higher_rate_alternates_between_two_values():
    result = long_run_population(3.2, keep=20)

    assert_allclose(result[::2], result[0])
    assert_allclose(result[1::2], result[1])
    assert_allclose(sorted(result[:2]), [0.5130445, 0.7994555], atol=1e-6)


def test_long_run_of_a_still_higher_rate_repeats_every_four_seasons():
    result = long_run_population(3.5, keep=20)

    assert_allclose(result[4:], result[:-4])
    assert len(np.unique(result.round(6))) == 4
