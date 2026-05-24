"""
Hermes Orchestrator — drives the canonical pipeline:

    Signal → Opportunity → Decision → Execution → Trust → Outcome → Asset

Every step records to its store. Trust checks gate every execution. Outcomes
are mandatory; every outcome carries an asset_review flag. The orchestrator
itself never sends external messages — it only plans and records.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from dealix.hermes.core.assets import get_asset_store
from dealix.hermes.core.decisions import get_decision_store
from dealix.hermes.core.executions import get_execution_store
from dealix.hermes.core.opportunities import get_opportunity_store
from dealix.hermes.core.outcomes import get_outcome_store
from dealix.hermes.core.schemas import (
    Asset,
    AssetType,
    Decision,
    Execution,
    Opportunity,
    OpportunityType,
    Outcome,
    OutcomeStatus,
    PermissionLevel,
    RiskLevel,
    Signal,
    SignalType,
    SovereigntyLevel,
)
from dealix.hermes.core.signals import get_signal_store
from dealix.hermes.sovereignty import SovereignVerdict, get_sovereign_layer
from dealix.hermes.trust.audit import get_audit_log
from dealix.hermes.trust.guardrails import (
    GuardrailReport,
    check_guardrails,
)
from dealix.hermes.trust.permissions import (
    PermissionDecision,
    get_permission_matrix,
)


@dataclass
class PipelineResult:
    signal: Signal | None = None
    opportunity: Opportunity | None = None
    decision: Decision | None = None
    execution: Execution | None = None
    outcome: Outcome | None = None
    asset: Asset | None = None
    sovereign_verdict: SovereignVerdict | None = None
    permission_decision: PermissionDecision | None = None
    guardrail_report: GuardrailReport | None = None
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "signal": self.signal.model_dump(mode="json") if self.signal else None,
            "opportunity": self.opportunity.model_dump(mode="json") if self.opportunity else None,
            "decision": self.decision.model_dump(mode="json") if self.decision else None,
            "execution": self.execution.model_dump(mode="json") if self.execution else None,
            "outcome": self.outcome.model_dump(mode="json") if self.outcome else None,
            "asset": self.asset.model_dump(mode="json") if self.asset else None,
            "sovereign_verdict": (
                {
                    "allowed": self.sovereign_verdict.allowed,
                    "requires_approval": self.sovereign_verdict.requires_approval,
                    "sovereignty_level": self.sovereign_verdict.sovereignty_level.value,
                    "reason": self.sovereign_verdict.reason,
                    "approval_id": self.sovereign_verdict.approval_id,
                }
                if self.sovereign_verdict
                else None
            ),
            "permission_decision": (
                {
                    "allowed": self.permission_decision.allowed,
                    "requires_approval": self.permission_decision.requires_approval,
                    "reason": self.permission_decision.reason,
                }
                if self.permission_decision
                else None
            ),
            "guardrail_report": (
                {
                    "passed": self.guardrail_report.passed,
                    "violations": self.guardrail_report.violations,
                    "checks": self.guardrail_report.checks,
                }
                if self.guardrail_report
                else None
            ),
            "notes": self.notes,
        }


class HermesOrchestrator:
    """End-to-end driver for the kernel pipeline."""

    # ── Step 1: Signal Intake ──────────────────────────────────
    def ingest_signal(
        self,
        *,
        source: str,
        signal_type: SignalType | str,
        title: str,
        content: str = "",
        confidence: float = 0.5,
        raw_payload: dict[str, Any] | None = None,
    ) -> Signal:
        return get_signal_store().ingest(
            source=source,
            signal_type=signal_type,
            title=title,
            content=content,
            confidence=confidence,
            raw_payload=raw_payload,
        )

    # ── Step 2: Opportunity Evaluation ─────────────────────────
    def evaluate_opportunity(
        self,
        signal: Signal,
        *,
        opportunity_type: OpportunityType | str | None = None,
        estimated_value_sar: float = 0.0,
        cash_speed: int = 3,
        strategic: int = 3,
        repeatability: int = 3,
        data_moat: int = 3,
        difficulty: int = 3,
        risk: int = 2,
        recommended_action: str = "",
    ) -> Opportunity:
        opp = get_opportunity_store().evaluate(
            signal,
            opportunity_type=opportunity_type,
            estimated_value_sar=estimated_value_sar,
            cash_speed=cash_speed,
            strategic=strategic,
            repeatability=repeatability,
            data_moat=data_moat,
            difficulty=difficulty,
            risk=risk,
            recommended_action=recommended_action,
        )
        get_signal_store().mark_processed(signal.id)
        return opp

    # ── Step 3: Decision ───────────────────────────────────────
    def make_decision(
        self,
        opportunity: Opportunity,
        *,
        decision_type: str = "execute",
        recommendation: str = "Proceed",
        risk_level: RiskLevel | str = RiskLevel.LOW,
        options: list[str] | None = None,
    ) -> Decision:
        return get_decision_store().propose(
            opportunity,
            decision_type=decision_type,
            recommendation=recommendation,
            risk_level=risk_level,
            options=options,
        )

    # ── Step 4: Plan Execution + Trust check ───────────────────
    def plan_execution(
        self,
        decision: Decision,
        *,
        agent_id: str,
        tool_id: str,
        action_type: str,
        permission_level: PermissionLevel | str = PermissionLevel.L1_DRAFT,
        external_action: bool = False,
        expected_result: str = "",
        payload: dict[str, Any] | None = None,
    ) -> PipelineResult:
        result = PipelineResult(decision=decision)

        # Permission check
        perm = get_permission_matrix().check(
            agent_id=agent_id,
            tool_id=tool_id,
            action_sovereignty=decision.sovereignty_level,
            permission_level=permission_level,
            external_action=external_action,
        )
        result.permission_decision = perm
        if not perm.allowed:
            result.notes.append(f"permission_denied:{perm.reason}")
            get_audit_log().record(
                action_type=action_type,
                agent_id=agent_id,
                tool_id=tool_id,
                payload=payload,
                sovereignty_level=decision.sovereignty_level,
                result=f"permission_denied:{perm.reason}",
            )
            return result

        # Sovereign verdict
        verdict = get_sovereign_layer().evaluate(
            action_type=action_type,
            agent_id=agent_id,
            payload=payload,
            sovereignty_override=decision.sovereignty_level,
        )
        result.sovereign_verdict = verdict

        # Plan the execution regardless — its status reflects the verdict.
        exe = get_execution_store().plan(
            decision,
            agent_id=agent_id,
            action_type=action_type,
            permission_level=permission_level,
            external_action=external_action,
            expected_result=expected_result,
            payload=payload,
        )

        # Guardrails always run before any execution becomes runnable.
        report = check_guardrails(exe)
        result.guardrail_report = report
        if not report.passed:
            exe = get_execution_store().set_status(
                exe.id, "blocked", block_reason=";".join(report.violations)
            ) or exe
            result.notes.append("guardrails_blocked")
            get_audit_log().record(
                action_type=action_type,
                agent_id=agent_id,
                tool_id=tool_id,
                payload=payload,
                sovereignty_level=decision.sovereignty_level,
                result="guardrails_blocked",
            )
            result.execution = exe
            return result

        if not verdict.allowed:
            exe = get_execution_store().set_status(
                exe.id,
                "held" if verdict.requires_approval else "blocked",
                block_reason=verdict.reason,
            ) or exe
            result.execution = exe
            result.notes.append(f"sovereign_hold:{verdict.reason}")
            return result

        if perm.requires_approval:
            exe = get_execution_store().set_status(
                exe.id, "held", block_reason="permission_requires_approval"
            ) or exe
            result.execution = exe
            result.notes.append("permission_requires_approval")
            return result

        result.execution = exe
        return result

    # ── Step 5: Run (only when planning produced a ready execution) ───
    def run(
        self,
        execution: Execution,
        *,
        result_text: str = "",
    ) -> Execution | None:
        if execution.status in {"blocked", "held"}:
            return execution
        return get_execution_store().set_status(execution.id, "done")

    # ── Step 6: Outcome ────────────────────────────────────────
    def record_outcome(
        self,
        execution: Execution,
        *,
        status: OutcomeStatus | str,
        actual_result: str = "",
        revenue_sar: float = 0.0,
        learning: str = "",
    ) -> Outcome:
        return get_outcome_store().record(
            execution,
            status=status,
            actual_result=actual_result,
            revenue_sar=revenue_sar,
            learning=learning,
        )

    # ── Step 7: Asset ──────────────────────────────────────────
    def register_asset(
        self,
        outcome: Outcome,
        *,
        asset_type: AssetType | str,
        title: str,
        description: str = "",
        commercializable: bool = False,
    ) -> Asset:
        asset = get_asset_store().register(
            outcome,
            asset_type=asset_type,
            title=title,
            description=description,
            commercializable=commercializable,
        )
        get_outcome_store().attach_asset(outcome.id, asset.id)
        return asset

    # ── One-shot pipeline ──────────────────────────────────────
    def run_pipeline(
        self,
        *,
        source: str,
        signal_type: SignalType | str,
        title: str,
        content: str = "",
        agent_id: str = "revenue_hunter",
        tool_id: str = "draft_message",
        action_type: str = "draft_outreach",
        estimated_value_sar: float = 5_000.0,
    ) -> PipelineResult:
        signal = self.ingest_signal(
            source=source,
            signal_type=signal_type,
            title=title,
            content=content,
        )
        opp = self.evaluate_opportunity(
            signal, estimated_value_sar=estimated_value_sar
        )
        dec = self.make_decision(opp)
        result = self.plan_execution(
            dec,
            agent_id=agent_id,
            tool_id=tool_id,
            action_type=action_type,
        )
        result.signal = signal
        result.opportunity = opp
        return result


_default_orchestrator: HermesOrchestrator | None = None


def get_orchestrator() -> HermesOrchestrator:
    global _default_orchestrator
    if _default_orchestrator is None:
        _default_orchestrator = HermesOrchestrator()
    return _default_orchestrator
