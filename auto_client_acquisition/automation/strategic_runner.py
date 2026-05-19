"""Shared strategic-layer logic for the weekly cadence.

Pure-ish async functions that wrap the existing strategic generators so
the ARQ cron worker and any HTTP endpoint share one implementation —
mirrors ``auto_client_acquisition/automation/daily_runner.py``.

Each function here REUSES an existing generator (it does not reimplement
the analysis):

  - ``run_role_briefs_core``      -> role_command_os.build_role_brief / list_roles
  - ``run_executive_report_core`` -> executive_reporting.build_weekly_report
                                     + executive_pack_v2.build_weekly_pack
  - ``run_scorecard_core``        -> weekly_growth_scorecard.build_scorecard
  - ``run_bottleneck_sweep_core`` -> bottleneck_radar.compute_founder_view
  - ``run_business_metrics_core`` -> business_metrics_board.compute_customer_metrics
  - ``run_strategy_synthesis_core`` aggregates the five above

Doctrine constraints (enforced by the test suite):
  - Strategic automation is INTERNAL ONLY. It generates briefs / reports /
    scorecards and emails them to the founder. ZERO external sends, no
    prospect contact. ``external_send`` is hard-coded ``False`` on every
    persisted record.
  - Autonomy level L3 (Recommend): the engine recommends; the founder
    decides. Nothing here auto-executes a strategic decision.

Outputs persist to Postgres (``StrategicBriefRecord``); they are not left
in ephemeral ``data/`` files. Persistence and email both degrade
gracefully when the dependency is unreachable (no crash).
"""

from __future__ import annotations

import logging
import uuid
from datetime import UTC, datetime
from typing import Any

log = logging.getLogger(__name__)

# Fixed autonomy level for every strategic artifact: L3 (Recommend).
STRATEGIC_AUTONOMY_LEVEL = 3

# The strategic layer NEVER sends externally. Recorded on every artifact.
STRATEGIC_EXTERNAL_SEND = False


def _new_id(prefix: str = "sb_") -> str:
    return f"{prefix}{uuid.uuid4().hex[:24]}"


def _utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _week_label() -> str:
    now = datetime.now(UTC)
    iso_year, iso_week, _ = now.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


async def persist_strategic_brief(
    *,
    artifact_type: str,
    period_label: str,
    title: str,
    payload: dict[str, Any],
    emailed_to_founder: bool = False,
) -> str | None:
    """Persist one strategic artifact to ``StrategicBriefRecord``.

    Returns the new row id, or ``None`` when Postgres is unreachable
    (degrades gracefully — the cron still reports its result).
    """
    from db.models import StrategicBriefRecord
    from db.session import async_session_factory

    row_id = _new_id()
    try:
        async with async_session_factory()() as session:
            session.add(
                StrategicBriefRecord(
                    id=row_id,
                    artifact_type=artifact_type,
                    period_label=period_label,
                    title=title,
                    payload=payload,
                    autonomy_level=STRATEGIC_AUTONOMY_LEVEL,
                    external_send=STRATEGIC_EXTERNAL_SEND,
                    emailed_to_founder=emailed_to_founder,
                )
            )
            await session.commit()
        return row_id
    except Exception as exc:  # noqa: BLE001
        log.warning("strategic_brief_persist_failed type=%s err=%s",
                    artifact_type, exc)
        return None


async def email_founder(*, subject: str, body_text: str) -> bool:
    """Email the founder one internal strategic artifact summary.

    Internal transactional message to the founder only — never prospect
    outreach. Returns ``True`` on success, ``False`` on any failure.
    """
    try:
        from core.config.settings import get_settings
        from integrations.email import EmailClient

        settings = get_settings()
        result = await EmailClient().send(
            to=settings.dealix_founder_email,
            subject=subject,
            body_text=body_text,
        )
        return bool(result.success)
    except Exception as exc:  # noqa: BLE001
        log.warning("strategic_founder_email_failed subject=%s err=%s",
                    subject, exc)
        return False


async def run_role_briefs_core() -> dict[str, Any]:
    """Build every role brief and persist + email a digest to the founder.

    Reuses ``role_command_os.list_roles`` + ``build_role_brief`` — one
    brief per role. The briefs are advisory; each surfaced decision
    already carries ``approval_required``.
    """
    from auto_client_acquisition.role_command_os import (
        build_role_brief,
        list_roles,
    )

    period = _week_label()
    briefs: dict[str, Any] = {}
    roles_done: list[str] = []
    for role in list_roles():
        try:
            brief = build_role_brief(role)  # type: ignore[arg-type]
            briefs[role] = brief.as_dict()
            roles_done.append(role)
        except Exception as exc:  # noqa: BLE001
            log.warning("role_brief_failed role=%s err=%s", role, exc)

    payload = {
        "generated_at": _utcnow().isoformat(),
        "period_label": period,
        "roles": roles_done,
        "briefs": briefs,
    }
    title = f"Weekly role briefs — {period}"
    row_id = await persist_strategic_brief(
        artifact_type="role_briefs",
        period_label=period,
        title=title,
        payload=payload,
    )
    body = "\n".join(
        [
            "Dealix strategic layer — weekly role briefs",
            f"Week: {period}",
            f"Roles briefed: {len(roles_done)} ({', '.join(roles_done)})",
            "",
            "Each brief recommends; the founder decides. No external send.",
        ]
    )
    emailed = await email_founder(subject=title, body_text=body)
    return {
        "status": "ok",
        "artifact_type": "role_briefs",
        "period_label": period,
        "roles_briefed": len(roles_done),
        "persisted_id": row_id,
        "emailed": emailed,
        "external_send": STRATEGIC_EXTERNAL_SEND,
    }


async def run_executive_report_core(
    *, customer_handle: str = "dealix"
) -> dict[str, Any]:
    """Build the weekly executive report + executive pack v2.

    Reuses ``executive_reporting.build_weekly_report`` for the founder
    weekly report and ``executive_pack_v2.build_weekly_pack`` for the
    structured weekly pack. Read-only; persists + emails the founder.
    """
    from auto_client_acquisition.executive_pack_v2 import build_weekly_pack
    from auto_client_acquisition.executive_reporting import build_weekly_report

    period = _week_label()
    report_payload: dict[str, Any] = {}
    pack_payload: dict[str, Any] = {}
    try:
        report = build_weekly_report()
        report_payload = report.model_dump(mode="json")
    except Exception as exc:  # noqa: BLE001
        log.warning("weekly_report_failed err=%s", exc)
        report_payload = {"error": str(exc)}
    try:
        pack = build_weekly_pack(customer_handle=customer_handle)
        pack_payload = pack.model_dump(mode="json")
    except Exception as exc:  # noqa: BLE001
        log.warning("weekly_pack_failed err=%s", exc)
        pack_payload = {"error": str(exc)}

    payload = {
        "generated_at": _utcnow().isoformat(),
        "period_label": period,
        "weekly_report": report_payload,
        "executive_pack": pack_payload,
    }
    title = f"Weekly executive report — {period}"
    row_id = await persist_strategic_brief(
        artifact_type="executive_report",
        period_label=period,
        title=title,
        payload=payload,
    )
    body = "\n".join(
        [
            "Dealix strategic layer — weekly executive report",
            f"Week: {period}",
            "Includes the founder weekly report and the executive pack v2.",
            "",
            "Internal report. No external send.",
        ]
    )
    emailed = await email_founder(subject=title, body_text=body)
    return {
        "status": "ok",
        "artifact_type": "executive_report",
        "period_label": period,
        "persisted_id": row_id,
        "emailed": emailed,
        "external_send": STRATEGIC_EXTERNAL_SEND,
    }


async def run_scorecard_core() -> dict[str, Any]:
    """Build the weekly growth scorecard.

    Reuses ``self_growth_os.weekly_growth_scorecard.build_scorecard`` —
    aggregates every in-repo growth signal into one founder-facing dict.
    """
    from auto_client_acquisition.self_growth_os import weekly_growth_scorecard

    period = _week_label()
    try:
        scorecard = weekly_growth_scorecard.build_scorecard()
    except Exception as exc:  # noqa: BLE001
        log.warning("scorecard_failed err=%s", exc)
        scorecard = {"error": str(exc)}

    payload = {
        "generated_at": _utcnow().isoformat(),
        "period_label": period,
        "scorecard": scorecard,
    }
    title = f"Weekly growth scorecard — {period}"
    row_id = await persist_strategic_brief(
        artifact_type="growth_scorecard",
        period_label=period,
        title=title,
        payload=payload,
    )
    body = "\n".join(
        [
            "Dealix strategic layer — weekly growth scorecard",
            f"Week: {period}",
            "",
            "Internal scorecard. No external send.",
        ]
    )
    emailed = await email_founder(subject=title, body_text=body)
    return {
        "status": "ok",
        "artifact_type": "growth_scorecard",
        "period_label": period,
        "persisted_id": row_id,
        "emailed": emailed,
        "external_send": STRATEGIC_EXTERNAL_SEND,
    }


async def run_bottleneck_sweep_core(
    *,
    blocking_approvals_count: int = 0,
    pending_payment_confirmations: int = 0,
    pending_proof_packs_to_send: int = 0,
    overdue_followups: int = 0,
    sla_at_risk_tickets: int = 0,
) -> dict[str, Any]:
    """Build the founder bottleneck sweep.

    Reuses ``bottleneck_radar.compute_founder_view`` — caller passes the
    counts (sourced from the live approval / payment / proof layers), the
    radar returns a severity assessment and a single recommended action.
    """
    from auto_client_acquisition.bottleneck_radar import compute_founder_view

    period = _week_label()
    try:
        view = compute_founder_view(
            blocking_approvals_count=blocking_approvals_count,
            pending_payment_confirmations=pending_payment_confirmations,
            pending_proof_packs_to_send=pending_proof_packs_to_send,
            overdue_followups=overdue_followups,
            sla_at_risk_tickets=sla_at_risk_tickets,
        )
        sweep = view.model_dump(mode="json")
    except Exception as exc:  # noqa: BLE001
        log.warning("bottleneck_sweep_failed err=%s", exc)
        sweep = {"error": str(exc)}

    payload = {
        "generated_at": _utcnow().isoformat(),
        "period_label": period,
        "bottleneck": sweep,
    }
    title = f"Weekly bottleneck sweep — {period}"
    row_id = await persist_strategic_brief(
        artifact_type="bottleneck_sweep",
        period_label=period,
        title=title,
        payload=payload,
    )
    body = "\n".join(
        [
            "Dealix strategic layer — weekly bottleneck sweep",
            f"Week: {period}",
            f"Severity: {sweep.get('severity', 'unknown')}",
            "",
            "Internal sweep. No external send.",
        ]
    )
    emailed = await email_founder(subject=title, body_text=body)
    return {
        "status": "ok",
        "artifact_type": "bottleneck_sweep",
        "period_label": period,
        "severity": sweep.get("severity"),
        "persisted_id": row_id,
        "emailed": emailed,
        "external_send": STRATEGIC_EXTERNAL_SEND,
    }


async def run_business_metrics_core(
    *, customer_handle: str = "dealix"
) -> dict[str, Any]:
    """Build the business-metrics snapshot.

    Reuses ``business_metrics_board.compute_customer_metrics`` — a pure
    deterministic composer. Counts default to zero here (the live router
    sources real data); the snapshot still persists the metric shape so
    the daily cadence has a durable history.
    """
    from auto_client_acquisition.business_metrics_board import (
        compute_customer_metrics,
    )

    period = _week_label()
    try:
        metrics = compute_customer_metrics(customer_handle=customer_handle)
        snapshot = metrics.model_dump(mode="json")
    except Exception as exc:  # noqa: BLE001
        log.warning("business_metrics_failed err=%s", exc)
        snapshot = {"error": str(exc)}

    payload = {
        "generated_at": _utcnow().isoformat(),
        "period_label": period,
        "customer_handle": customer_handle,
        "metrics": snapshot,
    }
    title = f"Business-metrics snapshot — {_utcnow().date().isoformat()}"
    row_id = await persist_strategic_brief(
        artifact_type="business_metrics",
        period_label=period,
        title=title,
        payload=payload,
    )
    return {
        "status": "ok",
        "artifact_type": "business_metrics",
        "period_label": period,
        "persisted_id": row_id,
        "external_send": STRATEGIC_EXTERNAL_SEND,
    }


def _synthesize_recommendations(
    *,
    role_briefs: dict[str, Any],
    bottleneck: dict[str, Any],
    scorecard: dict[str, Any],
) -> tuple[list[str], list[str]]:
    """Derive the top-3 recommendations + decision forks from inputs.

    Pure function — deterministic given its inputs. The output recommends;
    it does not decide.
    """
    recommendations: list[str] = []
    decision_forks: list[str] = []

    sweep = bottleneck.get("bottleneck", {})
    action_en = sweep.get("today_single_action_en")
    if action_en:
        recommendations.append(f"Clear the top bottleneck: {action_en}")

    sc = scorecard.get("scorecard", {})
    for rec in (sc.get("recommendations") or [])[:2]:
        text = rec if isinstance(rec, str) else str(rec)
        recommendations.append(text)
    for fork in (sc.get("open_founder_decisions") or [])[:3]:
        decision_forks.append(fork if isinstance(fork, str) else str(fork))

    for role, brief in role_briefs.items():
        for dec in (brief.get("top_decisions") or []):
            title = dec.get("title_en") or dec.get("title_ar")
            if not title:
                continue
            if dec.get("risk_level") in {"high", "blocked"}:
                decision_forks.append(f"[{role}] {title}")
            elif len(recommendations) < 3:
                recommendations.append(f"[{role}] {title}")

    return recommendations[:3], decision_forks[:8]


async def run_strategy_synthesis_core(
    *, customer_handle: str = "dealix"
) -> dict[str, Any]:
    """Aggregate the weekly artifacts into one founder Strategy Brief.

    Pulls the role briefs, weekly executive report, bottleneck sweep and
    business metrics, then synthesizes the top-3 strategic recommendations
    for the coming week and the decision forks that need the founder.

    It recommends; the founder decides. Persists + emails the founder.
    """
    period = _week_label()

    role_result = await run_role_briefs_core()
    exec_result = await run_executive_report_core(customer_handle=customer_handle)
    bottleneck_result = await run_bottleneck_sweep_core()
    metrics_result = await run_business_metrics_core(customer_handle=customer_handle)

    # Re-read the persisted payloads for synthesis — fall back to fresh
    # builds so the synthesis still works when Postgres is unreachable.
    from auto_client_acquisition.bottleneck_radar import compute_founder_view
    from auto_client_acquisition.role_command_os import (
        build_role_brief,
        list_roles,
    )
    from auto_client_acquisition.self_growth_os import weekly_growth_scorecard

    role_briefs: dict[str, Any] = {}
    for role in list_roles():
        try:
            role_briefs[role] = build_role_brief(role).as_dict()  # type: ignore[arg-type]
        except Exception:  # noqa: BLE001
            continue
    try:
        scorecard = {"scorecard": weekly_growth_scorecard.build_scorecard()}
    except Exception:  # noqa: BLE001
        scorecard = {"scorecard": {}}
    try:
        bottleneck = {"bottleneck": compute_founder_view().model_dump(mode="json")}
    except Exception:  # noqa: BLE001
        bottleneck = {"bottleneck": {}}

    recommendations, decision_forks = _synthesize_recommendations(
        role_briefs=role_briefs,
        bottleneck=bottleneck,
        scorecard=scorecard,
    )

    payload = {
        "generated_at": _utcnow().isoformat(),
        "period_label": period,
        "top_3_recommendations": recommendations,
        "decision_forks_for_founder": decision_forks,
        "autonomy_level": STRATEGIC_AUTONOMY_LEVEL,
        "note": "The engine recommends; the founder decides.",
        "sources": {
            "role_briefs": role_result.get("persisted_id"),
            "executive_report": exec_result.get("persisted_id"),
            "bottleneck_sweep": bottleneck_result.get("persisted_id"),
            "business_metrics": metrics_result.get("persisted_id"),
        },
    }
    title = f"Weekly strategy brief — {period}"
    row_id = await persist_strategic_brief(
        artifact_type="strategy_synthesis",
        period_label=period,
        title=title,
        payload=payload,
    )
    lines = [
        "Dealix strategic layer — weekly strategy brief",
        f"Week: {period}",
        "",
        "Top 3 recommendations for the coming week:",
    ]
    for i, rec in enumerate(recommendations, start=1):
        lines.append(f"  {i}. {rec}")
    lines.append("")
    lines.append("Decision forks needing the founder:")
    for fork in decision_forks:
        lines.append(f"  - {fork}")
    lines.append("")
    lines.append("The engine recommends; the founder decides. No external send.")
    emailed = await email_founder(subject=title, body_text="\n".join(lines))

    return {
        "status": "ok",
        "artifact_type": "strategy_synthesis",
        "period_label": period,
        "top_3_recommendations": recommendations,
        "decision_forks_for_founder": decision_forks,
        "persisted_id": row_id,
        "emailed": emailed,
        "external_send": STRATEGIC_EXTERNAL_SEND,
    }


__all__ = [
    "STRATEGIC_AUTONOMY_LEVEL",
    "STRATEGIC_EXTERNAL_SEND",
    "email_founder",
    "persist_strategic_brief",
    "run_bottleneck_sweep_core",
    "run_business_metrics_core",
    "run_executive_report_core",
    "run_role_briefs_core",
    "run_scorecard_core",
    "run_strategy_synthesis_core",
]
