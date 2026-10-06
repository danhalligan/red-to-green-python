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


def test_hard_m_step_uses_population_moments_and_label_fractions():
    observations = np.array([-4.0, -2.0, -3.0, 2.0, 4.0])
    labels = np.array([True, True, True, False, False])

    fitted = hard_maximization_step(observations, labels)

    assert fitted.mean1 == pytest.approx(-3.0)
    assert fitted.standard_deviation1 == pytest.approx(np.std([-4, -2, -3], ddof=0))
    assert fitted.mean2 == pytest.approx(3.0)
    assert fitted.standard_deviation2 == pytest.approx(1.0)
    assert fitted.weight1 == pytest.approx(0.6)


def test_soft_m_step_uses_weighted_population_moments():
    observations = np.array([-3.0, -2.5, -1.0, 0.5, 2.0, 4.0])
    weights = np.array([0.9, 0.8, 0.7, 0.2, 0.1, 0.05])
    other = 1 - weights

    fitted = soft_maximization_step(observations, weights)

    mean1 = weights @ observations / weights.sum()
    mean2 = other @ observations / other.sum()
    assert fitted.mean1 == pytest.approx(mean1)
    assert fitted.mean2 == pytest.approx(mean2)
    assert fitted.standard_deviation1**2 == pytest.approx(
        weights @ (observations - mean1) ** 2 / weights.sum()
    )
    assert fitted.standard_deviation2**2 == pytest.approx(
        other @ (observations - mean2) ** 2 / other.sum()
    )
    assert fitted.weight1 == pytest.approx(weights.mean())


def test_multivariate_m_step_uses_weighted_population_covariance():
    generator = np.random.default_rng(5)
    observations = np.sort(generator.normal(size=(6, 2)), axis=0)
    weights = np.array([0.95, 0.9, 0.8, 0.3, 0.1, 0.05])
    other = 1 - weights

    fitted = multivariate_soft_maximization_step(observations, weights)

    for mean, covariance, w in (
        (fitted.mean1, fitted.covariance1, weights),
        (fitted.mean2, fitted.covariance2, other),
    ):
        expected_mean = w @ observations / w.sum()
        centred = observations - expected_mean
        assert mean == pytest.approx(expected_mean)
        assert covariance == pytest.approx((w[:, None] * centred).T @ centred / w.sum())
    assert fitted.weight1 == pytest.approx(weights.mean())


def test_e_steps_stay_finite_far_from_both_components():
    parameters = GaussianMixtureParameters(0, 1, 5, 1, 0.5)
    far = soft_expectation_step([-1000.0, 1000.0], parameters)
    assert far == pytest.approx([1.0, 0.0])

    identity = np.eye(2)
    multivariate = MultivariateGaussianMixtureParameters(
        np.zeros(2), identity, np.full(2, 5.0), identity, 0.5
    )
    points = np.array([[-1000.0, -1000.0], [1000.0, 1000.0]])
    assert multivariate_soft_expectation_step(points, multivariate) == pytest.approx(
        [1.0, 0.0]
    )
    assert np.isfinite(
        multivariate_gaussian_mixture_log_likelihood(points, multivariate)
    )
    assert np.isfinite(mixture_log_likelihood([-1000.0, 1000.0], parameters))


def test_soft_em_never_decreases_the_observed_log_likelihood():
    generator = np.random.default_rng(2026)
    observations = np.concatenate(
        (generator.normal(-3, 0.7, 120), generator.normal(4, 1.0, 180))
    )
    parameters = GaussianMixtureParameters(-2, 1.5, 3, 1.5, 0.5)
    previous = mixture_log_likelihood(observations, parameters)

    for _ in range(30):
        weights = soft_expectation_step(observations, parameters)
        parameters = soft_maximization_step(observations, weights)
        current = mixture_log_likelihood(observations, parameters)
        assert current >= previous - 1e-9
        previous = current


def test_a_hard_em_step_can_decrease_the_observed_log_likelihood():
    observations = np.array([0.8, -0.2, 0.7, 1.4, -1.5, 0.2, -0.7, 0.7])
    parameters = GaussianMixtureParameters(0.0, 0.8, 0.2, 1.0, 0.5)

    updated = hard_maximization_step(
        observations, hard_expectation_step(observations, parameters)
    )

    assert mixture_log_likelihood(observations, updated) < (
        mixture_log_likelihood(observations, parameters) - 1.0
    )


def scripted_em(log_likelihoods):
    """E/M/log-likelihood callables whose likelihood depends only on the step."""

    def expectation(observations, parameters):
        return parameters.mean1

    def maximization(observations, step):
        return GaussianMixtureParameters(step + 1, 1.0, 1e9, 1.0, 0.5)

    def log_likelihood(observations, parameters):
        return log_likelihoods[int(parameters.mean1)]

    initial = GaussianMixtureParameters(0, 1.0, 1e9, 1.0, 0.5)

    def run(**options):
        return expectation_maximization(
            [0.0], initial, expectation, maximization, log_likelihood, **options
        )

    return run, initial


def test_em_does_not_treat_a_likelihood_decrease_as_convergence():
    run, _ = scripted_em([-10.0, -20.0, -20.0, -20.0])

    fitted = run(tolerance=1e-3)

    assert fitted.converged
    assert fitted.iterations == 2
    assert fitted.log_likelihood == -20.0
    assert fitted.parameters.mean1 == 2


def test_em_with_no_iterations_returns_the_unconverged_initial_fit():
    run, initial = scripted_em([-10.0, -10.0])

    fitted = run(max_iterations=0)

    assert not fitted.converged
    assert fitted.iterations == 0
    assert fitted.parameters == initial
    assert fitted.log_likelihood == -10.0


def test_em_judges_convergence_after_a_single_update():
    run, _ = scripted_em([-10.0, -10.0, -10.0])

    fitted = run(max_iterations=1)

    assert fitted.converged
    assert fitted.iterations == 1


def test_em_reports_an_exhausted_iteration_budget_as_unconverged():
    run, _ = scripted_em([0.0, 1.0, 2.0, 3.0, 4.0])

    fitted = run(tolerance=1e-3, max_iterations=3)

    assert not fitted.converged
    assert fitted.iterations == 3
    assert fitted.log_likelihood == 3.0


@pytest.mark.parametrize(
    "labels",
    [
        [True, True, True, True],
        [False, False, False, False],
        [True, False, False, False],
    ],
)
def test_hard_m_step_rejects_empty_or_zero_variance_components(labels):
    with pytest.raises(ValueError):
        hard_maximization_step([-2.0, -1.0, 1.0, 2.0], labels)


def test_soft_m_step_rejects_components_without_weight():
    with pytest.raises(ValueError):
        soft_maximization_step([-2.0, -1.0, 1.0, 2.0], [0.0, 0.0, 0.0, 0.0])


def test_multivariate_m_step_rejects_singular_covariance():
    on_a_line = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]])

    with pytest.raises(ValueError):
        multivariate_soft_maximization_step(on_a_line, [1.0, 1.0, 0.0, 0.0])


def test_multivariate_fit_orders_components_by_the_first_mean_coordinate():
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

    forward = fit_multivariate_gaussian_mixture(
        observations,
        MultivariateGaussianMixtureParameters(low, identity, high, identity, 0.5),
    ).parameters
    swapped = fit_multivariate_gaussian_mixture(
        observations,
        MultivariateGaussianMixtureParameters(high, identity, low, identity, 0.5),
    ).parameters

    assert forward.mean1[0] < forward.mean2[0]
    assert swapped.mean1 == pytest.approx(forward.mean1)
    assert swapped.mean2 == pytest.approx(forward.mean2)
    assert swapped.weight1 == pytest.approx(forward.weight1)
