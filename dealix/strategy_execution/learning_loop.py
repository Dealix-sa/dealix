"""Learning loop — turns today's run into notes that bias tomorrow's run.

No ML, no persistence of secrets. Just heuristics: which strategies produced the
most approval-ready drafts, where the engine was blocked, and what the founder
should decide next."""

from __future__ import annotations

from collections import Counter

from .schemas import Action, Strategy


def build_learning_notes(
    strategies: list[Strategy], actions: list[Action]
) -> list[str]:
    notes: list[str] = []

    executed = Counter(a.strategy for a in actions if a.status == "executed_internal")
    queued = Counter(a.strategy for a in actions if a.status == "queued_for_approval")
    blocked = Counter(a.strategy for a in actions if a.status == "blocked")

    if executed:
        top = executed.most_common(1)[0]
        notes.append(
            f"Most internal progress today: '{top[0]}' ({top[1]} internal actions). "
            "Keep prioritising it while it produces artifacts."
        )
    if queued:
        top = queued.most_common(1)[0]
        notes.append(
            f"Largest approval backlog: '{top[0]}' ({top[1]} drafts waiting). "
            "Founder review here unblocks the most downstream work."
        )
    if blocked:
        notes.append(
            "Live actions were correctly blocked: "
            + ", ".join(f"{k} ({v})" for k, v in blocked.items())
            + ". These stay manual until an approved controlled-live PR exists."
        )
    if not actions:
        notes.append("No actions generated — check that strategy files loaded.")

    # Stop-condition reminders from the strategies themselves.
    for strat in strategies:
        for cond in strat.stop_conditions:
            if cond:
                notes.append(f"[{strat.name}] stop-condition to watch: {cond}")
                break

    notes.append(
        "Learning rule for next run: rank strategies by (real evidence events "
        "produced) first, then by approval-ready drafts, then by priority."
    )
    return notes
