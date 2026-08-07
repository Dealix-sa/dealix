#!/usr/bin/env python3
"""Test that outreach drafts have review_status pending."""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

def test_outreach_drafts_pending_review():
    rc = subprocess.call([
        sys.executable, str(REPO / "scripts" / "generate_outreach_drafts.py"),
        "--top", "3", "--language", "both", "--channel", "whatsapp", "--mode", "demo"
    ])
    assert rc == 0, "generate_outreach_drafts.py failed"
    exports = REPO / "business" / "persuasion" / "exports"
    files = sorted(exports.glob("outreach-drafts-*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    assert files, "No outreach drafts generated"
    drafts = json.loads(files[0].read_text(encoding="utf-8"))
    for d in drafts:
        assert d.get("review_status") == "pending_review", f"Draft {d} missing pending_review"
        assert "DRAFT" in d.get("disclaimer", ""), f"Draft {d} missing disclaimer"
