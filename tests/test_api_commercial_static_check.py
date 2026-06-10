"""Commercial API contract is read-only; no send surfaces declared as available."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import api_commercial_static_check as api  # noqa: E402


def test_api_static_check_passes():
    assert api.run() == []


def test_only_get_endpoints_allowed():
    assert all(ep.startswith("GET ") for ep in api.ALLOWED_READONLY)
