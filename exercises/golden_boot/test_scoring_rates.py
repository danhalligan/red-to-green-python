"""Tests for the Gamma-Poisson scoring-rate functions, using invented examples."""

import math

import pytest
from scipy.stats import beta, gamma

from exercises.golden_boot.scoring_rates import (
    beta_posterior_summary,
    posterior_summary,
    probability_greater,
    update_gamma,
)


def test_update_adds_goals_to_shape_and_exposure_to_rate():
    assert update_gamma(3, 2.5, 6, 18) == (9, 20.5)


def test_no_evidence_returns_the_prior():
    assert update_gamma(0, 0, 6, 18) == (6, 18)


def test_no_goals_still_adds_exposure():
    assert update_gamma(0, 4, 6, 18) == (6, 22)


def test_fractional_exposure_is_allowed():
    shape, rate = update_gamma(1, 0.5, 6, 18)

    assert shape == 7
    assert rate == pytest.approx(18.5)


def test_any_positive_prior_can_be_used():
    shape, rate = update_gamma(2, 10, 0.5, 0.1)

    assert shape == pytest.approx(2.5)
    assert rate == pytest.approx(10.1)


@pytest.mark.parametrize(
    ("goals", "nineties", "alpha", "beta"),
    [
        (-1, 2, 6, 18),
        (1.5, 2, 6, 18),
        (1, -0.1, 6, 18),
        (1, math.nan, 6, 18),
        (1, math.inf, 6, 18),
        (1, 2, 0, 18),
        (1, 2, 6, 0),
        (1, 2, -6, 18),
        (1, 2, 6, math.nan),
    ],
)
def test_update_rejects_invalid_arguments(goals, nineties, alpha, beta):
    with pytest.raises(ValueError):
        update_gamma(goals, nineties, alpha, beta)


def test_posterior_mean_is_shape_over_rate():
    mean, _, _ = posterior_summary(12, 20)

    assert mean == pytest.approx((6 + 12) / (18 + 20))


def test_no_evidence_gives_the_prior_mean_and_interval():
    mean, lower, upper = posterior_summary(0, 0)

    assert mean == pytest.approx(1 / 3)
    assert lower == pytest.approx(gamma.ppf(0.025, 6, scale=1 / 18))
    assert upper == pytest.approx(gamma.ppf(0.975, 6, scale=1 / 18))


def test_interval_is_the_central_95_percent_of_the_posterior():
    _, lower, upper = posterior_summary(10, 30, prior_alpha=2, prior_beta=5)

    posterior = gamma(12, scale=1 / 35)
    assert lower == pytest.approx(posterior.ppf(0.025))
    assert upper == pytest.approx(posterior.ppf(0.975))


def test_interval_contains_the_mean():
    mean, lower, upper = posterior_summary(7, 25)

    assert 0 < lower < mean < upper


def test_a_short_perfect_record_is_pulled_towards_the_prior():
    mean, _, _ = posterior_summary(1, 1)

    raw_rate = 1.0
    prior_mean = 1 / 3
    assert prior_mean < mean < raw_rate
    assert mean - prior_mean < raw_rate - mean


def test_long_records_stay_close_to_their_raw_rate():
    mean, _, _ = posterior_summary(450, 900)

    assert mean == pytest.approx(0.5, abs=0.01)


def test_more_exposure_gives_a_narrower_interval_at_the_same_raw_rate():
    _, short_lower, short_upper = posterior_summary(3, 10)
    _, long_lower, long_upper = posterior_summary(30, 100)

    assert long_upper - long_lower < short_upper - short_lower


def test_defaults_are_the_gamma_6_18_prior():
    assert posterior_summary(5, 12) == pytest.approx(
        posterior_summary(5, 12, prior_alpha=6, prior_beta=18)
    )


def test_a_different_prior_changes_the_answer():
    weak, _, _ = posterior_summary(5, 12, prior_alpha=0.6, prior_beta=1.8)
    strong, _, _ = posterior_summary(5, 12, prior_alpha=60, prior_beta=180)

    raw_rate = 5 / 12
    assert abs(weak - raw_rate) < abs(strong - raw_rate)


def test_summary_returns_three_floats():
    result = posterior_summary(4, 9)

    assert len(result) == 3
    assert all(isinstance(value, float) for value in result)


def test_summary_rejects_invalid_arguments():
    with pytest.raises(ValueError):
        posterior_summary(-1, 5)
    with pytest.raises(ValueError):
        posterior_summary(1, -5)
    with pytest.raises(ValueError):
        posterior_summary(1, 5, prior_alpha=0)


def test_probability_greater_is_a_half_for_identical_posteriors():
    assert probability_greater((6, 18), (6, 18)) == pytest.approx(0.5, abs=0.01)


def test_probability_greater_matches_a_known_exact_answer():
    # For exponential rates r1 and r2, P(first > second) = r2 / (r1 + r2).
    assert probability_greater((1, 1), (1, 3)) == pytest.approx(0.75, abs=0.01)


def test_probability_greater_of_separated_posteriors_is_almost_certain():
    assert probability_greater((100, 100), (100, 400)) > 0.999
    assert probability_greater((100, 400), (100, 100)) < 0.001


def test_probability_greater_of_swapped_posteriors_adds_to_one():
    forward = probability_greater((12, 30), (9, 25))
    backward = probability_greater((9, 25), (12, 30))

    assert forward + backward == pytest.approx(1, abs=0.01)


def test_probability_greater_is_repeatable_for_a_seed():
    first = probability_greater((12, 30), (9, 25), draws=5_000, seed=3)

    assert first == probability_greater((12, 30), (9, 25), draws=5_000, seed=3)
    assert 0 <= first <= 1


@pytest.mark.parametrize(
    ("first", "second", "draws"),
    [
        ((0, 18), (6, 18), 1_000),
        ((6, -18), (6, 18), 1_000),
        ((6, 18), (math.nan, 18), 1_000),
        ((6, 18), (6, math.inf), 1_000),
        ((6, 18), (6, 18), 0),
        ((6, 18), (6, 18), 10.5),
    ],
)
def test_probability_greater_rejects_invalid_arguments(first, second, draws):
    with pytest.raises(ValueError):
        probability_greater(first, second, draws=draws)


def test_beta_posterior_mean_adds_successes_and_failures_to_the_prior():
    mean, _, _ = beta_posterior_summary(15, 60, 15, 85)

    assert mean == pytest.approx((15 + 15) / (15 + 85 + 60))


def test_beta_posterior_with_no_trials_is_the_prior():
    mean, lower, upper = beta_posterior_summary(0, 0, 15, 85)

    assert mean == pytest.approx(0.15)
    assert lower == pytest.approx(beta.ppf(0.025, 15, 85))
    assert upper == pytest.approx(beta.ppf(0.975, 15, 85))


def test_beta_posterior_interval_is_the_central_95_percent():
    _, lower, upper = beta_posterior_summary(27, 172, 15, 85)

    assert lower == pytest.approx(beta.ppf(0.025, 42, 230))
    assert upper == pytest.approx(beta.ppf(0.975, 42, 230))


@pytest.mark.parametrize(("successes", "trials"), [(0, 20), (20, 20)])
def test_beta_posterior_stays_strictly_between_zero_and_one(successes, trials):
    mean, lower, upper = beta_posterior_summary(successes, trials, 15, 85)

    assert 0 < lower < mean < upper < 1


def test_beta_posterior_pulls_a_short_record_towards_the_prior():
    mean, _, _ = beta_posterior_summary(3, 4, 15, 85)

    assert 0.15 < mean < 0.75
    assert mean - 0.15 < 0.75 - mean


def test_beta_posterior_interval_narrows_with_more_trials():
    _, short_lower, short_upper = beta_posterior_summary(6, 40, 15, 85)
    _, long_lower, long_upper = beta_posterior_summary(60, 400, 15, 85)

    assert long_upper - long_lower < short_upper - short_lower


@pytest.mark.parametrize(
    ("successes", "trials", "alpha", "prior_beta"),
    [
        (-1, 10, 15, 85),
        (11, 10, 15, 85),
        (2.5, 10, 15, 85),
        (2, 10, 0, 85),
        (2, 10, 15, -1),
        (2, 10, 15, math.nan),
    ],
)
def test_beta_posterior_rejects_invalid_arguments(successes, trials, alpha, prior_beta):
    with pytest.raises(ValueError):
        beta_posterior_summary(successes, trials, alpha, prior_beta)
