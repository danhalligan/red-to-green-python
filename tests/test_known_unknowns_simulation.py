import numpy as np
import pytest

from exercises.known_unknowns.simulation import POPULATIONS, coverage_study


def test_populations_have_a_true_mean_of_one():
    rng = np.random.default_rng(0)

    for draw in POPULATIONS.values():
        assert draw(rng, 100_000).mean() == pytest.approx(1.0, abs=0.02)


def test_coverage_study_reports_one_row_per_population_size_and_method():
    def methods(sample):
        return {"wide": (-100.0, 100.0), "empty": (50.0, 51.0)}

    table = coverage_study(
        methods,
        {"normal": 1.0, "exponential": 1.0},
        rng=np.random.default_rng(1),
        sizes=(5, 10),
        repetitions=20,
    )

    assert len(table) == 2 * 2 * 2
    wide = table[table["method"] == "wide"]
    empty = table[table["method"] == "empty"]
    assert (wide["coverage"] == 1.0).all()
    assert (empty["coverage"] == 0.0).all()
    assert (wide["mean_width"] == 200.0).all()
    assert (empty["mc_se"] == 0.0).all()


def test_coverage_study_is_reproducible_with_a_seeded_generator():
    def methods(sample):
        return {"around the mean": (sample.mean() - 0.5, sample.mean() + 0.5)}

    def study(seed):
        return coverage_study(
            methods,
            {"normal": 1.0, "exponential": 1.0},
            rng=np.random.default_rng(seed),
            sizes=(10,),
            repetitions=50,
        )

    assert study(3).equals(study(3))
    assert not study(3).equals(study(4))
