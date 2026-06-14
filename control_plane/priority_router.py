"""Priority Router.

Given a CEO Business Score dict (with ``metrics``), decide the single
highest-leverage next action across Revenue, Sales, Finance, Delivery,
Client Success, and Learning.
"""
from __future__ import annotations


def route_priority(score: dict) -> dict:
    metrics = score.get("metrics", {})
    if metrics.get("lead_count", 0) < 25:
        return {
            "area": "Revenue",
            "priority": "Add 25 qualified leads",
            "reason": "Pipeline is below minimum execution threshold.",
            "action": "Update pipeline/pipeline_tracker.csv.",
        }
    if metrics.get("contacted", 0) < 25:
        return {
            "area": "Sales",
            "priority": "Send 25 founder-led DMs",
            "reason": "Outbound target has not been reached.",
            "action": "Use Revenue Sprint Founder DM Pack.",
        }
    if metrics.get("sample_sent", 0) < 3:
        return {
            "area": "Sales",
            "priority": "Prepare 3 sample packs",
            "reason": "Samples are needed to convert interest into proposals.",
            "action": "Use offers/revenue_sprint/sample_pack_template.md.",
        }
    if metrics.get("proposal_sent", 0) < 1:
        return {
            "area": "Revenue",
            "priority": "Send 1 proposal",
            "reason": "No proposal means no near-term payment path.",
            "action": "Use proposal_fast_template.md.",
        }
    if metrics.get("cash_collected", 0) <= 0 and metrics.get("proposal_sent", 0) >= 1:
        return {
            "area": "Finance",
            "priority": "Pursue payment, PO, or written approval",
            "reason": "Proposal exists but no cash is recorded.",
            "action": "Use payment_followup_templates.md.",
        }
    if metrics.get("paid", 0) >= 1 and metrics.get("delivered", 0) < 1:
        return {
            "area": "Delivery",
            "priority": "Deliver with QA",
            "reason": "Paid/approved work must become proof.",
            "action": "Run delivery report and QA checklist.",
        }
    if metrics.get("delivered", 0) >= 1 and metrics.get("retainer", 0) < 1:
        return {
            "area": "Client Success",
            "priority": "Ask for feedback and retainer",
            "reason": "Delivery must convert into retention or proof.",
            "action": "Use feedback_request.md and retainer_ask.md.",
        }
    return {
        "area": "Learning",
        "priority": "Run weekly review and update one system",
        "reason": "Execution loop needs learning and system improvement.",
        "action": "Run weekly-close and commit one playbook update.",
    }
