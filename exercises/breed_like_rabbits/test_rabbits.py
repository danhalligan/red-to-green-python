import numpy as np
import pytest
from numpy.testing import assert_allclose, assert_array_equal

from exercises.breed_like_rabbits.rabbits import breed, simulate_seasons


def test_breed_applies_breeding_and_overcrowding():
    assert_allclose(breed(0.5, 2), 0.5)
    assert_allclose(breed(0.2, 3), 0.48)


def test_empty_and_full_fields_have_no_rabbits_next_season():
    assert_allclose(breed([0.0, 1.0], 3.7), [0.0, 0.0])


def test_breed_works_elementwise_without_changing_the_input():
    populations = np.array([0.1, 0.5, 0.9])

    result = breed(populations, 2)

    assert_allclose(result, [0.18, 0.5, 0.18])
    assert_array_equal(populations, [0.1, 0.5, 0.9])


def test_breed_combines_arrays_of_populations_and_rates():
    assert_allclose(breed(0.5, [1.0, 2.0, 4.0]), [0.25, 0.5, 1.0])
    assert_allclose(breed([0.2, 0.5], [3.0, 2.0]), [0.48, 0.5])


def test_simulation_starts_at_start_and_has_one_value_per_season():
    population = simulate_seasons(2.5, start=0.3, seasons=10)

    assert population.shape == (11,)
    assert population[0] == pytest.approx(0.3)


def test_simulation_applies_breed_each_season():
    population = simulate_seasons(3.1, start=0.4, seasons=5)

    for before, after in zip(population[:-1], population[1:], strict=True):
        assert after == pytest.approx(breed(before, 3.1))


def test_a_low_breeding_rate_dies_out():
    population = simulate_seasons(0.5, start=0.8, seasons=50)

    assert population[-1] < 1e-6
    assert np.all(np.diff(population) < 0)


def test_a_moderate_breeding_rate_settles_to_a_steady_population():
    population = simulate_seasons(2.5, seasons=100)

    assert population[-1] == pytest.approx(0.6)
    assert breed(population[-1], 2.5) == pytest.approx(population[-1])


def test_simulating_many_rates_gives_one_column_per_rate():
    rates = np.array([2.5, 3.2, 3.5, 3.9])

    result = simulate_seasons(rates, start=0.2, seasons=30)

    assert result.shape == (31, 4)
    assert_allclose(result[0], 0.2)
    for column, rate in zip(result.T, rates, strict=True):
        assert_allclose(column, simulate_seasons(rate, start=0.2, seasons=30))


def test_simulating_a_grid_of_rates_keeps_its_shape():
    rates = np.array([[2.5, 3.2, 3.5], [3.6, 3.8, 3.9]])

    result = simulate_seasons(rates, seasons=10)

    assert result.shape == (11, 2, 3)
    assert_allclose(result[:, 1, 2], simulate_seasons(3.9, seasons=10))


def test_simulating_does_not_modify_the_rates():
    rates = np.linspace(2.5, 3.5, 5)
    original = rates.copy()

    simulate_seasons(rates, seasons=10)

    assert_array_equal(rates, original)


def test_discarding_seasons_skips_the_start_of_the_simulation():
    everything = simulate_seasons(3.3, start=0.2, seasons=47)

    result = simulate_seasons(3.3, start=0.2, seasons=7, discard=40)

    assert result.shape == (8,)
    assert_allclose(result, everything[40:])


def test_discarding_works_for_many_rates_at_once():
    rates = np.array([2.5, 3.2, 3.5, 3.9])

    result = simulate_seasons(rates, seasons=12, discard=60)

    assert result.shape == (13, 4)
    assert_allclose(result, simulate_seasons(rates, seasons=72)[60:])


def test_discarding_nothing_is_the_default():
    assert_allclose(
        simulate_seasons(3.1, seasons=9, discard=0),
        simulate_seasons(3.1, seasons=9),
    )


def test_simulating_thousands_of_rates_for_hundreds_of_seasons():
    rates = np.linspace(2.5, 4.0, 2000)

    result = simulate_seasons(rates, seasons=100, discard=500)

    assert result.shape == (101, 2000)
    assert np.all((result >= 0) & (result <= 1))


def test_a_moderate_rate_settles_to_a_single_steady_value():
    result = simulate_seasons([2.5, 2.8], seasons=500)

    assert_allclose(result[-1], [0.6, 1 - 1 / 2.8])


def test_a_higher_rate_alternates_between_two_values():
    result = simulate_seasons(3.2, seasons=20, discard=500)

    assert_allclose(result[::2], result[0])
    assert_allclose(result[1::2], result[1])
    assert_allclose(sorted(result[:2]), [0.5130445, 0.7994555], atol=1e-6)


def test_a_still_higher_rate_repeats_every_four_seasons():
    result = simulate_seasons(3.5, seasons=20, discard=500)

    assert_allclose(result[4:], result[:-4])
    assert len(np.unique(result.round(6))) == 4
