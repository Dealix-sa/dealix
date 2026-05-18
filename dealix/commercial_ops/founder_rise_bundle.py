"""Assemble founder executive day brief (markdown + JSON)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from dealix.commercial_ops.founder_agent_tasks import build_queue_status
from dealix.commercial_ops.founder_executive import build_founder_executive_snapshot
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT


def build_executive_day_bundle(
    *,
    api_base: str = "https://api.dealix.me",
    skip_live: bool = False,
) -> dict[str, Any]:
    snap = build_founder_executive_snapshot(api_base=api_base, skip_live=skip_live)
    queue = build_queue_status()
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "api_base": api_base,
        "executive_snapshot": snap,
        "agent_queue": queue,
        "verdict": "BLOCKED" if snap.get("blockers") else "CLEAR",
        "top_actions_ar": _top_actions(snap, queue),
    }


def _top_actions(snap: dict[str, Any], queue: dict[str, Any]) -> list[str]:
    actions: list[str] = []
    for b in (snap.get("blockers") or [])[:5]:
        actions.append(f"إزالة حاجز: {b}")
    for tid in (queue.get("pending_p0_ids") or [])[:3]:
        actions.append(f"تنفيذ مهمة P0: {tid}")
    if not actions:
        actions.append("3 لمسات War Room + موافقة مسودات + متابعة Proof Pack")
    return actions


def write_executive_day_artifacts(
    bundle: dict[str, Any],
    *,
    date_str: str | None = None,
) -> dict[str, str]:
    FOUNDER_BRIEFS_DIR.mkdir(parents=True, exist_ok=True)
    day = date_str or datetime.now(UTC).strftime("%Y-%m-%d")
    json_path = FOUNDER_BRIEFS_DIR / f"executive_day_{day}.json"
    md_path = FOUNDER_BRIEFS_DIR / f"executive_day_{day}.md"
    json_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    md_path.write_text(render_executive_day_md(bundle), encoding="utf-8")
    return {"json": str(json_path.relative_to(REPO_ROOT)), "markdown": str(md_path.relative_to(REPO_ROOT))}


def render_executive_day_md(bundle: dict[str, Any]) -> str:
    snap = bundle["executive_snapshot"]
    q = bundle["agent_queue"]
    lines = [
        f"# يوم المؤسس التنفيذي — {bundle.get('generated_at', '')[:10]}",
        "",
        f"**الحكم:** `{bundle.get('verdict')}` · API: `{bundle.get('api_base')}`",
        "",
        "## أولويات اليوم (3)",
    ]
    for i, a in enumerate(bundle.get("top_actions_ar") or [], 1):
        lines.append(f"{i}. {a}")
    lines.extend(
        [
            "",
            "## Railway",
            f"- verdict: `{snap['railway'].get('verdict')}`",
        ]
    )
    if snap["railway"].get("deploy_note_ar"):
        lines.append(f"- **ملاحظة:** {snap['railway']['deploy_note_ar']}")
    for key in ("live_healthz", "live_version", "live_meta"):
        live = snap["railway"].get(key) or {}
        if live.get("probed"):
            lines.append(f"- {key}: HTTP {live.get('status')}")
    lines.extend(
        [
            "",
            "## أول إغلاق مدفوع",
            f"- verdict: `{snap['first_paid'].get('verdict')}`",
            "",
            "## طابور الوكلاء",
            f"- P0 معلّق: {q.get('pending_p0_count', 0)}",
            "",
            "## حواجز",
        ]
    )
    blockers = snap.get("blockers") or []
    if blockers:
        for b in blockers:
            lines.append(f"- {b}")
    else:
        lines.append("- لا حواجز آلية — ركّز على Pipeline وموافقات")
    lines.extend(
        [
            "",
            "---",
            "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة",
        ]
    )
    return "\n".join(lines) + "\n"
