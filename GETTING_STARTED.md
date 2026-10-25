# Getting going in VS Code

This guide takes you from nothing installed to your first test turning from red
to green. It assumes you will use [Visual Studio Code](https://code.visualstudio.com/)
(VS Code), and no prior experience with testing tools.

**On this page:** [Install the tools](#1-install-the-tools) ·
[Get the code](#2-get-the-code-and-open-it) ·
[Set up the environment](#3-set-up-the-environment) ·
[Select the interpreter](#4-select-the-interpreter) ·
[Your first exercise](#5-your-first-exercise) ·
[Read a failure](#6-how-to-read-a-failing-test) ·
[Keep the output small](#7-keep-the-output-small) ·
[Testing panel](#8-use-the-testing-panel) ·
[Notebooks](#9-notebooks) ·
[Troubleshooting](#troubleshooting)

## 1. Install the tools

You need three things:

- [VS Code](https://code.visualstudio.com/).
- [uv](https://docs.astral.sh/uv/getting-started/installation/), which installs
  the right version of Python and the packages for you, so you do not need to
  install Python separately.
- [Git](https://git-scm.com/downloads), if you want to clone the repository. You
  can instead download it as a ZIP file.

## 2. Get the code and open it

Clone the repository (or choose **Code → Download ZIP** on its
[GitHub page](https://github.com/danhalligan/red-to-green-python) and unzip it):

```bash
git clone https://github.com/danhalligan/red-to-green-python
```

In VS Code choose **File → Open Folder...** and select the
`red-to-green-python` folder itself, not the folder that contains it. Opening
that exact folder is what lets VS Code find this project's settings.

When VS Code asks whether you trust the authors, choose **Yes, I trust the
authors**.

VS Code will also offer to install the project's recommended extensions. Accept:
they add Python support (Python, Pylance), automatic code formatting (Ruff) and
notebooks (Jupyter). If you missed the prompt, open the Extensions view
(`Ctrl+Shift+X`, or `Cmd+Shift+X` on a Mac), type `@recommended` in the search
box and install the ones listed.

## 3. Set up the environment

An *environment* is a private copy of Python and the packages this project needs.
Open a terminal inside VS Code with **Terminal → New Terminal** (or
`` Ctrl+` ``) and run:

```bash
uv sync --all-groups --extra science
```

This creates a `.venv` folder in the project and installs everything into it,
including the testing tool (pytest) and the packages for the data analysis
notebooks. It can take a minute or two the first time.

If you do not plan to use the notebooks, `uv sync --group dev` installs less.

You can also use the dev container instead (it needs Docker): choose **Dev
Containers: Reopen in Container** from the Command Palette. See
[DEVELOPMENT.md](DEVELOPMENT.md).

## 4. Select the interpreter

VS Code needs to know which Python to use for this project. You want the one in
`.venv`.

1. Open the Command Palette with `Ctrl+Shift+P` (`Cmd+Shift+P` on a Mac).
2. Type **Python: Select Interpreter** and press Enter.
3. Choose the entry marked `.venv`, for example `Python 3.12.x (.venv)`.

The chosen interpreter appears at the bottom right of the window. If you open a
Python file and the entry is missing, use **Enter interpreter path... → Find...**
and pick `.venv/bin/python` (`.venv\Scripts\python.exe` on Windows).

This project's settings already point to `.venv`, so on macOS and Linux VS Code
often picks the right one for you, but it is worth checking. The commands in a
terminal start with `uv run`, which always uses `.venv` whatever you selected.

## 5. Your first exercise

Open [Python Fundamentals](exercises/python_fundamentals/README.md) and
read **Q1: Exponentiation**. Tip: open a Markdown file's formatted preview with
`Ctrl+Shift+V` (`Cmd+Shift+V` on a Mac).

Every exercise works the same way: each one has its own folder under
`exercises/`, holding the instructions (`README.md`), the starter code and the
tests. A function in the starter code is
a *stub*: it has a name and a description but no working code. For this one,
open `exercises/python_fundamentals/fundamentals.py`:

```python
def exponentiate(values: Iterable[float]) -> list[float]:
    """Return the exponential of each value in an iterable."""
    raise NotImplementedError
```

Next to it, a test file (`test_fundamentals.py`) checks your function. The tests are
**expected to fail** at first: that is the *red* in red to green. Run this
exercise's test in the terminal:

```bash
uv run pytest exercises/python_fundamentals/test_fundamentals.py -k exponentiate -q
```

Now replace `raise NotImplementedError` with your own code and run the command
again. Keep going until the test passes.

## 6. How to read a failing test

Here is what you see before you write anything:

```text
F                                                                        [100%]
=================================== FAILURES ===================================
_____________________ test_exponentiate_accepts_iterables ______________________

    def test_exponentiate_accepts_iterables():
>       values = exponentiate([0.0, 1.0, 2.0])
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

exercises/python_fundamentals/test_fundamentals.py:23: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

values = [0.0, 1.0, 2.0]

    def exponentiate(values: Iterable[float]) -> list[float]:
        """Return the exponential of each value in an iterable."""
>       raise NotImplementedError
E       NotImplementedError

exercises/python_fundamentals/fundamentals.py:8: NotImplementedError
=========================== short test summary info ============================
FAILED exercises/python_fundamentals/test_fundamentals.py::test_exponentiate_accepts_iterables - NotI...
1 failed, 33 deselected in 0.03s
```

Read it from the bottom up:

- **The last line** is the score: `1 failed`. You want `1 passed`. The 33
  `deselected` tests are other exercises that your `-k exponentiate` filter
  skipped.
- **The `FAILED` line** names the failing test, and the reason is after the dash.
- **Lines starting with `E`** are the error. `NotImplementedError` means "this
  function is still a stub": you have not written it yet.
- **Lines starting with `>`** point to the line that went wrong, and the
  `file:line` below it says where it is.
- **The first `F`** (and `.` for a pass) is one character per test.

When you have written code that runs but gives the wrong answer, the message
changes. This is what a function returning the squares of the values looks like:

```text
>       assert values == pytest.approx([1.0, math.e, math.e**2])
E       assert [0.0, 1.0, 4.0] == approx([1.0 ±...95 ± 7.4e-06])
E         comparison failed. Mismatched elements: 3 / 3:
E         Index | Obtained | Expected
E         0     | 0.0      | 1.0 ± 1.0e-06
E         1     | 1.0      | 2.718281828459045 ± 2.7e-06
E         2     | 4.0      | 7.3890560989306495 ± 7.4e-06
```

Here `Obtained` is what your function returned and `Expected` is what the test
wanted. Each row is one value, so you can see exactly which ones are wrong. A
test describes the behaviour it wants, so read the test body (the line with `>`)
to see what it is checking.

When your code is right you see the *green* result:

```text
.                                                                        [100%]
1 passed, 33 deselected in 0.01s
```

## 7. Keep the output small

Running `uv run pytest` on its own runs **every** exercise in the repository.
Because most are unfinished, that prints about twenty thousand lines of red
failures (`634 failed, 167 passed`). That is normal, and it is not a sign that
anything is broken, but it is not helpful either. Instead, run only the tests for
the exercise you are working on, using the command at the end of its problem page.
A few options make the output shorter:

| Add this | What it does |
| --- | --- |
| `-k name` | Only run tests whose names contain `name`. Problem pages give you the command. |
| `-q` | A quieter report. |
| `--tb=short` | Shows the failing lines, not the whole function. |
| `--tb=no` | No error details at all, just a pass/fail line for each test. |
| `-x` | Stop at the first failure, so you can fix one thing at a time. |

For example, to work through a file one failure at a time:

```bash
uv run pytest exercises/python_fundamentals/ -x -q --tb=short
```

And to see just which tests pass and fail:

```bash
uv run pytest exercises/python_fundamentals/ -q --tb=no
```

You can combine them, and you can always scroll back to the first `E` line of the
first failure, which is usually the most useful one.

## 8. Use the testing panel

VS Code can run your tests for you, which many people find easier than the
terminal. This project is already set up for it.

1. Click the **Testing** icon (a flask or beaker) in the left sidebar.
2. After a moment you see a tree of folders, files and tests. If it is empty,
   see [Troubleshooting](#troubleshooting).
3. Hover over any item and click the **play button** to run it. You can run one
   test, a whole file or everything, but beware that running everything makes lots
   of red marks.
4. A red cross means a failure, and a green tick means a pass.
5. Click a failed test to see the message in the **Test Results** panel at the
   bottom. It is the same information as in the terminal, but only for that one
   test.

You can also run a single test from the editor. Open a test file (named
`test_...py`, next to the exercise's README)
and click the green play icon in the gutter, next to a `def test_...` line. A
failing test also marks the line in the *test* file that failed.

When you are working on one exercise, use the search box at the top of the
Testing panel to filter to your exercise's tests (for example `exponentiate`),
and use the **Run Test** button on just those. Failures in later exercises that
you have not reached yet will be out of the way.

## 9. Notebooks

Some problems use a Jupyter notebook (a file ending `.ipynb`) to explore your
functions. Open it in VS Code, click **Select Kernel** at the top right, choose
**Python Environments**, and pick the `.venv` entry. Run a cell with
`Shift+Enter`. Start with the first cell, which imports your functions: later
cells depend on it.

## Troubleshooting

- **`uv: command not found`.** uv is not installed, or the terminal was opened
  before you installed it. Install it from the link above, then open a new
  terminal.
- **The Testing panel is empty, or says no tests were found.** Check the
  interpreter at the bottom right (see
  [step 4](#4-select-the-interpreter)). Run `uv sync --all-groups --extra science`
  again, then use the Command Palette to run **Developer: Reload Window**.
- **`ModuleNotFoundError: No module named 'exercises'`.** Python cannot find the
  project's code. Run `uv sync` and check you selected the `.venv` interpreter.
  If your project folder lives inside a folder synced by iCloud (such as Desktop
  or Documents on a Mac) this can come and go. Move the project out of the synced
  folder.
- **Red underlines on imports.** VS Code is using a different Python than
  `.venv`. Select the interpreter again.
- **Every test fails, even after I finished an exercise.** Check you are running
  a command for that exercise (`-k name`) and that you saved the file
  (`Ctrl+S` / `Cmd+S`).

## Where next

Go back to the [README](README.md#the-problems-) and pick a problem. If you are
new to Python, [Python Fundamentals](exercises/python_fundamentals/README.md)
is the gentlest start. The [How to work through the problems](README.md#how-to-work-through-the-problems-)
section explains the 💡 hints and 🚀 extensions.
