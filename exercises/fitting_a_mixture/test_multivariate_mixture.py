import numpy as np
import pytest

from exercises.fitting_a_mixture.loaders import load_faithful_data
from exercises.fitting_a_mixture.multivariate_mixture import (
    MixtureParameters,
    expectation_step,
    fit,
    log_likelihood,
    maximization_step,
)

pytestmark = pytest.mark.advanced


def test_likelihood_and_fit_accept_two_dimensional_data():
    generator = np.random.default_rng(9)
    observations = np.vstack(
        (
            generator.normal((-3, -2), 0.5, size=(80, 2)),
            generator.normal((3, 2), 0.7, size=(100, 2)),
        )
    )
    identity = np.eye(2)
    initial = MixtureParameters(
        np.array([-2.5, -1.5]), identity, np.array([2.5, 1.5]), identity, 0.5
    )

    assert np.isfinite(log_likelihood(observations, initial))
    fitted = fit(observations, initial)
    probabilities = expectation_step(observations, initial)
    updated = maximization_step(observations, probabilities)
    assert fitted.converged
    assert updated.mean1.shape == (2,)
    assert probabilities.shape == (len(observations),)
    assert fitted.log_likelihood > log_likelihood(
        observations,
        MixtureParameters(
            observations.mean(axis=0),
            np.eye(2) * 20,
            observations.mean(axis=0),
            np.eye(2) * 20,
            0.5,
        ),
    )


def test_faithful_fit_uses_the_packaged_data():
    initial = MixtureParameters(
        np.array([2.8, 75.0]),
        np.array([[0.8, 7.0], [7.0, 70.0]]),
        np.array([3.6, 58.0]),
        np.array([[0.8, 7.0], [7.0, 70.0]]),
        0.5,
    )

    fitted = fit(np.array(load_faithful_data()), initial)

    assert fitted.converged
    assert fitted.log_likelihood == pytest.approx(-1130.272, abs=0.1)


def test_m_step_uses_weighted_population_covariance():
    generator = np.random.default_rng(5)
    observations = np.sort(generator.normal(size=(6, 2)), axis=0)
    weights = np.array([0.95, 0.9, 0.8, 0.3, 0.1, 0.05])
    other = 1 - weights

    fitted = maximization_step(observations, weights)

    for mean, covariance, w in (
        (fitted.mean1, fitted.covariance1, weights),
        (fitted.mean2, fitted.covariance2, other),
    ):
        expected_mean = w @ observations / w.sum()
        centred = observations - expected_mean
        assert mean == pytest.approx(expected_mean)
        assert covariance == pytest.approx((w[:, None] * centred).T @ centred / w.sum())
    assert fitted.weight1 == pytest.approx(weights.mean())


def test_e_step_and_likelihood_stay_finite_far_from_both_components():
    identity = np.eye(2)
    parameters = MixtureParameters(
        np.zeros(2), identity, np.full(2, 5.0), identity, 0.5
    )
    points = np.array([[-1000.0, -1000.0], [1000.0, 1000.0]])

    assert expectation_step(points, parameters) == pytest.approx([1.0, 0.0])
    assert np.isfinite(log_likelihood(points, parameters))


def test_fit_keeps_the_labels_of_the_starting_values():
    generator = np.random.default_rng(9)
    observations = np.vstack(
        (
            generator.normal((-3, 2), 0.5, size=(80, 2)),
            generator.normal((3, -2), 0.7, size=(100, 2)),
        )
    )
    identity = np.eye(2)
    low = np.array([-2.5, 1.5])
    high = np.array([2.5, -1.5])

    forward = fit(observations, MixtureParameters(low, identity, high, identity, 0.5))
    swapped = fit(observations, MixtureParameters(high, identity, low, identity, 0.5))

    assert forward.parameters.mean1[0] < forward.parameters.mean2[0]
    assert swapped.parameters.mean1 == pytest.approx(forward.parameters.mean2)
    assert swapped.parameters.mean2 == pytest.approx(forward.parameters.mean1)
    assert swapped.parameters.weight1 == pytest.approx(1 - forward.parameters.weight1)
    assert swapped.log_likelihood == pytest.approx(forward.log_likelihood)
