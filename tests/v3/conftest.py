"""Pytest conftest for the v3 test bundle.

Adds the repo root to sys.path so that ``from scripts.xxx import ...``
works in tests that import scripts as regular modules.
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
