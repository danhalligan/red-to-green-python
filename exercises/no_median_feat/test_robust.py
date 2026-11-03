import random

import numpy as np
import pytest

from exercises.no_median_feat.robust import (
    flag_outliers,
    mad,
    theil_sen,
    trimmed_mean,
)


def test_trimmed_mean_with_no_trimming_is_the_mean():
    assert trimmed_mean([1, 2, 3, 10], proportion=0) == pytest.approx(4)


def test_trimmed_mean_discards_a_proportion_from_each_end():
    values = [100, 1, 2, 3, 4, 5, 6, 7, 8, -50]

    assert trimmed_mean(values, proportion=0.1) == pytest.approx(4.5)


def test_trimmed_mean_ignores_the_order_of_the_values():
    assert trimmed_mean([9, 1, 5, 3, 7], proportion=0.2) == pytest.approx(5)


def test_trimmed_mean_approaches_the_median():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1000]

    assert trimmed_mean(values, proportion=0.49) == pytest.approx(np.median(values))


def test_mad_is_the_median_distance_from_the_median():
    assert mad([1, 2, 3, 4, 100], scale=False) == pytest.approx(1)
    assert mad([1, 2, 4, 8, 16], scale=False) == pytest.approx(3)


def test_mad_scales_to_estimate_a_normal_standard_deviation():
    assert mad([1, 2, 3, 4, 100]) == pytest.approx(1.4826, rel=1e-3)

    values = [random.gauss(0, 3) for _ in range(10_000)]

    assert mad(values) == pytest.approx(3, abs=0.2)


def test_mad_ignores_a_wild_value():
    values = [10, 11, 12, 13, 14, 15, 16]

    assert mad([*values, 1e6]) == pytest.approx(mad([*values, 17]), rel=0.5)


def test_flag_outliers_finds_wild_values():
    values = [9.8, 10.1, 10.0, 9.9, 10.2, 10.1, 9.7, 10.0, 35.0, 60.0]

    flags = flag_outliers(values)

    assert flags.dtype == bool
    assert flags.tolist() == [False] * 8 + [True, True]


def test_flag_outliers_finds_low_values_and_respects_the_threshold():
    values = [-40, 9, 10, 10, 10, 11, 11, 12, 12, 13]

    assert flag_outliers(values).tolist() == [True] + [False] * 9
    assert not flag_outliers(values, threshold=1000).any()


def test_theil_sen_recovers_an_exact_line():
    x = np.arange(10.0)

    fit = theil_sen(x, 2 + 3 * x)

    assert fit.intercept == pytest.approx(2)
    assert fit.slope == pytest.approx(3)


def test_theil_sen_shrugs_off_a_wild_point():
    x = np.arange(20.0)
    y = 2 + 3 * x
    y[-1] += 1000

    fit = theil_sen(x, y)

    assert fit.intercept == pytest.approx(2)
    assert fit.slope == pytest.approx(3)


def test_theil_sen_does_not_need_sorted_x():
    x = np.array([5.0, 1, 4, 0, 3, 2])

    fit = theil_sen(x, 1 - 2 * x)

    assert fit.slope == pytest.approx(-2)
    assert fit.intercept == pytest.approx(1)


def test_theil_sen_agrees_with_least_squares_on_well_behaved_data():
    x = np.arange(50.0)
    y = 4 + 2 * x + np.array([random.gauss(0, 1) for _ in x])

    fit = theil_sen(x, y)
    slope, intercept = np.polyfit(x, y, 1)

    assert fit.slope == pytest.approx(slope, abs=0.05)
    assert fit.intercept == pytest.approx(intercept, abs=1.5)
