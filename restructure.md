# Implementation specification: Exercise-centred repository restructuring

**Repository:** `danhalligan/red-to-green-python`  
**Goal:** Reorganise the repository around self-contained learning exercises while preserving the existing red-to-green testing workflow.

## 1. Background and objectives

The repository is a pick-and-mix collection of Python exercises, rather than a software library intended for distribution.

Currently, related materials are separated across:

- `problems/` — learner-facing instructions.
- `src/pyproblems/` — starter implementations and datasets.
- `tests/` — automated tests that mark solutions.
- `analysis/` — investigative Jupyter notebooks.

This follows a conventional package structure but creates unnecessary navigation for learners.

**The primary objective is to make each exercise a discoverable, coherent unit, containing its instructions, code, tests, notebook and resources.**

Secondary objectives:

- Retain the benefits of Python modules, imports, pytest and `uv`.
- Make it easy to run tests for one exercise.
- Simplify adding new exercises.
- Reduce infrastructure designed exclusively for package distribution.
- Preserve the current learning experience, content and scientific datasets.

This is primarily a structural refactor. Do not redesign, solve or substantially rewrite exercises.

## 1a. Agreed decisions

- **Package name:** the top-level import package is `exercises`.
- **No backwards compatibility:** old `problems/` URLs and `pyproblems` imports
  do not need forwarding pages or shims. This is a clean break.
- **Catalogue:** use topic-level index READMEs (for example
  `exercises/algorithms/README.md`) linked from the root README, so adding an
  exercise rarely touches the root README. A topic index is not itself an
  exercise.
- **Solutions repository:** `red-to-green-python-solutions` (a sibling
  directory) mirrors the current `src/pyproblems/` paths. It must be
  restructured in lockstep with this repository, using the same path mapping, so
  every exercise has the same location in both. Treat it as part of the
  migration, not an afterthought.

## 2. Target architecture

Adopt this general structure:

```text
red-to-green-python/
├── README.md
├── AGENTS.md
├── DEVELOPMENT.md
├── CONTRIBUTING.md
├── pyproject.toml
├── uv.lock
│
├── exercises/
│   ├── __init__.py
│   │
│   ├── pythonic_python/
│   │   ├── __init__.py
│   │   ├── python_fundamentals/
│   │   │   ├── __init__.py
│   │   │   ├── README.md
│   │   │   ├── language.py
│   │   │   └── test_language.py
│   │   ├── object_oriented_python/
│   │   ├── gilded_rose/
│   │   └── ninety_nine_bottles/
│   │
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── word_ladder/
│   │   ├── rugby/
│   │   ├── sudoku/
│   │   └── sequence_alignment/
│   │
│   ├── data_analysis/
│   │   ├── __init__.py
│   │   ├── spinning_plates/
│   │   │   ├── __init__.py
│   │   │   ├── README.md
│   │   │   ├── plate_reader.py
│   │   │   ├── test_plate_reader.py
│   │   │   ├── investigate.ipynb
│   │   │   └── data/
│   │   │       ├── plate_reader_export.txt
│   │   │       ├── plate_layout.csv
│   │   │       └── plate_run_record.json
│   │   ├── mysterious_data/
│   │   ├── steak_tea_toast/
│   │   └── titanic/
│   │
│   ├── against_the_odds/
│   │   ├── __init__.py
│   │   ├── investigate.ipynb
│   │   ├── office_party/
│   │   ├── waiting_for_heads/
│   │   └── hundred_prisoners/
│   │
│   ├── models_of_life/
│   ├── uncertainty_and_simulation/
│   ├── parameter_estimation/
│   ├── generative_models/
│   │
│   └── _shared/
│       ├── __init__.py
│       ├── data.py
│       └── data/
│           └── words.txt
│
└── tests/
    ├── test_docs.py
    ├── test_notebooks.py
    └── test_scaffold.py
```

The structure above is illustrative. Preserve current subject categories and make pragmatic choices where exercises share code.

### Structural rules

**A. One directory per coherent learning unit**

An exercise may contain several closely related questions. For example, *Python Fundamentals* should remain one unit, not become seven miniature projects.

**B. Use `README.md` as the main exercise document**

GitHub should display the instructions automatically when opening the exercise directory.

**C. Co-locate implementation and tests**

For example:

```text
exercises/algorithms/word_ladder/
    README.md
    word_ladder.py
    test_word_ladder.py
```

**D. Keep notebooks alongside their exercise**

Use `investigate.ipynb` where an exercise has one principal notebook.

**E. Keep exercise-specific data alongside the exercise**

For example, the *Spinning Plates* plate-reader export should live inside `spinning_plates/data/`.

**F. Preserve genuinely shared resources**

If multiple exercises depend on a word list or utility, place it under `exercises/_shared/`.

Shared notebooks or implementations can live at topic level when they genuinely support several neighbouring exercises.

Do not duplicate files simply to create identical directory structures.

**G. Use importable Python directory names**

Use `snake_case` for folders containing Python code. Keep the existing human-readable exercise titles in Markdown.

------
!IMPORTANT 

NOTE: In some cases we might share notebooks between problems. Following
restrucutre this might not be the right solution. We might want to share
data but separate the notebooks so each problem is more stand alone.

In these cases prompt me and ask me the question before implementing but
provide a recommendation.
-------

## 3. Packaging and environment

Retain:

- `uv`
- `pyproject.toml`
- `uv.lock`
- Existing dependency groups and the `science` extra.
- Standard Python module imports.
- Pytest and Ruff.

**Recommended packaging approach:** Make `exercises` an importable Python package and retain editable project installation through `uv sync`.

An example import should be:

```python
from exercises.data_analysis.spinning_plates.plate_reader import (
    parse_plate_export,
)
```

The exact function name should follow the existing implementation.

Configure Hatchling appropriately for the new package root. For example, the final wheel configuration can target `exercises` rather than `src/pyproblems`.

The objective is reliable imports in pytest, notebooks and VS Code, **not publishing a distributable package**.

The existing `pyproblems` distribution name may be changed to something more representative if useful, but avoid unnecessary metadata or lockfile changes during the pilot.

Do not introduce:

- `sys.path.append()` in notebooks.
- Custom dynamic module loaders.
- Per-exercise virtual environments.
- Separate dependency files for every exercise.
- A new plugin framework for discovering exercises.

One repository-level environment must remain sufficient.

## 4. Migration phases

### Phase 0 — Inventory and baseline

**Goal:** Understand dependencies and record what currently works.

Before moving files:

1. Inventory every problem page, implementation module, test module, notebook, dataset and supporting asset.
2. Create a mapping from existing paths to proposed locations.
3. Identify files shared across exercises.
4. Find all references to `pyproblems`, `problems/`, `analysis/`, `src/` and `tests/`.
5. Identify assumptions in the README, development documentation, agent instructions, pytest configuration and GitHub Actions.
6. Record baseline structural checks and test collection.
7. Record relevant GitHub Markdown anchors and relative links.
8. Inventory `tests/conftest.py` (the autouse `seeded_random` fixture and the
   `time_limit` fixture) and `tests/fixtures/` (`99_bottles.txt`,
   `animal_song_full.txt`, `animal_song_short.txt`, `dna.txt`). Record which
   tests consume each fixture file.
9. Inventory `../red-to-green-python-solutions` and extend the path mapping to
   it, so both repositories move to identical locations. Record a baseline in
   the solutions repository showing which tests pass against which solutions.
10. Inventory root-level files that are not listed above: `assets/`,
    `GETTING_STARTED.md`, `NEWS.md`, `.devcontainer/`, `.vscode/` and
    `.github/workflows/python-checks.yml`.

Pay special attention to existing many-to-many relationships:

- `statistics.py` supports multiple statistical investigations.
- `evolution.py` supports several stages of the Weasel exercise.
- The *Against the Odds* notebook covers three puzzles.
- The English word list is shared by Word Ladder and Wordsmith.
- The current `data.py` provides several dataset loaders.
- `mixture_models.py` and the Old Faithful investigation share material with parameter-estimation exercises.

Do not assume every source module belongs to precisely one problem page.

**Deliverable:** A migration inventory and agreed target directory mapping, committed as part of the migration work or documented in the PR.

### Phase 1 — Establish structure and migrate Spinning Plates

**Goal:** Prove the architecture on a representative, relatively complex exercise.

Create:

```text
exercises/data_analysis/spinning_plates/
    README.md
    plate_reader.py
    test_plate_reader.py
    investigate.ipynb
    data/
```

Move the existing files using `git mv` where possible.

Update:

- Exercise-local imports.
- Dataset loading.
- Notebook setup cells.
- The focused pytest command.
- Links within the exercise Markdown.
- README catalogue link.
- Relevant infrastructure checks.

Preserve the original plate measurements, metadata and incomplete learner functions exactly.

The exercise should be accessible from the root README with one click.

Its tests should run with:

```bash
uv run pytest exercises/data_analysis/spinning_plates/ -q
```

These tests are expected to fail where learner implementations remain incomplete.

Ensure that the notebook can be launched from the normal repository environment without modifying `sys.path`.

During this phase, permit both the original `pyproblems` package and the new `exercises` package to coexist temporarily. Do not migrate unrelated files merely to eliminate the old package immediately.

**Phase 1 acceptance criteria:**

- Spinning Plates instructions, source, tests, notebook and data are co-located.
- Its tests collect and execute with normal pytest.
- Its notebook setup still loads the intended files.
- No solution code or completed notebook investigation has been introduced.
- The main README links to the new location.
- The new structure works with `uv sync --all-groups --extra science`.

Stop and fix structural issues before migrating everything else.

### Phase 2 — Migrate independent exercises

**Goal:** Move exercises with simple one-to-one relationships.

Start with examples such as:

- Word Ladder.
- Rugby.
- Sudoku.
- Gilded Rose.
- 99 Bottles.
- Python Fundamentals.
- Object-oriented Python.
- Titanic.
- Game of Life.

Move instructions, implementations, tests, notebooks, fixtures and exercise-specific assets into their new directories.

Distribute `tests/fixtures/` files to the exercises that use them (for example
`99_bottles.txt` to `ninety_nine_bottles/`). If a fixture is used by several
exercises, keep a single copy under the nearest shared location and ask before
deciding where.

Apply each move to `red-to-green-python-solutions` in the same step, then run
the moved tests against the moved solutions to confirm that imports and data
paths still resolve.

Update imports and focused test commands.

Keep source and tests unchanged except where required by relocation.

Use one or more small, reviewable commits organised by topic, rather than one enormous undifferentiated file move.

**Acceptance criteria:**

- Every migrated exercise has a working focused test command.
- Tests produce the same expected red/green behaviour as before.
- No datasets, fixtures, images or notebook dependencies are missing.
- Learner-facing wording and hints remain unchanged except for paths and commands.

### Phase 3 — Migrate shared and multi-part exercises

**Goal:** Resolve exercises that do not have a simple one-to-one relationship between problem, implementation and notebook.

This phase requires judgement.

For example, *Against the Odds* can keep a shared notebook:

```text
exercises/against_the_odds/
    investigate.ipynb
    office_party/
        README.md
        birthday.py
        test_birthday.py
    waiting_for_heads/
        README.md
        coin_patterns.py
        test_coin_patterns.py
    hundred_prisoners/
        README.md
        prisoners.py
        test_prisoners.py
```

The shared notebook can import from the three sibling exercise modules using absolute package imports.

For the statistical exercises, prefer temporarily retaining a coherent shared module at topic level rather than splitting its implementation into many tiny modules.

For example, the sections *Standard Error*, *Bootstrap* and *Confidence Intervals* may continue sharing a statistical implementation and notebook if that reflects how the material has been designed.

If splitting a shared implementation would materially improve the learning experience, treat that as a separately reviewable change. Do not combine significant code redesign with the structural migration.

Move shared data only after all consumers have been identified.

**Acceptance criteria:**

- No duplicate implementations or unnecessary duplicated datasets.
- Shared imports are unambiguous.
- No circular dependencies are introduced.
- Multi-part learning progressions are preserved.
- Shared notebook setup continues to work.

### Phase 4 — Update repository infrastructure

**Goal:** Make the new layout the repository's canonical structure.

#### Pytest

Update `pyproject.toml` so pytest discovers tests from both:

- `exercises/` — learner exercise tests.
- `tests/` — repository infrastructure tests.

Use regular Python packages with `__init__.py` files where appropriate to avoid import-name collisions.

Ensure test names can repeat safely in different exercise packages.

Keep commands straightforward:

```bash
# One exercise
uv run pytest exercises/algorithms/word_ladder/ -q

# One topic
uv run pytest exercises/algorithms/ -q

# Collect everything
uv run pytest --collect-only
```

Do not create an unnecessary custom test runner.

#### Shared test fixtures and tooling configuration

- Move `tests/conftest.py` to `exercises/conftest.py` so the autouse
  `seeded_random` fixture and the `time_limit` fixture still apply to every
  exercise test. Verify seeding and timeouts still work; losing them would
  change red/green behaviour without causing an obvious error.
- Keep `tests/` for repository infrastructure tests only. If those need their
  own fixtures, give them a separate `tests/conftest.py`.
- Update `[tool.pytest.ini_options]` `testpaths` to `["exercises", "tests"]`.
- Update the Ruff `per-file-ignores` entry for `analysis/*.ipynb` to
  `exercises/**/*.ipynb`.
- While `pyproblems` and `exercises` coexist (Phases 1-4), list both in
  `[tool.hatch.build.targets.wheel] packages`. Remove `src/pyproblems` in
  Phase 5.

#### Documentation checking

Update `tests/test_docs.py` to:

- Discover exercise README files recursively.
- Validate relative links and heading anchors.
- Confirm every exercise is discoverable from the main README, directly or through a clearly linked topic index.
- Avoid treating a topic-level index or shared infrastructure README as a standalone exercise.

Preserve the existing GitHub anchor and footnote validation where possible.

#### Notebook checks

Update `tests/test_notebooks.py` to discover notebooks recursively under `exercises/`.

Remove hard-coded assumptions such as:

- All notebooks are under `analysis/`.
- There are exactly ten notebooks.
- Notebook paths can be derived from a flat filename list.

Prefer explicit assertions that required named exercise notebooks exist, plus general recursive schema/setup checks.

Adapt tests that currently use fixed notebook paths.

Keep the distinction between runnable setup cells and intentionally unfinished learner investigations.

#### Data checks

Replace reliance on one global `pyproblems.datasets` namespace with exercise-local data paths and shared loaders where appropriate.

Use `pathlib` or `importlib.resources` consistently. Prefer paths derived from the owning module rather than the current working directory.

Preserve source attribution and licence notices alongside their data.

Keep dataset-integrity tests in `tests/` (they are repository infrastructure, not learner exercises), one file per dataset-owning exercise or shared resource (for example `tests/test_spinning_plates_data.py`), so adding an exercise does not mean editing a shared file. Read the data from the exercise's package path, and retain meaningful checks of row counts, schema and expected values.

#### GitHub Actions

Preserve checks for:

- Dependency installation.
- Ruff linting and formatting.
- Test collection.
- Documentation links.
- Notebook setup.
- Repository infrastructure checks.

**Remove CI steps whose only purpose is checking the contents of built wheels or source distributions**, unless they are needed for the retained editable-installation approach.

Keep a simple import/setup smoke test.

The pipeline must not require all learner exercise tests to pass.

#### VS Code and dev containers

Confirm that:

- Existing interpreter selection works.
- Test discovery finds tests in the new directories.
- Notebooks use the correct Python environment.
- No setting assumes that source code lives in `src/pyproblems`.

Update any relevant launch configurations, working-directory assumptions and extension recommendations.

#### Documentation and agent guidance

Update:

- Root `README.md`.
- `AGENTS.md`.
- `DEVELOPMENT.md`.
- `CONTRIBUTING.md`.
- `.github` workflows and templates, where applicable.
- `GETTING_STARTED.md` (setup and focused test commands).
- `NEWS.md` (add an entry describing the restructure and the new commands).
- `CONTRIBUTING.md`, specifically:
  - Replace the instruction that `tests/conftest.py` seeds `random` with
    `exercises/conftest.py`.
  - Replace the pre-PR command `uv run pytest tests/test_scaffold.py
    tests/test_data.py` with the new infrastructure checks (`tests/`, which
    includes the per-exercise data-integrity tests).
  - Add the "how to create a new exercise" convention from section 7.
  - Keep the guidance on not completing starter code and on testing the concept.
- `DEVELOPMENT.md`, specifically:
  - Project conventions: replace references to `problems/`, `analysis/` and
    "packaged datasets", and the requirement to verify datasets "from built
    distributions", with exercise-local README, notebook and `data/`
    conventions.
  - Replace "Keep the core package on the Python standard library" with an
    equivalent rule for `exercises/` (scientific libraries stay in the `science`
    extra).
  - Checks: replace `tests/test_scaffold.py tests/test_data.py` with the new
    infrastructure commands; replace "from its page in `problems/`" with "from
    the exercise README".
  - Remove the `uv build` section and the wheel/sdist wording under Continuous
    integration; describe the simplified CI from this document.
  - Describe the new repository structure and the `exercises/` / `tests/`
    split.

Agent instructions must explicitly say:

> Each exercise is self-contained. Read the exercise README, source and tests together. Most starter implementations are intentionally incomplete. Do not complete them during repository maintenance or attempt to make the full exercise suite pass.

Preserve the existing coaching-first guidance and rules about not giving away solutions.

### Phase 5 — Cleanup and final verification

**Goal:** Remove obsolete structure and establish the new conventions.

When every existing exercise has been migrated:

1. Remove obsolete `problems/`, `analysis/` and `src/pyproblems/` directories.
2. Remove unused dataset loaders and abandoned package configuration.
3. Remove old package-distribution verification tests.
4. Search again for stale references to old paths.
5. Check all catalogue links and exercise-specific test commands.
6. Verify all notebooks are output-free and contain no completed answers.
7. Verify that no learner functions were accidentally implemented.
8. Update documentation to explain how to create a new exercise.

No forwarding pages or backwards-compatibility shims are required for old `problems/` URLs or `pyproblems` imports.

Confirm `red-to-green-python-solutions` has the same structure, contains no leftover `src/pyproblems` paths, and that every exercise's solutions pass the new co-located tests.

Produce a final migration summary noting any intentional exceptions to the one-folder-per-exercise convention.

## 5. CI and validation policy

**Distinguish infrastructure tests from learner tests.**

The repository deliberately ships unfinished functions. A failing exercise test is not necessarily a regression.

Infrastructure checks must pass, including:

- Import/setup smoke tests.
- Documentation links.
- Dataset integrity.
- Notebook setup.
- Ruff.
- Pytest collection.

Run focused learner tests and compare their behaviour before and after migration.

For tests that were already red, verify that failures still arise from the intended learner stubs or assertions, not from broken imports, missing data or file paths.

Do not modify tests to make the build superficially green.

A successful structural migration does **not** mean `uv run pytest` passes every exercise.

## 6. Principles and non-goals

### Principles

1. **Colocate by learning unit.** The exercise is the primary organising concept.
2. **Optimise for novice navigation.** A learner should not need to understand Python package internals to find the files.
3. **Keep idiomatic Python.** Use modules, imports and pytest normally.
4. **Prefer explicit over clever.** Avoid custom loaders, discovery frameworks or path manipulation.
5. **Keep shared infrastructure small.** Reuse common code only when there's a genuine cross-exercise need.
6. **Preserve learner challenges.** Do not reveal answers, pre-fill notebooks or weaken tests.
7. **Separate migration from redesign.** Move first; improve individual exercises in later changes.
8. **Preserve scientific data integrity.** No regenerated or altered fixtures unless explicitly required.
9. **Preserve discoverability.** GitHub READMEs, main catalogue links and focused commands should work together.
10. **Keep phases independently verifiable.** Do not leave broken imports or documentation between phases.
11 **Make it easy to add new problems** Restructure should facilitate easily expanding the set of questions and should not require touching 
large shared files. 

### Non-goals

This migration is not intended to:

- Publish a Python package.
- Rewrite the exercises.
- Implement missing learner functions.
- Create a full exercise-management framework.
- Introduce an automated grading service.
- Require each exercise to have its own environment.
- Eliminate useful shared modules merely to achieve a uniform directory tree.
- Reorganise topics or change the educational progression.

## 7. Suggested contributor convention

After migration, document a simple convention for new exercises.

A typical coding exercise should need only:

```text
exercises/topic/exercise_name/
    README.md
    exercise_name.py
    test_exercise_name.py
```

Add an `investigate.ipynb`, `data/` or `assets/` directory only if needed.

Every learner-facing README should have:

- An engaging title and brief premise.
- Difficulty and relevant prerequisites.
- A focused pytest command.
- Clear instructions identifying the starter code.
- Progressive hints where useful.
- Optional extensions or notebook investigations.

Avoid generating boilerplate files that serve no purpose.

## 8. Final definition of done

The migration is complete when a learner can:

1. Open the repository README.
2. Choose an exercise.
3. Click through to one directory containing everything relevant.
4. Read the problem, find the starter implementation and tests.
5. Run its focused pytest command.
6. Edit the code and observe tests turn from red to green.
7. Open any associated notebook or dataset without manual path configuration.

Meanwhile:

- All existing exercises and investigations remain available.
- Every test collects.
- Infrastructure CI is green.
- No solutions have been accidentally revealed.
- The old four-way split between problems, source, tests and analysis is no longer needed.

**Execution instruction:** Implement the migration in the phases described above. Validate and commit each phase separately, retaining a clear audit trail of moves and import changes. Make pragmatic decisions about genuinely shared exercises, but do not expand the scope into an educational redesign.