"""
Learning Loop — daily reflection over the proof log.

Reads the append-only proof trail, computes simple, honest metrics per
strategy (how many drafts prepared, how many approvals requested, blocked
counts, approval outcomes) and persists a rolling "scores" file the planner
can later use to bias priority. No black-box learning — just transparent,
auditable counters the founder can inspect.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from .proof_logger import ProofLogger


class LearningLoop:
    def __init__(self, root: Path | str, proof_logger: ProofLogger) -> None:
        self.root = Path(root) / "learning"
        self.root.mkdir(parents=True, exist_ok=True)
        self.proofs = proof_logger
        self.scores_path = self.root / "strategy_scores.json"

    def _empty_metric(self) -> dict[str, int]:
        return {"drafted": 0, "approval_requested": 0, "blocked": 0, "approved": 0, "rejected": 0}

    def compute(self) -> dict[str, Any]:
        by_strategy: dict[str, dict[str, int]] = defaultdict(self._empty_metric)

        for record in self.proofs.read_all():
            event = record.get("event_type", "")
            payload = record.get("payload", {}) or {}
            sid = str(payload.get("strategy_id", "")) or "_unknown"
            if event == "action_drafted":
                by_strategy[sid]["drafted"] += 1
            elif event == "approval_requested":
                by_strategy[sid]["approval_requested"] += 1
            elif event == "step_blocked":
                by_strategy[sid]["blocked"] += 1
            elif event == "approval_decided":
                if payload.get("approved"):
                    by_strategy[sid]["approved"] += 1
                else:
                    by_strategy[sid]["rejected"] += 1

        scores: dict[str, Any] = {}
        for sid, m in by_strategy.items():
            decided = m["approved"] + m["rejected"]
            approval_rate = (m["approved"] / decided) if decided else None
            # Transparent weight: reward drafted volume + approval rate, damp blocks.
            weight = m["drafted"] + 2 * m["approved"] - m["blocked"]
            scores[sid] = {
                **m,
                "approval_rate": approval_rate,
                "weight": weight,
            }

        summary = {
            "strategies": scores,
            "totals": {
                "strategies_seen": len(scores),
                "drafted": sum(s["drafted"] for s in scores.values()),
                "approval_requested": sum(s["approval_requested"] for s in scores.values()),
                "blocked": sum(s["blocked"] for s in scores.values()),
            },
        }
        return summary

    def run(self) -> dict[str, Any]:
        summary = self.compute()
        self.scores_path.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return summary

    def scores(self) -> dict[str, Any]:
        if not self.scores_path.exists():
            return {}
        return json.loads(self.scores_path.read_text(encoding="utf-8"))
