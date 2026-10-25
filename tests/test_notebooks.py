"""Smoke-test the supplied notebook setup, not the learner's analyses.

Each notebook's setup is its code up to the first ``TODO`` comment. Learner
work after that point is deliberately unfinished and is not executed here.
"""

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
ANALYSIS_DIR = ROOT / "analysis"
SPINNING_PLATES_DIR = ROOT / "exercises" / "data_analysis" / "spinning_plates"
# Notebooks are migrating from analysis/ into exercises/.
NOTEBOOKS = sorted(
    [*ANALYSIS_DIR.glob("*.ipynb"), *(ROOT / "exercises").rglob("*.ipynb")]
)


def notebook_id(path: Path) -> str:
    return str(path.relative_to(ROOT))


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
    for module in (
        "matplotlib",
        "numpy",
        "pandas",
        "scipy",
        "sklearn",
        "statsmodels",
        "yaml",
    ):
        pytest.importorskip(module)
    monkeypatch.setenv("MPLBACKEND", "Agg")


def test_notebooks_are_present():
    assert len(NOTEBOOKS) == 11


@pytest.mark.parametrize("path", NOTEBOOKS, ids=notebook_id)
def test_notebook_matches_schema(path):
    nbformat = pytest.importorskip("nbformat")
    nbformat.validate(nbformat.read(path, as_version=4))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=notebook_id)
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


def test_titanic_setup_reserves_disjoint_labelled_test_rows(science_stack):
    namespace = run_setup(ANALYSIS_DIR / "titanic.ipynb")
    train, test = namespace["X_train"], namespace["X_test"]
    y_train, y_test = namespace["y_train"], namespace["y_test"]

    assert train.shape == (1047, 11)
    assert test.shape == (262, 11)
    assert set(train.index).isdisjoint(test.index)
    assert set(train.index) | set(test.index) == set(range(1309))
    assert train.index.equals(y_train.index)
    assert test.index.equals(y_test.index)
    assert set(y_train) == set(y_test) == {0, 1}
    assert "Survived" not in train
    assert train["Age"].isna().any()
    assert train["Age"].dtype.kind == "f"
    assert namespace["passengers"]["Age"].iloc[0] == 29.0
    assert namespace["cv"].n_splits == 5


def test_spinning_plates_setup_points_at_the_data_files(science_stack):
    namespace = run_setup(SPINNING_PLATES_DIR / "investigate.ipynb")
    data_dir = namespace["data_dir"]

    for name in (
        "plate_reader_export.txt",
        "plate_layout.csv",
        "plate_run_record.json",
    ):
        assert data_dir.joinpath(name).is_file()
