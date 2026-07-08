"""
Orchestrator — the Autonomous OS control loop.

One `run()` performs a full, draft-only cycle:

  1. Tripwire: assert the environment is draft-only.
  2. Load strategies from the registry.
  3. For each active strategy: plan it (SafetyGate routes each step).
  4. Dispatch:
       - AUTO_DRAFT  -> ActionQueue (internal draft artifact)
       - APPROVAL    -> ApprovalQueue (founder decides; nothing is sent)
       - BLOCKED     -> recorded only (never queued)
  5. Fold in the GrowthEngine's commercial recommendations.
  6. Log everything to the ProofLogger.
  7. Run the LearningLoop over the accumulated proof trail.
  8. Write a human-readable daily report.

The orchestrator never sends anything and never approves anything.
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any

from . import integrations
from .action_queue import ActionQueue
from .adapters import all_status as adapters_status
from .adapters.twenty_adapter import TwentyCRMAdapter
from .adapters.whatsapp_draft_adapter import WhatsAppDraftAdapter
from .approval_queue import ApprovalQueue
from .draft_composer import DraftComposer
from .execution_planner import ExecutionPlanner, PlannedStep
from .growth_engine import GrowthContext, GrowthEngine
from .learning_loop import LearningLoop
from .model_router import ModelRouter
from .proof_logger import ProofLogger
from .safety_gate import Route, SafetyGate
from .strategy_registry import StrategyRegistry


class AutonomousOS:
    def __init__(
        self,
        *,
        runtime_root: Path | str,
        strategies_dir: Path | str | None = None,
        env: dict[str, str] | None = None,
    ) -> None:
        self.root = Path(runtime_root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.gate = SafetyGate(env=env)
        self.registry = StrategyRegistry(strategies_dir=strategies_dir)
        self.planner = ExecutionPlanner(self.gate)
        self.actions = ActionQueue(self.root)
        self.proofs = ProofLogger(self.root)
        # Approval queue logs founder decisions to the proof trail so the
        # learning loop can count real approval/rejection outcomes.
        self.approvals = ApprovalQueue(self.root, proof_logger=self.proofs)
        self.learning = LearningLoop(self.root, self.proofs)
        self.router = ModelRouter(env=env)
        self.growth = GrowthEngine()
        self._env = env
        self.composer = DraftComposer(env=env)
        self.crm = TwentyCRMAdapter(env=env, local_snapshot=self.root / "crm_context.json")
        self.whatsapp = WhatsAppDraftAdapter(env=env)

    # ---- dispatch helpers ----
    def _compose(self, step: PlannedStep, language: str) -> dict[str, Any]:
        return self.composer.compose(
            action=step.action,
            strategy_id=step.strategy_id,
            language=language,
            offer=step.offer,
            description=step.description,
        )

    def _dispatch_step(self, step: PlannedStep, language: str) -> str:
        if step.route == Route.AUTO_DRAFT.value:
            composed = self._compose(step, language)
            payload = {**step.to_dict(), "composed": composed}
            self.actions.enqueue(
                strategy_id=step.strategy_id,
                action=step.action,
                summary=step.description or step.action,
                offer=step.offer,
                payload=payload,
            )
            self.proofs.log(
                "action_drafted", {**step.to_dict(), "mode": composed["generation_mode"]}
            )
            return "drafted"
        if step.route == Route.APPROVAL.value:
            composed = self._compose(step, language)
            draft_text = str(composed["draft_text"])
            payload: dict[str, Any] = {**step.to_dict(), "composed": composed}
            # For WhatsApp steps, also attach a review-ready payload draft that
            # is provably incapable of being sent.
            if (step.channel or "").lower() == "whatsapp":
                wa = self.whatsapp.build_draft(
                    to_label=f"account:{step.strategy_id}",
                    message=draft_text,
                    account_id=None,
                    consent_confirmed=False,
                )
                payload["whatsapp_draft"] = wa.data
            self.approvals.submit(
                strategy_id=step.strategy_id,
                action=step.action,
                draft=draft_text,
                reason=step.reason,
                risk=step.risk,
                channel=step.channel,
                offer=step.offer,
                payload=payload,
            )
            self.proofs.log(
                "approval_requested", {**step.to_dict(), "mode": composed["generation_mode"]}
            )
            return "approval"
        # blocked
        self.proofs.log("step_blocked", step.to_dict())
        return "blocked"

    # ---- main loop ----
    def run(self, growth_context: dict[str, Any] | None = None) -> dict[str, Any]:
        self.gate.assert_draft_only()
        self.registry.load()

        model = self.router.route("strategy")
        self.proofs.log(
            "run_started",
            {
                "safety": self.gate.summary(),
                "model": model.to_dict(),
                "strategies_loaded": len(self.registry),
            },
        )

        counters = {"drafted": 0, "approval": 0, "blocked": 0}
        plans: list[dict[str, Any]] = []

        for strategy in self.registry.active():
            plan = self.planner.plan(strategy)
            self.proofs.log("plan_created", plan.to_dict())
            for step in plan.steps:
                outcome = self._dispatch_step(step, strategy.language)
                counters[outcome] += 1
            plans.append(plan.to_dict())

        # Commercial context: explicit override wins; otherwise pull from CRM
        # adapter (which itself falls back to a local snapshot / zeros).
        if growth_context:
            ctx = GrowthContext.from_dict(growth_context)
            ctx_source = "explicit"
        else:
            crm_result = self.crm.fetch_growth_context()
            ctx = GrowthContext.from_dict(crm_result.data)
            ctx_source = f"twenty_crm:{crm_result.mode}"
        recs = [a.to_dict() for a in self.growth.recommend(ctx)]
        self.proofs.log(
            "growth_recommendations",
            {"context": ctx.__dict__, "context_source": ctx_source, "actions": recs},
        )

        # Reflect.
        learning = self.learning.run()

        summary = {
            "date": dt.date.today().isoformat(),
            "mode": "draft_only",
            "model": model.to_dict(),
            "strategies_active": len(self.registry.active()),
            "counters": counters,
            "approval_stats": self.approvals.stats(),
            "growth_context_source": ctx_source,
            "growth_recommendations": recs,
            "adapters": adapters_status(self._env),
            "integrations": integrations.summary(),
            "learning": learning.get("totals", {}),
            "plans": plans,
        }
        self._write_report(summary)
        self.proofs.log("run_completed", {"counters": counters})
        return summary

    # ---- reporting ----
    def _write_report(self, summary: dict[str, Any]) -> None:
        report_dir = self.root / "reports"
        report_dir.mkdir(parents=True, exist_ok=True)
        day = summary["date"]
        (report_dir / f"autonomous-os-{day}.json").write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        lines = [
            f"# Dealix Autonomous Growth OS — {day}",
            "",
            f"Mode: **{summary['mode']}** (no external send, approval-first)",
            f"Model: {summary['model']['provider']}/{summary['model']['model']} "
            f"(local={summary['model']['is_local']})",
            "",
            "## Cycle counters",
            f"- Drafts prepared: {summary['counters']['drafted']}",
            f"- Sent to approval queue: {summary['counters']['approval']}",
            f"- Blocked by safety doctrine: {summary['counters']['blocked']}",
            "",
            "## Commercial recommendations (draft-only)",
        ]
        for rec in summary["growth_recommendations"]:
            lines.append(
                f"- [{rec['priority']}] {rec['title']} "
                f"→ {rec['offer_label']} ({rec['price_band_sar']} SAR)"
            )
        lines += [
            "",
            f"_Commercial context source: {summary.get('growth_context_source', 'n/a')}_",
            "",
            "## Core-stack adapters",
        ]
        for ad in summary.get("adapters", []):
            lines.append(f"- {ad['name']}: {ad['mode']} — {ad['detail']}")
        lines += [
            "",
            "## Approval queue",
            f"- Pending: {summary['approval_stats'].get('pending', 0)}",
            "",
            "> All external actions require founder approval. Nothing was sent.",
            "",
        ]
        (report_dir / f"autonomous-os-{day}.md").write_text("\n".join(lines), encoding="utf-8")
