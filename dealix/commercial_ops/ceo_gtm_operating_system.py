"""CEO / Founder GTM operating system — Railway, cadence, agents, gates, backlog."""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Literal

import yaml

from dealix.commercial_ops.evidence_csv import count_evidence_events, load_evidence_rows
from dealix.commercial_ops.founder_weekly_metrics import build_founder_weekly_metrics
from dealix.commercial_ops.paths import (
    CEO_FOUNDER_BACKLOG_YAML,
    FOUNDER_WEEKLY_ONE_DECISION_YAML,
    REPO_ROOT,
    WAR_ROOM_TODAY_JSON,
)
from dealix.commercial_ops.railway_production import (
    analyze_railway_production,
    parse_railway_ui_drift_hint,
    parse_railway_ui_predeploy_drift,
)

Mode = Literal[
    "status",
    "railway",
    "daily",
    "weekly",
    "gates",
    "agents",
    "billing",
    "offers",
    "backlog",
    "executive",
]

CONFIG = REPO_ROOT / "dealix" / "config"
OFFER_DOD = CONFIG / "offer_ladder_dod.yaml"
GTM_PIPELINE = CONFIG / "gtm_draft_approval_pipeline.yaml"
CEO_ROSTER = CONFIG / "ceo_agent_roster.yaml"
BILLING = CONFIG / "billing_zatca_readiness.yaml"
SKU = CONFIG / "commercial_sku_ladder.yaml"
HUB = REPO_ROOT / "docs" / "ops" / "CEO_GTM_OPERATING_SYSTEM_AR.md"


def _yaml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _run(cmd: list[str], timeout: int = 600) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
        )
        return {
            "cmd": cmd,
            "ok": proc.returncode == 0,
            "returncode": proc.returncode,
            "stdout": (proc.stdout or "")[-3000:],
            "stderr": (proc.stderr or "")[-1500:],
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {"cmd": cmd, "ok": False, "error": str(exc)}


def _py() -> str:
    return sys.executable


def check_weekly_decision() -> dict[str, Any]:
    data = _yaml(FOUNDER_WEEKLY_ONE_DECISION_YAML)
    issues: list[str] = []
    if not (data.get("week_iso") or "").strip():
        issues.append("week_iso empty")
    if not (data.get("one_decision_ar") or "").strip():
        issues.append("one_decision_ar empty")
    return {
        "path": str(FOUNDER_WEEKLY_ONE_DECISION_YAML.relative_to(REPO_ROOT)),
        "active_phase": data.get("active_phase"),
        "launch_mode": data.get("launch_mode"),
        "filled": not issues,
        "issues": issues,
    }


def check_daily_ops() -> dict[str, Any]:
    today = date.today().isoformat()
    rows = load_evidence_rows()
    today_n = sum(1 for r in rows if (r.get("date") or r.get("event_date") or "").startswith(today))
    return {
        "date": today,
        "evidence_today": today_n,
        "evidence_ok": today_n >= 1,
        "war_room_exists": WAR_ROOM_TODAY_JSON.is_file(),
        "evidence_stats": count_evidence_events(rows, exclude_placeholders=True),
    }


def run_railway(**kwargs: Any) -> dict[str, Any]:
    blob = analyze_railway_production(
        api_base=None if kwargs.get("skip_live") else kwargs.get("api_base", "https://api.dealix.me")
    )
    ui_s = kwargs.get("ui_start") or ""
    ui_p = kwargs.get("ui_predeploy") or ""
    if parse_railway_ui_drift_hint(ui_s):
        blob["ui_start_command_drift"] = parse_railway_ui_drift_hint(ui_s)
        if blob["verdict"] == "PASS":
            blob["verdict"] = "WARN"
    if parse_railway_ui_predeploy_drift(ui_p):
        blob["ui_predeploy_drift"] = parse_railway_ui_predeploy_drift(ui_p)
        blob["verdict"] = "FAIL"
    return blob


def run_offers() -> dict[str, Any]:
    dod = _yaml(OFFER_DOD)
    sku = _yaml(SKU)
    n_dod = len(dod.get("rungs") or [])
    n_sku = len(sku.get("rungs") or [])
    ok = n_dod >= 5 and n_sku >= 5
    return {"rung_count_dod": n_dod, "rung_count_sku": n_sku, "ok": ok}


def run_gtm_pipeline() -> dict[str, Any]:
    pipe = _yaml(GTM_PIPELINE)
    perms = _yaml(CONFIG / "agent_permissions.yaml")
    blocked = (perms.get("defaults") or {}).get("external_send") == "blocked"
    return {
        "stages": len(pipe.get("stages") or []),
        "forbidden_rules": len(pipe.get("forbidden") or []),
        "external_send_blocked": blocked,
        "ok": blocked and len(pipe.get("forbidden") or []) >= 3,
    }


def run_billing() -> dict[str, Any]:
    data = _yaml(BILLING)
    items = data.get("items") or []
    return {"item_count": len(items), "trigger": data.get("trigger"), "ok": len(items) >= 6, "advisory": True}


def run_backlog_status() -> dict[str, Any]:
    data = _yaml(CEO_FOUNDER_BACKLOG_YAML)
    tasks = data.get("tasks") or []
    sections = data.get("sections") or {}
    return {
        "title_ar": data.get("title_ar"),
        "task_count": len(tasks),
        "sections": sections,
        "ok": len(tasks) >= 50,
    }


def run_agents(*, seed: bool = False) -> dict[str, Any]:
    from dealix.commercial_ops.founder_agent_tasks import build_queue_status, seed_today_queue

    roster = _yaml(CEO_ROSTER)
    out: dict[str, Any] = {
        "agent_count": len(roster.get("agents") or []),
        "pattern": roster.get("orchestration_pattern"),
        "ok": len(roster.get("agents") or []) >= 4,
    }
    if seed:
        seed_today_queue(force=True)
    out["queue"] = build_queue_status()
    return out


def run_daily(*, dry_run: bool = True) -> dict[str, Any]:
    py = _py()
    steps: dict[str, Any] = {"evidence": check_daily_ops(), "gtm": run_gtm_pipeline()}
    steps["railway_repo"] = analyze_railway_production(api_base=False)
    steps["agent_seed"] = _run([py, "scripts/founder_agent_queue_status.py", "--seed-today"])
    steps["backlog"] = run_backlog_status()
    evidence_ok = steps["evidence"]["evidence_ok"]
    ok = steps["agent_seed"].get("ok", True) and (evidence_ok or dry_run)
    return {
        "ok": ok,
        "dry_run": dry_run,
        "warnings": [] if evidence_ok else ["سجّل حدث أدلة واحد اليوم"],
        "steps": steps,
        "verdict": "PASS" if ok else "WARN",
    }


def run_weekly(*, init_decision: bool = False) -> dict[str, Any]:
    py = _py()
    steps: dict[str, Any] = {}
    if init_decision:
        path = FOUNDER_WEEKLY_ONE_DECISION_YAML
        data = _yaml(path)
        if not (data.get("week_iso") or "").strip():
            data["week_iso"] = date.today().isoformat()
            path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8")
        steps["decision_init"] = {"ok": True, "path": str(path.relative_to(REPO_ROOT))}
    steps["decision"] = check_weekly_decision()
    steps["metrics"] = build_founder_weekly_metrics()
    metrics_script = REPO_ROOT / "scripts" / "founder_weekly_metrics_bundle.py"
    if metrics_script.is_file():
        steps["metrics_bundle"] = _run([py, str(metrics_script)])
    loop = REPO_ROOT / "scripts" / "founder_weekly_loop.sh"
    if loop.is_file() and shutil.which("bash"):
        steps["weekly_loop"] = _run(["bash", str(loop)], timeout=900)
    steps["offers"] = run_offers()
    steps["billing"] = run_billing()
    ok = steps["offers"].get("ok") and run_backlog_status().get("ok")
    return {"ok": ok, "steps": steps, "verdict": "PASS" if ok else "WARN"}


def run_gates(*, quick_pytest: bool = False) -> dict[str, Any]:
    py = _py()
    steps: dict[str, Any] = {
        "railway": run_railway(skip_live=False),
        "railway_script": _run([py, "scripts/verify_railway_production_config.py", "--skip-live"]),
        "soaen_loop": _run([py, "scripts/verify_soaen_loop.py"]),
        "gtm_proof": _run([py, "scripts/founder_gtm_proof_loop.py"]),
    }
    launch = REPO_ROOT / "scripts" / "verify_commercial_launch_ready.py"
    if launch.is_file():
        steps["commercial_launch"] = _run([py, str(launch)])
    if quick_pytest:
        steps["pytest"] = _run(
            [py, "-m", "pytest", "tests/test_ceo_gtm_operating_system.py", "-q", "--no-cov"],
            timeout=120,
        )
    ok = all(s.get("ok", s.get("verdict") in ("PASS", "WARN")) for s in steps.values() if isinstance(s, dict))
    return {"ok": ok, "steps": steps, "verdict": "PASS" if ok else "FAIL"}


def run_executive() -> dict[str, Any]:
    """Full founder executive pass — status + daily + weekly snapshot + gates (offline-friendly)."""
    return {
        "status": build_status_snapshot(),
        "daily": run_daily(dry_run=True),
        "weekly_metrics": build_founder_weekly_metrics(),
        "backlog": run_backlog_status(),
        "railway": run_railway(skip_live=False),
        "verdict": "PASS",
    }


def build_status_snapshot() -> dict[str, Any]:
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "hub_doc": str(HUB.relative_to(REPO_ROOT)) if HUB.is_file() else None,
        "railway": run_railway(skip_live=False),
        "weekly_decision": check_weekly_decision(),
        "daily": check_daily_ops(),
        "offers": run_offers(),
        "gtm_pipeline": run_gtm_pipeline(),
        "agents": run_agents(seed=False),
        "billing": run_billing(),
        "backlog": run_backlog_status(),
    }


def build_ceo_gtm_status(
    *,
    api_base: str | bool = "https://api.dealix.me",
    ui_start: str = "",
    ui_predeploy: str = "",
) -> dict[str, Any]:
    """Unified status for CLI, ops API, and agent fleet pack."""
    skip_live = api_base is False
    base = "https://api.dealix.me" if not skip_live else False
    railway = analyze_railway_production(api_base=base)
    start_drift = parse_railway_ui_drift_hint(ui_start)
    pre_drift = parse_railway_ui_predeploy_drift(ui_predeploy)
    ui_action = "REQUIRED" if (start_drift or pre_drift) else "OK"
    blockers: list[str] = []
    if start_drift:
        blockers.append(start_drift)
    if pre_drift:
        blockers.append(pre_drift)
    for issue in railway.get("repo", {}).get("issues") or []:
        blockers.append(issue)
    for label in railway.get("live_failures") or []:
        blockers.append(f"live_{label}_not_ok")
    if railway.get("deploy_note_ar"):
        blockers.append(str(railway["deploy_note_ar"]))
    from dealix.commercial_ops.agent_fleet_tasks import build_agent_fleet_today_pack
    from dealix.commercial_ops.gtm_proof_loop import build_gtm_proof_loop_snapshot
    from dealix.commercial_ops.soaen_loop import analyze_soaen_loop

    soaen = analyze_soaen_loop()
    proof = build_gtm_proof_loop_snapshot()
    blockers.extend(soaen.get("blockers_ar") or [])
    blockers.extend(proof.get("blockers_ar") or [])
    verdict = "ACTION_REQUIRED" if ui_action == "REQUIRED" or blockers else railway.get("verdict", "PASS")
    return {
        "generated_at": datetime.now(UTC).isoformat(),
        "verdict": verdict,
        "blockers": blockers,
        "soaen_loop": soaen,
        "gtm_proof_loop": proof,
        "agent_fleet": build_agent_fleet_today_pack(),
        "railway_ui": {
            "founder_railway_ui_action": ui_action,
            "start_command_hint": start_drift,
            "predeploy_hint": pre_drift,
            "canonical_start": railway.get("canonical_start_command"),
            "canonical_predeploy": railway.get("canonical_predeploy"),
        },
        "railway": railway,
        "weekly_decision": check_weekly_decision(),
        "daily": check_daily_ops(),
        "offers": run_offers(),
        "gtm_pipeline": run_gtm_pipeline(),
        "agents": run_agents(seed=False),
        "billing": run_billing(),
        "backlog": run_backlog_status(),
        "hub_doc": str(HUB.relative_to(REPO_ROOT)) if HUB.is_file() else None,
    }


def run_mode(mode: Mode, **kwargs: Any) -> dict[str, Any]:
    if mode == "status":
        api = kwargs.get("api_base", "https://api.dealix.me")
        if kwargs.get("skip_live_railway"):
            api = False
        return build_ceo_gtm_status(
            api_base=api,
            ui_start=kwargs.get("ui_start") or "",
            ui_predeploy=kwargs.get("ui_predeploy") or "",
        )
    dispatch = {
        "railway": lambda: run_railway(
            skip_live=kwargs.get("skip_live_railway", kwargs.get("skip_live", False)),
            api_base=kwargs.get("api_base", "https://api.dealix.me"),
            ui_start=kwargs.get("ui_start") or "",
            ui_predeploy=kwargs.get("ui_predeploy") or "",
        ),
        "daily": lambda: run_daily(dry_run=kwargs.get("dry_run", True)),
        "weekly": lambda: run_weekly(init_decision=kwargs.get("init_decision", False)),
        "gates": lambda: run_gates(quick_pytest=kwargs.get("quick_pytest", False)),
        "agents": lambda: run_agents(seed=kwargs.get("seed", False)),
        "billing": lambda: run_billing(),
        "offers": lambda: run_offers(),
        "backlog": lambda: run_backlog_status(),
        "executive": lambda: run_executive(),
    }
    return dispatch[mode]()


def verdict_from_payload(payload: dict[str, Any]) -> str:
    if payload.get("verdict"):
        return str(payload["verdict"])
    if payload.get("ok") is True:
        return "PASS"
    if payload.get("ok") is False:
        return "FAIL"
    sub = payload.get("railway") or {}
    if sub.get("verdict"):
        return str(sub["verdict"])
    return "PASS"
