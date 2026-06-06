#!/usr/bin/env python3
"""Create a founder-operations customer workspace under customers/<slug>/.

Writes 12 bilingual (AR+EN) markdown working files for a single customer.
Each file carries a ``governance_status: draft`` front-matter-style line so
no file in the workspace is treated as an externally-sent artifact by default.

Self-contained: no third-party imports, runs under a plain python3.
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]

# Ordered list of (filename, title_en, title_ar, purpose_en, purpose_ar).
WORKSPACE_FILES: list[tuple[str, str, str, str, str]] = [
    (
        "00_intake.md",
        "Intake",
        "الاستقبال",
        "Capture the first known facts about the prospect before any outreach.",
        "تسجيل أول الحقائق المعروفة عن العميل المحتمل قبل أي تواصل.",
    ),
    (
        "01_company_intelligence.md",
        "Company Intelligence",
        "معلومات الشركة",
        "Hold sourced facts about the company; every fact needs a Source Passport.",
        "حفظ الحقائق الموثقة عن الشركة؛ كل حقيقة تحتاج جواز مصدر.",
    ),
    (
        "02_diagnostic_summary.md",
        "Diagnostic Summary",
        "ملخص التشخيص",
        "Summarise the revenue-acquisition diagnostic findings for this account.",
        "تلخيص نتائج تشخيص اكتساب الإيرادات لهذا الحساب.",
    ),
    (
        "03_command_sprint_scope.md",
        "Command Sprint Scope",
        "نطاق سبرنت القيادة",
        "Define the scope, boundaries, and exit criteria of the paid sprint.",
        "تحديد نطاق وحدود ومعايير إنهاء السبرنت المدفوع.",
    ),
    (
        "04_revenue_map.md",
        "Revenue Map",
        "خريطة الإيرادات",
        "Map where revenue enters, leaks, and could compound for this customer.",
        "رسم أين تدخل الإيرادات وأين تتسرب وأين يمكن أن تتراكم لهذا العميل.",
    ),
    (
        "05_proof_register.md",
        "Proof Register",
        "سجل الإثبات",
        "Track every claim and the evidence tier that backs it.",
        "تتبع كل ادعاء ومستوى الدليل الذي يسنده.",
    ),
    (
        "06_approval_register.md",
        "Approval Register",
        "سجل الموافقات",
        "Record every external action and its explicit founder approval state.",
        "تسجيل كل إجراء خارجي وحالة موافقة المؤسس الصريحة عليه.",
    ),
    (
        "07_next_action_board.md",
        "Next Action Board",
        "لوحة الإجراء التالي",
        "Hold the next concrete actions and their owners.",
        "حفظ الإجراءات التالية الملموسة وأصحابها.",
    ),
    (
        "08_executive_command_brief.md",
        "Executive Command Brief",
        "موجز القيادة التنفيذي",
        "One-page executive view the founder can read in under a minute.",
        "عرض تنفيذي من صفحة واحدة يقرأه المؤسس في أقل من دقيقة.",
    ),
    (
        "09_delivery_log.md",
        "Delivery Log",
        "سجل التسليم",
        "Append-only log of what was delivered, when, and the outcome.",
        "سجل إضافي لما تم تسليمه ومتى والنتيجة.",
    ),
    (
        "10_proof_pack.md",
        "Proof Pack",
        "حزمة الإثبات",
        "The 14-section proof pack assembled before any upsell is offered.",
        "حزمة الإثبات من 14 قسماً تُجمَّع قبل عرض أي توسعة.",
    ),
    (
        "11_upsell_recommendation.md",
        "Upsell Recommendation",
        "توصية التوسعة",
        "Recommend the next rung only after the proof pack is complete.",
        "التوصية بالدرجة التالية فقط بعد اكتمال حزمة الإثبات.",
    ),
]


def slugify(name: str) -> str:
    """Return a filesystem-safe slug for a customer name."""
    s = name.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s or "customer"


def _render_file(
    filename: str,
    title_en: str,
    title_ar: str,
    purpose_en: str,
    purpose_ar: str,
    customer_name: str,
) -> str:
    """Render the markdown body for a single workspace file."""
    today = date.today().isoformat()
    return (
        f"governance_status: draft\n"
        f"customer: {customer_name}\n"
        f"file: {filename}\n"
        f"created: {today}\n"
        f"mode: founder_operations\n"
        f"\n"
        f"# {title_ar} | {title_en}\n"
        f"\n"
        f"## الغرض | Purpose\n"
        f"\n"
        f"- AR: {purpose_ar}\n"
        f"- EN: {purpose_en}\n"
        f"\n"
        f"## الحالة | Status\n"
        f"\n"
        f"- governance_status: draft (no external action without explicit approval).\n"
        f"- Every external-facing claim requires a Source Passport and an approval record.\n"
        f"\n"
        f"## ملاحظات | Notes\n"
        f"\n"
        f"_Fill in during the engagement._\n"
    )


def _is_nonempty_workspace(workspace: Path) -> bool:
    """Return True if the workspace dir exists and holds any non-empty file."""
    if not workspace.is_dir():
        return False
    for child in workspace.iterdir():
        if child.is_file() and child.stat().st_size > 0:
            return True
    return False


def create_workspace(name: str, force: bool = False, base_dir: Path | None = None) -> Path:
    """Create the customer workspace and write all 12 files.

    Returns the workspace directory path. Refuses to overwrite an existing
    non-empty workspace unless ``force`` is True.
    """
    base = base_dir if base_dir is not None else (ROOT / "customers")
    workspace = base / slugify(name)
    if _is_nonempty_workspace(workspace) and not force:
        raise FileExistsError(
            f"workspace already exists and is non-empty: {workspace} (use force=True)"
        )
    workspace.mkdir(parents=True, exist_ok=True)
    for filename, title_en, title_ar, purpose_en, purpose_ar in WORKSPACE_FILES:
        body = _render_file(filename, title_en, title_ar, purpose_en, purpose_ar, name)
        (workspace / filename).write_text(body, encoding="utf-8")
    return workspace


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="customer name")
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing non-empty workspace",
    )
    args = parser.parse_args(argv)
    try:
        workspace = create_workspace(args.name, force=args.force)
    except FileExistsError as exc:
        print(f"BLOCKER: {exc}")
        return 1
    written = sorted(p.name for p in workspace.iterdir() if p.is_file())
    print(f"PASS: workspace created at {workspace}")
    print(f"PASS: {len(written)} files written")
    for name in written:
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
