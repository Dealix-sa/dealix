"""Secret/risk scanner reports the launch surface clean and flags real secrets."""

from __future__ import annotations

import re

from tests._lc_util import load_script


def test_launch_surface_is_clean():
    mod = load_script("final_secret_and_risk_scan")
    result = mod.scan()
    assert result["clean"] is True, f"findings: {result['findings']}"
    assert result["files_scanned"] > 0


def test_scanner_detects_a_real_key(tmp_path, monkeypatch):
    mod = load_script("final_secret_and_risk_scan")
    # A fabricated AWS-style key must be detected by the pattern set.
    sample = "AKIAIOSFODNN7EXAMPLE"  # canonical 20-char AWS example key
    assert re.search(mod.SECRET_PATTERNS["aws_access_key"], sample)


def test_placeholders_are_ignored():
    mod = load_script("final_secret_and_risk_scan")
    assert mod.PLACEHOLDER_RE.search("your-api-key-here")
    assert mod.PLACEHOLDER_RE.search("<REDACTED>")
