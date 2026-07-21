#!/usr/bin/env python3
"""Verify that OpenShip remains an isolated, non-production Dealix pilot.

This verifier is intentionally dependency-free and checks both the adoption
policy and the existing Dealix deployment contracts. It never connects to an
OpenShip server and never reads secret values.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
POLICY_PATH = ROOT / "dealix/config/openship_adoption_policy.json"


def _read(path: Path) -> str:
    if not path.is_file():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def verify() -> list[str]:
    failures: list[str] = []

    try:
        policy = json.loads(_read(POLICY_PATH))
