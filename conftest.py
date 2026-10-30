"""Pytest configuration shared by every test in the repository."""

import os

# Matplotlib reads MPLBACKEND when it is first imported, and collecting the
# exercise tests imports it, so a fixture is too late. Without this, a GUI
# backend such as macOS's opens (and waits on) a window for every plt.show().
os.environ["MPLBACKEND"] = "Agg"
