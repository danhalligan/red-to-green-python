import numpy as np
import pytest

from pyproblems.data import load_faithful_data
from pyproblems.mixture_models import (
    ExpectationMaximizationResult,
    GaussianMixtureParameters,
    MultivariateGaussianMixtureParameters,
    expectation_maximization,
    fit_faithful_gaussian_mixture,
    fit_hard_gaussian_mixture,
    fit_multivariate_gaussian_mixture,
    fit_soft_gaussian_mixture,
    hard_expectation_step,
    hard_maximization_step,
    mixture_log_likelihood,
    multivariate_gaussian_mixture_log_likelihood,
    multivariate_soft_expectation_step,
    multivariate_soft_maximization_step,
    soft_expectation_step,
    soft_maximization_step,
)

pytestmark = pytest.mark.advanced


def test_hard_e_step_assigns_to_the_more_likely_component():
    parameters = GaussianMixtureParameters(-3, 1, 3, 1, 0.5)

    assert hard_expectation_step([-3, 0, 3], parameters).tolist() == [True, True, False]


def test_soft_e_step_returns_component_probabilities():
    parameters = GaussianMixtureParameters(-3, 1, 3, 1, 0.5)
    probabilities = soft_expectation_step([-3, 0, 3], parameters)

    assert probabilities.shape == (3,)
    assert np.all((probabilities >= 0) & (probabilities <= 1))
    assert probabilities[0] > probabilities[1] > probabilities[2]


def test_hard_and_soft_m_steps_recover_weighted_component_means():
    observations = np.array([-4.0, -2.0, 2.0, 4.0])
    labels = np.array([True, True, False, False])
    weights = labels.astype(float)

    hard = hard_maximization_step(observations, labels)
    soft = soft_maximization_step(observations, weights)

    assert hard.mean1 == pytest.approx(-3)
    assert hard.mean2 == pytest.approx(3)
    assert soft == hard


def test_soft_em_returns_a_converged_fit_with_finite_likelihood():
    generator = np.random.default_rng(2026)
    observations = np.concatenate(
        (generator.normal(-3, 0.7, 120), generator.normal(4, 1.0, 180))
    )
    initial = GaussianMixtureParameters(-2, 1.5, 3, 1.5, 0.5)

    fitted = fit_soft_gaussian_mixture(observations, initial)

    assert isinstance(fitted, ExpectationMaximizationResult)
    assert fitted.converged
    assert fitted.iterations > 0
    assert np.isfinite(fitted.log_likelihood)
    assert fitted.parameters.mean1 < fitted.parameters.mean2
    assert mixture_log_likelihood(observations, fitted.parameters) == pytest.approx(
        fitted.log_likelihood
    )


def test_hard_em_returns_a_finite_fit():
    observations = np.array([-4.0, -3.0, -2.0, 2.0, 3.0, 4.0])
    initial = GaussianMixtureParameters(-3, 1, 3, 1, 0.5)

    fitted = fit_hard_gaussian_mixture(observations, initial)

    assert fitted.converged
    assert np.isfinite(fitted.log_likelihood)
    assert fitted.parameters.mean1 < fitted.parameters.mean2


def test_generic_em_accepts_step_and_likelihood_callables():
    observations = np.array([-4.0, -2.0, 2.0, 4.0])
    initial = GaussianMixtureParameters(-3, 1.5, 3, 1.5, 0.5)
    fitted = expectation_maximization(
        observations,
        initial,
        soft_expectation_step,
        soft_maximization_step,
        mixture_log_likelihood,
    )

    assert fitted.converged
    assert np.isfinite(fitted.log_likelihood)


def test_multivariate_likelihood_and_fit_accept_two_dimensional_data():
    generator = np.random.default_rng(9)
    observations = np.vstack(
        (
            generator.normal((-3, -2), 0.5, size=(80, 2)),
            generator.normal((3, 2), 0.7, size=(100, 2)),
        )
    )
    identity = np.eye(2)
    initial = MultivariateGaussianMixtureParameters(
        np.array([-2.5, -1.5]), identity, np.array([2.5, 1.5]), identity, 0.5
    )

    assert np.isfinite(
        multivariate_gaussian_mixture_log_likelihood(observations, initial)
    )
    fitted = fit_multivariate_gaussian_mixture(observations, initial)
    probabilities = multivariate_soft_expectation_step(observations, initial)
    updated = multivariate_soft_maximization_step(observations, probabilities)
    assert fitted.converged
    assert updated.mean1.shape == (2,)
    assert probabilities.shape == (len(observations),)
    assert fitted.log_likelihood > multivariate_gaussian_mixture_log_likelihood(
        observations,
        MultivariateGaussianMixtureParameters(
            observations.mean(axis=0),
            np.eye(2) * 20,
            observations.mean(axis=0),
            np.eye(2) * 20,
            0.5,
        ),
    )


def test_faithful_fit_uses_the_packaged_data():
    initial = MultivariateGaussianMixtureParameters(
        np.array([2.8, 75.0]),
        np.array([[0.8, 7.0], [7.0, 70.0]]),
        np.array([3.6, 58.0]),
        np.array([[0.8, 7.0], [7.0, 70.0]]),
        0.5,
    )

    assert len(load_faithful_data()) == 272
    fitted = fit_faithful_gaussian_mixture(initial)

    assert fitted.converged
    assert fitted.log_likelihood == pytest.approx(-1130.272, abs=0.1)
