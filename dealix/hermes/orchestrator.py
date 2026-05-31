"""HermesOrchestrator — the public entry point above dealix-pm.

Lifecycle of dispatch():
  1. Build identity + new run_id.
  2. Governance gate evaluates the intent (refuse / queue / approve).
  3. Router picks task_class, sub_agent, gear.
  4. If approved → invoke the executor callable supplied by the caller.
     If needs_approval → return placeholder; caller surfaces to approval_center.
     If rejected / kill_switched → return refusal.
  5. Audit record written + bridged into friction_log.

This module never sends external traffic itself. Executors are responsible
for the work; the orchestrator's job is doctrine enforcement and audit.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable, Optional

from .audit import (
    AuditWriteError,
    HermesAuditRecord,
    bridge_to_friction_log,
    write,
)
from .governance_gate import Decision, GovernanceDecision, GovernanceGate
from .identity import HermesIdentity, new_run_id
from .integrations import bridge_to_approval_center, bridge_to_capital_ledger
from .router import HermesRouter, Route, TaskClass


Executor = Callable[["HermesTask", Route], dict[str, Any]]


@dataclass
class HermesTask:
    intent: str
    customer_id: str = "dealix_internal"
    channel: str = ""
    hint: Optional[TaskClass] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HermesTaskResult:
    run_id: str
    decision: GovernanceDecision
    route: Optional[Route]
    output: dict[str, Any]
    signature: dict[str, str]
    occurred_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    @property
    def success(self) -> bool:
        return self.decision.decision == Decision.APPROVED.value and bool(self.output.get("ok"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "occurred_at": self.occurred_at,
            "signature": self.signature,
            "governance_decision": {
                "decision": self.decision.decision,
                "reason": self.decision.reason,
                "safe_alternative": self.decision.safe_alternative,
                "matched_rules": self.decision.matched_rules,
                "requires_channel_approval": self.decision.requires_channel_approval,
            },
            "route": (
                {
                    "task_class": self.route.task_class.value,
                    "sub_agent": self.route.sub_agent,
                    "gear": self.route.gear.value,
                    "provider": self.route.gear_config.provider,
                    "model_id": self.route.gear_config.model_id,
                }
                if self.route
                else None
            ),
            "output": self.output,
        }


def _refusal_output(decision: GovernanceDecision) -> dict[str, Any]:
    return {
        "ok": False,
        "kind": "refusal",
        "decision": decision.decision,
        "reason": decision.reason,
        "safe_alternative": decision.safe_alternative,
    }


def _approval_placeholder(decision: GovernanceDecision) -> dict[str, Any]:
    return {
        "ok": True,
        "kind": "queued_for_approval",
        "reason": decision.reason,
        "queued_in": "approval_center",
        "channel": decision.requires_channel_approval,
    }


class HermesOrchestrator:
    """The top-layer orchestrator.

    Caller supplies an executor — a function that, given a task and a route,
    performs the actual work (LLM call, sub-agent spawn, file edit, etc.) and
    returns a dict with at least {"ok": bool}.
    """

    def __init__(
        self,
        *,
        executor: Executor,
        router: Optional[HermesRouter] = None,
        gate: Optional[GovernanceGate] = None,
        identity: Optional[HermesIdentity] = None,
    ) -> None:
        self.executor = executor
        self.identity = identity or HermesIdentity.current()
        self.router = router or HermesRouter()
        self.gate = gate or GovernanceGate(kill_switch=self.identity.kill_switch)

    def dispatch(self, task: HermesTask) -> HermesTaskResult:
        run_id = new_run_id()
        signature = self.identity.signature(run_id)
        decision = self.gate.evaluate(task.intent, channel=task.channel)

        route: Optional[Route] = None
        output: dict[str, Any]

        if decision.decision == Decision.APPROVED.value:
            route = self.router.route(task.intent, hint=task.hint)
            try:
                output = self.executor(task, route) or {"ok": False, "error": "executor returned empty"}
                if "ok" not in output:
                    output["ok"] = False
            except Exception as exc:  # noqa: BLE001 — orchestrator must not crash
                output = {"ok": False, "kind": "executor_error", "error": str(exc)}
        elif decision.decision == Decision.NEEDS_APPROVAL.value:
            output = _approval_placeholder(decision)
        else:
            output = _refusal_output(decision)

        record = HermesAuditRecord(
            run_id=run_id,
            agent_id=self.identity.agent_id,
            task_class=route.task_class.value if route else "",
            customer_id=task.customer_id,
            intent_summary=task.intent[:200],
            intent=task.intent,
            governance_decision={
                "decision": decision.decision,
                "reason": decision.reason,
                "matched_rules": decision.matched_rules,
            },
            sub_agent=route.sub_agent if route else "",
            provider=route.gear_config.provider if route else "",
            model_id=route.gear_config.model_id if route else "",
            success=bool(output.get("ok")),
            error=str(output.get("error", "")),
            output_ref=str(output.get("ref", "")),
            live=output.get("kind") == "live_completion",
        )
        # Charter §6: audit writes are mandatory. If the write fails, the
        # run is marked rejected_audit_failure and the output is replaced
        # with a refusal payload so callers can't act on a result the
        # audit trail does not capture.
        try:
            write(record)
        except AuditWriteError as exc:
            decision = GovernanceDecision(
                decision=Decision.REJECTED.value,
                reason="rejected_audit_failure: " + str(exc)[:120],
                safe_alternative="Investigate audit ledger storage before retrying.",
            )
            output = {
                "ok": False,
                "kind": "audit_write_failed",
                "error": str(exc)[:300],
            }
            return HermesTaskResult(
                run_id=run_id,
                decision=decision,
                route=None,
                output=output,
                signature=signature,
            )

        bridge_to_friction_log(record, decision)

        # Bridges only fire on truly-successful approved runs. A run that
        # was gate-approved but failed in the executor (e.g. cost budget
        # exceeded, live LLM error, no_executor) must NOT trigger an
        # approval queue entry or a capital-asset registration — that
        # would be a phantom artefact. record.success captures
        # output.get("ok") at audit-write time.
        if record.success:
            # Capital ledger reads the produced content first (from a
            # successful live completion), falls back to the envelope's
            # deliverable description, then the intent. This keeps
            # non-negotiable #11 honest when live mode is active without
            # forcing every envelope-only run to register an asset.
            asset_text = (
                str(output.get("content", ""))
                or str(output.get("deliverable", ""))
            )
            approval_id = bridge_to_approval_center(
                record, decision, intent=task.intent
            )
            if approval_id:
                output["approval_id"] = approval_id
            capital_asset_id = bridge_to_capital_ledger(
                record, decision, intent=task.intent, deliverable_text=asset_text
            )
            if capital_asset_id:
                output["capital_asset_id"] = capital_asset_id

        # The needs_approval path advertises queued_in=approval_center
        # even before the bridge runs. If the bridge silently dropped
        # (missing customer_id, ImportError, store unavailable), correct
        # the output so the caller knows the queue did not actually
        # receive the draft.
        if (
            decision.decision == Decision.NEEDS_APPROVAL.value
            and "approval_id" not in output
        ):
            output["queued_in"] = "approval_center_unavailable"
            output["ok"] = False

        return HermesTaskResult(
            run_id=run_id,
            decision=decision,
            route=route,
            output=output,
            signature=signature,
        )
