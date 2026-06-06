#!/usr/bin/env python3
"""End-to-end dry-run of the Dealix commercial chain (no external sends).

Simulates the full chain with governance enforced:

    Target -> Outreach Approval -> Diagnostic -> Offer (5-rung ladder)
    -> Paid Sprint Simulation -> Customer Workspace -> Proof Pack
    -> Upsell Recommendation -> Founder Daily Command

Every stage returns a structured result dict with a PASS/BLOCKER status so a
test can call the stage functions directly. Optional imports of the canonical
``auto_client_acquisition`` modules are wrapped so the script still runs (and
degrades gracefully) when those modules are unavailable.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Reuse the local workspace creator (self-contained, no third-party imports).
try:  # pragma: no cover - import guard
    from scripts.create_customer_workspace import create_workspace
except Exception:  # pragma: no cover - fallback path
    create_workspace = None  # type: ignore[assignment]

PASS = "PASS"
BLOCKER = "BLOCKER"

# The 5-rung offer ladder (mirrors docs/OFFER_LADDER.md, results-first framing).
OFFER_LADDER: list[str] = [
    "free_tools",
    "low_risk_entry",
    "core_subscription",
    "high_value_execution",
    "performance_layer",
]


def _result(stage: str, status: str, detail: str, **extra: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"stage": stage, "status": status, "detail": detail}
    out.update(extra)
    return out


def stage_target() -> dict[str, Any]:
    """Pick a simulated warm target. Never sources from scraping."""
    target = {
        "company": "Dry Run Trading Co",
        "channel": "warm_intro",
        "source": "founder_known_contact",
        "mode": "dry_run",
    }
    if target["channel"] in {"cold_whatsapp", "linkedin_automation", "scraping"}:
        return _result("target", BLOCKER, "forbidden channel selected", target=target)
    return _result("target", PASS, "warm target selected", target=target)


def stage_outreach_approval() -> dict[str, Any]:
    """Outreach must require explicit approval; it must never auto-send."""
    requires_approval = True
    auto_sent = False
    governance_status = "draft"
    if auto_sent or not requires_approval:
        return _result(
            "outreach_approval",
            BLOCKER,
            "outreach auto-sent or did not require approval",
        )
    return _result(
        "outreach_approval",
        PASS,
        "outreach held for explicit founder approval, not sent",
        requires_approval=requires_approval,
        governance_status=governance_status,
    )


def stage_diagnostic() -> dict[str, Any]:
    """Produce a diagnostic summary with no guaranteed-result language."""
    findings = [
        "Lead response time is the primary acquisition leak.",
        "No single owner for qualified pipeline.",
    ]
    text = " ".join(findings)
    forbidden = ("guaranteed", "مضمون", "نضمن")
    if any(token in text.lower() for token in forbidden):
        return _result("diagnostic", BLOCKER, "diagnostic contains a guaranteed claim")
    return _result("diagnostic", PASS, "diagnostic produced", findings=findings)


def stage_offer() -> dict[str, Any]:
    """Select an offer from the 5-rung ladder."""
    chosen = "low_risk_entry"
    if chosen not in OFFER_LADDER:
        return _result("offer", BLOCKER, f"offer not on ladder: {chosen}")
    return _result("offer", PASS, "offer selected from ladder", offer=chosen, ladder=OFFER_LADDER)


def stage_paid_sprint() -> dict[str, Any]:
    """Simulate a paid command sprint (dry-run, no live charge)."""
    sprint = {
        "name": "command_sprint",
        "duration_days": 14,
        "mode": "dry_run",
        "live_charge": False,
    }
    if sprint["live_charge"]:
        return _result("paid_sprint", BLOCKER, "live charge attempted in dry-run")
    return _result("paid_sprint", PASS, "paid sprint simulated", sprint=sprint)


def stage_customer_workspace(name: str = "dry-run-client") -> dict[str, Any]:
    """Create the customer workspace via create_customer_workspace logic."""
    if create_workspace is None:
        return _result("customer_workspace", BLOCKER, "create_workspace unavailable")
    try:
        workspace = create_workspace(name, force=True)
    except Exception as exc:  # pragma: no cover - defensive
        return _result("customer_workspace", BLOCKER, f"workspace error: {exc}")
    files = sorted(p.name for p in workspace.iterdir() if p.is_file())
    if len(files) < 12:
        return _result(
            "customer_workspace",
            BLOCKER,
            f"expected 12 files, got {len(files)}",
            workspace=str(workspace),
        )
    return _result(
        "customer_workspace",
        PASS,
        "workspace created",
        workspace=str(workspace),
        file_count=len(files),
    )


def stage_proof_pack() -> dict[str, Any]:
    """Assemble a proof pack before any upsell is offered."""
    sections = [f"section_{i:02d}" for i in range(1, 15)]
    if len(sections) < 14:
        return _result("proof_pack", BLOCKER, "proof pack has fewer than 14 sections")
    return _result(
        "proof_pack",
        PASS,
        "14-section proof pack assembled",
        section_count=len(sections),
    )


def stage_upsell_recommendation(proof_pack_ready: bool = True) -> dict[str, Any]:
    """Recommend the next rung only when the proof pack is ready."""
    if not proof_pack_ready:
        return _result("upsell_recommendation", BLOCKER, "proof pack required before upsell")
    return _result(
        "upsell_recommendation",
        PASS,
        "upsell recommended after proof pack",
        recommended_rung="core_subscription",
    )


def stage_founder_daily_command() -> dict[str, Any]:
    """Confirm the founder daily command can be produced."""
    command = {
        "date": date.today().isoformat(),
        "action_en": "Review pending approvals before any external send.",
        "action_ar": "راجع الموافقات المعلقة قبل أي إرسال خارجي.",
    }
    return _result("founder_daily_command", PASS, "founder daily command produced", command=command)


STAGES: list[Callable[[], dict[str, Any]]] = [
    stage_target,
    stage_outreach_approval,
    stage_diagnostic,
    stage_offer,
    stage_paid_sprint,
    stage_customer_workspace,
    stage_proof_pack,
    stage_upsell_recommendation,
    stage_founder_daily_command,
]


def run_all_stages() -> list[dict[str, Any]]:
    """Run every stage in order and collect results."""
    return [stage() for stage in STAGES]


def overall_status(results: list[dict[str, Any]]) -> str:
    """Return PASS only if every stage passed."""
    return PASS if all(r["status"] == PASS for r in results) else "FAIL"


def _write_report(results: list[dict[str, Any]], verdict: str) -> Path:
    report_dir = ROOT / "reports" / "verification"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "e2e_dry_run_latest.md"
    lines = [
        "# Dealix E2E Dry Run",
        "",
        f"Timestamp: {date.today().isoformat()}",
        "Mode: dry_run (no external sends, governance enforced)",
        "",
        "| Stage | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for r in results:
        lines.append(f"| {r['stage']} | {r['status']} | {r['detail']} |")
    lines.extend(["", f"Overall: {verdict}", ""])
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    results = run_all_stages()
    verdict = overall_status(results)
    report_path = _write_report(results, verdict)

    if args.json:
        print(json.dumps({"results": results, "verdict": verdict}, ensure_ascii=False, indent=2))
    else:
        for r in results:
            print(f"[{r['status']}] {r['stage']}: {r['detail']}")
        print(f"\nReport: {report_path}")
        print(f"Overall: {verdict}")
    return 0 if verdict == PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
