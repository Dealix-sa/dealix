"""Structural proof: the commercial scripts contain no live external-send transport."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "lib"))

import commercial_generate_400_drafts as gen  # noqa: E402
import commercial_safety_audit as audit  # noqa: E402

LIVE_SEND = [
    r"smtplib\.SMTP\s*\(",
    r"\.send_message\s*\(",
    r"requests\.post\s*\(\s*['\"]https?://",
    r"\.messages\.create\s*\(",
]


def test_scanned_scripts_have_no_live_send():
    scripts_dir = ROOT / "scripts"
    for name in audit.SCANNED_SCRIPTS:
        p = scripts_dir / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for pat in LIVE_SEND:
            assert not re.search(pat, text), f"{name} contains live-send pattern {pat}"


def test_all_drafts_blocked():
    drafts = gen.generate(400, "2099-03-01")
    assert all(d["external_send_blocked"] and not d["send_allowed"] for d in drafts)
