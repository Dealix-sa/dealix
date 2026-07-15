"""Founder daily verdict — one GO/WARN/BLOCKED signal aggregating production + KPI + morning ops.

Doctrine: no invented data. Every signal traces to a real repo source.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from dealix.commercial_ops.founder_production_gates import build_founder_production_gates
from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
from dealix.commercial_ops.paths import FOUNDER_BRIEFS_DIR, REPO_ROOT

_KPI_IMPORT = REPO_ROOT / "dealix" / "transformation" / "kpi_founder_commercial_import.yaml"
_KPI_REGISTRY = REPO_ROOT / "dealix" / "transformation" / "kpi_founder_commercial_registry.yaml"

# Tolerances tuned to the founder cadence (morning every weekday).
_BRIEF_STALE_HOURS = 36
_KPI_STALE_DAYS = 9  # one weekly retro + a 2-day grace window


def _now_utc(at: datetime | None = None) -> datetime:
    if at is None:
        return datetime.now(UTC)
    return at.astimezone(UTC) if at.tzinfo else at.replace(tzinfo=UTC)


def _today_iso(at: datetime | None = None) -> str:
    return _now_utc(at).strftime("%Y-%m-%d")


def _file_age_hours(path: Path, at: datetime) -> float | None:
    if not path.is_file():
        return None
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
    return (at - mtime).total_seconds() / 3600.0


def _rel(path: Path) -> str:
    """Path relative to REPO_ROOT when possible; absolute otherwise (tests use tmp dirs)."""
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _latest_brief(at: datetime, *, briefs_dir: Path) -> dict[str, Any]:
    """Locate the most recent brief_YYYY-MM-DD.md and report age."""
    today = at.strftime("%Y-%m-%d")
    today_brief = briefs_dir / f"brief_{today}.md"
    if not briefs_dir.is_dir():
        return {
            "exists": False,
            "today_present": False,
            "today_path": _rel(today_brief),
            "latest_path": None,
            "latest_age_hours": None,
        }

    if today_brief.is_file():
        age = _file_age_hours(today_brief, at)
        return {
            "exists": True,
            "today_present": True,
            "today_path": _rel(today_brief),
            "latest_path": _rel(today_brief),
            "latest_age_hours": age,
        }

    briefs = sorted(briefs_dir.glob("brief_*.md"))
    if not briefs:
        return {
            "exists": False,
            "today_present": False,
            "today_path": _rel(today_brief),
            "latest_path": None,
            "latest_age_hours": None,
        }
    latest = briefs[-1]
    return {
        "exists": True,
        "today_present": False,
        "today_path": _rel(today_brief),
        "latest_path": _rel(latest),
        "latest_age_hours": _file_age_hours(latest, at),
    }


def _kpi_freshness(at: datetime) -> dict[str, Any]:
    status = load_kpi_commercial_status()
    age_hours = _file_age_hours(_KPI_IMPORT, at) if _KPI_IMPORT.is_file() else None
    stale = age_hours is None or age_hours > _KPI_STALE_DAYS * 24
    return {
        "registry_exists": status.get("registry_exists", False),
        "import_file_exists": status.get("import_file_exists", False),
        "pending_count": status.get("pending_count", 0),
        "ready_count": status.get("ready_count", 0),
        "import_age_hours": age_hours,
        "stale": bool(stale),
        "hint_ar": status.get("hint_ar", ""),
    }


def _classify_morning(brief: dict[str, Any]) -> tuple[str, str | None]:
    """Return (status, action_ar). Status is one of: present, stale, missing."""
    if brief.get("today_present"):
        return "present", None
    age = brief.get("latest_age_hours")
    if age is None:
        return "missing", (
            "شغّل موجز الصباح: bash scripts/run_founder_commercial_day.sh "
            "(لا يوجد أي brief في data/founder_briefs/)"
        )
    if age > _BRIEF_STALE_HOURS:
        return "stale", (
            f"موجز اليوم مفقود و آخر brief عمره {int(age)} ساعة — "
            "شغّل bash scripts/run_founder_commercial_day.sh"
        )
    return "stale", (
        "موجز اليوم لم يُولَّد بعد — شغّل bash scripts/run_founder_commercial_day.sh"
    )


def _classify_kpi(kpi: dict[str, Any]) -> tuple[str, str | None]:
    """Return (status, action_ar). Status: ok, pending, missing, stale."""
    if not kpi["registry_exists"]:
        return "missing", "kpi_founder_commercial_registry.yaml غير موجود"
    if not kpi["import_file_exists"]:
        return "missing", (
            "انسخ kpi_founder_commercial_import.example.yaml → "
            "kpi_founder_commercial_import.yaml وعبّئ من CRM"
        )
    if kpi["pending_count"] > 0:
        return "pending", (
            f"{kpi['pending_count']} KPI معلّقة — "
            "أكمل source_ref ثم شغّل python3 scripts/apply_kpi_founder_commercial.py"
        )
    if kpi["stale"]:
        return "stale", (
            "kpi_founder_commercial_import.yaml قديم — "
            "أعد المزامنة من CRM (آخر تحديث أسبوعي)"
        )
    return "ok", None


def build_founder_daily_verdict(
    *,
    at: datetime | None = None,
    api_base: str | None = None,
    skip_live: bool = True,
    briefs_dir: Path | None = None,
) -> dict[str, Any]:
    """Single morning signal — combines production gates + KPI + today's brief."""
    now = _now_utc(at)
    briefs = briefs_dir or FOUNDER_BRIEFS_DIR

    production = build_founder_production_gates(
        api_base=api_base,
        skip_live=skip_live,
    )
    kpi = _kpi_freshness(now)
    brief = _latest_brief(now, briefs_dir=briefs)

    morning_status, morning_action = _classify_morning(brief)
    kpi_status, kpi_action = _classify_kpi(kpi)

    actions: list[str] = list(production.get("founder_actions_ar") or [])
    if morning_action:
        actions.append(morning_action)
    if kpi_action:
        actions.append(kpi_action)

    verdict = "GO"
    prod_verdict = production.get("verdict", "FAIL")
    if prod_verdict == "FAIL":
        verdict = "BLOCKED"
    elif morning_status == "missing":
        verdict = "BLOCKED"
    elif kpi_status == "missing":
        verdict = "BLOCKED"
    elif prod_verdict == "WARN" or morning_status == "stale" or kpi_status in ("pending", "stale"):
        verdict = "WARN"

    return {
        "iso_date": now.strftime("%Y-%m-%d"),
        "generated_at": now.isoformat(),
        "verdict": verdict,
        "production_gates": {
            "verdict": prod_verdict,
            "api_base": production.get("api_base"),
            "weekly_verdict": production["weekly_metrics"]["verdict"],
        },
        "kpi_freshness": {**kpi, "status": kpi_status},
        "morning_ops": {**brief, "status": morning_status},
        "founder_actions_ar": actions,
        "commands": {
            "morning": "bash scripts/run_founder_commercial_day.sh",
            "production_gates": "python scripts/run_founder_production_gates.py",
            "kpi_apply": "python3 scripts/apply_kpi_founder_commercial.py",
            "weekly_metrics": "python scripts/founder_weekly_metrics_bundle.py --write",
        },
        "sources": {
            "kpi_registry": _rel(_KPI_REGISTRY),
            "kpi_import": _rel(_KPI_IMPORT),
            "briefs_dir": _rel(briefs),
        },
    }
