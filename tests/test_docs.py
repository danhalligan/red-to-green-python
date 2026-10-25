"""Check that links, heading anchors and footnotes in the Markdown docs resolve."""

import re
import unicodedata
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = [
    ROOT / "README.md",
    ROOT / "DEVELOPMENT.md",
    ROOT / "CONTRIBUTING.md",
    ROOT / "GETTING_STARTED.md",
    *sorted((ROOT / "exercises").rglob("README.md")),
]
EXERCISE_READMES = [
    path for path in DOCS if "exercises" in path.relative_to(ROOT).parts
]
DIFFICULTY = re.compile(r"\*\*Difficulty:\*\*\s*((?:🌶️)+)")


def github_slug(heading: str) -> str:
    """Return the anchor GitHub generates for a heading (emoji leave a hyphen)."""
    text = re.sub(r"`", "", heading)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text).lower()
    kept = (
        ch
        for ch in text
        if ch in "- _"
        or unicodedata.category(ch)[0] in "LMN"
        or unicodedata.category(ch) == "Pc"
    )
    return "".join(kept).replace(" ", "-")


def prose_lines(path: Path):
    """Yield the lines of a Markdown file outside fenced code blocks."""
    fenced = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        elif not fenced:
            yield line


def anchors(path: Path) -> set[str]:
    seen: dict[str, int] = {}
    found = set()
    for line in prose_lines(path):
        match = re.match(r"^#{1,6} (.*?)\s*$", line)
        if match:
            slug = github_slug(match.group(1))
            count = seen.get(slug, 0)
            seen[slug] = count + 1
            found.add(slug if count == 0 else f"{slug}-{count}")
    return found


def local_links(path: Path):
    """Yield (target, fragment) for every relative link in a Markdown file."""
    for line in prose_lines(path):
        line = re.sub(r"`[^`]*`", "", line)
        for target in re.findall(r"\]\(([^)\s]+)", line):
            if not target.startswith(("http://", "https://", "mailto:")):
                file, _, fragment = target.partition("#")
                yield file, fragment


@pytest.mark.parametrize("doc", DOCS, ids=lambda doc: str(doc.relative_to(ROOT)))
def test_links_and_anchors_resolve(doc):
    problems = []
    for file, fragment in local_links(doc):
        target = doc if file == "" else (doc.parent / file).resolve()
        if not target.exists():
            problems.append(f"missing file: {file}")
        elif fragment and target.suffix == ".md" and fragment not in anchors(target):
            problems.append(f"missing heading: {file}#{fragment}")
    assert not problems


@pytest.mark.parametrize("doc", DOCS, ids=lambda doc: str(doc.relative_to(ROOT)))
def test_footnotes_are_defined_and_used(doc):
    text = "\n".join(prose_lines(doc))
    text = re.sub(r"`[^`]*`", "", text)
    used = set(re.findall(r"\[\^([^\]]+)\](?!:)", text))
    defined = set(re.findall(r"^\[\^([^\]]+)\]:", text, re.MULTILINE))
    assert used == defined


def catalogue_entries() -> dict[Path, int]:
    """Map each exercise README linked from the root README to its chili count."""
    readme = ROOT / "README.md"
    entries: dict[Path, int] = {}
    bullets = re.split(r"^(?=- \[)", readme.read_text(encoding="utf-8"), flags=re.M)
    for bullet in bullets:
        link = re.match(r"- \[[^\]]*\]\(([^)#\s]+)", bullet)
        if not link:
            continue
        chilis = re.search(r"((?:🌶️)+)", bullet)
        entries[(readme.parent / link.group(1)).resolve()] = (
            len(chilis.group(1)) // len("🌶️") if chilis else 0
        )
    return entries


@pytest.mark.parametrize(
    "page", EXERCISE_READMES, ids=lambda page: str(page.relative_to(ROOT))
)
def test_exercises_are_listed_in_the_catalogue(page):
    assert page.resolve() in catalogue_entries()


@pytest.mark.parametrize(
    "page", EXERCISE_READMES, ids=lambda page: str(page.relative_to(ROOT))
)
def test_catalogue_difficulty_matches_the_exercise(page):
    match = DIFFICULTY.search(page.read_text(encoding="utf-8"))
    assert match, "the exercise README needs a **Difficulty:** line"
    chilis = len(match.group(1)) // len("🌶️")
    assert catalogue_entries().get(page.resolve()) == chilis


@pytest.mark.parametrize(
    "page", EXERCISE_READMES, ids=lambda page: str(page.relative_to(ROOT))
)
def test_exercises_with_tests_give_a_focused_command(page):
    exercise = page.parent
    if not any(exercise.glob("test_*.py")):
        pytest.skip("this exercise has no tests of its own")
    expected = f"uv run pytest {exercise.relative_to(ROOT)}"
    assert expected in page.read_text(encoding="utf-8")
