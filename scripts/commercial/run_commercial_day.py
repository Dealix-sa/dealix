#!/usr/bin/env python3
"""
Dealix Commercial Day Runner - يشغل اليوم التجاري الكامل
Runs: Lead Research -> Account Scoring -> Draft Generation -> KPI Update -> CEO Brief
All external sends stay in draft_only mode.
"""

from __future__ import annotations

import json
import logging
import os
import sys
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Safety gate — must be checked before any action.
# ---------------------------------------------------------------------------
EXTERNAL_SEND_ENABLED: bool = os.getenv("EXTERNAL_SEND_ENABLED", "false").lower() in (
    "true",
    "1",
    "yes",
)

_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=_LOG_FORMAT, stream=sys.stdout)
log = logging.getLogger("commercial_day")

OPERATOR = os.getenv("DEALIX_OPERATOR", "founder")
TODAY = datetime.now(UTC).strftime("%Y-%m-%d")
REPORT_DIR = Path("reports/commercial")


def _assert_safe() -> None:
    """Abort if EXTERNAL_SEND_ENABLED is True. Never bypass this check."""
    assert not EXTERNAL_SEND_ENABLED, (
        "EXTERNAL_SEND_ENABLED is True — commercial day runner must not run "
        "with external send active. Set EXTERNAL_SEND_ENABLED=false and retry."
    )


# ---------------------------------------------------------------------------
# Section runners — each returns a dict with 'status' and 'data'.
# ---------------------------------------------------------------------------


def run_lead_research() -> dict[str, Any]:
    """Section 1: Collect or refresh lead targets from data/targets/."""
    lead_dir = Path("data/targets")
    count = len(list(lead_dir.glob("*.json"))) if lead_dir.exists() else 0
    return {
        "status": "ok",
        "data": {
            "target_files_found": count,
            "source_dir": str(lead_dir),
            "note": "No external fetch — dry run only",
        },
    }


def run_account_scoring() -> dict[str, Any]:
    """Section 2: Score all known accounts against Dealix ICP."""
    # Import here to avoid circular issues if called as a module.
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    from score_accounts import run as score_run  # type: ignore[import]

    summary = score_run(dry_run=True)
    return {"status": "ok", "data": summary}


def run_draft_generation() -> dict[str, Any]:
    """Section 3: Check for draft output files in company/runtime/."""
    draft_dir = Path("data/drafts")
    count = len(list(draft_dir.glob("*.md"))) if draft_dir.exists() else 0
    runtime_draft_dir = Path("company/runtime/drafts")
    runtime_count = len(list(runtime_draft_dir.glob("*.md"))) if runtime_draft_dir.exists() else 0
    return {
        "status": "ok",
        "data": {
            "draft_files_in_data": count,
            "draft_files_in_runtime": runtime_count,
            "mode": "draft_only",
            "external_send_enabled": EXTERNAL_SEND_ENABLED,
        },
    }


def run_kpi_update() -> dict[str, Any]:
    """Section 4: Read current KPI snapshot from runtime if available."""
    kpi_path = Path("company/runtime/kpi_snapshot.json")
    if kpi_path.exists():
        try:
            kpi = json.loads(kpi_path.read_text(encoding="utf-8"))
            return {"status": "ok", "data": kpi}
        except (json.JSONDecodeError, OSError):
            pass
    return {
        "status": "ok",
        "data": {
            "note": "No KPI snapshot found at company/runtime/kpi_snapshot.json",
            "mtd_revenue_sar": 0,
            "pipeline_deals": 0,
        },
    }


def run_ceo_brief() -> dict[str, Any]:
    """Section 5: Generate CEO decision brief."""
    scripts_dir = Path(__file__).parent
    sys.path.insert(0, str(scripts_dir))
    from generate_ceo_brief import run as brief_run  # type: ignore[import]

    paths = brief_run(today=TODAY)
    return {"status": "ok", "data": {"paths_written": paths}}


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

SECTIONS: list[tuple[str, Any]] = [
    ("Lead Research", run_lead_research),
    ("Account Scoring", run_account_scoring),
    ("Draft Generation", run_draft_generation),
    ("KPI Update", run_kpi_update),
    ("CEO Brief", run_ceo_brief),
]


def run_commercial_day() -> dict[str, Any]:
    """
    Orchestrate the full commercial day. Returns final status dict.
    All sections run in sequence; failures are caught and logged without
    aborting remaining sections.
    """
    _assert_safe()

    header = (
        f"=== Dealix Commercial Day Runner ===\n"
        f"Date: {TODAY}  Operator: {OPERATOR}\n"
        f"External send: {'ENABLED (BLOCKED)' if EXTERNAL_SEND_ENABLED else 'disabled (safe)'}\n"
    )
    log.info(header)

    results: dict[str, Any] = {}
    failures: list[str] = []

    for name, fn in SECTIONS:
        log.info("--- Running section: %s ---", name)
        try:
            result = fn()
            results[name] = result
            log.info("Section OK: %s — %s", name, result.get("data", {}))
        except Exception:  # noqa: BLE001
            tb = traceback.format_exc()
            log.error("Section FAILED: %s\n%s", name, tb)
            results[name] = {"status": "error", "traceback": tb}
            failures.append(name)

    final_status = "COMMERCIAL_DAY_COMPLETE" if not failures else "COMMERCIAL_DAY_PARTIAL"

    report = _build_report(header, results, failures, final_status)
    _write_report(report)

    log.info("=== %s ===", final_status)
    if failures:
        log.warning("Failed sections: %s", failures)

    return {
        "status": final_status,
        "date": TODAY,
        "sections_run": len(SECTIONS),
        "sections_failed": len(failures),
        "failed_sections": failures,
        "results": results,
    }


def _build_report(
    header: str,
    results: dict[str, Any],
    failures: list[str],
    final_status: str,
) -> str:
    lines = [
        f"# Commercial Day Report — {TODAY}",
        "",
        f"```\n{header}```",
        "",
    ]
    for name, result in results.items():
        status_icon = "OK" if result.get("status") == "ok" else "FAILED"
        lines.append(f"## [{status_icon}] {name}")
        lines.append(f"```json\n{json.dumps(result.get('data', {}), ensure_ascii=False, indent=2)}\n```")
        lines.append("")
    lines.append(f"## Final Status: {final_status}")
    if failures:
        lines.append(f"Failed sections: {', '.join(failures)}")
    return "\n".join(lines)


def _write_report(content: str) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"daily_{TODAY}.md"
    report_path.write_text(content, encoding="utf-8")
    log.info("Report written: %s", report_path)
    return report_path


if __name__ == "__main__":
    output = run_commercial_day()
    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(0 if output["status"] == "COMMERCIAL_DAY_COMPLETE" else 1)
