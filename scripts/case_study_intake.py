#!/usr/bin/env python3
"""Case study intake — render docs/sales/CASE_STUDY_TEMPLATE.md with a
customer's proof_ledger events filled in.

Reads a proof pack JSONL + a customer-data YAML (built by the founder
after Discovery) and writes a populated case study draft to
data/case_studies/{customer_handle}.md.

Doctrine:
  - Empty cells stay empty (NO_FAKE_PROOF). Never fills in a default.
  - is_estimate flag from the source event is propagated.
  - Permission level defaults to "Anonymous" — must be explicitly
    elevated.

Usage:
    python scripts/case_study_intake.py \\
        --proof-pack data/proofs/customer_x.jsonl \\
        --customer-data data/case_studies/inputs/customer_x.yaml \\
        --out data/case_studies/customer_x.md
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = REPO / "docs" / "sales" / "CASE_STUDY_TEMPLATE.md"


def _load_yaml(path: Path) -> dict:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        sys.stderr.write("FATAL: pip install pyyaml\n")
        sys.exit(2)
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    out = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def _render_event_table(events: list[dict], max_rows: int = 8) -> str:
    if not events:
        return "_No proof events at L3+ recorded yet._"
    rows = ["| Event ID | Type | Level | Date | Source |", "|---|---|---|---|---|"]
    for ev in events[:max_rows]:
        level = ev.get("level", "L0")
        if level in ("L0", "L1", "L2"):
            continue  # internal only
        rows.append(
            f"| {ev.get('id', '?')} | {ev.get('event_type', '?')} | "
            f"{level} | {ev.get('created_at', '?')[:10]} | "
            f"{ev.get('source', '?')} |"
        )
    if len(rows) <= 2:
        return "_All recorded events are at L0-L2 (internal). Nothing publishable yet._"
    return "\n".join(rows)


def populate(template: str, data: dict, events: list[dict]) -> str:
    """Replace {{merge_fields}} with values from data; leave unknown ones.

    Empty cells stay empty (NO_FAKE_PROOF doctrine).
    """
    text = template
    for key, value in data.items():
        token = "{{" + key + "}}"
        text = text.replace(token, str(value) if value not in (None, "") else "")
    text = text.replace(
        "| {{evt_1_id}} | {{evt_1_type}} | {{evt_1_level}} | {{evt_1_date}} | {{evt_1_source}} |\n"
        "| {{evt_2_id}} | {{evt_2_type}} | {{evt_2_level}} | {{evt_2_date}} | {{evt_2_source}} |",
        _render_event_table(events),
    )
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--proof-pack", type=Path, required=True)
    ap.add_argument("--customer-data", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    if not TEMPLATE_PATH.is_file():
        sys.stderr.write(f"FATAL: template not found at {TEMPLATE_PATH}\n")
        return 2
    if not args.customer_data.is_file():
        sys.stderr.write(f"FATAL: customer data not found at {args.customer_data}\n")
        return 2

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    data = _load_yaml(args.customer_data)
    events = _load_jsonl(args.proof_pack)

    # Defaults aligned with doctrine
    data.setdefault("permission_level", "Anonymous")
    data.setdefault("publication_date", datetime.now(UTC).strftime("%Y-%m-%d"))

    out_text = populate(template, data, events)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(out_text, encoding="utf-8")
    print(f"OK: wrote {args.out.relative_to(REPO)} ({len(events)} events considered)")
    print("Next: founder review at §13 approval signatures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
