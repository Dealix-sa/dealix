"""FullOpsOrchestrator — the spine of the Full Ops Sales System.

Sequences the 12-stage golden chain over a control-plane ``WorkflowRun``.
For each stage it: classifies the stage action against the auto-exec gate,
emits an ``EventEnvelope`` + a control event, routes non-auto actions to the
approval queue, and writes an append-only ``AuditEntry``.

Wave 18 builds the spine: stage business logic is stubbed; later waves wire
the real sales / delivery / expansion modules into ``run_stage``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from auto_client_acquisition.control_plane_os.repositories import (
    InMemoryControlPlaneRepository,
    WorkflowRun,
)
from auto_client_acquisition.full_ops_os import audit_store
from auto_client_acquisition.full_ops_os.gate import GateDecision, evaluate_gate
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
        actor: str = "revenue-conductor",
    ) -> None:
        self.repo = repo or InMemoryControlPlaneRepository()
        self.tenant_id = tenant_id
        self.actor = actor

    # ── lifecycle ────────────────────────────────────────────────
    def start_run(
        self,
        *,
        customer_id: str,
        correlation_id: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> WorkflowRun:
        """Register a new Full Ops workflow run."""
        run = self.repo.register_workflow_run(
            tenant_id=self.tenant_id,
            workflow_id=WORKFLOW_ID,
            customer_id=customer_id,
            correlation_id=correlation_id,
            metadata=dict(metadata or {}),
        )
        self._audit(
            run=run,
            action=AuditAction.WORKFLOW_STARTED,
            outcome="ok",
            reason="full_ops_run_started",
            details={"customer_id": customer_id},
        )
        log.info("full_ops_run_started", run_id=run.run_id, customer_id=customer_id)
        return run

    # ── stage execution ──────────────────────────────────────────
    def run_stage(self, run_id: str, stage: Stage) -> StageResult:
        """Execute one stage: classify, gate, emit events, audit."""
        run = self.repo.get_run(tenant_id=self.tenant_id, run_id=run_id)
        spec = stage_spec(stage)
        gate = evaluate_gate(spec.action_type)

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
            data={"stage": stage.name, "run_id": run_id, "module": spec.module},
        )

        approval_ticket_id: str | None = None
        if gate.auto_exec_allowed:
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
                metadata={"stage": stage.name, "gate_reason": gate.reason},
            )
            approval_ticket_id = ticket.ticket_id

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
            },
        )

        audit = self._audit(
            run=run,
            action=audit_action,
            outcome=audit_outcome,
            reason=gate.reason,
            event_id=envelope.id,
            gate=gate,
            details={
                "stage": stage.name,
                "action_type": spec.action_type,
                "auto_executed": auto_executed,
                "approval_ticket_id": approval_ticket_id,
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
            event_id=envelope.id,
            control_event_id=control_event.id,
            audit_id=audit.audit_id,
        )

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
