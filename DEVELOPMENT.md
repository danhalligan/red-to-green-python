# Development

## Requirements

Use Python 3.11 or newer and [uv](https://docs.astral.sh/uv/). The project
keeps its core runtime dependency-free; NumPy, pandas, SciPy, Matplotlib,
statsmodels and scikit-learn are available through the optional `science` extra.

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

## Repository layout

Each exercise is one directory, `exercises/<topic>/<exercise>/`, holding
everything a learner needs:

```text
exercises/<topic>/<exercise>/
    README.md           the instructions (learner-facing)
    <module>.py         the starter code
    test_<module>.py    the tests, red until the exercise is solved
    investigate.ipynb   the notebook, if there is one
    data/               data and expected outputs, if needed
exercises/_shared/      code and data used by several exercises
exercises/conftest.py   fixtures shared by every exercise test
tests/                  repository checks that are expected to pass
```

A few exercises share code at topic level instead of duplicating it; for
example `exercises/uncertainty_and_simulation/uncertainty.py` and its tests serve
both Standard Error and Bootstrap.

## Project conventions

- Treat `README.md` and each exercise's own `README.md` as the learner-facing
  source of truth. The root README introduces the collection and lists every
  exercise with its difficulty (🌶️), a hook, and optional "try first"
  suggestions (only list a real dependency as **Needs**). Each exercise README
  keeps its prompts and focused test commands together. Link to a specific
  exercise heading rather than only the exercise.
- Keep starter implementations intentionally incomplete; do not commit
  reference answers. Learner tests are expected to fail until the exercises
  are implemented.
- Keep exercises that do not need the scientific stack on the Python standard
  library. Scientific libraries belong in the optional `science` extra.
- Load exercise data with `importlib.resources` relative to the owning package
  (for example `files("exercises.data_analysis.titanic_disaster")`), never through the
  working directory or `sys.path`. Put a loader in the exercise's `loaders.py`
  when more than one file needs it, and add a `tests/test_<exercise>_data.py`
  integrity test for each dataset.
- Keep analysis and plotting tasks in the exercise's `investigate.ipynb`. Commit
  notebooks without execution outputs or completed answers.
- Open an investigation with the question, not the answer. Give help as
  collapsible hints (`<details>` with a `<summary>`), in up to three levels:
  a nudge, a strategy, then implementation guidance without complete Python.
  Use collapsible hints for explanations containing math: GitHub does not render
  math in footnotes. Reserve footnotes for math-free explanations and notes.
  Put the explanation of a surprising result in a collapsible
  **What did you discover?** section after the investigation, and keep
  results out of headings, intros and hints that are visible beforehand.

## Checks

The learner branch deliberately contains incomplete exercise stubs. Use
focused tests while working; unfinished exercises raise `NotImplementedError`
or fail their behavioural assertions. The repository checks in `tests/` are
expected to pass:

```bash
uv run pytest tests -q
```

That runs the import smoke test, the data-integrity tests
(`tests/test_*_data.py`), the notebook setup checks and the documentation
checks. Confirm that every exercise test still collects with:

```bash
uv run pytest --collect-only
```

`tests/test_docs.py` checks that every relative link, heading anchor and
footnote in the Markdown docs resolves, that every exercise is listed in the
root README with the same difficulty as its own README, and that exercises with
their own tests give a focused `uv run pytest` command. Heading anchors follow
GitHub's rules, so a heading with an emoji ends in a hyphen (`#noisy-animals-`);
update links if you rename a heading. External links are not checked.

Run a single exercise or topic with its focused command from the exercise
README, for example:

```bash
uv run pytest exercises/algorithms/word_ladder/ -q   # one exercise
uv run pytest exercises/algorithms/ -q               # one topic
```

The optional mixture-model contracts use the `advanced` marker:

```bash
uv run pytest -m advanced -q
```

Check Python code and formatting with:

```bash
uv run ruff check .
uv run ruff format --check .
```

To work through the scientific analysis prompts, launch JupyterLab:

```bash
uv run jupyter lab
```

The `investigate.ipynb` notebooks are output-free learner workspaces. Their setup
cells import the relevant exercise code and data and the optional scientific
stack; analysis cells are left for you to complete.

## Continuous integration

GitHub Actions checks supported Python versions, runs Ruff, confirms all tests
collect, runs the repository checks (import smoke test, data integrity,
documentation links) and smoke-tests each notebook's setup code (everything
before its first `TODO` comment). CI does not run the exercise tests as a
required green check because the starter branch intentionally contains
unfinished exercises.
