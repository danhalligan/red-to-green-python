"""Smoke-test the supplied notebook setup, not the learner's analyses.

Each notebook's setup is its code up to the first ``TODO`` comment. Learner
work after that point is deliberately unfinished and is not executed here.
"""

import json
from pathlib import Path

import pytest

ANALYSIS_DIR = Path(__file__).parents[1] / "analysis"
NOTEBOOKS = sorted(ANALYSIS_DIR.glob("*.ipynb"))


def setup_source(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    lines: list[str] = []
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        for line in "".join(cell["source"]).splitlines():
            if "TODO" in line:
                return "\n".join(lines)
            lines.append(line)
        lines.append("")
    return "\n".join(lines)


def run_setup(path: Path) -> dict:
    namespace: dict = {"__name__": "__notebook_setup__"}
    exec(compile(setup_source(path), path.name, "exec"), namespace)
    return namespace


@pytest.fixture
def science_stack(monkeypatch):
    for module in ("matplotlib", "numpy", "pandas", "scipy", "statsmodels", "yaml"):
        pytest.importorskip(module)
    monkeypatch.setenv("MPLBACKEND", "Agg")


def test_notebooks_are_present():
    assert len(NOTEBOOKS) == 7


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda path: path.stem)
def test_notebook_matches_schema(path):
    nbformat = pytest.importorskip("nbformat")
    nbformat.validate(nbformat.read(path, as_version=4))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda path: path.stem)
def test_notebook_setup_runs(path, science_stack):
    run_setup(path)


def test_steak_tea_toast_setup_loads_raw_responses_as_a_dataframe(science_stack):
    namespace = run_setup(ANALYSIS_DIR / "steak_tea_toast.ipynb")
    raw_responses = namespace["raw_responses"]

    assert raw_responses.shape == (79, 3)
    assert raw_responses.isna().sum().to_dict() == {"Steak": 1, "Toast": 0, "Tea": 6}


def test_mysterious_data_setup_loads_all_datasets(science_stack):
    namespace = run_setup(ANALYSIS_DIR / "mysterious_data.ipynb")

    assert len(namespace["coordinate_data"]) == 13


def test_old_faithful_setup_loads_the_dataset_as_a_dataframe(science_stack):
    namespace = run_setup(ANALYSIS_DIR / "old_faithful.ipynb")
    faithful = namespace["faithful"]

    assert faithful.shape == (272, 2)
    assert list(faithful.columns) == ["eruptions", "waiting"]
