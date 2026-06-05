#!/usr/bin/env python3
"""Generate anonymized, case-safe proof-insight posts (no customer PII)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    REPORTS_DIR,
    assert_single_cta,
    ensure_dirs,
    read_json,
)

_OUT = REPORTS_DIR / "case_safe_content.md"
_INPUT = DATA_DIR / "anonymized_proof_inputs.json"

# Synthetic, fully anonymized fallback inputs. No real customer data, no PII.
# Each metric is labeled operational, never a guarantee.
_SAMPLE_INPUTS: list[dict[str, Any]] = [
    {
        "id": "pattern_followup_gap",
        "sector": "consulting",
        "pattern_ar": "غياب مالك واضح لمتابعة العملاء المحتملين يطيل زمن الرد.",
        "operational_metric_ar": "تقليص زمن الرد التشغيلي من أيام إلى ساعات بعد تعيين مالك.",
        "cta": "Free Diagnostic",
    },
    {
        "id": "pattern_proof_thin",
        "sector": "accounting-advisory",
        "pattern_ar": "اعتماد التجديد على الذاكرة بدل سجل إثبات موثق.",
        "operational_metric_ar": "بناء سجل إثبات بصف واحد لكل ارتباط خلال أسبوع تشغيلي.",
        "cta": "Command Sprint",
    },
    {
        "id": "pattern_delivery_blind",
        "sector": "it-services",
        "pattern_ar": "عدم قدرة العميل على رؤية حالة التسليم يرفع الأسئلة المتكررة.",
        "operational_metric_ar": "انخفاض الأسئلة المتكررة بعد إتاحة لوحة الإجراء التالي.",
        "cta": "Business OS Score",
    },
    {
        "id": "pattern_memory_loss",
        "sector": "recruitment",
        "pattern_ar": "فقدان سياق المرشح بين التفاعلات يكرر العمل نفسه.",
        "operational_metric_ar": "تقليل تكرار جمع نفس المعلومة بعد توحيد سجل السياق.",
        "cta": "Free Diagnostic",
    },
]

_PII_HINTS = ("@", "+9665", "05", "http://", "https://")


def load_inputs() -> list[dict[str, Any]]:
    """Load anonymized inputs from disk, falling back to the synthetic sample."""
    loaded = read_json(_INPUT)
    if isinstance(loaded, list) and loaded:
        return loaded
    return _SAMPLE_INPUTS


def _assert_no_pii(record: dict[str, Any]) -> None:
    """Guard against customer names, logos, or contact details in a record."""
    blob = " ".join(str(v) for v in record.values()).lower()
    for hint in _PII_HINTS:
        if hint.lower() in blob:
            raise ValueError(f"record {record.get('id')} may contain PII: {hint}")
    if "customer_name" in record or "company_name" in record or "logo" in record:
        raise ValueError(f"record {record.get('id')} carries a forbidden field")


def build_markdown(records: list[dict[str, Any]]) -> str:
    """Compose the case-safe markdown report from anonymized records."""
    ordered = sorted(records, key=lambda r: r["id"])
    lines: list[str] = []
    lines.append("# Dealix Case-Safe Proof Insights")
    lines.append("")
    lines.append(
        "Anonymized operational patterns only. No customer name or logo appears. "
        "Every metric is operational, not a guarantee.",
    )
    lines.append("")
    for record in ordered:
        _assert_no_pii(record)
        assert_single_cta(record["cta"])
        lines.append(f"## {record['id']}")
        lines.append("")
        lines.append(f"- Sector: {record['sector']}")
        lines.append(f"- Pattern: {record['pattern_ar']}")
        lines.append(
            f"- Operational metric (not a guarantee): {record['operational_metric_ar']}",
        )
        lines.append(f"- CTA: {record['cta']}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    """Write the case-safe content report and print a summary line."""
    ensure_dirs()
    records = load_inputs()
    markdown = build_markdown(records)
    _OUT.write_text(markdown, encoding="utf-8")
    size = len(markdown.encode("utf-8"))
    print(
        f"case_safe_content: wrote {len(records)} anonymized posts to {_OUT} ({size} bytes)",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
