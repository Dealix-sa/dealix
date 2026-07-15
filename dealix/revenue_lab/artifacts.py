"""Artifact writers for a reviewable Revenue Lab run."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .models import RevenueLabBundle


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_bundle(output_dir: Path, bundle: RevenueLabBundle) -> dict[str, Path]:
    """Write the canonical daily JSON, Markdown, queues, and proof log."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = bundle.to_dict()
    latest_json = output_dir / "latest.json"
    latest_json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    opportunity_rows = [dict(item) for item in payload["opportunities"]]
    for row in opportunity_rows:
        for key in ("pain_hypotheses", "unknowns", "evidence_refs"):
            row[key] = " | ".join(row.get(key) or ())
    opportunity_csv = output_dir / "opportunity_graph.csv"
    _write_csv(
        opportunity_csv,
        opportunity_rows,
        [
            "account_id",
            "company_name",
            "sector",
            "company_size",
            "decision_maker_role",
            "pain_hypotheses",
            "unknowns",
            "offer_match",
            "why_now",
            "priority_score",
            "evidence_status",
            "evidence_refs",
            "prediction_status",
            "conversion_probability",
            "stage",
            "next_action",
        ],
    )

    approval_rows = [dict(item) for item in payload["approval_requests"]]
    for row in approval_rows:
        row["edit_history"] = json.dumps(row.get("edit_history") or [], ensure_ascii=False)
    approval_csv = output_dir / "approval_queue.csv"
    _write_csv(
        approval_csv,
        approval_rows,
        [
            "approval_id",
            "action_id",
            "object_type",
            "object_id",
            "action_type",
            "action_mode",
            "channel",
            "summary_ar",
            "summary_en",
            "risk_level",
            "proof_impact",
            "status",
            "customer_id",
            "audit_ref",
            "proof_target",
            "created_at",
            "updated_at",
            "expires_at",
            "due_date",
            "edit_history",
            "reject_reason",
        ],
    )

    proof_log = {
        "run_id": bundle.run_id,
        "generated_at": bundle.generated_at,
        "proof_policy": (
            "Process evidence is not a customer result. Demo inputs never create proof events. "
            "Public use requires consent and approval."
        ),
        "verified_customer_outcomes": bundle.summary["verified_customer_outcomes"],
        "events": list(payload["proof_events"]),
        "blockers": list(bundle.blockers),
    }
    proof_path = output_dir / "proof_log.json"
    proof_path.write_text(
        json.dumps(proof_log, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    latest_md = output_dir / "latest.md"
    lines = [
        "# Dealix Revenue Lab — Daily Draft-Only Run",
        "",
        f"- Run: `{bundle.run_id}`",
        f"- Mode: `{bundle.mode}`",
        f"- Opportunities: `{bundle.summary['opportunities']}`",
        f"- Source-backed signals: `{bundle.summary['source_backed_signals']}`",
        f"- Approval requests: `{bundle.summary['approval_requests']}`",
        f"- External actions executed: `{bundle.summary['external_actions_executed']}`",
        f"- Verified customer outcomes: `{bundle.summary['verified_customer_outcomes']}`",
        "",
        "## Priorities",
        "",
    ]
    for item in sorted(bundle.opportunities, key=lambda row: -row.priority_score):
        lines.extend(
            [
                f"### {item.company_name}",
                f"- Priority: `{item.priority_score}` (not conversion probability)",
                f"- Evidence: `{item.evidence_status}`",
                f"- Offer: {item.offer_match}",
                f"- Next action: `{item.next_action}`",
                f"- Unknowns: {', '.join(item.unknowns) or 'none recorded'}",
                "",
            ]
        )
    lines.extend(["## Blockers", ""])
    lines.extend(f"- {item}" for item in bundle.blockers)
    if not bundle.blockers:
        lines.append("- None recorded")
    lines.extend(
        [
            "",
            "> No live outbound, price approval, legal commitment, payment, merge, or production change occurred.",
        ]
    )
    latest_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {
        "latest_json": latest_json,
        "latest_md": latest_md,
        "opportunity_graph": opportunity_csv,
        "approval_queue": approval_csv,
        "proof_log": proof_path,
    }


__all__ = ["write_bundle"]
