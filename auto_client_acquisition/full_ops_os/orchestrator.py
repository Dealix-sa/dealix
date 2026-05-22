"""FullOpsOrchestrator — the spine of the Full Ops Sales System.

Sequences the 12-stage golden chain over a control-plane ``WorkflowRun``.
For each stage it: runs the stage business logic, classifies the action
against the auto-exec gate, emits an ``EventEnvelope`` + a control event,
routes non-auto actions to both the control-plane queue and the founder
approval inbox, and writes an append-only ``AuditEntry``.

Wave 20 wires stages 1-8 (signal intake → approval gate); stages 9-12 are
stubbed and wired in Wave 21.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.approval_center import (
    ApprovalRequest,
    get_default_approval_store,
)
from auto_client_acquisition.control_plane_os.repositories import (
    InMemoryControlPlaneRepository,
    WorkflowRun,
)
from auto_client_acquisition.full_ops_os import audit_store
from auto_client_acquisition.full_ops_os.agents import (
    CONDUCTOR_ID,
    register_full_ops_agents,
)
from auto_client_acquisition.full_ops_os.auto_exec import BLOCKED, governed_dispatch
from auto_client_acquisition.full_ops_os.gate import GateDecision
from auto_client_acquisition.full_ops_os.stage_logic import run_stage_logic
from auto_client_acquisition.full_ops_os.stages import (
    STAGES,
    Stage,
    first_stage,
    next_stage,
    stage_spec,
)
from core.logging import get_logger
from dealix.classifications import ApprovalClass, ReversibilityClass, SensitivityClass
from dealix.contracts.audit_log import AuditAction, AuditEntry
from dealix.contracts.event_envelope import EventEnvelope

log = get_logger(__name__)

WORKFLOW_ID = "full_ops_sales"


@dataclass(frozen=True, slots=True)
class StageResult:
    """Outcome of running one stage."""

    run_id: str
    stage: Stage
    action_type: str
    gate: GateDecision
    auto_executed: bool
    approval_ticket_id: str | None
    approval_request_id: str | None
    worker_agent: str
    director_agent: str
    metrics: dict[str, Any]
    event_id: str
    control_event_id: str
    audit_id: str

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "stage": self.stage.name,
            "stage_index": int(self.stage),
            "action_type": self.action_type,
            "gate": self.gate.to_dict(),
            "auto_executed": self.auto_executed,
            "approval_ticket_id": self.approval_ticket_id,
            "approval_request_id": self.approval_request_id,
            "worker_agent": self.worker_agent,
            "director_agent": self.director_agent,
            "metrics": self.metrics,
            "event_id": self.event_id,
            "control_event_id": self.control_event_id,
            "audit_id": self.audit_id,
        }


class FullOpsOrchestrator:
    """Drives a sell-deliver-expand workflow run, stage by stage."""

    def __init__(
        self,
        repo: InMemoryControlPlaneRepository | None = None,
        *,
        tenant_id: str = "default",
        actor: str = CONDUCTOR_ID,
    ) -> None:
        self.repo = repo or InMemoryControlPlaneRepository()
        self.tenant_id = tenant_id
        self.actor = actor
        # Identity gate (#9): the agent pyramid must exist before any run.
        register_full_ops_agents()

    # ── lifecycle ────────────────────────────────────────────────
    def start_run(
        self,
        *,
        customer_id: str,
        lead: dict[str, Any] | None = None,
        correlation_id: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> WorkflowRun:
        """Register a new Full Ops workflow run.

        ``lead`` carries the input record (company, sector, request text,
        discovery flags). It is kept in the run's in-memory metadata only.
        """
        run_metadata: dict[str, Any] = dict(metadata or {})
        run_metadata["lead"] = dict(lead or {})
        run_metadata["state"] = {}
        run = self.repo.register_workflow_run(
            tenant_id=self.tenant_id,
            workflow_id=WORKFLOW_ID,
            customer_id=customer_id,
            correlation_id=correlation_id,
            metadata=run_metadata,
        )
        self._audit(
            run=run,
            action=AuditAction.WORKFLOW_STARTED,
            outcome="ok",
            reason="full_ops_run_started",
            details={"customer_id": customer_id, "lead_fields": sorted(run_metadata["lead"].keys())},
        )
        log.info("full_ops_run_started", run_id=run.run_id, customer_id=customer_id)
        return run

    # ── stage execution ──────────────────────────────────────────
    def run_stage(self, run_id: str, stage: Stage) -> StageResult:
        """Execute one stage: stage logic, governed dispatch, emit, audit."""
        run = self.repo.get_run(tenant_id=self.tenant_id, run_id=run_id)
        spec = stage_spec(stage)
        dispatch = governed_dispatch(stage)
        gate = dispatch.gate

        if dispatch.mode == BLOCKED:
            self._audit(
                run=run,
                action=AuditAction.POLICY_DENIED,
                outcome="blocked",
                reason=dispatch.reason,
                gate=gate,
                details={"stage": stage.name, "dispatch": dispatch.to_dict()},
            )
            raise ValueError(
                f"stage {stage.name} blocked by governance: {dispatch.reason}"
            )

        # Stage business logic — deterministic, no external side effects.
        lead: dict[str, Any] = dict(run.metadata.get("lead", {}))
        run_state: dict[str, Any] = run.metadata.setdefault("state", {})
        output = run_stage_logic(stage, lead, run_state)
        run_state[stage.name] = output.state

        envelope = EventEnvelope(
            source=spec.event_source,
            type=spec.event_type,
            tenant_id=self.tenant_id,
            entity_id=run.customer_id,
            subject=run_id,
            correlation_id=run.correlation_id,
            actor_type="workflow",
            actor_id=self.actor,
            approval_class=gate.approval_class,
            reversibility_class=gate.reversibility_class,
            sensitivity_class=gate.sensitivity_class,
            data={
                "stage": stage.name,
                "run_id": run_id,
                "module": spec.module,
                "worker_agent": dispatch.worker_agent,
                "director_agent": dispatch.director_agent,
                "metrics": output.metrics,
            },
        )

        approval_ticket_id: str | None = None
        approval_request_id: str | None = None
        if dispatch.auto_executes:
            auto_executed = True
            decision = "auto_executed"
            audit_action = AuditAction.POLICY_ALLOWED
            audit_outcome = "ok"
        else:
            auto_executed = False
            decision = "approval_requested"
            audit_action = AuditAction.APPROVAL_REQUESTED
            audit_outcome = "escalated"
            ticket = self.repo.request_approval(
                tenant_id=self.tenant_id,
                action_type=spec.action_type,
                description=f"Full Ops stage {stage.name} for run {run_id}",
                requested_by=self.actor,
                source_module="full_ops_os",
                subject_type="workflow_run",
                subject_id=run_id,
                run_id=run_id,
                metadata={
                    "stage": stage.name,
                    "gate_reason": dispatch.reason,
                    "worker_agent": dispatch.worker_agent,
                },
            )
            approval_ticket_id = ticket.ticket_id
            approval_request_id = self._queue_founder_approval(
                run=run, stage=stage, spec=spec, gate=gate
            )

        control_event = self.repo.append_event(
            tenant_id=self.tenant_id,
            event_type=spec.event_type,
            source_module="full_ops_os",
            actor=self.actor,
            subject_type="workflow_run",
            subject_id=run_id,
            run_id=run_id,
            correlation_id=run.correlation_id,
            decision=decision,
            payload={
                "stage": stage.name,
                "action_type": spec.action_type,
                "auto_executed": auto_executed,
                "approval_ticket_id": approval_ticket_id,
                "approval_request_id": approval_request_id,
                "worker_agent": dispatch.worker_agent,
                "director_agent": dispatch.director_agent,
            },
        )

        audit = self._audit(
            run=run,
            action=audit_action,
            outcome=audit_outcome,
            reason=dispatch.reason,
            event_id=envelope.id,
            gate=gate,
            details={
                "stage": stage.name,
                "action_type": spec.action_type,
                "auto_executed": auto_executed,
                "approval_ticket_id": approval_ticket_id,
                "approval_request_id": approval_request_id,
                "worker_agent": dispatch.worker_agent,
                "director_agent": dispatch.director_agent,
                "metrics": output.metrics,
            },
        )

        run.current_step = stage.name
        run.updated_at = datetime.now(UTC)
        if stage == Stage.LEARNING:
            run.state = "completed"
            self._audit(
                run=run,
                action=AuditAction.WORKFLOW_COMPLETED,
                outcome="ok",
                reason="full_ops_run_completed",
                details={"run_id": run_id},
            )

        log.info(
            "full_ops_stage_run",
            run_id=run_id,
            stage=stage.name,
            auto_executed=auto_executed,
            gate_reason=gate.reason,
        )
        return StageResult(
            run_id=run_id,
            stage=stage,
            action_type=spec.action_type,
            gate=gate,
            auto_executed=auto_executed,
            approval_ticket_id=approval_ticket_id,
            approval_request_id=approval_request_id,
            worker_agent=dispatch.worker_agent,
            director_agent=dispatch.director_agent,
            metrics=output.metrics,
            event_id=envelope.id,
            control_event_id=control_event.id,
            audit_id=audit.audit_id,
        )

    def _queue_founder_approval(
        self,
        *,
        run: WorkflowRun,
        stage: Stage,
        spec: Any,
        gate: GateDecision,
    ) -> str | None:
        """Queue an approval-required stage into the founder approval inbox.

        The control-plane ticket links the action to the run; this adds the
        founder-facing card in ``approval_center``. Failure here never aborts
        the stage — the control-plane ticket remains the authoritative gate.
        """
        risk = "high" if gate.approval_class == ApprovalClass.A3 else "medium"
        request = ApprovalRequest(
            object_type="full_ops_stage",
            object_id=f"{run.run_id}:{stage.name}",
            action_type=spec.action_type,
            action_mode="approval_required",
            customer_id=run.customer_id,
            summary_ar=f"موافقة مطلوبة — مرحلة {stage.name} في تشغيل المبيعات",
            summary_en=f"Approval required — stage {stage.name} of the sales run",
            risk_level=risk,
            proof_impact="full_ops_stage_progression",
        )
        try:
            stored = get_default_approval_store().create(request)
            return stored.approval_id
        except Exception as exc:  # noqa: BLE001 — inbox is best-effort
            log.warning(
                "full_ops_founder_approval_failed",
                run_id=run.run_id,
                stage=stage.name,
                error=str(exc),
            )
            return None

    def advance(self, run_id: str) -> StageResult:
        """Run the next not-yet-run stage of the workflow."""
        run = self.repo.get_run(tenant_id=self.tenant_id, run_id=run_id)
        if run.current_step is None:
            return self.run_stage(run_id, first_stage())
        nxt = next_stage(Stage[run.current_step])
        if nxt is None:
            raise ValueError(f"run {run_id} already completed all stages")
        return self.run_stage(run_id, nxt)

    def run_all(self, run_id: str) -> list[StageResult]:
        """Run every remaining stage in order."""
        results: list[StageResult] = []
        for spec in STAGES:
            run = self.repo.get_run(tenant_id=self.tenant_id, run_id=run_id)
            if run.current_step is not None and int(Stage[run.current_step]) >= int(spec.stage):
                continue
            results.append(self.run_stage(run_id, spec.stage))
        return results

    # ── introspection ────────────────────────────────────────────
    def trace(self, run_id: str) -> tuple[object, ...]:
        """Return the ordered control-event trace for a run."""
        return self.repo.trace(tenant_id=self.tenant_id, run_id=run_id)

    def audit_trail(self, run_id: str, *, limit: int = 200) -> list[AuditEntry]:
        """Return the audit entries for a run, newest first."""
        return audit_store.list_entries(workflow_id=run_id, limit=limit)

    # ── internals ────────────────────────────────────────────────
    def _audit(
        self,
        *,
        run: WorkflowRun,
        action: AuditAction,
        outcome: str,
        reason: str,
        event_id: str | None = None,
        gate: GateDecision | None = None,
        details: dict[str, object] | None = None,
    ) -> AuditEntry:
        entry = AuditEntry(
            tenant_id=self.tenant_id,
            action=action,
            actor_type="workflow",
            actor_id=self.actor,
            entity_id=run.customer_id,
            event_id=event_id,
            workflow_id=run.run_id,
            approval_class=gate.approval_class if gate else ApprovalClass.A0,
            reversibility_class=gate.reversibility_class if gate else ReversibilityClass.R0,
            sensitivity_class=gate.sensitivity_class if gate else SensitivityClass.S1,
            outcome=outcome,
            reason=reason,
            correlation_id=run.correlation_id,
            details=dict(details or {}),
        )
        return audit_store.record(entry)


__all__ = ["FullOpsOrchestrator", "StageResult", "WORKFLOW_ID"]
