#!/usr/bin/env python3
"""Run the single canonical Dealix Company OS cycle.

This runner consolidates the richer existing self-operating feature module into
one scheduled, draft-only operating path. It creates a commercial command
packet, opportunity graph, approval queue, proof log, and evidence-backed
revenue status. It never sends, publishes, charges, deploys, merges, or prints
secret values.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import os
import sys
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from types import ModuleType
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "reports" / "canonical_company_os"
FEATURE_MODULE_PATH = ROOT / "scripts" / "commercial" / "run_self_operating_company_os.py"

FORBIDDEN_ENV_FLAGS = (
    "EXTERNAL_SEND_ENABLED",
    "LIVE_OUTBOUND_ENABLED",
    "AUTO_SEND_ENABLED",
    "AUTO_WHATSAPP_ENABLED",
    "WHATSAPP_AUTO_SEND",
    "EMAIL_AUTO_SEND",
    "SMS_AUTO_SEND",
    "LINKEDIN_AUTO_SEND",
    "AUTO_LINKEDIN_ENABLED",
    "AUTO_PAYMENT_CAPTURE_ENABLED",
    "LIVE_PAYMENT_CAPTURE_ENABLED",
    "AUTO_MERGE_ENABLED",
    "AUTO_DEPLOY_ENABLED",
    "PRODUCTION_MUTATION_ENABLED",
)


def utc_now() -> datetime:
    return datetime.now(UTC)


def _is_true(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def unsafe_flags() -> list[str]:
    return sorted(name for name in FORBIDDEN_ENV_FLAGS if _is_true(os.getenv(name, "")))


def load_feature_module() -> ModuleType:
    spec = importlib.util.spec_from_file_location("dealix_self_operating_feature", FEATURE_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load feature module: {FEATURE_MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_revenue_status() -> dict[str, Any]:
    from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic

    return analyze_first_paid_diagnostic()


def revenue_next_action(status: dict[str, Any]) -> str:
    if int(status.get("payment_received_real", 0)) == 0:
        return "Select one real warm target, approve the 499 SAR offer, and collect verifiable payment evidence."
    if int(status.get("proof_pack_delivered_real", 0)) == 0:
        return "Deliver the paid proof pack and append a real proof_pack_delivered evidence event."
    if bool(status.get("crm_kpi_pending", True)):
        return "Sync the real close into the canonical CRM/KPI import without changing the payment evidence."
    return "First paid close is evidenced; convert the proof into the next Revenue Command Pilot opportunity."


def build_priorities(revenue_status: dict[str, Any], target_mode: str) -> list[dict[str, str]]:
    priorities = [
        {
            "priority": "P0",
            "area": "production_trust",
            "action": "Complete Railway canonical config verification through PR #882, then validate the live deployment.",
            "evidence": "PR #882 and CI checks",
        },
        {
            "priority": "P0",
            "area": "production_smoke",
            "action": "Synchronize the sealed smoke key through approval package #884 and rerun Production Smoke.",
            "evidence": "Issue #884 and Production Smoke artifact",
        },
        {
            "priority": "P0",
            "area": "revenue",
            "action": revenue_next_action(revenue_status),
            "evidence": str(revenue_status.get("evidence_path", "")),
        },
        {
            "priority": "P1",
            "area": "runtime_consolidation",
            "action": "Extract unique capabilities through #883; do not merge parallel Company OS kernels wholesale.",
            "evidence": "Issue #883",
        },
    ]
    if target_mode == "safe_seed_only":
        priorities.insert(
            2,
            {
                "priority": "P0",
                "area": "real_targets",
                "action": "Load real warm, inbound, referral, or explicitly approved targets before any external action.",
                "evidence": "data/self_operating_company_os/targets.json",
            },
        )
    return priorities


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Dealix Daily Command — Canonical Company OS",
        "",
        f"- Run ID: `{payload['run_id']}`",
        f"- Generated: `{payload['generated_at']}`",
        f"- Mode: `{payload['mode']}`",
        f"- Target mode: `{payload['target_mode']}`",
        f"- Revenue verdict: `{payload['revenue_status']['verdict']}`",
        "",
        "## Top priorities",
    ]
    for item in payload["priorities"]:
        lines.append(f"- **{item['priority']} / {item['area']}** — {item['action']} Evidence: `{item['evidence']}`")

    lines.extend(["", "## Opportunity Graph"])
    for item in payload["opportunity_graph"][:10]:
        lines.append(
            f"- **{item['company_name']}** | score {item['score']} | {item['offer_fit']} | "
            f"{item['next_action']} | approval: {item['approval_status']}"
        )

    lines.extend(["", "## Approval Queue"])
    for item in payload["approval_queue"][:10]:
        lines.append(
            f"- **{item['target_id']} / {item['company_name']}** — {item['action_type']} via "
            f"{item['channel']} | `{item['status']}`"
        )

    revenue = payload["revenue_status"]
    lines.extend(
        [
            "",
            "## Verified revenue status",
            f"- Real evidence events: {revenue['real_company_events']}",
            f"- Invoice sent: {revenue['invoice_sent_real']}",
            f"- Payment received: {revenue['payment_received_real']}",
            f"- Proof pack delivered: {revenue['proof_pack_delivered_real']}",
            f"- CRM/KPI pending: {revenue['crm_kpi_pending']}",
            f"- Next exact action: {payload['revenue_next_action']}",
            "",
            "## Proof Log",
        ]
    )
    for event in payload["proof_log"]:
        lines.append(f"- **{event['event']}** — {event['evidence']} | risk: {event['risk']}")

    lines.extend(
        [
            "",
            "## Safety",
            "- No external send was performed.",
            "- No cold WhatsApp or mass LinkedIn automation.",
            "- No payment capture or invented revenue.",
            "- No production mutation or secret printing.",
            "- Revenue is counted only from real `payment_received` evidence.",
            "- Closed status requires payment, proof delivery, and KPI synchronization.",
        ]
    )
    return "\n".join(lines) + "\n"


def run(limit: int = 50, output_root: Path = OUT_ROOT) -> dict[str, Any]:
    violations = unsafe_flags()
    if violations:
        raise RuntimeError("Unsafe live automation flags enabled: " + ", ".join(violations))

    feature = load_feature_module()
    targets_file = feature.DATA_ROOT / "targets.json"
    target_mode = "runtime_data" if targets_file.is_file() else "safe_seed_only"

    cards = feature.build_target_cards(max(1, limit))
    actions = feature.build_actions()
    approvals = feature.build_approval_queue(cards)
    revenue_status = load_revenue_status()

    now = utc_now()
    run_id = f"dealix-canonical-company-os-{now.strftime('%Y%m%dT%H%M%SZ')}"
    day = now.date().isoformat()

    proof_log = [
        {
            "event": "canonical_cycle_generated",
            "evidence": f"{len(cards)} opportunities, {len(actions)} internal actions, {len(approvals)} approval items",
            "source": "scripts/commercial/run_canonical_company_os.py",
            "risk": "low",
        },
        {
            "event": "revenue_evidence_checked",
            "evidence": (
                f"payment_received={revenue_status['payment_received_real']}; "
                f"proof_pack_delivered={revenue_status['proof_pack_delivered_real']}; "
                f"verdict={revenue_status['verdict']}"
            ),
            "source": str(revenue_status.get("evidence_path", "")),
            "risk": "low",
        },
        {
            "event": "external_execution_blocked",
            "evidence": "All external actions remain in the approval queue; no sender is invoked.",
            "source": "runtime safety contract",
            "risk": "low",
        },
    ]

    payload: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "generated_at": now.isoformat(),
        "mode": "draft-only",
        "target_mode": target_mode,
        "company_brain": {
            "positioning": "Saudi AI Business Operating System / Company OS, not a CRM clone.",
            "first_offer": "499 SAR Revenue Proof Sprint for a real warm or approved target.",
            "expansion_path": "Revenue Command Pilot -> monthly Revenue Command Room -> AI Company OS setup.",
            "proof_rule": "No revenue without payment_received; no closed-won without proof delivery and KPI sync.",
        },
        "priorities": build_priorities(revenue_status, target_mode),
        "opportunity_graph": [asdict(card) for card in cards],
        "action_queue": [asdict(action) for action in actions],
        "approval_queue": approvals,
        "revenue_status": revenue_status,
        "revenue_next_action": revenue_next_action(revenue_status),
        "proof_log": proof_log,
        "safety": {
            "external_send": False,
            "cold_whatsapp": False,
            "mass_linkedin": False,
            "payment_capture": False,
            "production_mutation": False,
            "secret_printing": False,
        },
    }

    dated = output_root / day
    write_json(output_root / "latest.json", payload)
    write_json(dated / "bundle.json", payload)
    write_json(dated / "revenue_status.json", revenue_status)
    write_json(dated / "proof_log.json", proof_log)
    write_csv(
        dated / "opportunity_graph.csv",
        payload["opportunity_graph"],
        [
            "id",
            "company_name",
            "target_type",
            "sector",
            "pain_hypothesis",
            "offer_fit",
            "score",
            "risk_level",
            "recommended_channel",
            "next_action",
            "approval_status",
        ],
    )
    write_csv(
        dated / "action_queue.csv",
        payload["action_queue"],
        ["id", "playbook", "action", "owner", "status", "approval_required", "risk_level"],
    )
    write_csv(
        dated / "approval_queue.csv",
        approvals,
        [
            "target_id",
            "company_name",
            "action_type",
            "channel",
            "draft_text",
            "risk_flags",
            "proof_to_attach",
            "status",
        ],
    )
    markdown = render_markdown(payload)
    (output_root / "latest.md").write_text(markdown, encoding="utf-8")
    (dated / "daily_command.md").write_text(markdown, encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--output-root", default=str(OUT_ROOT))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    payload = run(limit=max(1, args.limit), output_root=Path(args.output_root))
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            "CANONICAL_COMPANY_OS=PASS "
            f"run_id={payload['run_id']} targets={len(payload['opportunity_graph'])} "
            f"approvals={len(payload['approval_queue'])} revenue={payload['revenue_status']['verdict']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
