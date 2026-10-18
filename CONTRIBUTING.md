# Contributing

Issues and pull requests that add Python problems, fix bugs, or improve the
learning experience are welcome.

Keep exercises idiomatic for Python rather than reproducing APIs from another
language. Starter implementations should make the learning task clear without
including a completed answer. Tests should express behaviour with fixed inputs
or stable invariants; mark optional numerical optimisation tests `advanced`.

The collection is intended to be a set of interesting, independently approachable puzzles, not a comprehensive Python course.

**Guiding principle:** Every substantial task should present an interesting decision, reveal something surprising or enable a more rewarding challenge. Remove or demote steps that are primarily mechanical without a worthwhile payoff.

Before opening a pull request, run:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --collect-only
uv run pytest tests/test_scaffold.py tests/test_data.py
```

The exercise suite intentionally includes failures while learner stubs remain
unfinished. Do not turn those failures into CI failures by running the entire
suite as a required green check on the starter branch.
