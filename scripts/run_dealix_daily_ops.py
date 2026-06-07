#!/usr/bin/env python3
"""Unified governed daily commercial ops — bridge, health, weekly pack, digest hooks."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

BRIEFS_DIR = REPO_ROOT / "data" / "founder_briefs"


def _api_base() -> str:
    return (
        os.environ.get("DEALIX_API_BASE")
        or os.environ.get("DEALIX_API_URL")
        or os.environ.get("NEXT_PUBLIC_API_URL")
        or ""
    ).rstrip("/")


def _admin_key() -> str:
    return os.environ.get("DEALIX_ADMIN_API_KEY") or os.environ.get("DEALIX_API_KEY") or ""


def _api_key() -> str:
    """General API key for the APIKeyMiddleware (X-API-Key) gate.

    Falls back to the admin key so a single configured secret still works.
    """
    return os.environ.get("DEALIX_API_KEY") or os.environ.get("DEALIX_ADMIN_API_KEY") or ""


def _http_json(
    method: str,
    path: str,
    *,
    body: dict[str, Any] | None = None,
    query: str = "",
) -> dict[str, Any] | None:
    base = _api_base()
    admin_key = _admin_key()
    api_key = _api_key()
    if not base or not admin_key:
        return None
    url = f"{base}{path}"
    if query:
        url = f"{url}?{query}"
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/json",
            # APIKeyMiddleware guards every non-public /api/* path via X-API-Key.
            "X-API-Key": api_key,
            # Admin routers (e.g. /api/v1/ops-autopilot/*) add require_admin_key.
            "X-Admin-API-Key": admin_key,
        },
        method=method,
    )
    try:
        with urlopen(req, timeout=45) as resp:  # noqa: S310
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw.strip() else {}
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"API {method} {path}: SKIP ({exc})", file=sys.stderr)
        return None


def step_replay_postgres(*, limit: int = 50) -> dict[str, Any] | None:
    return _http_json(
        "POST",
        "/api/v1/ops-autopilot/ingest/replay-postgres",
        query=f"limit={limit}&sources=google_ads,meta_lead_ads",
    )


def step_full_ops_health() -> dict[str, Any] | None:
    return _http_json("GET", "/api/v1/ops-autopilot/full-ops-health")


def step_weekly_pack_if_monday() -> dict[str, Any] | None:
    if datetime.now(UTC).weekday() != 0:
        print("weekly-pack: skip (not Monday)")
        return None
    return _http_json(
        "POST",
        "/api/v1/ops-autopilot/marketing/weekly-pack/apply",
        body={"queue_approvals": True},
    )


def step_kpi_status() -> int:
    py = sys.executable
    script = REPO_ROOT / "scripts" / "apply_kpi_founder_commercial.py"
    if not script.is_file():
        print("kpi: script missing", file=sys.stderr)
        return 0
    return subprocess.call([py, str(script), "--status"], cwd=REPO_ROOT)


def step_commercial_digest(*, out_path: Path | None = None) -> int:
    py = sys.executable
    script = REPO_ROOT / "scripts" / "founder_commercial_digest.py"
    if not script.is_file():
        return 0
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    out = out_path or BRIEFS_DIR / f"commercial_{date}.md"
    args = [py, str(script), "--out", str(out)]
    if os.environ.get("DEALIX_SYNC_EVIDENCE") == "1":
        args.append("--sync-evidence")
    return subprocess.call(args, cwd=REPO_ROOT)


def step_war_room_sync() -> int:
    py = sys.executable
    script = REPO_ROOT / "scripts" / "commercial_war_room_sync.py"
    if not script.is_file():
        return 0
    return subprocess.call([py, str(script)], cwd=REPO_ROOT)


def _extract_brief_counts(health: dict[str, Any] | None) -> dict[str, str]:
    """Best-effort map of full-ops-health → founder-brief CLI flags.

    Defensive by design: only emits flags it can confidently resolve, so an
    unrecognized health shape yields ``{}`` and the brief still renders with
    honest zeros (never fabricated numbers — Article 8).
    """
    out: dict[str, str] = {}
    if not isinstance(health, dict):
        return out
    candidates = [health]
    for k in ("signals", "operator_signals", "bottleneck", "summary", "data"):
        v = health.get(k)
        if isinstance(v, dict):
            candidates.append(v)
    mapping = {
        "--blocking-approvals": ("blocking_approvals", "blocking_approvals_count", "pending_approvals"),
        "--pending-payments": ("pending_payments", "pending_payment_confirmations"),
        "--pending-proof-packs": ("pending_proof_packs", "pending_proof_packs_to_send"),
        "--overdue-followups": ("overdue_followups",),
        "--sla-at-risk": ("sla_at_risk", "sla_at_risk_tickets"),
    }
    for flag, keys in mapping.items():
        for src in candidates:
            val = next((src[k] for k in keys if isinstance(src.get(k), int) and src[k] > 0), None)
            if val is not None:
                out[flag] = str(val)
                break
    return out


def step_founder_brief(*, health: dict[str, Any] | None = None) -> int:
    """Wave 15 founder daily brief → data/founder_briefs/today_<date>.md.

    Pure-local composition (Bottleneck Radar + service catalog + today's single
    action). Works offline; reflects real counts when ops-health is available.
    """
    py = sys.executable
    script = REPO_ROOT / "scripts" / "dealix_founder_daily_brief.py"
    if not script.is_file():
        return 0
    date = datetime.now(UTC).strftime("%Y-%m-%d")
    out = BRIEFS_DIR / f"today_{date}.md"
    args = [py, str(script), "--out", str(out)]
    for flag, val in _extract_brief_counts(health).items():
        args += [flag, val]
    return subprocess.call(args, cwd=REPO_ROOT)


def step_daily_lead_prep() -> int:
    """Wave 12.8 scored lead board → data/wave12/daily_lead_prep/<date>.{json,md}.

    Auto-sources from lead_inbox.jsonl when no CSV is supplied. Exit code 1 means
    "no candidates yet" (informational), which is not an ops failure.
    """
    py = sys.executable
    script = REPO_ROOT / "scripts" / "dealix_daily_lead_prep.py"
    if not script.is_file():
        return 0
    rc = subprocess.call([py, str(script)], cwd=REPO_ROOT)
    return 0 if rc in (0, 1) else rc


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-api", action="store_true", help="Skip HTTP steps (offline digest only)")
    p.add_argument("--api-only", action="store_true", help="Only HTTP bridge/health/weekly-pack")
    p.add_argument("--with-business-now", action="store_true")
    p.add_argument("--replay-limit", type=int, default=50)
    args = p.parse_args()

    date = datetime.now(UTC).strftime("%Y-%m-%d")
    BRIEFS_DIR.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        print("DRY-RUN - Dealix Daily Ops")
        print("1. POST ingest/replay-postgres")
        print("2. GET full-ops-health -> data/founder_briefs/ops_health_DATE.json")
        print("3. Monday: POST marketing/weekly-pack/apply")
        print("4. apply_kpi_founder_commercial.py --status")
        print("5. commercial_war_room_sync.py")
        print("6. founder_commercial_digest.py")
        print("7. dealix_founder_daily_brief.py -> data/founder_briefs/today_DATE.md")
        print("8. dealix_daily_lead_prep.py -> data/wave12/daily_lead_prep/DATE.{json,md}")
        print("DEALIX_DAILY_OPS_VERDICT=READY")
        return 0

    degraded = False
    health: dict[str, Any] | None = None

    if not args.skip_api and _api_base() and _admin_key():
        print("== 1/8 Postgres -> Autopilot replay ==")
        replay = step_replay_postgres(limit=args.replay_limit)
        if replay:
            print(json.dumps(replay, ensure_ascii=False, indent=2))
        else:
            degraded = True

        print("\n== 2/8 Full Ops Health ==")
        health = step_full_ops_health()
        if health:
            hp = BRIEFS_DIR / f"ops_health_{date}.json"
            hp.write_text(json.dumps(health, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(f"WROTE {hp}")
        else:
            degraded = True

        print("\n== 3/8 Weekly marketing pack (Monday only) ==")
        wp = step_weekly_pack_if_monday()
        if wp:
            print(json.dumps(wp, ensure_ascii=False, indent=2))
    else:
        print("API steps skipped (set DEALIX_API_BASE + DEALIX_ADMIN_API_KEY)", file=sys.stderr)
        degraded = True

    if args.with_business_now:
        bn = REPO_ROOT / "scripts" / "run_business_now.sh"
        if bn.is_file():
            print("\n== optional: Business NOW ==")
            subprocess.call(["bash", str(bn)], cwd=REPO_ROOT)

    if args.api_only:
        verdict = "DEGRADED" if degraded else "READY"
        print(f"\nDEALIX_DAILY_OPS_VERDICT={verdict}")
        return 0

    print("\n== 4/8 KPI commercial status ==")
    step_kpi_status()

    print("\n== 5/8 War Room sync ==")
    step_war_room_sync()

    print("\n== 6/8 Commercial digest ==")
    step_commercial_digest()

    print("\n== 7/8 Founder daily brief ==")
    step_founder_brief(health=health)

    print("\n== 8/8 Daily lead prep (scored board) ==")
    step_daily_lead_prep()

    verdict = "DEGRADED" if degraded else "READY"
    print(f"\nDEALIX_DAILY_OPS_VERDICT={verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
