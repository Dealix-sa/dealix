#!/usr/bin/env python3
"""Validate generated JSON files are well-formed."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

def test_founder_dashboard_json():
    path = REPO / "business" / "_generated" / "founder-dashboard.json"
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "generated_at" in data
        assert "summary" in data
