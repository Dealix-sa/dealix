"""Site launch static check passes (SEO files + bilingual claim-safe copy deck)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import site_launch_static_check as slc  # noqa: E402


def test_site_static_check_passes():
    assert slc.run() == []


def test_banned_claims_defined():
    assert any("guaranteed" in c for c in slc.BANNED_CLAIMS)
