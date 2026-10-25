# Restructure: Phase 0 inventory and proposed mapping

Working document for [restructure.md](restructure.md). Delete both, and
`restructure-baseline.tsv`, in Phase 5. Nothing has been moved yet. The mapping
in section 3 is a **proposal for approval**; open questions are in section 6.

Both repositories are on a branch named `restructure`:
`red-to-green-python` (public) and `red-to-green-python-solutions` (private).

## 1. Baseline (main, before any move)

| Check | Result |
| --- | --- |
| `uv run pytest --collect-only` | 802 tests collected, no errors |
| Infrastructure tests (`test_docs` 77, `test_notebooks` 28, `test_data` 10, `test_scaffold` 2) | 117 pass |
| Full `uv run pytest` | 633 failed, 169 passed |
| Learner failures | 629 `NotImplementedError` (unfinished stubs); 4 `AssertionError` (see below) |
| Learner tests that already pass on the stubs | 52 (see below) |

The 4 assertion failures are deliberate: 3 in `test_gilded_rose` (the refactoring
exercise ships working code that the new-feature tests then break) and 1 in
`test_oop`. The 52 already-green learner tests are `alignment` 5, `game_of_life`
6, `gilded_rose` 27, `mixture_models` 2, `oop` 3, `prisoners` 4, `titanic` 5.
Those exercises supply some working code.

[restructure-baseline.tsv](restructure-baseline.tsv) records the outcome and
failure kind of every test. After each phase, re-run and compare by
`module::name`: only the path prefix should differ.

Solutions repository baseline: `scripts/verify.sh ../red-to-green-python` on the
unmodified `main` (log in `/tmp/r2g-verify-baseline.log`; result recorded in
section 7).

Notes on the spec:

- There are **11** notebooks, not ten.
- Root docs checked by `tests/test_docs.py` are a fixed list (README, DEVELOPMENT,
  CONTRIBUTING, GETTING_STARTED) plus `problems/**/*.md`. `restructure*.md` and
  `AGENTS.md`/`NEWS.md` are not checked.

## 2. Current inventory

### Problem pages (23) and what each uses

| Problem page | Module | Tests | Notebook | Data / assets |
| --- | --- | --- | --- | --- |
| pythonic-python/python-fundamentals | `fundamentals` | `test_fundamentals` | - | - |
| pythonic-python/object-oriented-python | `oop` | `test_oop` | `animal_playground` | `tests/fixtures/animal_song_{full,short}.txt` |
| pythonic-python/gilded-rose | `gilded_rose` | `test_gilded_rose` | - | - |
| pythonic-python/99-bottles | `bottles` | `test_bottles` | - | `tests/fixtures/99_bottles.txt` |
| algorithms/word-ladder | `word_ladder` | `test_word_ladder` | - | `words.txt` (+ `WORDS_LICENSE.txt`) via `data.load_words` |
| algorithms/rugby ("Try, try again") | `rugby` | `test_rugby` | - | - |
| algorithms/sudoku-solver | `sudoku` | `test_sudoku`, `test_sudoku_solver` | - | `sudoku.json` via `data.load_sudoku_data` |
| algorithms/sequence-alignment | `alignment` | `test_alignment` | - | `tests/fixtures/dna.txt` |
| data-analysis/mysterious-data | - | - | `mysterious_data` | `xy.json` via `data.load_xy_data` |
| data-analysis/steak-tea-and-toast | - | - | `steak_tea_toast` | `steak_toast_tea.csv` via `data.load_steak_toast_tea`; `assets/steak-toast-tea-poll.png` |
| data-analysis/titanic | `titanic` | `test_titanic` | `titanic` | `titanic.csv` via `data.load_titanic_data`; `TITANIC_SOURCE.md` |
| data-analysis/spinning-plates | `spinning_plates` | `test_spinning_plates` | `spinning_plates` | `plate_reader_export.txt`, `plate_layout.csv`, `plate_run_record.json` |
| generative-models/wordsmith | `wordsmith` | `test_wordsmith` | `wordsmith` | `words.txt` via `data.load_words` |
| models-of-life/game-of-life | `game_of_life` | `test_game_of_life` | `game_of_life` | `game_of_life_shapes.yaml` (read in the module itself) |
| models-of-life/weasel | `weasel` | `test_weasel`, `test_weasel_crossover`, `test_weasel_tournament` | `weasel` | - |
| against-the-odds/office-party | `birthday` | `test_birthday` | `against_the_odds` (shared) | - |
| against-the-odds/waiting-for-heads | `coin_patterns` | `test_coin_patterns` | `against_the_odds` (shared) | - |
| against-the-odds/100-prisoners | `prisoners` | `test_prisoners` | `against_the_odds` (shared) | - |
| uncertainty-and-simulation/standard-error | `uncertainty` (shared) | `test_uncertainty -k "standard_error and not bootstrap"` | `old_faithful`, `simulation_studies` (shared) | `faithful.csv` |
| uncertainty-and-simulation/bootstrap | `uncertainty` (shared) | `test_uncertainty -k bootstrap` | `old_faithful` (shared) | `faithful.csv` |
| uncertainty-and-simulation/confidence-intervals | none | none | `simulation_studies` (shared) | - |
| parameter-estimation/recovering-the-parameters | `likelihood` | `test_likelihood` | `old_faithful`, `simulation_studies` (shared) | `faithful.csv` |
| parameter-estimation/fitting-a-mixture | `mixture_models` | `test_mixture_models` | `old_faithful` (shared) | `faithful.csv` via `data.load_faithful_data` |

### Infrastructure and other files

- `tests/conftest.py`: autouse `seeded_random` (seeds `random` with 2026 before
  every test) and the `time_limit` fixture. **Not mentioned in the original
  spec.** Must become `exercises/conftest.py`.
- `tests/fixtures/`: `99_bottles.txt` (`test_bottles`), `animal_song_full.txt`
  (`test_oop`, `animal_playground` notebook, README link on the OOP page),
  `animal_song_short.txt` (`test_oop`), `dna.txt` (`test_alignment`).
- `tests/test_data.py`: 10 integrity tests across all datasets (reads
  `files("pyproblems.datasets")`). Split by dataset into exercise/shared
  directories.
- `tests/test_notebooks.py`: globs `analysis/*.ipynb`, asserts `== 11`, has
  fixed-path tests for steak, mysterious_data, old_faithful, titanic,
  spinning_plates. Setup cells are executed with the repository root as the
  working directory.
- `tests/test_docs.py`: fixed doc list, `problems/**` as `PROBLEM_PAGES`, and
  `test_problem_pages_are_listed_in_the_index`, which requires each problem page
  to be **linked directly from the root README**. Must change for topic indexes.
- `tests/test_scaffold.py`: imports `pyproblems` and `pyproblems.datasets`.
  Replace with a small `exercises` import smoke test.
- `src/pyproblems/data.py`: loaders for steak, sudoku, xy, faithful, titanic and
  words (stdlib only, uses `importlib.resources`). Imported by 6 test modules,
  `titanic.py`, `mixture_models.py` (inside a function; the docstring also names
  it) and 5 notebooks.
- `src/pyproblems/game_of_life.py` reads its YAML itself with
  `files("pyproblems.datasets")`.
- `assets/steak-toast-tea-poll.png`: used by the steak notebook and its page.
- Root docs: `README.md`, `AGENTS.md`, `GETTING_STARTED.md`, `NEWS.md`,
  `CONTRIBUTING.md`, `DEVELOPMENT.md`, `LICENSE`.
- Config: `pyproject.toml` (hatch `packages = ["src/pyproblems"]`, `testpaths =
  ["tests"]`, Ruff ignore for `analysis/*.ipynb`), `.vscode/settings.json`
  (`pytestArgs: ["tests"]`; `notebook.notebookFileRoot` is the workspace root),
  `.devcontainer/` (no path assumptions found), `.github/workflows/python-checks.yml`
  (runs `tests/test_scaffold.py tests/test_data.py`, `tests/test_notebooks.py`,
  `uv build` and a wheel-contents check).
- `dist/` is a gitignored local build output; ignore it.

### Many-to-many relationships

| Shared item | Shared by | Notes |
| --- | --- | --- |
| `uncertainty.py` | standard-error, bootstrap | Tests selected with `-k`. |
| `likelihood.py` | recovering-the-parameters; also used in `old_faithful` and `simulation_studies` notebooks | |
| `old_faithful.ipynb` | standard-error, bootstrap, recovering-the-parameters, fitting-a-mixture | Sections: The data, Standard error, Bootstrap, A normal model, Gaussian mixture, Waiting-time prediction. |
| `simulation_studies.ipynb` | standard-error (§1), recovering-the-parameters (§2), confidence-intervals (§3) | Sections map one-to-one onto problems. |
| `faithful.csv` | `old_faithful` notebook (spans two topics), `mixture_models` docstring/test, `test_data` | |
| `against_the_odds.ipynb` | office-party, waiting-for-heads, 100-prisoners | One section per puzzle. |
| `words.txt` + licence | word-ladder, wordsmith, `test_data` | Genuinely shared. |
| `weasel.py` | three test files, one notebook | One exercise, several stages. |
| `sudoku.py` | `test_sudoku` (checker warm-up) and `test_sudoku_solver` | One exercise. |
| `animal_song_full.txt` | `test_oop`, `animal_playground` notebook | One exercise. |
| Cross-page links | fundamentals <-> rugby, waiting-for-heads and rugby -> fundamentals Q6, sudoku-solver -> fundamentals, wordsmith -> word-ladder, recovering -> bootstrap and standard-error | Relative links must be rewritten. |

## 3. Proposed mapping (public repository)

Rules: keep existing module and test file names (the solutions overlay and the
`-k` commands depend on them); the notebook in each exercise is `investigate.ipynb`;
exercise data goes in the exercise's `data/`; topic folders and exercise folders
use `snake_case` and each has an `__init__.py`.

Root of every row below is `exercises/`.

| Exercise directory | README from | Module(s) | Tests | Notebook | Data / assets |
| --- | --- | --- | --- | --- | --- |
| `pythonic_python/python_fundamentals/` | `python-fundamentals.md` | `fundamentals.py` | `test_fundamentals.py` | - | - |
| `pythonic_python/object_oriented_python/` | `object-oriented-python.md` | `oop.py` | `test_oop.py` | `animal_playground` | `data/animal_song_{full,short}.txt` |
| `pythonic_python/gilded_rose/` | `gilded-rose.md` | `gilded_rose.py` | `test_gilded_rose.py` | - | - |
| `pythonic_python/ninety_nine_bottles/` | `99-bottles.md` | `bottles.py` | `test_bottles.py` | - | `data/99_bottles.txt` |
| `algorithms/word_ladder/` | `word-ladder.md` | `word_ladder.py` | `test_word_ladder.py` | - | uses `_shared` words |
| `algorithms/rugby/` | `rugby.md` | `rugby.py` | `test_rugby.py` | - | - |
| `algorithms/sudoku/` | `sudoku-solver.md` | `sudoku.py` | `test_sudoku.py`, `test_sudoku_solver.py` | - | `data/sudoku.json` |
| `algorithms/sequence_alignment/` | `sequence-alignment.md` | `alignment.py` | `test_alignment.py` | - | `data/dna.txt` |
| `data_analysis/mysterious_data/` | `mysterious-data.md` | (loader, Q3) | - | `mysterious_data` | `data/xy.json` |
| `data_analysis/steak_tea_toast/` | `steak-tea-and-toast.md` | (loader, Q3) | - | `steak_tea_toast` | `data/steak_toast_tea.csv`, `data/steak-toast-tea-poll.png` |
| `data_analysis/titanic/` | `titanic.md` | `titanic.py` | `test_titanic.py` | `titanic` | `data/titanic.csv`, `data/TITANIC_SOURCE.md` |
| `data_analysis/spinning_plates/` | `spinning-plates.md` | `spinning_plates.py` | `test_spinning_plates.py` | `spinning_plates` | `data/` (3 files) |
| `generative_models/wordsmith/` | `wordsmith.md` | `wordsmith.py` | `test_wordsmith.py` | `wordsmith` | uses `_shared` words |
| `models_of_life/game_of_life/` | `game-of-life.md` | `game_of_life.py` | `test_game_of_life.py` | `game_of_life` | `data/game_of_life_shapes.yaml` |
| `models_of_life/weasel/` | `weasel.md` | `weasel.py` | `test_weasel.py`, `test_weasel_crossover.py`, `test_weasel_tournament.py` | `weasel` | - |
| `against_the_odds/office_party/` | `office-party.md` | `birthday.py` | `test_birthday.py` | shared, Q1 | - |
| `against_the_odds/waiting_for_heads/` | `waiting-for-heads.md` | `coin_patterns.py` | `test_coin_patterns.py` | shared, Q1 | - |
| `against_the_odds/hundred_prisoners/` | `100-prisoners.md` | `prisoners.py` | `test_prisoners.py` | shared, Q1 | - |
| `uncertainty_and_simulation/standard_error/` | `standard-error.md` | shared, Q2 | shared, Q2 | Q2 | Q2 |
| `uncertainty_and_simulation/bootstrap/` | `bootstrap.md` | shared, Q2 | shared, Q2 | Q2 | Q2 |
| `uncertainty_and_simulation/confidence_intervals/` | `confidence-intervals.md` | none | none | Q2 | - |
| `parameter_estimation/recovering_the_parameters/` | `recovering-the-parameters.md` | `likelihood.py` | `test_likelihood.py` | Q2 | Q2 |
| `parameter_estimation/fitting_a_mixture/` | `fitting-a-mixture.md` | `mixture_models.py` | `test_mixture_models.py` | Q2 | Q2 |
| `_shared/` | - | `data.py` (words loader only) | `test_data.py` (words check) | - | `data/words.txt`, `data/WORDS_LICENSE.txt` |

Also: `exercises/conftest.py` (from `tests/conftest.py`), a `README.md` in each
topic directory as the topic index (README catalogue decision), and one root
`README.md` catalogue pointing at the topic indexes.

`tests/` keeps `test_docs.py`, `test_notebooks.py` and a rewritten
`test_scaffold.py`. `test_data.py` is dissolved into the exercise/shared
directories (10 tests: steak x2, xy, sudoku, faithful, words, titanic, plate x3).

Python test-name collisions: none (all basenames are unique), and every directory
has `__init__.py`, so repeated names would still be safe.

## 4. Solutions repository mapping

`solutions/` is copied over a public checkout, replacing files **by path**, so it
must mirror the new layout exactly.

| Now | After |
| --- | --- |
| `solutions/src/pyproblems/<module>.py` (19 files) | `solutions/exercises/<topic>/<exercise>/<module>.py`, same paths as section 3 |
| `solutions/analysis/<name>.ipynb` (11 files) | `solutions/exercises/<topic>/<exercise>/investigate.ipynb` (or the Q1/Q2 shared location) |
| `extras/*.py` (imports `pyproblems.*`) | Update to `exercises.*` imports |
| `extras/spinning_plates_fixtures.py` (`--write` default `src/pyproblems/datasets`) | Default to `exercises/data_analysis/spinning_plates/data` |
| `extras/test_spinning_plates.py` (reads `files("pyproblems.datasets")`) | Read from the exercise data directory |
| `extras/test_bottles_six_pack.py`, `extras/written_answers.md` link to `solutions/src/pyproblems/sudoku.py` | Update paths |
| `scripts/verify.sh` (`pytest --nbmake analysis`; clones `main` by default) | `--nbmake exercises`; during the migration run it against the local `restructure` checkout |
| `.github/workflows/verify.yml` (`--nbmake analysis`; checks out public `main`) | `exercises`; point `ref` at `restructure` while migrating, back to `main` at merge |
| `README.md` (layout section, links to `problems/` pages and `src/` paths) | Rewrite for the new layout |

Pre-existing observation: its README mentions `extras/spinning_plates_spec.md`,
which is not tracked in git. Not part of this work.

`solutions/**` file contents include non-exercise helper code that must stay in
sync with the public stub (for example `load_shape`). Moving files does not
change that, but the loader decision (Q3) affects it.

## 5. References to update (public repository)

Searched for `pyproblems`, `problems/`, `analysis/`, `src/`, `tests/`.

| Location | What |
| --- | --- |
| `README.md` | the catalogue links to every `problems/...` page; the quick start commands and `src/pyproblems/fundamentals.py`; the "Working with notebooks" section linking `analysis/` and four notebooks; intro text about `problems/` |
| `GETTING_STARTED.md` | `src/pyproblems/` and `tests/` descriptions, the sample failure output with paths, the `ModuleNotFoundError: pyproblems` troubleshooting entry, editor test-run instructions |
| `AGENTS.md` | "problem page under `problems/`, starter code under `src/pyproblems/`" |
| `CONTRIBUTING.md`, `DEVELOPMENT.md` | see restructure.md section 4 |
| `NEWS.md` | title "pyproblems 0.1.0"; add a restructure entry |
| `pyproject.toml` | hatch `packages`, `testpaths`, Ruff ignore glob, `name` (leave) |
| `.vscode/settings.json` | `python.testing.pytestArgs: ["tests"]` |
| `.github/workflows/python-checks.yml` | scaffold/data test command; remove `uv build` and wheel-check steps |
| 23 problem pages | `../../src/pyproblems/...`, `../../analysis/...#anchor`, `../../tests/...`, `../../assets/...`, and every `uv run pytest tests/test_x.py` command; heading anchors into notebooks (`old_faithful.ipynb#...`, `simulation_studies.ipynb#2.-Does...`, `against_the_odds.ipynb#...`) |
| 11 notebooks | `from pyproblems...` imports (see below), links back to `../problems/...`, `../src/...`, `../tests/...`, `../assets/...`, the spinning_plates `data_dir = files("pyproblems.datasets")` cell and its text, the Titanic data-source link |
| `src/pyproblems/game_of_life.py`, `titanic.py`, `mixture_models.py` | `files("pyproblems.datasets")` and `pyproblems.data` references |

Notebook `from pyproblems...` imports: `birthday`, `coin_patterns`, `prisoners`
(against_the_odds); `oop`; `game_of_life`; `data` (4 loaders); `likelihood`,
`mixture_models`, `uncertainty` (old_faithful); `spinning_plates`; `titanic`;
`weasel`; `wordsmith`. Notebook paths currently resolve with the repository root
as the working directory (`notebookFileRoot`), so they must not rely on the
working directory after the move; derive data paths from imported modules.

## 6. Open questions (please decide before the relevant phase)

**Q1. Against the Odds notebook.** One notebook covers three puzzles, one section
each. Recommendation: **split into three `investigate.ipynb` files**, one per
puzzle, since the sections are already independent and each page only links to
its own section. Alternative from the spec: keep one shared notebook at topic
level. Needed for Phase 3.

**Q2. Statistical exercises (largest decision).** `old_faithful` and
`simulation_studies` each serve three or four problems, and
`uncertainty.py` serves two. Recommendation:

- Share the **code** at topic level: keep `uncertainty.py` and its tests together
  (`exercises/uncertainty_and_simulation/`), since the two problems use `-k`
  selection anyway.
- Share the **dataset** `faithful.csv` in `exercises/_shared/data/`, used by both
  topics.
- **Split the notebooks per problem** (standard error, bootstrap, normal model,
  mixture, confidence intervals), because the sections already match problems 1:1
  and the cross-topic narrative ("uses the same data to explore uncertainty,
  prediction and model choice") would otherwise force a notebook to live under
  one topic. Cost: the shared "The data" introduction is repeated or shortened.
  This is a content change to the notebooks, so it needs your approval.

**Q3. Loaders for exercises that have only data and a notebook** (mysterious
data, steak tea toast, and also Titanic/sudoku/faithful). `data.py` currently
provides the loaders and the notebooks call them. After moving data into each
exercise, a notebook still needs a working-directory-independent way to locate
its file. Recommendation: a small `data.py` inside each exercise that has data
and no Python of its own (mysterious_data, steak_tea_toast), and for exercises
that already have a module keep the loader beside it. For Titanic, sudoku and
others whose module already exists, I would keep the existing `load_*` function
in a per-exercise `data.py` rather than editing the learner-facing stubs.
This keeps notebook code like `from exercises...mysterious_data.data import load_xy_data`
and avoids `sys.path` or cwd tricks.

**Q4. Module names that stutter or differ.** I propose keeping existing module
names (`bottles.py`, `oop.py`, `fundamentals.py`, `alignment.py`, `birthday.py`,
`coin_patterns.py`, `prisoners.py`, `likelihood.py`, `uncertainty.py`), not
renaming to match their folder (for example `ninety_nine_bottles.py`), so the
solutions overlay, `-k` commands and learner-facing text stay stable. Agree?

**Q5. Fixtures and assets directory name.** Expected-output files such as
`99_bottles.txt` and `animal_song_*.txt` are learner-visible (linked from the
README). I propose placing them in each exercise's `data/` for consistency with
the spec, and the steak poll image in the same folder (no separate `assets/`).
Agree?

**Q6. Topic index for single-exercise topics.** `generative_models` (1 exercise),
`models_of_life` (2) etc. would each get a topic README. For one-exercise topics
I suggest still adding the topic README (a short index) so the root README links
uniformly to topic indexes, and the root catalogue keeps its current prose.

## 7. Solutions baseline result

`scripts/verify.sh ../red-to-green-python` on unmodified `main` in both repos
passed fully: 802 tests pass with the solutions overlaid, 11 solution notebooks
execute under `nbmake` (about 3 minutes), 20 `extras/` tests pass, the extras
scripts run, and Ruff check and format are clean. Total about 7 minutes, mostly
the exercise suite and notebooks. This is the target to reproduce after each
phase.
