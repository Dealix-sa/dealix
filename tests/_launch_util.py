"""Shared path setup for the launch OS tests (self-contained, no heavy app deps)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

for _p in (str(ROOT), str(SCRIPTS)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

SEED = ROOT / "data" / "commercial_seed_leads.example.jsonl"
TEST_DAY = "2099-01-01"
