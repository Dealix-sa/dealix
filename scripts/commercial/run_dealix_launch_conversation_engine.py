#!/usr/bin/env python3
"""Run the Dealix Launch Conversation & Negotiation Engine (draft-only).

Usage:
    python scripts/commercial/run_dealix_launch_conversation_engine.py \
        --mode draft-only --limit 25

Generates (all draft-only, nothing sent):
    reports/dealix_conversation_negotiation/latest.json
    reports/dealix_conversation_negotiation/latest.md
    reports/dealix_conversation_negotiation/approval_queue.csv
    reports/dealix_conversation_negotiation/opportunity_graph.csv
    reports/dealix_conversation_negotiation/email_drafts.csv
    reports/dealix_conversation_negotiation/whatsapp_drafts.csv
    reports/dealix_conversation_negotiation/negotiation_playbooks.csv
    reports/dealix_conversation_negotiation/proof_pack.md
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.conversation_engine import engine  # noqa: E402
from dealix.conversation_engine.channel_adapter import (  # noqa: E402
    email_csv_row,
    whatsapp_csv_row,
)

REPORT_DIR = ROOT / "reports" / "dealix_conversation_negotiation"


def _write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fieldnames})


def _write_reports(payload: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    (REPORT_DIR / "latest.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # approval_queue.csv
    _write_csv(
        REPORT_DIR / "approval_queue.csv",
        [
            {
                "id": a["id"],
                "channel": a["channel"],
                "target_company": a["target_company"],
                "contact_name": a["contact_name"],
                "draft": " ".join(str(a["draft"]).split()),
                "reason": a["reason"],
                "risk": a["risk"],
                "approval_required": str(a["approval_required"]).lower(),
                "status": a["status"],
                "decision_options": "|".join(a["decision_options"]),
            }
            for a in payload.get("approval_queue", [])
        ],
        [
            "id", "channel", "target_company", "contact_name", "draft",
            "reason", "risk", "approval_required", "status", "decision_options",
        ],
    )

    # opportunity_graph.csv
    _write_csv(
        REPORT_DIR / "opportunity_graph.csv",
        [
            {
                "company": o["company"],
                "segment": o["segment"],
                "persona": o["persona"],
                "score": str(o["score"]),
                "band": o["band"],
                "offer": o.get("offer_match", {}).get("primary_offer_id", ""),
                "pain_hypothesis_ar": o.get("pain_hypothesis_ar", ""),
                "source": o.get("source", ""),
            }
            for o in payload.get("opportunities", [])
        ],
        ["company", "segment", "persona", "score", "band", "offer", "pain_hypothesis_ar", "source"],
    )

    # email_drafts.csv / whatsapp_drafts.csv
    _write_csv(
        REPORT_DIR / "email_drafts.csv",
        [email_csv_row(d.get("company", ""), d.get("contact_name", ""), d) for d in payload.get("email_drafts", [])],
        ["company", "contact_name", "from_email", "subject", "short_version", "cta", "approval_required", "status"],
    )
    _write_csv(
        REPORT_DIR / "whatsapp_drafts.csv",
        [whatsapp_csv_row(d.get("company", ""), d.get("contact_name", ""), d) for d in payload.get("whatsapp_drafts", [])],
        ["company", "contact_name", "opening_message", "short_value_message", "permission_cta", "cold_send_forbidden", "approval_required", "status"],
    )

    # negotiation_playbooks.csv
    _write_csv(
        REPORT_DIR / "negotiation_playbooks.csv",
        [
            {
                "target": p["target"],
                "offer": p["offer"],
                "starting_position": p["starting_position"],
                "minimum_commitment": p["minimum_commitment"],
                "likely_objections": "|".join(p["likely_objections"]),
                "close_question": p["close_question"],
                "next_best_action": p["next_best_action"],
                "approval_required": str(p["approval_required"]).lower(),
            }
            for p in payload.get("negotiation_playbooks", [])
        ],
        [
            "target", "offer", "starting_position", "minimum_commitment",
            "likely_objections", "close_question", "next_best_action", "approval_required",
        ],
    )

    (REPORT_DIR / "latest.md").write_text(_render_command_report(payload), encoding="utf-8")
    (REPORT_DIR / "proof_pack.md").write_text(_render_proof_pack(payload), encoding="utf-8")
    (REPORT_DIR / "slack_brief.md").write_text(_render_slack_brief(payload), encoding="utf-8")


def _render_slack_brief(payload: dict) -> str:
    """Internal Slack brief draft for the founder — draft-only, never posted."""
    s = payload.get("summary", {})
    top = payload.get("opportunities", [])[:3]
    lines = [
        ":rocket: *Dealix Launch Brief (draft — internal only)*",
        f"> verdict: `{payload.get('verdict')}` · mode: `{payload.get('mode')}`",
        "",
        f"*Highest-leverage action:* {payload.get('highest_leverage_action', '')}",
        "",
        "*Top opportunities:*",
    ]
    for o in top:
        lines.append(
            f"• {o.get('company')} — score {o.get('score')} ({o.get('band')}) → "
            f"{o.get('offer_match', {}).get('primary_offer_id', '')}"
        )
    lines += [
        "",
        f"*Approval queue:* {s.get('approval_items', 0)} item(s) pending founder decision "
        f"(approve/revise/reject/hold).",
        f"*Drafts ready:* {s.get('email_drafts', 0)} email · {s.get('whatsapp_drafts', 0)} whatsapp "
        f"(warm-only) · {s.get('negotiation_playbooks', 0)} negotiation playbook(s).",
        "",
        "_Nothing is sent. Review the approval queue before any outbound._",
        "",
    ]
    return "\n".join(lines)


def _render_command_report(payload: dict) -> str:
    s = payload.get("summary", {})
    lines = [
        "# Dealix Daily Launch Command",
        "",
        f"- generated_at: `{payload.get('generated_at')}`",
        f"- mode: `{payload.get('mode')}`",
        f"- founder_email: `{payload.get('founder_email')}`",
        "",
        "## Verdict",
        "",
        f"`{payload.get('verdict')}`",
        "",
        "## Today's highest leverage action",
        "",
        payload.get("highest_leverage_action", ""),
        "",
        "## Top opportunities",
        "",
        "| Company | Segment | Offer | Score | Band | Next Action |",
        "|---|---|---|---|---|---|",
    ]
    for o in payload.get("opportunities", [])[:10]:
        lines.append(
            f"| {o['company']} | {o['segment']} | {o.get('offer_match', {}).get('primary_offer_id', '')} "
            f"| {o['score']} | {o['band']} | إرسال ملخص (draft) |"
        )
    lines += ["", "## Approval Queue", "", "| ID | Channel | Target | Risk | Decision |", "|---|---|---|---|---|"]
    for a in payload.get("approval_queue", []):
        lines.append(
            f"| {a['id']} | {a['channel']} | {a['target_company']} | {a['risk']} | {'/'.join(a['decision_options'])} |"
        )
    lines += ["", "## Negotiation Queue", "", "| Target | Offer | Close Question | Next Move |", "|---|---|---|---|"]
    for p in payload.get("negotiation_playbooks", []):
        lines.append(f"| {p['target']} | {p['offer']} | {p['close_question']} | {p['next_best_action']} |")
    lines += ["", "## Follow-up Queue", "", "| Target | Channel | Timing | Approval |", "|---|---|---|---|"]
    for f in payload.get("followups", []):
        lines.append(f"| {f['target']} | {f['channel']} | {f['timing']} | required |")

    learning = payload.get("learning", {})
    lines += ["", "## What failed / what to improve", ""]
    for item in learning.get("improvements", []):
        lines.append(f"- {item}")
    lines += ["", "## Tomorrow plan", ""]
    for item in learning.get("tomorrow_plan", []):
        lines.append(f"- {item}")
    lines += [
        "",
        "## Summary",
        "",
        f"- opportunities: `{s.get('opportunities', 0)}`",
        f"- approval_items: `{s.get('approval_items', 0)}`",
        f"- email_drafts: `{s.get('email_drafts', 0)}`",
        f"- whatsapp_drafts: `{s.get('whatsapp_drafts', 0)}`",
        f"- negotiation_playbooks: `{s.get('negotiation_playbooks', 0)}`",
        f"- proof_packs: `{s.get('proof_packs', 0)}`",
        f"- all_external_require_approval: `{s.get('all_external_require_approval', False)}`",
        f"- live_send: `{s.get('live_send', False)}`",
        "",
        "> Draft-only. Nothing is sent. Founder approves every external message.",
        "",
    ]
    return "\n".join(lines)


def _render_proof_pack(payload: dict) -> str:
    lines = ["# Dealix Proof Pack (draft-only)", ""]
    for pack in payload.get("proof_packs", []):
        lines += [
            f"## {pack.get('company', '')}",
            "",
            f"- pain_hypothesis: {pack.get('pain_hypothesis', '')}",
            f"- evidence_source: `{pack.get('evidence_source', '')}`",
            f"- opportunity_score: `{pack.get('opportunity_score', 0)}`",
            f"- offer_match: {pack.get('offer_match', '')}",
            f"- expected_outcome: {pack.get('expected_outcome', '')}",
            f"- what_we_will_measure: {', '.join(pack.get('what_we_will_measure', []))}",
            f"- what_client_provides: {', '.join(pack.get('what_client_provides', []))}",
            f"- what_dealix_delivers: {', '.join(pack.get('what_dealix_delivers', []))}",
            f"- next_approval_needed: {pack.get('next_approval_needed', '')}",
            f"- safe (no fake claims): `{pack.get('safe', True)}`",
            "",
        ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Dealix Launch Conversation & Negotiation Engine")
    parser.add_argument("--mode", default="draft-only", help="operating mode (draft-only)")
    parser.add_argument("--limit", type=int, default=25, help="max targets to process")
    args = parser.parse_args(argv)

    payload = engine.run(mode=args.mode, limit=args.limit)
    _write_reports(payload)

    safe = payload.get("safety", {}).get("safe", False)
    print("DEALIX_LAUNCH_CONVERSATION_ENGINE=" + ("PASS" if safe else "BLOCKED"))
    print(f"mode={args.mode}")
    print(f"verdict={payload.get('verdict')}")
    print("reports/dealix_conversation_negotiation/latest.json")
    print("reports/dealix_conversation_negotiation/latest.md")
    print("reports/dealix_conversation_negotiation/approval_queue.csv")
    print("reports/dealix_conversation_negotiation/opportunity_graph.csv")
    print("reports/dealix_conversation_negotiation/email_drafts.csv")
    print("reports/dealix_conversation_negotiation/whatsapp_drafts.csv")
    print("reports/dealix_conversation_negotiation/negotiation_playbooks.csv")
    print("reports/dealix_conversation_negotiation/proof_pack.md")
    print("reports/dealix_conversation_negotiation/slack_brief.md")
    if not safe:
        for v in payload.get("safety", {}).get("violations", []):
            print("BLOCKED_BY_SAFETY_GUARD: " + v)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
