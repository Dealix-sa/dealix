"""Pytest config for the V3 test bundle.

CI invokes this directory with ``--confcutdir=tests/v3``, which prevents
pytest from walking up to the repo root for conftest discovery and from
putting the repo root on ``sys.path``. Tests in this directory import
from the top-level ``scripts`` package (e.g. ``from scripts.score_leads
import score_lead``), so we need the repo root importable.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))