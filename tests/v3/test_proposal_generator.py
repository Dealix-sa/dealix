#!/usr/bin/env python3
"""Test proposal generation."""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

def test_generate_proposal():
    rc = subprocess.call([
        sys.executable, str(REPO / "scripts" / "generate_proposal.py"),
        "--account-id", "demo-test", "--offer", "Revenue OS",
        "--lang", "en", "--timeline", "21 days", "--mode", "demo"
    ])
    assert rc == 0, "generate_proposal.py failed"

def test_review_proposal_quality():
    rc = subprocess.call([
        sys.executable, str(REPO / "scripts" / "review_proposal_quality.py"), "--latest"
    ])
    assert rc == 0, "review_proposal_quality.py failed"
