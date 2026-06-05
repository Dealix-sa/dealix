#!/usr/bin/env python3
"""Render nurture sequence drafts from data/growth/nurture_sequences.json.

Offline, deterministic. Sequences are DRAFTS only — no message is sent.
No cold WhatsApp, no LinkedIn automation (non-negotiables #2, #3).
Every message has exactly one CTA.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "growth" / "nurture_sequences.json"
OUT = ROOT / "reports" / "growth"


def main() -> int:
    if not DATA.exists():
        print("DEALIX_GROWTH_NURTURE=SKIP (no data file)")
        return 0
    payload = json.loads(DATA.read_text(encoding="utf-8"))
    sequences = payload.get("sequences", [])
    OUT.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Nurture Sequence Drafts — Dealix Self-Growth OS",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        f"Source: `data/growth/nurture_sequences.json` ({len(sequences)} sequences)",
        "",
        "> DRAFTS ONLY. No message is sent automatically. Founder approves before any send.",
        "> No cold WhatsApp. No LinkedIn automation. One CTA per message.",
        "",
    ]
    total_msgs = 0
    for seq in sequences:
        lines += [
            f"## {seq.get('name_ar', seq.get('slug', ''))} (`{seq.get('slug', '')}`)",
            "",
            f"- Trigger: `{seq.get('trigger', '')}`",
            f"- Audience: {seq.get('audience', '')}",
            f"- Channel: {seq.get('channel', '')}",
            "",
            "| Day | Subject | Intent | CTA |",
            "|---:|---|---|---|",
        ]
        for m in seq.get("messages", []):
            total_msgs += 1
            lines.append(
                "| {day} | {subject} | {intent} | {cta} |".format(
                    day=m.get("day", ""),
                    subject=m.get("subject_ar", "").replace("|", "/"),
                    intent=m.get("intent", ""),
                    cta=m.get("cta", ""),
                )
            )
        lines.append("")
    lines += [
        "## Governance",
        "",
        "- Every message routes through the founder approval step before sending.",
        "- No guaranteed-revenue language. Value references are estimates, not Verified value.",
        "- القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.",
        "",
    ]
    (OUT / "NURTURE_SEQUENCES.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DEALIX_GROWTH_NURTURE=PASS ({len(sequences)} sequences, {total_msgs} messages)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
