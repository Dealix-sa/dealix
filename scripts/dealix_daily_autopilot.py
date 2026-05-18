#!/usr/bin/env python3
"""Dealix Daily Autopilot — the founder's one-command operating loop.

This is the missing wire: it COMPOSES modules that already exist into a
single daily run that targets, drafts, scores, and queues — so the founder
opens one consolidated pack, batch-approves, and the day's selling is set up.

It builds (no new business logic — Article 11):

    Founder Daily Brief   (scripts.dealix_founder_daily_brief.build_brief)
      + Content drafts    (growth_beast.content_engine.draft_content)
      + Weekly calendar   (gtm_os.content_calendar.build_weekly_calendar)
      + Lead targeting    (scripts.dealix_daily_lead_prep.run_daily_prep, optional)
        → every draft pushed through the Approval Center (draft_only)
        → one consolidated bilingual pack (md + json), gitignored

Doctrine (Article 4 — IMMUTABLE):
- Autopilot = draft / score / schedule / QUEUE only. It NEVER sends, posts,
  publishes, or charges. Every queued item is action_mode="draft_only" and
  approval_required. The founder approves and executes the final send.
- Output path ``data/daily_autopilot/`` is gitignored — no PII committed.
- Article 8: numeric outputs carry is_estimate=True.

The pack file is the founder's review surface. The Approval Center the
orchestrator writes to is process-local; the running API keeps its own live
queue. Review the pack, then approve via the founder dashboard / API.

Rung 2-5 pre-staging:
    RUNG_2_5_FLAGS gates the frozen rungs 2-5 automation. Every flag is
    False during the Commercial Freeze (docs/ops/COMMERCIAL_FREEZE.md). The
    orchestrator does NOTHING for rungs 2-5 while they are False. Flip them
    only after the first paid pilot's Proof Pack is customer-approved (L3+).

Usage:
    python3 scripts/dealix_daily_autopilot.py
    python3 scripts/dealix_daily_autopilot.py --candidates leads.csv --top-n 5
    python3 scripts/dealix_daily_autopilot.py --content-plan plan.json
    python3 scripts/dealix_daily_autopilot.py --format json

Cron example (07:30 KSA = 04:30 UTC daily):
    30 4 * * * cd /home/user/dealix && python3 scripts/dealix_daily_autopilot.py
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, is_dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

DEFAULT_OUT_DIR = REPO_ROOT / "data" / "daily_autopilot"

from auto_client_acquisition.approval_center import (  # noqa: E402
    ApprovalRequest,
    create_approval,
    list_pending,
)
from auto_client_acquisition.growth_beast.content_engine import (  # noqa: E402
    draft_content,
)
from auto_client_acquisition.gtm_os.content_calendar import (  # noqa: E402
    build_weekly_calendar,
)
from scripts.dealix_founder_daily_brief import build_brief  # noqa: E402

# ─── Rung 2-5 pre-staging — INERT during the Commercial Freeze ──────────────
# Every flag stays False until the first paid pilot's Proof Pack is
# customer-approved (L3+). See docs/ops/COMMERCIAL_FREEZE.md and
# docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md. When False, the matching
# branch below is never entered — zero rung 2-5 capability ships or runs.
RUNG_2_5_FLAGS: dict[str, bool] = {
    "rung2_data_pack_autopilot": False,  # 1,500 SAR Data-to-Revenue Pack
    "rung3_managed_ops_cadence": False,  # 2,999-4,999 SAR/mo Managed Ops
    "rung4_command_center": False,  # Command Center
    "rung5_partner_os": False,  # Partner OS
}

# Default weekly content plan — Saudi B2B sectors × recurring gaps. Override
# with --content-plan plan.json (a list of {sector, angle, content_type}).
DEFAULT_CONTENT_PLAN: list[dict[str, str]] = [
    {
        "sector": "logistics",
        "angle": "slow lead follow-up after the first reply",
        "content_type": "linkedin_post",
    },
    {
        "sector": "b2b_saas",
        "angle": "no weekly proof of what was actually delivered",
        "content_type": "sector_insight",
    },
    {
        "sector": "professional_services",
        "angle": "pipeline visibility for the founder",
        "content_type": "diagnostic_cta",
    },
]

# content_type → Approval Center action_type. linkedin_post maps to the
# canonical draft_linkedin_manual; the rest use a free-form draft type.
_ACTION_TYPE_BY_CONTENT: dict[str, str] = {
    "linkedin_post": "draft_linkedin_manual",
}


def rung_2_5_status() -> dict[str, Any]:
    """Report the (inert) rung 2-5 pre-staging state — for the pack + audit."""
    return {
        "flags": dict(RUNG_2_5_FLAGS),
        "all_inert": not any(RUNG_2_5_FLAGS.values()),
        "note": (
            "Rungs 2-5 are frozen. Flip a flag only after the first paid "
            "pilot Proof Pack is customer-approved (L3+)."
        ),
    }


def build_content_drafts(
    content_plan: list[dict[str, str]],
) -> list[dict[str, Any]]:
    """Generate bilingual content drafts from the plan (no LLM, no send)."""
    drafts: list[dict[str, Any]] = []
    for item in content_plan:
        draft = draft_content(
            sector=item["sector"],
            angle=item["angle"],
            content_type=item.get("content_type", "linkedin_post"),  # type: ignore[arg-type]
        )
        drafts.append(draft)
    return drafts


def queue_content_drafts(
    drafts: list[dict[str, Any]],
    *,
    on_date: date,
) -> list[str]:
    """Push each content draft through the Approval Center as draft_only.

    Returns the list of created approval_ids. Every request is
    action_mode="draft_only" — it can never be auto-sent.
    """
    approval_ids: list[str] = []
    for i, draft in enumerate(drafts):
        content_type = draft.get("content_type", "linkedin_post")
        action_type = _ACTION_TYPE_BY_CONTENT.get(content_type, "content_draft")
        req = ApprovalRequest(
            object_type="content_draft",
            object_id=f"autopilot-{on_date.isoformat()}-content-{i}",
            action_type=action_type,
            action_mode="draft_only",
            channel="linkedin_manual_post",
            summary_ar=draft.get("draft_ar", "")[:280],
            summary_en=draft.get("draft_en", "")[:280],
            risk_level="low",
            proof_impact=f"autopilot:content:{content_type}",
        )
        created = create_approval(req)
        approval_ids.append(created.approval_id)
    return approval_ids


def _load_targeting(
    candidates_csv: str | None,
    *,
    top_n: int,
    on_date: date,
) -> dict[str, Any]:
    """Optional lead targeting via the existing daily lead-prep script.

    Targeting needs a founder-supplied candidate list — Dealix never
    scrapes. Without --candidates this returns a skipped marker.
    """
    if not candidates_csv:
        return {
            "status": "skipped",
            "reason": "no --candidates list supplied (Dealix never scrapes)",
            "top_leads": [],
        }
    from scripts.dealix_daily_lead_prep import (
        load_candidates_from_csv,
        run_daily_prep,
    )

    candidates = load_candidates_from_csv(Path(candidates_csv))
    board = run_daily_prep(candidates=candidates, on_date=on_date, top_n=top_n)
    board_dict: dict[str, Any] = asdict(board) if is_dataclass(board) else dict(board)
    return {
        "status": "prepared",
        "candidates_in": len(candidates),
        "top_leads": board_dict.get("top_leads", []),
    }


def build_autopilot_pack(
    *,
    on_date: date | None = None,
    content_plan: list[dict[str, str]] | None = None,
    calendar_slots: int = 5,
    candidates_csv: str | None = None,
    top_n: int = 5,
    brief_kwargs: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Compose the full daily autopilot pack.

    Every draft is queued draft_only; the returned pack is what the founder
    reviews. No external action is taken anywhere in this call.
    """
    on_date = on_date or datetime.now(UTC).date()
    content_plan = content_plan or DEFAULT_CONTENT_PLAN
    brief_kwargs = brief_kwargs or {}

    brief = build_brief(**brief_kwargs)
    drafts = build_content_drafts(content_plan)
    approval_ids = queue_content_drafts(drafts, on_date=on_date)
    calendar = build_weekly_calendar(slots_per_week=calendar_slots)
    targeting = _load_targeting(candidates_csv, top_n=top_n, on_date=on_date)

    pending = list_pending()
    queue = [
        {
            "approval_id": r.approval_id,
            "object_type": r.object_type,
            "action_type": r.action_type,
            "action_mode": r.action_mode,
            "channel": r.channel,
            "summary_ar": r.summary_ar,
            "summary_en": r.summary_en,
            "status": r.status,
        }
        for r in pending
    ]

    return {
        "schema_version": "1.0",
        "date": on_date.isoformat(),
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "is_estimate": True,  # Article 8
        "doctrine": {
            "action_mode": "draft_only",
            "auto_send": False,
            "auto_publish": False,
            "auto_charge": False,
        },
        "founder_brief": brief,
        "content_drafts": drafts,
        "queued_approval_ids": approval_ids,
        "approval_queue": queue,
        "weekly_calendar": calendar,
        "targeting": targeting,
        "rung_2_5_prestage": rung_2_5_status(),
    }


def render_markdown(pack: dict[str, Any]) -> str:
    n = pack["founder_brief"]["next_founder_action"]
    drafts = pack["content_drafts"]
    queue = pack["approval_queue"]
    targeting = pack["targeting"]
    rung = pack["rung_2_5_prestage"]

    lines = [
        f"# Dealix Daily Autopilot · {pack['date']}",
        "",
        "_Draft-only. Nothing here is sent, posted, or charged until you "
        "approve it. Article 4 — IMMUTABLE._",
        "",
        "## 1. Today's single action",
        "",
        f"### {n['ar']}",
        f"_{n['en']}_",
        "",
        f"**Why?** {n['rationale_en']}",
        "",
        f"## 2. Approval queue ({len(queue)} item(s) — all draft_only)",
        "",
    ]
    if queue:
        lines.append("| # | Type | Channel | Mode | Summary (EN) |")
        lines.append("|---|---|---|---|---|")
        for i, item in enumerate(queue, 1):
            summary = (item["summary_en"] or "").replace("\n", " ")[:70]
            lines.append(
                f"| {i} | {item['action_type']} | {item['channel'] or '-'} "
                f"| {item['action_mode']} | {summary} |"
            )
    else:
        lines.append("_No items queued._")
    lines.extend(["", "## 3. Content drafts", ""])
    for i, d in enumerate(drafts, 1):
        lines.extend(
            [
                f"### Draft {i} — {d['content_type']} · {d['sector']}",
                "",
                "**AR:**",
                "",
                d.get("draft_ar", ""),
                "",
                "**EN:**",
                "",
                d.get("draft_en", ""),
                "",
                f"_CTA: {d.get('cta', '')} · approval_required: " f"{d.get('approval_required')}_",
                "",
            ]
        )
    lines.extend(["## 4. Lead targeting", ""])
    if targeting["status"] == "prepared":
        lines.append(
            f"Prepared from **{targeting['candidates_in']}** candidate(s) — "
            f"top {len(targeting['top_leads'])} on the board."
        )
    else:
        lines.append(f"_Skipped: {targeting['reason']}._")
    lines.extend(
        [
            "",
            "## 5. Weekly content calendar",
            "",
            f"{pack['weekly_calendar']['slots_total']} draft slot(s) — "
            "every slot approval_required, no auto-publish.",
            "",
            "## 6. Rung 2-5 pre-stage (frozen)",
            "",
            f"All inert: **{rung['all_inert']}** · {rung['note']}",
            "",
            "---",
            "_Article 8: counts are estimates. Article 4: never auto-send._",
            f"_Generated: {pack['generated_at']}_",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--candidates", default=None, help="CSV of founder-supplied lead candidates (optional)."
    )
    p.add_argument("--top-n", type=int, default=5)
    p.add_argument("--calendar-slots", type=int, default=5)
    p.add_argument(
        "--content-plan", default=None, help="JSON file: list of {sector, angle, content_type}."
    )
    p.add_argument("--on-date", default=None, help="YYYY-MM-DD (default: today).")
    p.add_argument("--format", choices=("md", "json"), default="md")
    p.add_argument(
        "--out", default=None, help="Output path (default: gitignored data/daily_autopilot/)."
    )
    args = p.parse_args()

    on_date = date.fromisoformat(args.on_date) if args.on_date else datetime.now(UTC).date()
    content_plan = None
    if args.content_plan:
        content_plan = json.loads(Path(args.content_plan).read_text("utf-8"))

    pack = build_autopilot_pack(
        on_date=on_date,
        content_plan=content_plan,
        calendar_slots=args.calendar_slots,
        candidates_csv=args.candidates,
        top_n=args.top_n,
    )

    rendered = (
        json.dumps(pack, ensure_ascii=False, indent=2)
        if args.format == "json"
        else render_markdown(pack)
    )

    out_path = (
        Path(args.out) if args.out else DEFAULT_OUT_DIR / f"{on_date.isoformat()}.{args.format}"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    print(
        f"\nWROTE · {out_path} · {len(pack['queued_approval_ids'])} draft(s) "
        f"queued (draft_only)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
