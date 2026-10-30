import math

import pytest
from scipy.stats import beta

from exercises.beyond_reasonable_doubt.bayes_trial import (
    probability_of_benefit,
    update_posterior,
)


def test_update_posterior_adds_deaths_and_survivors_to_the_prior():
    assert update_posterior(3, 10, 2, 5) == pytest.approx((5, 12))


def test_update_posterior_defaults_to_a_uniform_prior():
    assert update_posterior(3, 10) == pytest.approx((4, 8))


def test_update_posterior_without_data_returns_the_prior():
    assert update_posterior(0, 0, 2.5, 0.5) == pytest.approx((2.5, 0.5))


def test_update_posterior_handles_all_deaths_and_no_deaths():
    assert update_posterior(10, 10, 1, 1) == pytest.approx((11, 1))
    assert update_posterior(0, 10, 1, 1) == pytest.approx((1, 11))


def test_update_posterior_in_two_batches_matches_one_batch():
    first = update_posterior(2, 5, 1.5, 3)
    second = update_posterior(3, 7, *first)

    assert second == pytest.approx(update_posterior(5, 12, 1.5, 3))


def test_update_posterior_result_describes_a_scipy_beta_distribution():
    posterior = update_posterior(3, 10)

    assert beta.mean(*posterior) == pytest.approx(4 / 12)


@pytest.mark.parametrize(
    ("deaths", "total"), [(-1, 10), (11, 10), (1, -5), (1.5, 10), (1, 10.5)]
)
def test_update_posterior_rejects_invalid_counts(deaths, total):
    with pytest.raises(ValueError):
        update_posterior(deaths, total)


@pytest.mark.parametrize(
    ("alpha", "prior_beta"),
    [(0, 1), (1, 0), (-1, 1), (1, -2), (math.nan, 1), (1, math.inf)],
)
def test_update_posterior_rejects_invalid_prior_parameters(alpha, prior_beta):
    with pytest.raises(ValueError):
        update_posterior(1, 2, alpha, prior_beta)


@pytest.mark.parametrize("posterior", [(2, 3), (0.5, 0.5), (40, 60)])
def test_probability_of_benefit_is_one_half_for_identical_groups(posterior):
    assert probability_of_benefit(posterior, posterior) == pytest.approx(0.5)


@pytest.mark.parametrize("threshold", [0.0, 0.1, 0.25, 0.5, 0.9])
def test_probability_of_benefit_matches_the_uniform_case(threshold):
    # The difference of two independent uniforms is triangular on -1 to 1.
    assert probability_of_benefit((1, 1), (1, 1), threshold) == pytest.approx(
        (1 - threshold) ** 2 / 2, abs=1e-7
    )


def test_probability_of_benefit_favours_the_group_with_lower_mortality():
    low, high = (2, 8), (8, 2)

    assert probability_of_benefit(low, high) > 0.99
    assert probability_of_benefit(high, low) < 0.01


def test_probability_of_benefit_of_either_direction_sums_to_one():
    a, b = (45, 81), (58, 69)

    total = probability_of_benefit(a, b) + probability_of_benefit(b, a)

    assert total == pytest.approx(1.0, abs=1e-7)


def test_probability_of_benefit_falls_as_the_required_benefit_rises():
    thresholds = [0, 0.02, 0.05, 0.1, 0.2, 0.5, 1]
    probabilities = [probability_of_benefit((12, 30), (20, 25), t) for t in thresholds]

    assert all(0 <= p <= 1 for p in probabilities)
    assert probabilities == sorted(probabilities, reverse=True)


def test_probability_of_benefit_handles_the_largest_threshold():
    assert probability_of_benefit((2, 3), (4, 5), 1.0) == pytest.approx(0.0)


def test_probability_of_benefit_copes_with_sharply_peaked_posteriors():
    assert probability_of_benefit((20, 180), (180, 20), 0.5) == pytest.approx(1.0)
    assert probability_of_benefit((180, 20), (20, 180), 0.0) == pytest.approx(0.0)


@pytest.mark.parametrize("threshold", [-0.01, 1.01])
def test_probability_of_benefit_rejects_thresholds_outside_zero_to_one(threshold):
    with pytest.raises(ValueError):
        probability_of_benefit((2, 3), (4, 5), threshold)


def test_probability_of_benefit_rejects_non_positive_posterior_parameters():
    with pytest.raises(ValueError):
        probability_of_benefit((0, 3), (4, 5))
