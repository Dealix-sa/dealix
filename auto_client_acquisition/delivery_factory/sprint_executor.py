"""Sprint executor — the stateful state machine the repo was missing.

Wraps the stateless `dealix.commercial.sprint_orchestrator.SprintOrchestrator`
(which runs one day as a pure function) with persistence + day-by-day advance +
the Day-5 founder-approval pause.

State lifecycle::

    start_sprint(ctx)            → status "running", current_day 0
    advance(eid)  (×4)           → runs days 1..4, current_day climbs
    advance(eid)  (day 5)        → Day-5 governance gate BLOCKS →
                                   status "awaiting_approval" (no further days)
    approve_day5(eid)            → founder_approved=True, status "running"
    advance(eid)                 → re-runs day 5 (now complete), then 6, 7
    advance(eid)  (after day 7)  → status "complete"

NOTHING is sent externally. The Day-5 gate is exactly the doctrine's
"no external action without approval" applied to sprint delivery.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from auto_client_acquisition.delivery_factory import sprint_store

TOTAL_DAYS = 7


def _orchestrator():
    # Deferred import keeps module import side-effect-free for `compileall`.
    from dealix.commercial.sprint_orchestrator import SprintOrchestrator
    return SprintOrchestrator()


def _context_from_state(state: dict[str, Any]):
    from dealix.commercial.sprint_orchestrator import SprintContext
    return SprintContext(**state["context"])


def start_sprint(ctx) -> dict[str, Any]:
    """Begin a sprint for the given SprintContext. Persists and returns state."""
    state: dict[str, Any] = {
        "engagement_id": ctx.engagement_id,
        "customer_id": ctx.customer_id,
        "customer_name": ctx.customer_name,
        "sector": ctx.sector,
        "city": ctx.city,
        "current_day": 0,
        "status": "running",
        "awaiting_approval": False,
        "day_results": [],
        "context": asdict(ctx),
        "no_live_send": True,
    }
    return sprint_store.save(state)


def advance(engagement_id: str) -> dict[str, Any] | None:
    """Run the next sprint day. Returns the new state, or None if not found.

    Stops (without running a day) when already complete or paused awaiting the
    Day-5 approval.
    """
    state = sprint_store.get(engagement_id)
    if state is None:
        return None
    if state.get("status") == "complete":
        return state
    if state.get("awaiting_approval"):
        return state  # caller must approve_day5 first

    next_day = int(state.get("current_day", 0)) + 1
    if next_day > TOTAL_DAYS:
        state["status"] = "complete"
        return sprint_store.save(state)

    ctx = _context_from_state(state)
    result = _orchestrator().run_day(next_day, ctx)
    rd = result.to_dict()
    state["day_results"] = [
        r for r in state.get("day_results", []) if r.get("day") != next_day
    ] + [rd]

    if result.status in ("complete", "pending"):
        # "pending" (e.g. Day-4 DRAFT_ONLY) is normal forward progress — the
        # drafts it produced flow through the separate founder approval queue.
        state["current_day"] = next_day
        state["status"] = "complete" if next_day >= TOTAL_DAYS else "running"
        state["awaiting_approval"] = False
    elif next_day == 5 and not ctx.founder_approved:
        # Day-5 governance gate — pause for founder approval.
        state["status"] = "awaiting_approval"
        state["awaiting_approval"] = True
    else:
        state["status"] = "blocked"
    return sprint_store.save(state)


def approve_day5(engagement_id: str, who: str = "founder") -> dict[str, Any] | None:
    """Record founder approval for the Day-5 gate and resume the sprint."""
    state = sprint_store.get(engagement_id)
    if state is None:
        return None
    state.setdefault("context", {})["founder_approved"] = True
    state["awaiting_approval"] = False
    state["status"] = "running"
    state["day5_approved_by"] = who
    return sprint_store.save(state)


def get(engagement_id: str) -> dict[str, Any] | None:
    return sprint_store.get(engagement_id)


def run_to_completion(engagement_id: str, auto_approve: bool = False,
                      max_steps: int = 20) -> dict[str, Any] | None:
    """Convenience for tests/CLI: advance until complete or paused.

    With auto_approve=True, clears the Day-5 gate automatically (used only in
    verification — production always routes Day-5 through a human)."""
    state = sprint_store.get(engagement_id)
    for _ in range(max_steps):
        state = advance(engagement_id)
        if state is None:
            return None
        if state.get("status") == "complete":
            return state
        if state.get("awaiting_approval"):
            if not auto_approve:
                return state
            approve_day5(engagement_id, who="verifier")
    return state


__all__ = [
    "TOTAL_DAYS",
    "start_sprint",
    "advance",
    "approve_day5",
    "get",
    "run_to_completion",
]
