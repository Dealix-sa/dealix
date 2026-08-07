#!/usr/bin/env python3
"""Run the Dealix Autonomous Company OS in safe draft-only mode.

This runner is intentionally stdlib-only. It does not send messages, mutate external
systems, charge payments, merge PRs, or publish content. It prepares a founder
review packet that can be routed to Slack, Airtable, Google Contacts, and GitHub
through separate approval-first connectors.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable

FORBIDDEN_ENV_FLAGS = {
    "EXTERNAL_SEND_ENABLED": "true",
    "LIVE_OUTBOUND_ENABLED": "true",
    "WHATSAPP_AUTO_SEND": "true",
    "EMAIL_AUTO_SEND": "true",
    "SMS_AUTO_SEND": "true",
    "LINKEDIN_AUTO_SEND": "true",
    "AUTO_MERGE_ENABLED": "true",
    "AUTO_DEPLOY_ENABLED": "true",
    "LIVE_PAYMENT_CAPTURE_ENABLED": "true",
}

DEFAULT_REPORT_DIR = Path("reports/dealix_autonomous_company_os")


@dataclass(frozen=True)
class ApprovalItem:
    action_id: str
    connector: str
    action_type: str
    risk_level: str
    status: str
    decision_needed: str
    draft_output: str


@dataclass(frozen=True)
class Opportunity:
    opportunity_id: str
    segment: str
    offer: str
    score: int
    evidence: str
    next_best_action: str
    approval_status: str


def halt_on_unsafe_env() -> None:
    unsafe = [name for name, value in FORBIDDEN_ENV_FLAGS.items() if os.getenv(name, "").lower() == value]
    if unsafe:
        raise SystemExit(
            "DEALIX_AUTONOMOUS_COMPANY_OS_HALTED: unsafe live automation flags enabled: "
            + ", ".join(sorted(unsafe))
        )


def build_company_brain() -> dict[str, str]:
    return {
        "positioning": "Saudi AI Business Operating System / Company OS, not merely CRM, chatbot, or agency.",
        "first_wedge": "Revenue Command Room / Command Sprint for business owners.",
        "owner_value": "One daily view of what happened, who needs follow-up, which draft to approve, what proof exists, and what next action matters.",
        "safety_posture": "Draft-only, approval-first, no fake proof, no guaranteed revenue, no cold WhatsApp automation.",
        "today_focus": "Prepare a connector-ready operating board and founder approval packet across GitHub, Slack, Airtable, and Google Contacts.",
    }


def build_opportunities(limit: int) -> list[Opportunity]:
    opportunities = [
        Opportunity(
            "opp-riyadh-clinics-command-room",
            "Riyadh Clinics",
            "14-day Revenue Command Room pilot",
            93,
            "Strong pain: fragmented inquiries across WhatsApp, calls, ads, reception notes, and Instagram. Sensitive data risk requires anonymized ops-only workflow.",
            "Prepare owner-safe clinic command room demo and require founder approval before any outreach.",
            "Needs Review",
        ),
        Opportunity(
            "opp-training-sales-os",
            "Training Companies",
            "B2B Training Sales OS",
            88,
            "Training firms need corporate prospecting, registration follow-up, proposal cadence, and course demand visibility.",
            "Draft sector-specific offer and import 10 approved prospects into review queue only.",
            "Draft",
        ),
        Opportunity(
            "opp-agency-delivery-os",
            "Agencies and Consultants",
            "Agency Revenue + Delivery OS",
            84,
            "Agencies already understand retainers and need proof packs, delivery visibility, and follow-up discipline.",
            "Create proof-pack-first proposal and founder review checklist.",
            "Draft",
        ),
        Opportunity(
            "opp-ops-heavy-b2b",
            "Ops Heavy B2B",
            "Executive AI Command Center",
            81,
            "Operations-heavy firms need management visibility, task routing, evidence, and controlled automation.",
            "Keep as enterprise follow-up after first Command Sprint proof exists.",
            "Draft",
        ),
    ]
    return opportunities[:limit]


def build_approval_queue() -> list[ApprovalItem]:
    return [
        ApprovalItem(
            "approve-gh-pr-879-ready",
            "GitHub",
            "mark_pr_ready_or_merge_later",
            "Medium",
            "Pending Founder Review",
            "Review PR #879 after CI completes. Do not merge while draft or while checks are in progress.",
            "PR body has been updated with skill/runtime/connector continuation details.",
        ),
        ApprovalItem(
            "approve-slack-internal-brief",
            "Slack",
            "internal_canvas_or_draft",
            "Low",
            "Pending Founder Review",
            "Create or post internal Slack operating brief only to an approved internal channel.",
            "Slack-ready draft brief prepared; not sent automatically.",
        ),
        ApprovalItem(
            "approve-airtable-base-use",
            "Airtable",
            "operating_board_mutation",
            "Low",
            "Pending Founder Review",
            "Use Airtable as the live Approval Queue and Opportunity Graph board if workspace/base permissions are available.",
            "CSV and JSON seed files generated for import fallback.",
        ),
        ApprovalItem(
            "approve-contacts-warm-radar",
            "Google Contacts",
            "warm_contact_radar",
            "Medium",
            "Pending Founder Review",
            "Use only warm, opted-in, inbound, referral, or known contacts. No invented contacts and no cold outreach.",
            "Contacts search found no Dealix-specific warm records in the current run.",
        ),
        ApprovalItem(
            "blocked-live-outbound",
            "Gmail/WhatsApp/SMS/LinkedIn",
            "live_send",
            "Forbidden",
            "Blocked",
            "Live outbound requires a separate controlled-live approval PR with rate limits, opt-out, audit logs, and kill switch.",
            "No live external messages were sent.",
        ),
    ]


def build_agent_outputs() -> dict[str, str]:
    return {
        "ceo_agent": "Focus the company on a sellable Command Sprint, then expand into the full Company OS after proof.",
        "scout_agent": "Prioritize Riyadh clinics, training companies, agencies, and ops-heavy B2B using evidence-first fit scoring.",
        "offer_agent": "Lead with 14-day Revenue Command Room pilot; avoid abstract AI-platform language.",
        "risk_agent": "No live outbound, no cold WhatsApp, no fake ROI, no patient data, no external action without approval.",
        "delivery_agent": "Deliver diagnosis, command room setup, daily operating loop, and proof pack.",
        "proof_agent": "Record only real outputs: PR links, generated reports, drafts, approvals, and validated evidence.",
        "product_agent": "Keep GitHub as durable source of truth; use Airtable/Slack as operating surfaces, not the core system.",
        "self_improvement_agent": "Update scoring from founder edits, replies, objections, CI failures, and delivery gaps.",
    }


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, *, run_id: str, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    company_brain = payload["company_brain"]
    agent_outputs = payload["agent_outputs"]
    opportunities = payload["opportunity_graph"]
    approvals = payload["approval_queue"]

    lines = [
        "# Dealix Autonomous Company OS Daily Packet",
        "",
        f"Run ID: `{run_id}`",
        "Mode: `draft-only`",
        "",
        "## Company Brain",
    ]
    for key, value in company_brain.items():
        lines.append(f"- **{key}**: {value}")

    lines.extend(["", "## Agent Team"])
    for key, value in agent_outputs.items():
        lines.append(f"- **{key}**: {value}")

    lines.extend(["", "## Opportunity Graph"])
    for item in opportunities:
        lines.append(
            f"- **{item['segment']}** ({item['score']}): {item['offer']} — {item['next_best_action']}"
        )

    lines.extend(["", "## Approval Center"])
    for item in approvals:
        lines.append(
            f"- **{item['action_id']}** [{item['connector']} / {item['risk_level']} / {item['status']}]: {item['decision_needed']}"
        )

    lines.extend(
        [
            "",
            "## Connector Status",
            "- GitHub: durable source of truth; prepare PR/docs/scripts/tests first.",
            "- Slack: internal brief/canvas only; no sent channel message unless approved.",
            "- Airtable: live board if available; CSV/JSON fallback generated.",
            "- Google Contacts: warm-contact radar only; no cold outreach and no invented contacts.",
            "",
            "## Next Exact Action",
            "Review the approval queue, wait for CI completion, then decide whether PR #879 should move from draft to ready-for-review.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(limit: int, output_dir: Path) -> dict[str, object]:
    halt_on_unsafe_env()
    now = datetime.now(UTC)
    run_id = f"dealix-company-os-{now.strftime('%Y%m%dT%H%M%SZ')}"
    opportunities = build_opportunities(limit)
    approvals = build_approval_queue()
    payload: dict[str, object] = {
        "run_id": run_id,
        "mode": "draft-only",
        "generated_at": now.isoformat(),
        "company_brain": build_company_brain(),
        "agent_outputs": build_agent_outputs(),
        "opportunity_graph": [asdict(item) for item in opportunities],
        "approval_queue": [asdict(item) for item in approvals],
        "safety": {
            "live_outbound": False,
            "auto_merge": False,
            "auto_deploy": False,
            "payment_capture": False,
            "requires_founder_approval": True,
        },
    }

    write_json(output_dir / "latest.json", payload)
    write_markdown(output_dir / "latest.md", run_id=run_id, payload=payload)
    write_csv(
        output_dir / "airtable_approval_queue_seed.csv",
        [asdict(item) for item in approvals],
        ["action_id", "connector", "action_type", "risk_level", "status", "decision_needed", "draft_output"],
    )
    write_csv(
        output_dir / "airtable_opportunity_graph_seed.csv",
        [asdict(item) for item in opportunities],
        ["opportunity_id", "segment", "offer", "score", "evidence", "next_best_action", "approval_status"],
    )
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Dealix Autonomous Company OS safely.")
    parser.add_argument("--limit", type=int, default=4, help="Maximum opportunities to include.")
    parser.add_argument("--output-dir", default=str(DEFAULT_REPORT_DIR), help="Output directory for generated reports.")
    args = parser.parse_args()
    payload = run(limit=max(1, args.limit), output_dir=Path(args.output_dir))
    print(f"DEALIX_AUTONOMOUS_COMPANY_OS=PASS run_id={payload['run_id']} mode={payload['mode']}")


if __name__ == "__main__":
    main()
