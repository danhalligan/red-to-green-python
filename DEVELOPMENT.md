# Development

## Requirements

Use Python 3.11 or newer and [uv](https://docs.astral.sh/uv/). The project
keeps its core runtime dependency-free; NumPy, pandas, SciPy, Matplotlib, and
statsmodels are available through the optional `science` extra.

## Set up

From the repository root, install all development, notebook, and scientific
packages:

```bash
uv sync --all-groups --extra science
```

The dev container runs the same frozen sync after creation. Open the folder in
VS Code and choose **Dev Containers: Reopen in Container** to use its Python
3.12 environment. For local work, the sync command creates `.venv`; VS Code is
configured to use that interpreter.

To install only development tools without the scientific stack, use:

```bash
uv sync --group dev
```

## Project conventions

- Treat `README.md` as the learner-facing source of truth. Keep each exercise
  prompt and its focused test command together.
- Keep starter implementations intentionally incomplete; do not commit
  reference answers. Learner tests are expected to fail until the exercises
  are implemented.
- Keep the core package on the Python standard library. Scientific libraries
  belong in the optional `science` extra.
- Load packaged datasets through `importlib.resources` and verify they remain
  available from built distributions.
- Keep analysis and plotting tasks in `analysis/` notebooks. Commit notebooks
  without execution outputs or completed answers.

## Checks

The learner branch deliberately contains incomplete exercise stubs. Use
focused tests while working; unfinished exercises raise `NotImplementedError`
or fail their behavioral assertions. The scaffold and packaged-data checks
are expected to pass:

```bash
uv run pytest tests/test_scaffold.py tests/test_data.py
uv run pytest --collect-only
```

Run a single exercise or topic with its focused command from `README.md`. The
optional mixture-model contracts use the `advanced` marker:

```bash
uv run pytest -m advanced -q
```

Check Python code and formatting with:

```bash
uv run ruff check .
uv run ruff format --check .
```

Build both source and wheel distributions with:

```bash
uv build
```

To work through the scientific analysis prompts, launch JupyterLab:

```bash
uv run jupyter lab
```

The notebooks under `analysis/` are output-free learner workspaces. Their setup
cells import the relevant packaged data and optional scientific stack; analysis
cells are left for you to complete.

## Continuous integration

GitHub Actions checks supported Python versions, runs Ruff, confirms all tests
collect, runs the passing scaffold and data checks, builds distributions, and
verifies that installed wheel resources load. CI does not run all exercise
tests as a required green check because the starter branch intentionally
contains unfinished exercises.
