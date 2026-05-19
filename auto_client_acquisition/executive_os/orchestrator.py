"""The executive tick — top of the autonomous pyramid.

``run_executive_tick`` runs a safety preflight, convenes the 7 role
briefs, synthesizes one executive brief, routes every approval-required
decision into the founder's approval queue, prepares internal LLM jobs,
audits every decision, and persists the brief.

Structural promise — queues, never sends:
  * the orchestrator card holds an empty ``allowed_tools`` tuple;
  * this module only ever calls ``create_approval`` (produces PENDING
    requests) — never ``approve`` and never ``action_mode=approved_execute``;
  * a doctrine preflight aborts the tick before any queueing.

``run_executive_tick`` never raises — any failure is caught and returned
as ``ExecutiveTickResult(ok=False, ...)``.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.agent_os import AutonomyLevel
from auto_client_acquisition.approval_center import ApprovalRequest, create_approval
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    record_event,
)
from auto_client_acquisition.executive_os.aggregator import (
    aggregator_degraded_roles,
    build_all_role_briefs,
)
from auto_client_acquisition.executive_os.brief_store import save_brief
from auto_client_acquisition.executive_os.identity import ensure_registered
from auto_client_acquisition.executive_os.schemas import (
    GUARDRAILS,
    ExecutiveBrief,
    ExecutiveTickResult,
    QueuedApproval,
    RankedDecision,
)
from auto_client_acquisition.role_command_os import RoleBrief
from auto_client_acquisition.safe_send_gateway import enforce_doctrine_non_negotiables
from auto_client_acquisition.secure_agent_runtime_os import (
    all_passed,
    check_all_boundaries,
    kill_switch_active,
)

_AUDIT_CUSTOMER = "__executive__"
_POLICY = "executive_orchestrator_doctrine"
_MAX_SPAWNED_JOBS = 5

_RISK_RANK = {"blocked": 0, "high": 1, "medium": 2, "low": 3}
_ROLE_PRIORITY = {
    "ceo": 0,
    "compliance": 1,
    "finance": 2,
    "sales": 3,
    "growth": 4,
    "partnership": 5,
    "cs": 6,
}
_DRAFT_ONLY_ACTIONS = {
    "draft_email",
    "draft_linkedin_manual",
    "call_script",
    "support_reply_draft",
}


def _derive_action_type(role: str, title_ar: str, title_en: str) -> str:
    """Map a role decision to one of the 11 canonical action types."""
    text = f"{title_ar} {title_en}".lower()
    if role == "sales":
        if "تشخيص" in text or "diagnostic" in text:
            return "prepare_diagnostic"
        if "ترقية" in text or "upsell" in text:
            return "upsell_recommendation"
        if "اتصال" in text or "call" in text:
            return "call_script"
        return "draft_email"
    if role == "partnership":
        return "partner_intro"
    if role == "cs":
        if "إثبات" in text or "proof" in text:
            return "proof_request"
        if "تسليم" in text or "delivery" in text:
            return "delivery_task"
        return "support_reply_draft"
    if role == "finance":
        return "payment_reminder"
    # ceo, growth, compliance
    return "follow_up_task"


def _derive_action_mode(action_type: str, risk_level: str) -> str:
    """Pick the approval mode — never ``approved_execute``."""
    if risk_level == "blocked":
        return "blocked"
    if action_type in _DRAFT_ONLY_ACTIONS:
        return "draft_only"
    return "approval_required"


def _rank_decisions(
    briefs: dict[str, RoleBrief | None],
) -> list[tuple[str, Any]]:
    """Flatten and order role decisions: risk first, then role priority."""
    pairs: list[tuple[str, Any]] = []
    for role, brief in briefs.items():
        if brief is None:
            continue
        for decision in brief.top_decisions:
            pairs.append((role, decision))
    pairs.sort(
        key=lambda p: (
            _RISK_RANK.get(p[1].risk_level, 3),
            _ROLE_PRIORITY.get(p[0], 9),
        )
    )
    return pairs


def _collect_risks(briefs: dict[str, RoleBrief | None]) -> list[str]:
    """Union of every role's risks, de-duplicated, order preserved."""
    seen: set[str] = set()
    out: list[str] = []
    for brief in briefs.values():
        if brief is None:
            continue
        for risk in brief.risks:
            if risk not in seen:
                seen.add(risk)
                out.append(risk)
    return out


def _prepare_internal_jobs(
    decisions: list[RankedDecision],
) -> list[dict[str, Any]]:
    """Prepare capped internal LLM jobs from top sales decisions."""
    jobs: list[dict[str, Any]] = []
    for rd in decisions:
        if rd.role != "sales":
            continue
        if len(jobs) >= _MAX_SPAWNED_JOBS:
            break
        jobs.append(
            {
                "job_type": "proposal_draft",
                "status": "prepared",
                "origin": f"{rd.role}:{rd.rank}",
                "payload": {"context": f"{rd.title_en}\n{rd.rationale_en}".strip()},
            }
        )
    return jobs


def _run(*, dry_run: bool) -> ExecutiveTickResult:
    # ── Safety preflight ─────────────────────────────────────────
    ensure_registered()
    if kill_switch_active():
        return ExecutiveTickResult(ok=False, reason="kill_switch_active", aborted_at="kill_switch")
    checks = check_all_boundaries(
        tool_name="recommend",
        allowed_tools=["recommend"],
        session_scope="executive_orchestrator",
    )
    if not all_passed(checks):
        failed = [name for name, c in checks.items() if not c.allowed]
        return ExecutiveTickResult(
            ok=False,
            reason=f"boundary_failed:{','.join(failed)}",
            aborted_at="boundaries",
        )
    # Raises ValueError on any doctrine breach — caught by run_executive_tick.
    enforce_doctrine_non_negotiables()

    # ── Convene the 7 role briefs ────────────────────────────────
    briefs = build_all_role_briefs()
    degraded = aggregator_degraded_roles(briefs)

    # ── Synthesize the ranked decision queue ─────────────────────
    ranked_pairs = _rank_decisions(briefs)
    ranked: list[RankedDecision] = []
    for idx, (role, d) in enumerate(ranked_pairs, start=1):
        ranked.append(
            RankedDecision(
                role=role,
                rank=idx,
                title_ar=d.title_ar,
                title_en=d.title_en,
                risk_level=d.risk_level,
                approval_required=d.approval_required,
                rationale_ar=d.rationale_ar,
                rationale_en=d.rationale_en,
                proof_event=d.proof_event,
                action_type=_derive_action_type(role, d.title_ar, d.title_en),
            )
        )
    one_number = sum(1 for rd in ranked if rd.approval_required)

    # ── Route approval-required decisions into the founder's queue ─
    queued: list[QueuedApproval] = []
    for rd in ranked:
        if not rd.approval_required:
            continue
        mode = _derive_action_mode(rd.action_type, rd.risk_level)
        if dry_run:
            queued.append(
                QueuedApproval(
                    approval_id="(dry-run)",
                    role=rd.role,
                    action_type=rd.action_type,
                    action_mode=mode,
                    risk_level=rd.risk_level,
                    status="not_created",
                    summary_ar=rd.title_ar,
                    summary_en=rd.title_en,
                )
            )
            continue
        created = create_approval(
            ApprovalRequest(
                object_type="executive_decision",
                object_id=f"{rd.role}:{rd.rank}",
                action_type=rd.action_type,
                action_mode=mode,
                risk_level=rd.risk_level,
                summary_ar=rd.title_ar,
                summary_en=rd.title_en,
                customer_id=_AUDIT_CUSTOMER,
                proof_target=rd.proof_event,
            )
        )
        queued.append(
            QueuedApproval(
                approval_id=created.approval_id,
                role=rd.role,
                action_type=created.action_type,
                action_mode=created.action_mode,
                risk_level=created.risk_level,
                status=str(created.status),
                summary_ar=created.summary_ar,
                summary_en=created.summary_en,
            )
        )
        record_event(
            customer_id=_AUDIT_CUSTOMER,
            kind=AuditEventKind.GOVERNANCE_DECISION,
            actor="executive_orchestrator",
            decision=f"queued:{created.action_type}:{created.action_mode}",
            policy_checked=_POLICY,
            summary=rd.title_en,
        )

    intended_jobs = _prepare_internal_jobs(ranked)
    now = datetime.now(UTC).isoformat()
    headline_ar = (
        f"بريف تنفيذي: {one_number} قرار يحتاج موافقتك، " f"{len(queued)} مُصفّ في الطابور."
    )
    headline_en = (
        f"Executive brief: {one_number} decisions need your approval, " f"{len(queued)} queued."
    )
    brief = ExecutiveBrief(
        generated_at=now,
        one_number_that_matters=one_number,
        headline_ar=headline_ar,
        headline_en=headline_en,
        ranked_decisions=ranked,
        queued_approvals=queued,
        cross_role_risks=_collect_risks(briefs),
        degraded_roles=degraded,
        spawned_jobs=intended_jobs,
        autonomy_level=int(AutonomyLevel.L3_RECOMMEND),
        guardrails=dict(GUARDRAILS),
    )

    if not dry_run:
        record_event(
            customer_id=_AUDIT_CUSTOMER,
            kind=AuditEventKind.GOVERNANCE_DECISION,
            actor="executive_orchestrator",
            decision=f"executive_tick:{one_number}_decisions_queued",
            policy_checked=_POLICY,
            summary=headline_en,
        )
        save_brief(brief)

    return ExecutiveTickResult(
        ok=True,
        reason="dry_run" if dry_run else "ok",
        brief=brief,
        intended_jobs=intended_jobs,
    )


def run_executive_tick(*, dry_run: bool = False) -> ExecutiveTickResult:
    """Run one executive tick. Never raises."""
    try:
        return _run(dry_run=dry_run)
    except Exception as exc:
        return ExecutiveTickResult(
            ok=False,
            reason=f"{type(exc).__name__}: {exc}",
            aborted_at="exception",
        )


async def spawn_internal_jobs(
    intended_jobs: list[dict[str, Any]],
    *,
    redis: Any = None,
) -> list[dict[str, Any]]:
    """Best-effort enqueue of prepared internal jobs.

    If Redis is unreachable each job is recorded as ``deferred`` rather
    than failing the tick. Internal jobs only — never an external send.
    """
    results: list[dict[str, Any]] = []
    pool = redis
    own_pool = False
    if pool is None and intended_jobs:
        try:
            from arq import create_pool
            from arq.connections import RedisSettings

            from core.config.settings import get_settings

            pool = await create_pool(RedisSettings.from_dsn(get_settings().redis_url))
            own_pool = True
        except Exception:
            pool = None

    for job in intended_jobs:
        spec = dict(job)
        if pool is None:
            spec["status"] = "deferred"
            spec["detail"] = "redis_unavailable"
        else:
            try:
                from core.queue import enqueue_agent_job

                job_id = await enqueue_agent_job(
                    pool, job["job_type"], dict(job.get("payload", {}))
                )
                spec["status"] = "enqueued"
                spec["job_id"] = job_id
            except Exception as exc:
                spec["status"] = "deferred"
                spec["detail"] = str(exc)[:120]
        results.append(spec)

    if own_pool and pool is not None:
        try:
            await pool.close()
        except Exception:
            pass
    return results


__all__ = ["run_executive_tick", "spawn_internal_jobs"]
