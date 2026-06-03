#!/usr/bin/env python3
"""Generate the trust review markdown."""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path


def _read(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="../dealix-ops-private")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if not root.exists():
        print(f"ERROR: private root missing: {root}")
        return 1

    approvals = _read(root / "trust" / "approval_log.csv")
    claims = _read(root / "trust" / "claim_review_log.csv")
    risks = _read(root / "trust" / "risk_register.csv")

    open_approvals = [a for a in approvals if (a.get("decision") or "").strip().lower() == "pending"]
    open_risks = [r for r in risks if (r.get("status") or "").strip().lower() in {"open", "mitigating"}]

    out = (
        f"# Trust Review\nGenerated on: {dt.date.today().isoformat()}\n\n"
        f"## Approvals\n- Total entries: {len(approvals)}\n- Pending: {len(open_approvals)}\n\n"
        f"## Claims\n- Total reviewed: {len(claims)}\n\n"
        f"## Risks\n- Total entries: {len(risks)}\n- Open / mitigating: {len(open_risks)}\n"
    )
    out_path = root / "trust" / "trust_review.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(out, encoding="utf-8")
    print(f"Wrote {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
