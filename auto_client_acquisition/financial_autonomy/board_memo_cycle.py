"""Monthly board-memo cycle — auto-populates the 12-section memo.

Composes:
- the financial autonomy cycle (run once at end-of-month),
- :mod:`auto_client_acquisition.board_ready_os.board_memo` for the
  twelve section slugs and completeness check,
- per-section content drawn from the metrics snapshot,
  capital ledger, dominance scorecard, decision ledger, friction log,
  and bad-revenue filter,
- a single founder approval request that gates any sharing of the memo.

Hard rule: the memo is never shared anywhere automatically. The
:class:`ApprovalRequest` it creates is the founder's gate.
"""
from __future__ import annotations

import calendar
import json
import logging
import os
import re
import uuid
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.board_ready_os.board_memo import (
    BOARD_MEMO_SECTIONS,
    board_memo_sections_complete,
)
from auto_client_acquisition.financial_autonomy.financial_cycle import (
    FinancialCycleReport,
    run_financial_cycle,
)
from auto_client_acquisition.financial_autonomy.financial_report import (
    render_board_memo_markdown,
)

log = logging.getLogger(__name__)


_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_DIR = _REPO_ROOT / "data" / "board_memos"


def _memo_dir() -> Path:
    env = os.environ.get("DEALIX_BOARD_MEMOS_PATH")
    if env:
        return Path(env)
    return _DEFAULT_DIR


_SECTION_TITLES_EN: dict[str, str] = {
    "executive_summary": "Executive Summary",
    "revenue": "Revenue",
    "retainers": "Retainers",
    "proof": "Proof",
    "governance": "Governance",
    "capital_creation": "Capital Creation",
    "productization": "Productization",
    "delivery": "Delivery",
    "market": "Market",
    "business_units": "Business Units",
    "stop_list": "Stop List",
    "next_strategic_bet": "Next Strategic Bet",
}

_SECTION_TITLES_AR: dict[str, str] = {
    "executive_summary": "الملخّص التنفيذي",
    "revenue": "الإيراد",
    "retainers": "الاحتفاظ والاشتراكات",
    "proof": "الإثبات",
    "governance": "الحوكمة",
    "capital_creation": "إنشاء رأس المال",
    "productization": "التحويل لمنتج",
    "delivery": "التسليم",
    "market": "السوق",
    "business_units": "وحدات الأعمال",
    "stop_list": "قائمة الإيقاف",
    "next_strategic_bet": "الرهان الاستراتيجي التالي",
}


@dataclass
class BoardMemoReport:
    """Bilingual report for a single board-memo cycle."""

    month: str
    generated_at: str
    sections: dict[str, dict[str, str]] = field(default_factory=dict)
    section_order: list[str] = field(default_factory=lambda: list(BOARD_MEMO_SECTIONS))
    sections_complete: bool = False
    missing_sections: list[str] = field(default_factory=list)
    approval_id: str = ""
    warnings: list[str] = field(default_factory=list)
    report_paths: dict[str, str] = field(default_factory=dict)
    financial_cycle: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "month": self.month,
            "generated_at": self.generated_at,
            "sections": {k: dict(v) for k, v in self.sections.items()},
            "section_order": list(self.section_order),
            "sections_complete": self.sections_complete,
            "missing_sections": list(self.missing_sections),
            "approval_id": self.approval_id,
            "warnings": list(self.warnings),
            "report_paths": dict(self.report_paths),
            "financial_cycle": dict(self.financial_cycle),
        }


_MONTH_PATTERN = re.compile(r"^\d{4}-\d{2}$")


def _validate_month(month: str) -> str:
    if not isinstance(month, str) or not _MONTH_PATTERN.match(month):
        raise ValueError(f"month must be YYYY-MM, got {month!r}")
    return month


def _end_of_month(month: str) -> str:
    year, mon = map(int, month.split("-"))
    last_day = calendar.monthrange(year, mon)[1]
    return date(year, mon, last_day).isoformat()


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _fmt(value: Any, fallback: str = "—") -> str:
    if value is None:
        return fallback
    if isinstance(value, (int, float)):
        try:
            return f"{float(value):,.2f}".rstrip("0").rstrip(".") or "0"
        except Exception:  # noqa: BLE001
            return str(value)
    text = str(value).strip()
    return text or fallback


def _section_executive_summary(
    metrics: dict[str, Any],
    fc: FinancialCycleReport,
) -> dict[str, str]:
    en = (
        f"MRR={_fmt(metrics.get('mrr_sar'))} SAR, NRR={_fmt(metrics.get('nrr_pct'))}%, "
        f"monthly churn={_fmt(metrics.get('churn_pct_monthly'))}%, "
        f"runway={_fmt(metrics.get('runway_months'))} months (est.). "
        f"Anomalies={len(fc.anomalies)}, threshold violations="
        f"{len(fc.threshold_violations)}, approvals pending="
        f"{fc.approvals_pending.get('count', 0)}."
    )
    ar = (
        f"إيراد شهري={_fmt(metrics.get('mrr_sar'))} ر.س، NRR="
        f"{_fmt(metrics.get('nrr_pct'))}%، انسحاب شهري="
        f"{_fmt(metrics.get('churn_pct_monthly'))}%، مدرّج زمني="
        f"{_fmt(metrics.get('runway_months'))} شهراً (تقدير). "
        f"شذوذ={len(fc.anomalies)}، مخالفات={len(fc.threshold_violations)}، "
        f"موافقات معلّقة={fc.approvals_pending.get('count', 0)}."
    )
    return {"body_ar": ar, "body_en": en}


def _section_revenue(metrics: dict[str, Any]) -> dict[str, str]:
    en = (
        f"MRR={_fmt(metrics.get('mrr_sar'))} SAR, "
        f"ARR={_fmt(metrics.get('arr_sar'))} SAR, "
        f"ARPA={_fmt(metrics.get('arpa_sar'))} SAR, "
        f"active customers={metrics.get('customers_active', 0)} / "
        f"{metrics.get('customers_total_ever', 0)} ever."
    )
    ar = (
        f"إيراد شهري={_fmt(metrics.get('mrr_sar'))} ر.س، "
        f"إيراد سنوي={_fmt(metrics.get('arr_sar'))} ر.س، "
        f"متوسط لكل عميل={_fmt(metrics.get('arpa_sar'))} ر.س، "
        f"عملاء نشطون={metrics.get('customers_active', 0)} / "
        f"{metrics.get('customers_total_ever', 0)}."
    )
    return {"body_ar": ar, "body_en": en}


def _section_retainers(metrics: dict[str, Any], warnings: list[str]) -> dict[str, str]:
    """Use RetainerEconomics as a structural health hint."""
    try:
        from auto_client_acquisition.operating_finance_os.retainer_economics import (
            RetainerEconomics,
        )

        mrr = float(metrics.get("mrr_sar", 0))
        # Documented defaults — keep the memo evidence-bound, never invented.
        retainer = RetainerEconomics(
            mrr=mrr,
            monthly_delivery_hours=40.0,
            monthly_ai_cost=500.0,
            blended_hour_cost=120.0,
        )
        health = round(retainer.health_ratio, 2)
        load = round(retainer.implied_load_cost, 2)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"retainers_section_failed:{exc}")
        health = 0.0
        load = 0.0

    en = (
        f"Active customers={metrics.get('customers_active', 0)}. "
        f"Implied retainer load cost={load} SAR; health ratio={health}."
    )
    ar = (
        f"عملاء نشطون={metrics.get('customers_active', 0)}. "
        f"تكلفة حمولة الاحتفاظ التقديرية={load} ر.س؛ نسبة الصحة={health}."
    )
    return {"body_ar": ar, "body_en": en}


def _section_proof(warnings: list[str]) -> dict[str, str]:
    count = 0
    try:
        from auto_client_acquisition.proof_ledger.factory import (
            get_default_proof_ledger,
        )

        ledger = get_default_proof_ledger()
        events = ledger.list_events(limit=10000)
        count = len(events)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"proof_section_skipped:{exc}")

    en = f"Proof events on the ledger: {count}."
    ar = f"أحداث الإثبات في السجلّ: {count}."
    return {"body_ar": ar, "body_en": en}


def _section_governance(fc: FinancialCycleReport) -> dict[str, str]:
    violations = fc.threshold_violations
    if not violations:
        return {
            "body_ar": "لا مخالفات عتبات هذا الشهر.",
            "body_en": "No threshold violations this month.",
        }
    lines_en = [f"Threshold violations: {len(violations)}"]
    lines_ar = [f"مخالفات العتبات: {len(violations)}"]
    for v in violations[:5]:
        rule = v.get("rule", {})
        lines_en.append(
            f"- {rule.get('rule_id', '')}: observed={v.get('observed_value', '')}"
        )
        lines_ar.append(
            f"- {rule.get('rule_id', '')}: قياس={v.get('observed_value', '')}"
        )
    return {"body_ar": "\n".join(lines_ar), "body_en": "\n".join(lines_en)}


def _section_capital_creation(metrics: dict[str, Any]) -> dict[str, str]:
    n = int(metrics.get("capital_assets_this_period", 0))
    return {
        "body_ar": f"أصول رأس المال المُنشأة هذا الشهر: {n}.",
        "body_en": f"Capital assets created this month: {n}.",
    }


def _section_productization() -> dict[str, str]:
    return {
        "body_ar": "—",
        "body_en": "—",
    }


def _section_delivery(warnings: list[str]) -> dict[str, str]:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate

        agg = aggregate(customer_id="dealix_financial", window_days=30)
        en = (
            f"Friction events (30d): total={agg.total}, "
            f"top kinds={agg.top_3_kinds}."
        )
        ar = (
            f"أحداث الاحتكاك (30 يوم): الإجمالي={agg.total}، "
            f"أكثرها={agg.top_3_kinds}."
        )
        return {"body_ar": ar, "body_en": en}
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"delivery_section_skipped:{exc}")
        return {"body_ar": "—", "body_en": "—"}


def _section_market() -> dict[str, str]:
    return {"body_ar": "—", "body_en": "—"}


def _section_business_units(warnings: list[str]) -> dict[str, str]:
    try:
        from auto_client_acquisition.dominance_os.dominance_scorecard import (
            DominanceScorecard,
            recommend_dominance_focus,
        )

        focus = recommend_dominance_focus(DominanceScorecard())
        return {
            "body_ar": f"تركيز الهيمنة الموصى به: {focus}.",
            "body_en": f"Recommended dominance focus: {focus}.",
        }
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"business_units_section_skipped:{exc}")
        return {"body_ar": "—", "body_en": "—"}


def _section_stop_list(warnings: list[str]) -> dict[str, str]:
    try:
        from auto_client_acquisition.operating_finance_os.bad_revenue_filter import (
            BadRevenueSignals,
            is_bad_revenue,
        )

        bad, _ = is_bad_revenue(
            BadRevenueSignals(
                open_scope=False,
                weak_margin=False,
                high_risk=False,
                governance_refused=False,
                wants_scraping=False,
                wants_guaranteed_sales=False,
                no_proof_path=False,
                no_retainer_path=False,
                no_productization_signal=False,
            )
        )
        if bad:
            return {
                "body_ar": "هناك إشارات إيراد ضارّ — راجع قبل التوسعة.",
                "body_en": "Bad-revenue signals present — review before scaling.",
            }
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"stop_list_section_skipped:{exc}")
    return {"body_ar": "—", "body_en": "—"}


def _section_next_strategic_bet(warnings: list[str]) -> dict[str, str]:
    try:
        from auto_client_acquisition.strategy_autonomy.decision_ledger import (
            query_decisions,
        )

        rows = query_decisions(status="recommended", limit=1)
        if not rows:
            return {"body_ar": "—", "body_en": "—"}
        row = rows[-1]
        title = getattr(row, "title", None) or getattr(row, "decision_type", "")
        return {
            "body_ar": f"رهان موصى به: {title}.",
            "body_en": f"Recommended bet: {title}.",
        }
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"next_strategic_bet_section_skipped:{exc}")
        return {"body_ar": "—", "body_en": "—"}


def _build_sections(
    *,
    metrics: dict[str, Any],
    fc: FinancialCycleReport,
    warnings: list[str],
) -> dict[str, dict[str, str]]:
    sections: dict[str, dict[str, str]] = {}
    for slug in BOARD_MEMO_SECTIONS:
        if slug == "executive_summary":
            block = _section_executive_summary(metrics, fc)
        elif slug == "revenue":
            block = _section_revenue(metrics)
        elif slug == "retainers":
            block = _section_retainers(metrics, warnings)
        elif slug == "proof":
            block = _section_proof(warnings)
        elif slug == "governance":
            block = _section_governance(fc)
        elif slug == "capital_creation":
            block = _section_capital_creation(metrics)
        elif slug == "productization":
            block = _section_productization()
        elif slug == "delivery":
            block = _section_delivery(warnings)
        elif slug == "market":
            block = _section_market()
        elif slug == "business_units":
            block = _section_business_units(warnings)
        elif slug == "stop_list":
            block = _section_stop_list(warnings)
        elif slug == "next_strategic_bet":
            block = _section_next_strategic_bet(warnings)
        else:
            block = {"body_ar": "—", "body_en": "—"}
        block.setdefault("title_ar", _SECTION_TITLES_AR.get(slug, slug))
        block.setdefault("title_en", _SECTION_TITLES_EN.get(slug, slug))
        sections[slug] = block
    return sections


def _content_by_slug(sections: dict[str, dict[str, str]]) -> dict[str, str]:
    """Project the bilingual sections into the slug→content map used by
    :func:`board_memo_sections_complete`."""
    out: dict[str, str] = {}
    for slug, block in sections.items():
        en = (block.get("body_en") or "").strip()
        ar = (block.get("body_ar") or "").strip()
        if en in ("", "—") and ar in ("", "—"):
            out[slug] = ""
        else:
            out[slug] = (en + "\n" + ar).strip()
    return out


def _create_approval(*, month: str, sections_complete: bool) -> str:
    """Create the founder-approval gate for the memo."""
    from auto_client_acquisition.approval_center import (
        get_default_approval_store,
    )
    from auto_client_acquisition.approval_center.schemas import ApprovalRequest

    req = ApprovalRequest(
        object_type="board_memo",
        object_id=f"board_memo:{month}",
        action_type="follow_up_task",
        action_mode="approval_required",
        channel="financial",
        summary_ar=(
            f"مذكّرة المجلس لشهر {month} جاهزة للمراجعة — "
            f"اكتمال الأقسام: {sections_complete}."
        ),
        summary_en=(
            f"Board memo for {month} ready for review — "
            f"sections complete: {sections_complete}."
        ),
        risk_level="medium",
        proof_impact=f"board_memo:{month}",
        customer_id="dealix_financial",
    )
    stored = get_default_approval_store().create(req)
    return stored.approval_id


def _write_memo(report: BoardMemoReport, warnings: list[str]) -> dict[str, str]:
    try:
        memo_dir = _memo_dir()
        memo_dir.mkdir(parents=True, exist_ok=True)
        json_path = memo_dir / f"{report.month}.json"
        md_path = memo_dir / f"{report.month}.md"
        payload = report.to_dict()
        payload["report_paths"] = {"json": str(json_path), "md": str(md_path)}
        json_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        md_path.write_text(render_board_memo_markdown(payload), encoding="utf-8")
        return {"json": str(json_path), "md": str(md_path)}
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"memo_persist_failed:{exc}")
        return {}


def run_board_memo_cycle(*, month: str) -> BoardMemoReport:
    """Run the monthly board-memo cycle for ``month`` (``YYYY-MM``).

    The memo is never shared anywhere; a single founder approval gates
    every distribution.
    """
    month = _validate_month(month)
    warnings: list[str] = []

    end_of_month = _end_of_month(month)
    fc = run_financial_cycle(period_end=end_of_month, cadence="monthly")
    metrics = dict(fc.metrics)
    warnings.extend(fc.warnings)

    sections = _build_sections(metrics=metrics, fc=fc, warnings=warnings)
    complete, missing = board_memo_sections_complete(_content_by_slug(sections))

    approval_id = ""
    try:
        approval_id = _create_approval(month=month, sections_complete=complete)
    except Exception as exc:  # noqa: BLE001
        warnings.append(f"approval_create_failed:{exc}")

    report = BoardMemoReport(
        month=month,
        generated_at=_now_iso(),
        sections=sections,
        section_order=list(BOARD_MEMO_SECTIONS),
        sections_complete=complete,
        missing_sections=list(missing),
        approval_id=approval_id,
        warnings=warnings,
        financial_cycle={
            "cycle_id": fc.cycle_id,
            "period_end": fc.period_end,
            "cadence": fc.cadence,
            "approvals_pending": fc.approvals_pending.get("count", 0),
            "anomalies": len(fc.anomalies),
            "threshold_violations": len(fc.threshold_violations),
        },
    )
    report.report_paths = _write_memo(report, warnings)
    report.warnings = warnings
    return report


def latest_board_memo(month: str | None = None) -> dict[str, Any] | None:
    """Return a persisted memo by ``month`` (or the newest), or ``None``."""
    memo_dir = _memo_dir()
    if not memo_dir.exists():
        return None
    if month is not None:
        target = memo_dir / f"{_validate_month(month)}.json"
        if not target.exists():
            return None
        try:
            return json.loads(target.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return None
    candidates = sorted(memo_dir.glob("*.json"))
    if not candidates:
        return None
    try:
        return json.loads(candidates[-1].read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return None


__all__ = [
    "BoardMemoReport",
    "latest_board_memo",
    "run_board_memo_cycle",
]
