#!/usr/bin/env python3
"""Generate case-safe content TEMPLATES for the Dealix Self-Growth OS.

Offline, deterministic. Turns the Proof → Content loop into reusable, anonymized
templates. It does NOT read or invent customer data, names, or metrics:
real proof stories require a recorded ProofEvent + founder approval before
publishing (non-negotiables #4 fake proof, #8 external send approval).

Output: anonymized content scaffolds with [PLACEHOLDER] slots and an
anonymization checklist, one CTA each.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "growth"

TEMPLATES = [
    {
        "id": "CS-LINKEDIN",
        "title": "Case-safe LinkedIn post",
        "body": (
            "في إحدى شركات [القطاع]، المشكلة لم تكن [الافتراض الشائع]؛\n"
            "كانت [الخلل التشغيلي الحقيقي — مثل غياب next action واضح بعد كل محادثة].\n\n"
            "ما الذي تغيّر بعد Command Sprint: [وصف نوعي للوضوح — بدون أرقام غير مُتحقَّقة].\n\n"
            "CTA: ابدأ تشخيص Dealix."
        ),
    },
    {
        "id": "CS-INSIGHT",
        "title": "Case-safe anonymized insight (blog/newsletter)",
        "body": (
            "نمط متكرر نراه في [القطاع]: [الخلل التشغيلي].\n"
            "لماذا يحدث: [السبب الجذري].\n"
            "كيف نعالجه في Command Sprint: [الخطوة — Decision/Proof].\n\n"
            "CTA: احصل على Business OS Score."
        ),
    },
    {
        "id": "CS-PROOF-LEDGER",
        "title": "Public proof ledger line (no names)",
        "body": (
            "Proof Packs Delivered: [count]\n"
            "Average Clarity Improvement: qualitative\n"
            "Published Case Studies: [count] (pending approval)\n\n"
            "CTA: ابدأ تشخيص Dealix."
        ),
    },
]

CHECKLIST = [
    "No customer name, logo, or identifying detail.",
    "No metric unless it comes from a recorded ProofEvent / Value Ledger with a source_ref.",
    "Any number is labelled estimate unless Verified (القيمة التقديرية ليست قيمة مُتحقَّقة).",
    "Customer consent + founder approval obtained before publishing a real story.",
    "Exactly one CTA.",
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Case-Safe Content Templates — Dealix Self-Growth OS",
        "",
        f"Generated: {datetime.now(UTC).isoformat()}",
        "",
        "> Templates only. No customer data is read or invented here.",
        "> Real proof stories require a recorded ProofEvent + customer consent + founder approval.",
        "",
        "## Anonymization checklist (apply before publishing)",
        "",
    ]
    for c in CHECKLIST:
        lines.append(f"- [ ] {c}")
    lines.append("")
    for t in TEMPLATES:
        lines += [
            f"## {t['title']} (`{t['id']}`)",
            "",
            "```",
            t["body"],
            "```",
            "",
        ]
    (OUT / "CASE_SAFE_CONTENT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"DEALIX_GROWTH_CASE_SAFE_CONTENT=PASS ({len(TEMPLATES)} templates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
