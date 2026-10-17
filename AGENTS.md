# Agent Guide

This is a learning repository: most exercise functions are deliberately
unfinished, and their tests are expected to fail. Help the learner build
understanding, not just collect passing tests.

## Helping With Exercises

- Read the relevant problem page under `problems/`, starter code under
  `src/pyproblems/`, and corresponding tests before advising.
- Default to coaching. Use what the learner has already shared; if their
  approach is unclear, ask what they have tried and where they are stuck.
- Give one small hint at a time, using the problem's hint levels when available.
  Do not reveal full solutions, answer sections, or later investigation results
  unless explicitly requested.
- Ask before editing exercise implementations unless the learner has already
  explicitly requested those edits. A request for a hint or explanation is not
  permission to implement a solution.
- When a full solution is explicitly requested, explain the reasoning and
  encourage the learner to explain and test it themselves.
- Use the focused test command on the problem page. Explain relevant failures;
  do not implement unrelated stubs or run the entire exercise suite to chase
  green results.
- Do not weaken assertions, skip tests, or hard-code expected outputs to make
  an exercise pass. If a supplied test appears wrong, explain the suspected
  defect before proposing a correction.
- For notebook investigations, prompt the learner to predict, experiment and
  explain. Do not fill all `TODO` cells or invent observations. Preserve their
  work and use seeded random generators for reproducible experiments.
- In reviews, discuss reasoning, edge cases and trade-offs as well as test
  results. Passing tests alone is not the learning goal.

## Maintaining the Repository

Explicit requests to fix documentation, tests, infrastructure, or exercise
design are maintenance work: make the requested changes directly without a
tutoring dialogue. If the intent is genuinely ambiguous, ask whether the user
wants exercise help or a repository change.

- Preserve unfinished learner stubs when maintaining the starter repository;
  do not ship completed exercise solutions.
- Keep changes scoped to the request and preserve existing learner work.
- Follow [CONTRIBUTING.md](CONTRIBUTING.md) for contribution checks and
  [DEVELOPMENT.md](DEVELOPMENT.md) for setup and repository structure.
- For Markdown changes, run `uv run pytest tests/test_docs.py -q` to check
  documentation links and heading anchors. Intentional exercise failures are
  not maintenance regressions.