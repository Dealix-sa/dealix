"""Self-improvement loop — turns a run's aggregate into improvement suggestions.

Read-only reflection: it never mutates data, it proposes what to sharpen next.
"""

from __future__ import annotations

from typing import Any


def reflect(run: dict[str, Any]) -> dict[str, Any]:
    opportunities = run.get("opportunities", [])
    total = len(opportunities)
    hot = sum(1 for o in opportunities if o.get("band") == "hot")
    warm = sum(1 for o in opportunities if o.get("band") == "warm")
    cold = total - hot - warm

    hypothesis_targets = sum(
        1 for o in opportunities if o.get("source") == "hypothesis"
    )

    improvements: list[str] = []
    if hypothesis_targets == total and total > 0:
        improvements.append(
            "All targets are hypothesis seeds — replace with real warm-list data before approval."
        )
    if hot == 0 and total > 0:
        improvements.append(
            "No hot opportunities — tighten signal capture (follow-up gaps, leaking leads)."
        )
    if cold > hot + warm and total > 0:
        improvements.append(
            "Cold-heavy list — refine targeting toward personas with known follow-up pain."
        )
    if not improvements:
        improvements.append("Pipeline balanced — proceed to founder approval on top opportunities.")

    return {
        "totals": {"total": total, "hot": hot, "warm": warm, "cold": cold},
        "hypothesis_targets": hypothesis_targets,
        "what_failed": run.get("safety", {}).get("violations", []),
        "improvements": improvements,
        "tomorrow_plan": [
            "استبدال الأهداف الافتراضية ببيانات warm-list حقيقية.",
            "مراجعة أعلى 3 فرص واعتماد drafts.",
            "قياس أول proof pack بعد أول اعتماد.",
        ],
    }
