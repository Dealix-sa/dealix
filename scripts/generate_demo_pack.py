#!/usr/bin/env python3
"""Generate a bilingual demo pack from the demo doc set.

Reads business/demo/*.md and produces a single dated bundle at
business/demo/exports/dealix-demo-pack-YYYY-MM-DD.md suitable for sharing
before a sales demo. Demo-only — no customer data is embedded.
"""

from __future__ import annotations

import argparse
import datetime as _dt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = ROOT / "business" / "demo"
EXPORTS = DEMO_DIR / "exports"

SECTIONS_BOTH = [
    ("DEALIX_DEMO_SCRIPT_AR.md", "## سيناريو العرض (عربي)"),
    ("DEALIX_DEMO_SCRIPT_EN.md", "## Demo Script (English)"),
    ("FOUNDER_DEMO_FLOW.md", "## Founder Demo Flow"),
    ("LIVE_WORKFLOW_REVIEW_SCRIPT.md", "## Live Workflow Review"),
    ("DEMO_QA_OBJECTIONS.md", "## Demo Q&A — Objections"),
    ("DEMO_CLOSE.md", "## Demo Close"),
]

SECTIONS_AR = [
    ("DEALIX_DEMO_SCRIPT_AR.md", "## سيناريو العرض"),
    ("FOUNDER_DEMO_FLOW.md", "## مسار المؤسس"),
    ("LIVE_WORKFLOW_REVIEW_SCRIPT.md", "## مراجعة Workflow حية"),
    ("DEMO_QA_OBJECTIONS.md", "## الأسئلة والاعتراضات"),
    ("DEMO_CLOSE.md", "## الإغلاق"),
]

SECTIONS_EN = [
    ("DEALIX_DEMO_SCRIPT_EN.md", "## Demo Script"),
    ("FOUNDER_DEMO_FLOW.md", "## Founder Demo Flow"),
    ("LIVE_WORKFLOW_REVIEW_SCRIPT.md", "## Live Workflow Review"),
    ("DEMO_QA_OBJECTIONS.md", "## Demo Q&A"),
    ("DEMO_CLOSE.md", "## Demo Close"),
]


def _read(name: str) -> str:
    path = DEMO_DIR / name
    if not path.exists():
        return f"_(missing: {name})_\n"
    return path.read_text(encoding="utf-8").strip() + "\n"


def _render(sections: list[tuple[str, str]], date: str, lang: str) -> str:
    parts = [
        f"# Dealix Demo Pack — {date} ({lang})",
        "",
        "_Demo material. No customer data. Founder-reviewed before any external share._",
        "",
    ]
    for name, heading in sections:
        parts.append(heading)
        parts.append("")
        parts.append(_read(name))
        parts.append("")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Dealix demo pack")
    parser.add_argument("--lang", choices=["ar", "en", "both"], default="both")
    args = parser.parse_args()

    EXPORTS.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()

    written: list[Path] = []
    if args.lang in ("both", "ar"):
        out = EXPORTS / f"dealix-demo-pack-{date}-ar.md"
        out.write_text(_render(SECTIONS_AR, date, "AR"), encoding="utf-8")
        written.append(out)
    if args.lang in ("both", "en"):
        out = EXPORTS / f"dealix-demo-pack-{date}-en.md"
        out.write_text(_render(SECTIONS_EN, date, "EN"), encoding="utf-8")
        written.append(out)
    if args.lang == "both":
        out = EXPORTS / f"dealix-demo-pack-{date}.md"
        out.write_text(_render(SECTIONS_BOTH, date, "AR+EN"), encoding="utf-8")
        written.append(out)

    for p in written:
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
