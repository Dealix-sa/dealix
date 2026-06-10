"""Secret scanner finds no real secrets in the Startup OS additions, but catches one."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import final_secret_and_risk_scan as scan  # noqa: E402


def test_no_secrets_in_additions():
    assert scan.scan() == []


def test_pattern_catches_a_fake_openai_key():
    # The detector should match an sk- style key (allow-list excludes 'example').
    line = "key = 'sk-" + "A" * 40 + "'"
    assert scan.PATTERNS["openai_key"].search(line)
    assert not scan.ALLOW.search(line)
