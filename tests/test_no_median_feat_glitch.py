import numpy as np
import pytest

from exercises.no_median_feat.glitch import glitch


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
