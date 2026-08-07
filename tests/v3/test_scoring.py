#!/usr/bin/env python3
"""Test lead scoring logic."""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

def test_score_leads_demo():
    rc = subprocess.call([sys.executable, str(REPO / "scripts" / "score_leads.py"), "--mode", "demo"])
    assert rc == 0, "score_leads.py demo mode failed"

def test_scoring_dimensions():
    from scripts.score_leads import score_lead
    lead = {"id": "t1", "fit": 35, "pain_clarity": 28, "budget_signal": 18, "urgency": 8}
    result = score_lead(lead)
    assert result["score"] == 89
    assert result["tier"] == "A"
