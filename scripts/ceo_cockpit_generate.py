#!/usr/bin/env python3
"""Generate the CEO Cockpit — a single-screen status that composes V10 signals.

Aggregates revenue, pipeline, delivery, site, media, safety, finance
assumptions, risks, decisions, next actions, and no-go warnings into
outputs/ceo_cockpit/latest/CEO_COCKPIT.md. Read/compose/report only — never
sends anything externally, never fabricates traction.

Run: python scripts/ceo_cockpit_generate.py
"""

from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO / "outputs" / "ceo_cockpit" / "latest" / "CEO_COCKPIT.md"

NON_NEGOTIABLE = (
    "AI يجهّز ويحلّل ويصيغ ويُقيّم ويرتّب ويوصي. "
    "المؤسس يراجع ويعتمد ويوقّع ويبيع ويرسل يدويًا ويقرر. النظام لا يرسل خارجيًا أبدًا."
)

# Signal sources composed into the cockpit (read-only references).
SIGNAL_SOURCES = [
    ("Revenue (assumptions)", "outputs/profitability/PROFITABILITY_SUMMARY.md"),
    ("Pipeline", "data/commercial/pipeline.csv"),
    ("Delivery", "docs/scope-control-os/05_DELIVERY_ACCEPTANCE_GATES.md"),
    ("Site / Media", "docs/market-domination-os/07_CATEGORY_EDUCATION_PLAN.md"),
    ("Safety", "docs/safe-lifecycle-automation-os/00_SAFE_LIFECYCLE_AUTOMATION_OS.md"),
    ("Finance Assumptions", "outputs/profitability/PROFITABILITY_SUMMARY.md"),
    ("Moat", "outputs/moat_metrics/MOAT_METRICS_SUMMARY.md"),
    ("Verification", "outputs/v10_verification/V10_MASTER_VERIFICATION.md"),
]

NO_GO_WARNINGS = [
    "الإرسال الخارجي (Email / WhatsApp / LinkedIn) — ممنوع.",
    "أتمتة المنصّات / scraping / auto-submit — ممنوع.",
    "traction مزيّفة أو أرقام بدون evidence — ممنوع.",
    "إعلانات مدفوعة حيّة — ممنوع.",
    "ادعاءات أمنية/امتثال/قانونية غير مراجَعة — ممنوع.",
]


def _status(rel: str) -> str:
    return "present" if (REPO / rel).exists() else "missing"


def build_cockpit(now: str) -> str:
    lines = ["# CEO Cockpit — Dealix (Composed Snapshot)", "", f"_Generated: {now}_", ""]
    lines += [f"> {NON_NEGOTIABLE}", ""]

    lines += ["## Signals — الإشارات المجمّعة", "", "| Area | Source | Status |", "|---|---|---|"]
    for label, rel in SIGNAL_SOURCES:
        lines.append(f"| {label} | `{rel}` | {_status(rel)} |")
    lines.append("")

    lines += [
        "## Decision Queue — طابور القرارات",
        "",
        "- [القرارات المطلوبة — راجع `docs/ceo-cockpit-os/04_DECISION_QUEUE.md`]",
        "",
    ]
    lines += [
        "## Risk Queue — طابور المخاطر",
        "",
        "- [المخاطر المفتوحة — راجع `docs/ceo-cockpit-os/05_RISK_QUEUE.md` و`docs/institutional-scale-os/08_SCALE_RISK_REGISTER.md`]",
        "",
    ]
    lines += [
        "## Opportunity Queue — طابور الفرص",
        "",
        "- [الفرص المؤهَّلة — راجع `docs/ceo-cockpit-os/06_OPPORTUNITY_QUEUE.md`]",
        "",
    ]
    lines += [
        "## Next Actions — الخطوات التالية",
        "",
        "- مراجعة المخرجات المولّدة (drafts/reports) واعتمادها.",
        "- تشغيل V10 verification والتأكد من PASS.",
        "",
    ]
    lines += [
        "## Finance Assumptions — افتراضات مالية",
        "",
        "- كل الأرقام المالية افتراضات (assumptions) من ملفات example فقط. لا أرقام إيراد حقيقية.",
        "",
    ]
    lines += ["## NO-GO Warnings — تحذيرات", ""]
    for w in NO_GO_WARNINGS:
        lines.append(f"- {w}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = p.parse_args(argv)

    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(build_cockpit(now), encoding="utf-8")
    print(f"ceo_cockpit_generate: wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
