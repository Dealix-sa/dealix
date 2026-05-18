"""Founder Executive OS — single snapshot for Railway + commercial + launch phase."""

from __future__ import annotations

from typing import Any

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.kpi_snapshot import load_kpi_commercial_status
from dealix.commercial_ops.paths import REPO_ROOT
from dealix.commercial_ops.railway_production import analyze_railway_production

PLAYBOOK = "docs/ops/FOUNDER_EXECUTIVE_RISE_PLAYBOOK_AR.md"
DAILY_LOOP = "scripts/run_founder_daily_operating_loop.sh"
MASTER_PLAN = "docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md"


def build_founder_executive_snapshot(*, api_base: str | None = "https://api.dealix.me") -> dict[str, Any]:
    railway = analyze_railway_production(api_base=api_base)
    kpi = load_kpi_commercial_status()
    first_paid = analyze_first_paid_diagnostic()
    soft_ok = kpi.get("registry_exists") and kpi.get("import_file_exists")
    launch_phase = "PAID_READY"
    if first_paid.get("verdict") != "PASS":
        launch_phase = "PAID_ROADMAP" if soft_ok else "SOFT"
    blockers: list[str] = []
    if railway.get("verdict") != "PASS":
        blockers.extend(railway.get("repo", {}).get("issues", []))
    if not kpi.get("import_file_exists"):
        blockers.append("kpi_founder_commercial_import.yaml missing — run bootstrap")
    if first_paid.get("verdict") == "PENDING":
        blockers.append("أول Diagnostic: سجّل payment_received + proof_pack_delivered")
    ver = railway.get("live_version") or {}
    if ver.get("status") == 404:
        blockers.append("نشر main — /version غير موجود على الإنتاج بعد")
    return {
        "launch_phase": launch_phase,
        "railway_verdict": railway.get("verdict"),
        "kpi": kpi,
        "first_paid": first_paid,
        "railway": railway,
        "blockers": blockers,
        "playbook": PLAYBOOK,
        "daily_loop": DAILY_LOOP,
        "master_plan": MASTER_PLAN,
        "repo_root": str(REPO_ROOT),
    }
