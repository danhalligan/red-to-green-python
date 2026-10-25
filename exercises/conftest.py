import random
import signal
from contextlib import contextmanager

import pytest


@pytest.fixture(autouse=True)
def seeded_random():
    """Start every test from the same state of the global `random` module."""
    random.seed(2026)


@pytest.fixture
def time_limit():
    """Return a context manager that fails the test instead of letting it hang."""

    @contextmanager
    def limit(seconds):
        if not hasattr(signal, "SIGALRM"):  # No SIGALRM on Windows: run unguarded.
            yield
            return

        def on_alarm(signum, frame):
            pytest.fail(
                f"Took longer than {seconds} s. Is the work growing exponentially? "
                "Is your code repeating work it has already done?",
                pytrace=False,
            )

        previous = signal.signal(signal.SIGALRM, on_alarm)
        signal.setitimer(signal.ITIMER_REAL, seconds)
        try:
            yield
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous)

    return limit
