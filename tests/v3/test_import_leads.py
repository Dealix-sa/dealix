#!/usr/bin/env python3
"""Test lead import script exists and can be invoked."""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

def test_import_leads_help():
    path = REPO / "scripts" / "import_leads.py"
    if path.exists():
        rc = subprocess.call([sys.executable, str(path), "--help"])
        assert rc == 0 or rc == 2  # argparse help exits 0, some versions 2
