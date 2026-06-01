"""
Daily Brief
===========
Generates the founder's daily command center brief.
Surfaces top opportunities, draft queue, approval queue,
replies, calls, proposals, delivery blockers, and revenue forecast.
"""

from datetime import date


def generate_brief(data: dict | None = None) -> dict:
    """Generate a structured daily brief for the founder."""
    data = data or {}
    today = date.today().isoformat()

    return {
        "date": today,
        "top_opportunities": data.get("top_opportunities", []),
        "draft_queue": data.get("draft_queue", []),
        "approval_queue": data.get("approval_queue", []),
        "replies_to_handle": data.get("replies_to_handle", []),
        "calls_to_book": data.get("calls_to_book", []),
        "proposals_pending": data.get("proposals_pending", []),
        "delivery_blockers": data.get("delivery_blockers", []),
        "channel_risks": data.get("channel_risks", []),
        "revenue_forecast": data.get("revenue_forecast", {}),
        "top_3_actions": _compute_top_actions(data),
        "summary": _compute_summary(data),
    }


def _compute_top_actions(data: dict) -> list[str]:
    actions = []
    if data.get("approval_queue"):
        actions.append(f"Review {len(data['approval_queue'])} items pending approval")
    if data.get("replies_to_handle"):
        actions.append(f"Handle {len(data['replies_to_handle'])} replies")
    if data.get("calls_to_book"):
        actions.append(f"Book {len(data['calls_to_book'])} discovery calls")
    if data.get("proposals_pending"):
        actions.append(f"Follow up on {len(data['proposals_pending'])} proposals")
    if data.get("delivery_blockers"):
        actions.append(f"Unblock {len(data['delivery_blockers'])} delivery items")
    return actions[:3]


def _compute_summary(data: dict) -> str:
    parts = []
    if data.get("top_opportunities"):
        parts.append(f"{len(data['top_opportunities'])} top opportunities")
    if data.get("draft_queue"):
        parts.append(f"{len(data['draft_queue'])} drafts ready")
    if data.get("approval_queue"):
        parts.append(f"{len(data['approval_queue'])} awaiting approval")
    return " | ".join(parts) if parts else "No active items — run growth-dry-run to generate opportunities."


def print_brief(brief: dict) -> None:
    """Print a formatted daily brief to stdout."""
    print(f"\n{'='*60}")
    print(f"  Dealix Founder Daily Brief — {brief['date']}")
    print(f"{'='*60}")
    print(f"\nSummary: {brief['summary']}")
    if brief["top_3_actions"]:
        print("\nTop 3 Actions:")
        for i, action in enumerate(brief["top_3_actions"], 1):
            print(f"  {i}. {action}")
    if brief["channel_risks"]:
        print(f"\nChannel Risks: {len(brief['channel_risks'])} active")
    print(f"\n{'='*60}\n")
