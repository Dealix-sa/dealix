"""CEO/founder production snapshot — Railway repo + live healthz + version."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.gtm_proof_loop import build_gtm_proof_loop_snapshot
from dealix.commercial_ops.railway_production import analyze_railway_production


def build_executive_production_snapshot(
    *,
    api_base: str = "https://api.dealix.me",
) -> dict[str, Any]:
    railway = analyze_railway_production(api_base=api_base)
    healthz = railway.get("live_healthz") or {}
    version = railway.get("live_version") or {}
    gtm = build_gtm_proof_loop_snapshot()

    blockers: list[str] = []
    if not railway.get("repo", {}).get("ok"):
        blockers.append("إصلاح railway.toml / Dockerfile في الريبو")
    if healthz.get("probed") and not healthz.get("ok"):
        blockers.append(f"/healthz فشل: {healthz.get('status') or healthz.get('error')}")
    if version.get("probed") and not version.get("ok"):
        blockers.append(
            railway.get("deploy_note_ar")
            or "GET /version غير متاح — ادفع main وانتظر CI ثم أعد النشر على Railway"
        )
    blockers.extend(gtm.get("blockers_ar") or [])

    verdict = railway.get("verdict", "FAIL")
    if verdict == "PASS" and gtm.get("verdict") != "PASS":
        verdict = "PARTIAL"

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(),
        "verdict": verdict,
        "railway": railway,
        "live": {"healthz": healthz, "version": version},
        "gtm_proof": gtm,
        "blockers_ar": blockers,
        "founder_actions_ar": [
            "Railway UI: امسح Start Command و Pre-deploy echo stub",
            "py -3 scripts/founder_executive_production_verify.py",
            "py -3 scripts/run_dealix_unified_founder_day.py",
        ],
    }
