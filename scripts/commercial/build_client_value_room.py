from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "dealix" / "registers" / "client_transparency_value_registry.json"


def load_registry(path: Path = REGISTRY_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return value is not None


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _value_status(metric: dict[str, Any]) -> str:
    baseline = metric.get("baseline")
    current = metric.get("current")
    source = metric.get("source")
    customer_accepted = metric.get("customer_accepted") is True
    verified = metric.get("verified") is True

    if not _present(baseline):
        return "baseline_missing"
    if not _present(current):
        return "baseline_established"
    if not _present(source):
        return "measurement_active"
    if customer_accepted and verified:
        return "customer_accepted"
    if verified:
        return "outcome_verified"
    return "directional_signal"


def _normalize_value_metric(metric: dict[str, Any]) -> dict[str, Any]:
    status = _value_status(metric)
    claim_allowed = status in {"outcome_verified", "customer_accepted", "not_achieved", "inconclusive"}
    return {
        "metric": metric.get("metric"),
        "baseline": metric.get("baseline"),
        "target": metric.get("target"),
        "current": metric.get("current"),
        "unit": metric.get("unit"),
        "measurement_window": metric.get("measurement_window"),
        "source": metric.get("source"),
        "confidence": metric.get("confidence"),
        "value_status": status,
        "claim_allowed": claim_allowed,
        "evidence_refs": _safe_list(metric.get("evidence_refs")),
        "customer_accepted": metric.get("customer_accepted") is True,
    }


def _missing_required(section: dict[str, Any], required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if not _present(section.get(field))]


def build_client_value_room(
    engagement: dict[str, Any],
    registry: dict[str, Any] | None = None,
) -> dict[str, Any]:
    registry = registry or load_registry()
    now = datetime.now(UTC).isoformat()

    value_metrics = [_normalize_value_metric(metric) for metric in _safe_list(engagement.get("value_metrics"))]
    accepted_value = [metric for metric in value_metrics if metric["value_status"] == "customer_accepted"]
    verified_value = [metric for metric in value_metrics if metric["value_status"] == "outcome_verified"]
    directional_value = [metric for metric in value_metrics if metric["value_status"] == "directional_signal"]

    risks = _safe_list(engagement.get("risks"))
    decisions = _safe_list(engagement.get("decisions"))
    work_items = _safe_list(engagement.get("work_items"))
    deliverables = _safe_list(engagement.get("deliverables"))
    timeline = _safe_list(engagement.get("timeline"))

    blocked_items = [item for item in work_items if item.get("status") == "blocked"]
    pending_decisions = [item for item in decisions if item.get("status") == "pending"]
    severe_risks = [item for item in risks if item.get("severity") in {"high", "critical"}]

    if accepted_value:
        overall_value_status = "customer_accepted"
    elif verified_value:
        overall_value_status = "outcome_verified"
    elif directional_value:
        overall_value_status = "directional_signal"
    elif value_metrics:
        overall_value_status = value_metrics[0]["value_status"]
    else:
        overall_value_status = "baseline_missing"

    overall_status = "at_risk" if severe_risks or blocked_items else engagement.get("overall_status", "on_track")

    scope_and_success = {
        "scope_in": _safe_list(engagement.get("scope_in")),
        "scope_out": _safe_list(engagement.get("scope_out")),
        "owner_matrix": engagement.get("owner_matrix", {}),
        "baseline": engagement.get("baseline"),
        "target_metrics": _safe_list(engagement.get("target_metrics")),
        "acceptance_criteria": _safe_list(engagement.get("acceptance_criteria")),
        "stop_rule": engagement.get("stop_rule"),
    }

    delivery_and_acceptance = []
    for item in deliverables:
        delivery_and_acceptance.append(
            {
                "deliverable": item.get("deliverable"),
                "completion_status": item.get("completion_status", "not_started"),
                "completion_evidence": _safe_list(item.get("completion_evidence")),
                "acceptance_status": item.get("acceptance_status", "not_requested"),
                "acceptance_evidence": _safe_list(item.get("acceptance_evidence")),
                "exceptions": _safe_list(item.get("exceptions")),
                "delivery_claim_allowed": bool(item.get("completion_evidence")) and item.get("completion_status") == "completed",
                "acceptance_claim_allowed": bool(item.get("acceptance_evidence")) and item.get("acceptance_status") == "accepted",
            }
        )

    sections = {section["id"]: section for section in registry["client_cockpit_sections"]}
    missing_data = {
        "scope_and_success": _missing_required(scope_and_success, sections["scope_and_success"]["required_fields"]),
        "value_metrics": [
            {
                "metric": metric.get("metric"),
                "missing": [field for field in ["baseline", "current", "source", "measurement_window", "confidence"] if not _present(metric.get(field))],
            }
            for metric in value_metrics
        ],
    }

    return {
        "schema_version": "1.0",
        "mode": "draft_only",
        "client_context": {
            "client_name": engagement.get("client_name"),
            "engagement_id": engagement.get("engagement_id"),
            "pilot_id": engagement.get("pilot_id"),
            "sector": engagement.get("sector"),
            "country": engagement.get("country", "Saudi Arabia"),
        },
        "executive_summary": {
            "overall_status": overall_status,
            "current_phase": engagement.get("current_phase"),
            "value_status": overall_value_status,
            "top_outcomes": _safe_list(engagement.get("top_outcomes"))[:5],
            "top_risks": severe_risks[:5],
            "decisions_needed": pending_decisions[:5],
            "next_checkpoint": engagement.get("next_checkpoint"),
        },
        "scope_and_success": scope_and_success,
        "work_items": work_items,
        "decisions_and_approvals": decisions,
        "risks_and_exceptions": risks,
        "delivery_and_acceptance": delivery_and_acceptance,
        "value_realization": value_metrics,
        "timeline": timeline,
        "renewal_and_expansion": {
            "recommendation": engagement.get("renewal_recommendation", "withheld_pending_evidence"),
            "evidence": _safe_list(engagement.get("renewal_evidence")),
            "unresolved_risks": severe_risks,
            "future_scope": _safe_list(engagement.get("future_scope")),
            "decision_date": engagement.get("renewal_decision_date"),
            "approval_status": engagement.get("renewal_approval_status", "not_requested"),
            "external_send_allowed": False,
        },
        "data_freshness": {
            "generated_at": now,
            "source_last_updated_at": engagement.get("source_last_updated_at"),
            "stale_sources": _safe_list(engagement.get("stale_sources")),
        },
        "disclosures": {
            "missing_data": missing_data,
            "synthetic_evidence_present": engagement.get("synthetic_evidence_present") is True,
            "unsupported_claims_withheld": [
                "guaranteed_roi",
                "guaranteed_revenue",
                "customer_value_without_baseline_and_source",
                "delivery_without_completion_evidence",
                "acceptance_without_customer_evidence",
            ],
            "negative_and_inconclusive_results_visible": True,
        },
        "external_actions_executed": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a transparent Dealix client value room from engagement JSON.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    engagement = json.loads(args.input.read_text(encoding="utf-8"))
    result = build_client_value_room(engagement)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
