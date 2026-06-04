#!/usr/bin/env python3
"""Lead intake validator — thin wrapper that reuses seed-leads validation rules.

No external calls, no CRM push. Validates a JSONL of leads (default: the example
seed file) and refuses to mark suppressed leads as contactable.
"""
from __future__ import annotations
import runpy, sys
from pathlib import Path

# Delegate to the canonical validator to avoid duplicated rules.
sys.argv = [sys.argv[0]]
runpy.run_path(str(Path(__file__).resolve().parent / "commercial_seed_leads_validate.py"), run_name="__main__")
