#!/usr/bin/env python3
"""Quality gate: fail if avg quality below threshold or reports missing."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import out_dir  # noqa: E402

THRESHOLD = 2.5


def main() -> int:
    d = out_dir()
    qp = d / "quality_report.json"
    if not qp.exists():
        print("quality_report.json missing — run commercial_score_drafts.py", file=sys.stderr)
        return 1
    q = json.loads(qp.read_text())
    ok = q.get("avg_quality", 0) >= THRESHOLD
    print(json.dumps({"gate": "quality", "ok": ok, "avg_quality": q.get("avg_quality")}, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
