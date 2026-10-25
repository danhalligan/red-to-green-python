# Contributing

Issues and pull requests that add Python problems, fix bugs, or improve the
learning experience are welcome.

Keep exercises idiomatic for Python rather than reproducing APIs from another
language. Starter implementations should make the learning task clear without
including a completed answer. Tests should express behaviour with fixed inputs
or stable invariants; mark optional numerical optimisation tests `advanced`.

Test the concept, not production-grade robustness. These exercises check that
learners understood the idea, not that they wrote a perfect function, so do not
test input validation or other pathological usage (negative sizes, out-of-range
probabilities, empty or malformed inputs) unless handling it is the point of the
exercise. Learners are welcome to add such checks, but the tests should not
require them. Reference solutions may include them as good practice.

Do not make learners pass a random generator through their functions unless
controlling reproducibility is the goal of the exercise. Simulation exercises
should use the global `random` module: `exercises/conftest.py` seeds it before every
test, and a test of reproducibility calls `random.seed` itself. Choose
tolerances of about five standard errors, so a correct implementation passes
whatever sequence of numbers it happens to draw.

The collection is intended to be a set of interesting, independently
approachable puzzles, not a comprehensive Python course.

**Guiding principle:** Every substantial task should present an interesting
decision, reveal something surprising or enable a more rewarding challenge.
Remove or demote steps that are primarily mechanical without a worthwhile
payoff.

## Adding an exercise

Each exercise is a self-contained directory, `exercises/<topic>/<exercise>/`
(`snake_case`, so it is importable). A typical coding exercise needs only:

```text
exercises/<topic>/<exercise>/
    __init__.py
    README.md
    <exercise>.py
    test_<exercise>.py
```

Add an `investigate.ipynb`, a `data/` directory (data, expected outputs or
images) or a `loaders.py` only if the exercise needs them; do not generate
boilerplate files that serve no purpose. A new topic needs its own `__init__.py`.
Put code or data in `exercises/_shared/` only when several exercises genuinely
share it.

Every exercise README should have:

- An engaging title and a brief premise.
- A `**Difficulty:**` line (🌶️ gentle, 🌶️🌶️ takes some thought, 🌶️🌶️🌶️
  challenging) and the relevant prerequisites.
- A focused command, `uv run pytest exercises/<topic>/<exercise>/ -q`, and
  clear instructions that point to the starter code.
- Progressive hints where useful, and optional extensions or notebook
  investigations.

Then add the exercise to the catalogue in the root `README.md`, with the same
difficulty. Notebooks import with absolute package imports (for example
`from exercises.<topic>.<exercise>.<module> import ...`) and find their data
with `importlib.resources`, never `sys.path` or the working directory. Add a
`tests/test_<exercise>_data.py` integrity test if you add a dataset.

Before opening a pull request, run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --collect-only
uv run pytest tests -q
```

The exercise suite intentionally includes failures while learner stubs remain
unfinished. Do not turn those failures into CI failures by running the entire
suite as a required green check on the starter branch.
