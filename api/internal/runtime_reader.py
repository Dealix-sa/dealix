"""
api.internal.runtime_reader — read CSVs from the private-ops runtime.

Default path: /opt/dealix (override via $PRIVATE_OPS or $DEALIX_PRIVATE_OPS).

Each public function returns a dict with shape:
  { "data": list[dict], "source": "api"|"fallback", "freshness": iso8601 }

If the underlying CSV is missing OR empty (header-only), `source` is
`"fallback"` and `data` is the static stub defined here. This way the
Founder Console pages can always render — they just show is_estimate=true
when source=fallback.
"""
from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _private_ops_root() -> Path:
    raw = os.environ.get("PRIVATE_OPS") or os.environ.get("DEALIX_PRIVATE_OPS") or "/opt/dealix"
    return Path(raw).expanduser()


def _read_csv(rel_path: str) -> tuple[list[dict[str, Any]], str]:
    """Return (rows, freshness_iso). Rows is [] if file missing or header-only."""
    p = _private_ops_root() / rel_path
    if not p.exists() or not p.is_file():
        return [], _now_iso()
    try:
        with p.open(encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
    except (OSError, UnicodeDecodeError, csv.Error):
        return [], _now_iso()
    try:
        mtime = datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).isoformat()
    except OSError:
        mtime = _now_iso()
    return rows, mtime


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _envelope(rel_path: str, fallback: list[dict[str, Any]]) -> dict[str, Any]:
    rows, freshness = _read_csv(rel_path)
    if rows:
        return {"data": rows, "source": "api", "freshness": freshness, "is_estimate": False}
    return {"data": fallback, "source": "fallback", "freshness": freshness, "is_estimate": True}


# ── Founder Console readers ────────────────────────────────────────────

def ceo_daily_brief() -> dict[str, Any]:
    fallback = [
        {
            "section": "top_action",
            "summary_en": "Run the master verifier and review approval-decisions ledger.",
            "summary_ar": "شغّل المتحقّق الرئيسي وراجع سجلّ قرارات الموافقات.",
        },
        {
            "section": "bottleneck",
            "summary_en": "Private ops runtime CSVs are empty — populate /opt/dealix.",
            "summary_ar": "ملفات CSV لتشغيل العمليات الخاصّة فارغة — املأ /opt/dealix.",
        },
    ]
    return _envelope("founder/decision_log.csv", fallback)


def capital_allocation() -> dict[str, Any]:
    fallback = [
        {"category": "tools", "subcategory": "compute", "monthly_sar": "0", "is_estimate": "true"},
        {"category": "founder_time", "subcategory": "founder_hours", "monthly_sar": "0", "is_estimate": "true"},
    ]
    return _envelope("finance/capital_allocation.csv", fallback)


def market_attack() -> dict[str, Any]:
    fallback = [
        {"sector": "_none_yet_", "fit_score": "0", "paid_pilots": "0", "is_estimate": "true"},
    ]
    return _envelope("market_attack/beachhead_sector_scorecard.csv", fallback)


def ai_governance() -> dict[str, Any]:
    """AI governance is sourced from policy_adapter (registries), not CSV.

    Returns the agent + machine count + invariant status as a structured
    response. source is always 'api' because it reads from the canonical
    in-repo registries.
    """
    try:
        import yaml  # type: ignore
        repo_root = Path(__file__).resolve().parents[2]
        agents = yaml.safe_load((repo_root / "registries" / "agent_registry.yaml").read_text(encoding="utf-8"))
        machines = yaml.safe_load((repo_root / "registries" / "machine_registry.yaml").read_text(encoding="utf-8"))
        return {
            "data": [
                {"label": "agents_registered", "value": str(len(agents.get("agents", [])))},
                {"label": "machines_registered", "value": str(len(machines.get("machines", [])))},
                {"label": "eval_required_default", "value": "true"},
                {"label": "kill_switch_default", "value": "true"},
                {"label": "audit_required_default", "value": "true"},
            ],
            "source": "api",
            "freshness": _now_iso(),
            "is_estimate": False,
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "data": [{"label": "error", "value": repr(exc)}],
            "source": "fallback",
            "freshness": _now_iso(),
            "is_estimate": True,
        }


def trust_flags() -> dict[str, Any]:
    fallback = [
        {"flag_id": "init", "category": "_no_data_", "severity": "info",
         "summary_en": "trust_flags.csv is empty in /opt/dealix",
         "summary_ar": "ملف trust_flags.csv فارغ في /opt/dealix"},
    ]
    return _envelope("trust/trust_flags.csv", fallback)


def audit_recent() -> dict[str, Any]:
    fallback = [
        {"decision_id": "init", "action_class": "_no_data_", "approved": "n/a",
         "decided_at": _now_iso(), "decided_by": "system"},
    ]
    return _envelope("trust/approval_decisions.csv", fallback)
