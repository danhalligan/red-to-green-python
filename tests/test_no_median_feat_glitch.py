import numpy as np
import pytest

from exercises.no_median_feat.glitch import glitch, sample, simulate


def test_glitch_adds_the_size_to_a_fraction_of_the_values():
    values = np.arange(20.0)

    glitched = glitch(values, 0.25, size=50, rng=np.random.default_rng(1))

    changed = glitched != values
    assert changed.sum() == 5
    assert np.allclose((glitched - values)[changed], 50)


def test_glitch_does_not_change_the_original():
    values = np.arange(10.0)

    glitch(values, 0.5, where="start")

    assert values.tolist() == list(range(10))


def test_glitch_can_choose_the_ends():
    values = np.zeros(10)

    assert glitch(values, 0.3, where="start").nonzero()[0].tolist() == [0, 1, 2]
    assert glitch(values, 0.3, where="end").nonzero()[0].tolist() == [7, 8, 9]


def test_glitch_random_positions_are_reproducible_and_spread_out():
    values = np.zeros(100)

    first = glitch(values, 0.1, rng=np.random.default_rng(5))
    second = glitch(values, 0.1, rng=np.random.default_rng(5))
    other = glitch(values, 0.1, rng=np.random.default_rng(6))

    assert np.array_equal(first, second)
    assert not np.array_equal(first, other)
    assert first.nonzero()[0].tolist() != list(range(10))


def test_glitch_direction():
    values = np.zeros(10)

    assert (glitch(values, 0.5, direction="down", where="start")[:5] == -100).all()

    both = glitch(values, 1.0, direction="both", rng=np.random.default_rng(2))
    assert set(both) == {-100.0, 100.0}


def test_glitch_with_no_fraction_changes_nothing():
    assert glitch([1.0, 2.0, 3.0], 0).tolist() == [1.0, 2.0, 3.0]


def test_glitch_rejects_unknown_options():
    with pytest.raises(ValueError, match="where"):
        glitch([1.0, 2.0], where="middle")
    with pytest.raises(ValueError, match="direction"):
        glitch([1.0, 2.0], direction="sideways")


def test_simulate_yields_the_requested_number_of_datasets():
    datasets = list(simulate(7, n=12, rng=np.random.default_rng(1)))

    assert len(datasets) == 7
    for x, y in datasets:
        assert x.tolist() == list(range(12))
        assert y.shape == (12,)


def test_simulate_is_reproducible_with_a_seeded_generator():
    first = list(simulate(3, glitches=0.2, rng=np.random.default_rng(4)))
    second = list(simulate(3, glitches=0.2, rng=np.random.default_rng(4)))

    for (_, y1), (_, y2) in zip(first, second, strict=True):
        assert np.array_equal(y1, y2)
    assert not np.array_equal(first[0][1], first[1][1])


def test_simulate_normal_noise_has_mean_zero_and_the_requested_sd():
    residuals = np.concatenate(
        [y - (1 + 2 * x) for x, y in simulate(200, sd=3, rng=np.random.default_rng(1))]
    )

    assert residuals.mean() == pytest.approx(0, abs=0.2)
    assert residuals.std() == pytest.approx(3, abs=0.15)


def test_simulate_exponential_noise_is_skewed_with_mean_zero():
    residuals = np.concatenate(
        [
            y - (1 + 2 * x)
            for x, y in simulate(200, noise="exponential", rng=np.random.default_rng(1))
        ]
    )

    assert residuals.mean() == pytest.approx(0, abs=0.2)
    assert residuals.std() == pytest.approx(3, abs=0.2)
    assert np.median(residuals) < -0.5


def test_simulate_follows_the_requested_line():
    x, y = next(simulate(sd=0, intercept=5, slope=-1.5, n=10))

    assert np.allclose(y, 5 - 1.5 * x)


def test_simulate_glitches_a_fraction_of_the_points():
    x, y = next(simulate(sd=0, glitches=0.1, size=50, rng=np.random.default_rng(3)))

    off_course = ~np.isclose(y, 1 + 2 * x)
    assert off_course.sum() == 3
    assert np.allclose((y - (1 + 2 * x))[off_course], 50)


def test_simulate_passes_glitch_options_through():
    x, y = next(simulate(sd=0, glitches=0.2, where="end", direction="down", size=10))

    assert (y - (1 + 2 * x))[-6:].tolist() == [-10.0] * 6
    assert np.allclose((y - (1 + 2 * x))[:-6], 0)


def test_simulate_is_clean_by_default():
    for x, y in simulate(5, sd=0):
        assert np.allclose(y, 1 + 2 * x)


def test_simulate_rejects_unknown_noise():
    with pytest.raises(ValueError, match="noise"):
        next(simulate(noise="uniform"))


def test_sample_yields_the_requested_number_of_samples():
    samples = list(sample(6, n=12, rng=np.random.default_rng(1)))

    assert len(samples) == 6
    assert all(values.shape == (12,) for values in samples)


def test_sample_is_reproducible_with_a_seeded_generator():
    first = list(sample(3, glitches=0.2, rng=np.random.default_rng(4)))
    second = list(sample(3, glitches=0.2, rng=np.random.default_rng(4)))

    for a, b in zip(first, second, strict=True):
        assert np.array_equal(a, b)
    assert not np.array_equal(first[0], first[1])


@pytest.mark.parametrize("noise", ["normal", "exponential", "t"])
def test_sample_noise_has_mean_zero_and_the_requested_sd(noise):
    values = np.concatenate(
        list(sample(400, noise=noise, sd=2, rng=np.random.default_rng(1)))
    )

    assert values.mean() == pytest.approx(0, abs=0.15)
    assert values.std() == pytest.approx(2, rel=0.15)


def test_sample_shapes_differ_between_distributions():
    exponential = np.concatenate(
        list(sample(200, noise="exponential", rng=np.random.default_rng(1)))
    )
    heavy = np.concatenate(list(sample(200, noise="t", rng=np.random.default_rng(1))))
    normal = np.concatenate(list(sample(200, rng=np.random.default_rng(1))))

    assert np.median(exponential) == pytest.approx(np.log(2) - 1, abs=0.05)
    assert np.abs(heavy).max() > 2 * np.abs(normal).max()


def test_sample_glitches_a_fraction_of_the_values():
    values = next(
        sample(sd=0, n=40, glitches=0.1, size=50, rng=np.random.default_rng(3))
    )

    assert (values != 0).sum() == 4
    assert set(values[values != 0]) == {50.0}


def test_sample_is_clean_by_default():
    for values in sample(5, sd=0):
        assert not values.any()


def test_simulate_accepts_heavy_tailed_noise():
    x, y = next(simulate(noise="t", rng=np.random.default_rng(2)))

    assert x.shape == y.shape == (30,)


def test_sample_rejects_unknown_noise():
    with pytest.raises(ValueError, match="noise"):
        next(sample(noise="uniform"))
