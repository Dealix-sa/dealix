#!/usr/bin/env python3
"""Generate daily CEO brief for founder decision-making."""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def _load_runtime_json(filename: str, default: Any) -> Any:
    """Load a JSON file from company/runtime/ with a fallback default."""
    p = Path("company/runtime") / filename
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return default


def _load_pipeline_data() -> dict[str, int]:
    data = _load_runtime_json("pipeline.json", {})
    defaults = {
        "prospect": 0,
        "qualified": 0,
        "proposal_sent": 0,
        "negotiation": 0,
        "won": 0,
    }
    if isinstance(data, dict):
        defaults.update({k: int(v) for k, v in data.items() if k in defaults})
    return defaults


def _load_revenue_data() -> dict[str, Any]:
    data = _load_runtime_json("revenue_mtd.json", {})
    defaults: dict[str, Any] = {
        "mtd_actual_sar": 0,
        "mtd_target_sar": 50000,
        "currency": "SAR",
    }
    if isinstance(data, dict):
        defaults.update(data)
    return defaults


def _load_risk_flags() -> list[str]:
    data = _load_runtime_json("risk_flags.json", [])
    if isinstance(data, list) and data:
        return [str(f) for f in data[:5]]
    return [
        "No active pipeline deals beyond prospect stage",
        "CEO brief relies on defaults — runtime data not yet populated",
        "External send gate is OFF — all outreach stays in draft",
        "Proof pack not confirmed for any active account",
        "No client-confirmed value events this month",
    ]


def build_brief(today: str | None = None) -> dict[str, Any]:
    """Assemble CEO brief data. Pure function — no external calls."""
    today = today or datetime.now(UTC).strftime("%Y-%m-%d")
    pipeline = _load_pipeline_data()
    revenue = _load_revenue_data()
    risk_flags = _load_risk_flags()

    actual = revenue.get("mtd_actual_sar", 0)
    target = revenue.get("mtd_target_sar", 50000)
    pct = round((actual / target) * 100, 1) if target else 0

    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "date": today,
        "revenue": {
            "mtd_actual_sar": actual,
            "mtd_target_sar": target,
            "attainment_pct": pct,
            "label_ar": "الإيرادات الشهرية",
        },
        "pipeline": {
            **pipeline,
            "label_ar": "مراحل خط الأنابيب",
        },
        "top_priorities": [
            "Convert at least one WARM account to proposal_sent stage",
            "Confirm proof pack readiness for top HOT account",
            "Review and approve outreach drafts before end of day",
        ],
        "top_priorities_ar": [
            "تحويل حساب دافئ واحد على الأقل إلى مرحلة إرسال العرض",
            "تأكيد جاهزية حزمة الإثبات للحساب الأكثر سخونة",
            "مراجعة واعتماد مسودات التواصل قبل نهاية اليوم",
        ],
        "risk_flags": risk_flags,
        "founder_decisions_needed": [
            "Approve or reject pending outreach drafts (check outbox/)",
            "Confirm ICP targeting list for this week",
            "Decide on proposal pricing for any deals in negotiation",
        ],
        "founder_decisions_needed_ar": [
            "اعتماد أو رفض مسودات التواصل المعلقة (راجع outbox/)",
            "تأكيد قائمة الاستهداف لهذا الأسبوع",
            "تحديد تسعير العروض للصفقات قيد التفاوض",
        ],
        "what_not_to_do_today": [
            "Do not send any external message without explicit approval",
            "Do not issue an invoice or contract automatically",
            "Do not merge any PR to main without founder review",
            "Do not share unverified metrics with prospects",
        ],
        "what_not_to_do_today_ar": [
            "لا ترسل أي رسالة خارجية بدون موافقة صريحة",
            "لا تصدر فاتورة أو عقد تلقائياً",
            "لا تدمج أي PR إلى الفرع الرئيسي بدون مراجعة المؤسس",
            "لا تشارك مقاييس غير مؤكدة مع العملاء المحتملين",
        ],
    }


def render_markdown(brief: dict[str, Any]) -> str:
    """Render brief dict to markdown string."""
    rev = brief["revenue"]
    pipe = brief["pipeline"]
    lines = [
        f"# CEO Brief — {brief['date']}",
        f"Generated: {brief['generated_at']}",
        "",
        "## Revenue Status (الإيرادات)",
        f"- MTD Actual: {rev['mtd_actual_sar']:,} SAR",
        f"- MTD Target: {rev['mtd_target_sar']:,} SAR",
        f"- Attainment: {rev['attainment_pct']}%",
        "",
        "## Pipeline (خط الأنابيب)",
    ]
    for stage, count in pipe.items():
        if stage != "label_ar":
            lines.append(f"- {stage}: {count}")
    lines += [
        "",
        "## Top 3 Priorities (الأولويات الثلاث الأولى)",
    ]
    for i, (en, ar) in enumerate(
        zip(brief["top_priorities"], brief["top_priorities_ar"]), 1
    ):
        lines.append(f"{i}. {en} / {ar}")
    lines += [
        "",
        "## Risk Flags (مؤشرات الخطر)",
    ]
    for flag in brief["risk_flags"]:
        lines.append(f"- {flag}")
    lines += [
        "",
        "## Founder Decisions Needed (قرارات يحتاجها المؤسس)",
    ]
    for en, ar in zip(
        brief["founder_decisions_needed"], brief["founder_decisions_needed_ar"]
    ):
        lines.append(f"- {en} / {ar}")
    lines += [
        "",
        "## What NOT To Do Today (ما لا تفعله اليوم)",
    ]
    for en, ar in zip(
        brief["what_not_to_do_today"], brief["what_not_to_do_today_ar"]
    ):
        lines.append(f"- {en} / {ar}")
    return "\n".join(lines)


def render_typescript_snapshot(brief: dict[str, Any]) -> str:
    """Render brief as a TypeScript const for web consumption."""
    serialized = json.dumps(brief, ensure_ascii=False, indent=2)
    return (
        "// Auto-generated — do not edit manually.\n"
        "// Source: scripts/commercial/generate_ceo_brief.py\n"
        f"export const ceoBriefSnapshot = {serialized} as const;\n"
    )


def run(today: str | None = None) -> dict[str, str]:
    """Generate and write all brief outputs. Returns paths written."""
    brief = build_brief(today=today)
    md = render_markdown(brief)
    ts = render_typescript_snapshot(brief)

    md_dir = Path("reports/ceo_brief")
    md_dir.mkdir(parents=True, exist_ok=True)
    md_path = md_dir / "latest.md"
    json_path = md_dir / "latest.json"
    md_path.write_text(md, encoding="utf-8")
    json_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2), encoding="utf-8")

    ts_dir = Path("apps/web/lib/generated")
    ts_dir.mkdir(parents=True, exist_ok=True)
    ts_path = ts_dir / "ceo-brief-snapshot.ts"
    ts_path.write_text(ts, encoding="utf-8")

    return {
        "markdown": str(md_path),
        "json": str(json_path),
        "typescript": str(ts_path),
    }


if __name__ == "__main__":
    paths = run()
    for key, path in paths.items():
        print(f"{key}: {path}")
