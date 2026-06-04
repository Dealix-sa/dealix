#!/usr/bin/env python3
"""Compliance gate: every draft must have opt-out and pass the safety audit."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import out_dir  # noqa: E402


def main() -> int:
    d = out_dir()
    cp = d / "compliance_report.json"
    sa = d / "safety_audit.json"
    if not cp.exists() or not sa.exists():
        print("run commercial_score_drafts.py and commercial_safety_audit.py first", file=sys.stderr)
        return 1
    comp = json.loads(cp.read_text())
    safety = json.loads(sa.read_text())
    ok = bool(comp.get("all_have_opt_out")) and bool(safety.get("ok"))
    print(json.dumps({"gate": "compliance", "ok": ok,
                      "all_have_opt_out": comp.get("all_have_opt_out"),
                      "safety_ok": safety.get("ok")}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
