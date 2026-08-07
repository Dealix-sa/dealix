#!/usr/bin/env python3
"""Test daily operator runs in demo mode."""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

def test_daily_operator_demo():
    rc = subprocess.call([sys.executable, str(REPO / "scripts" / "dealix_daily_operator.py"), "--mode", "demo"])
    assert rc == 0, "dealix_daily_operator.py demo mode failed"
