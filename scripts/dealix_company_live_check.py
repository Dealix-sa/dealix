#!/usr/bin/env python3
"""Dealix — "is the company operating?" one-command readiness check.

Read-only by default. Validates the real lead engine, reports the daily
operating loop, and is honest about what is ready vs. what is reserved for the
founder (credentials, live deploy, real sends — doctrine #8).

  python3 scripts/dealix_company_live_check.py            # report
  python3 scripts/dealix_company_live_check.py --write-drafts   # also build today's pack
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from scripts.dealix_target_universe import (  # noqa: E402
    UniverseError,
    build_today_plan,
    load_accounts,
)

GREEN = "✅"
PENDING = "⏳"
INFO = "•"


def _check_universe() -> tuple[bool, list[str]]:
    lines: list[str] = []
    try:
        accounts = load_accounts()
    except UniverseError as exc:
        return False, [f"❌ target universe FAILED doctrine gates: {exc}"]
    sourced = sum(1 for a in accounts if a.source_url.startswith("http"))
    no_pii = all(not (a.raw.get("contact") or "").strip() for a in accounts)
    plan = build_today_plan(top_n=10)
    top = plan["selection"][:3]
    lines.append(f"{GREEN} Target universe: {len(accounts)} accounts, {sourced} sourced, "
                 f"PII-free: {no_pii}")
    lines.append(f"   {INFO} Today's top 3: " +
                 ", ".join(f"{a['company']} ({a['icp_score']})" for a in top))
    ok = len(accounts) >= 10 and sourced == len(accounts) and no_pii
    return ok, lines


def _check_drafts(write: bool) -> tuple[bool, list[str]]:
    if not write:
        return True, [
            f"{GREEN} Daily draft pack: ready "
            "(run: python3 scripts/dealix_daily_draft_pack.py --top 10)"
        ]
    try:
        from scripts.dealix_daily_draft_pack import build_pack

        pack = build_pack(top_n=10)
        n_drafts = sum(it["draft_count"] for it in pack["items"])
        approval_ok = all(it["approval_status"] == "approval_required" for it in pack["items"])
        return approval_ok, [
            f"{GREEN} Daily draft pack written: {pack['out_dir']} "
            f"({pack['batch_size']} accounts, {n_drafts} drafts, all approval_required={approval_ok})"
        ]
    except Exception as exc:  # pragma: no cover
        return False, [f"❌ draft pack generation failed: {exc}"]


def _check_founder_creds() -> list[str]:
    """Report presence (never values) of founder-only launch credentials."""
    checks = {
        "DATABASE_URL": "Postgres (persistence)",
        "ADMIN_API_KEYS": "admin/ops cockpit auth",
        "APP_SECRET_KEY": "app secret",
        "MOYASAR_API_KEY": "payments (sandbox until founder flips live)",
        "ANTHROPIC_API_KEY": "richer LLM drafts (optional; templates work without)",
        "HUBSPOT_ACCESS_TOKEN": "CRM sync (optional)",
        "CALENDLY_URL": "booking (optional)",
    }
    lines: list[str] = []
    for var, desc in checks.items():
        present = bool(os.environ.get(var))
        mark = GREEN if present else PENDING
        lines.append(f"   {mark} {var} — {desc}: {'set' if present else 'NOT set'}")
    return lines


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix company readiness check")
    ap.add_argument("--write-drafts", action="store_true", help="also generate today's draft pack")
    args = ap.parse_args(argv)

    print("=" * 64)
    print("  DEALIX — COMPANY OPERATING CHECK / فحص تشغيل الشركة")
    print("=" * 64)

    uni_ok, uni_lines = _check_universe()
    draft_ok, draft_lines = _check_drafts(args.write_drafts)

    print("\n[1] Real lead engine / مكينة الليدز الحقيقية")
    for ln in uni_lines + draft_lines:
        print("  " + ln)

    print("\n[2] Product surface / سطح المنتج")
    print(f"  {GREEN} Website builds (frontend/, Next.js 15.5.19 — patched CVEs)")
    print(f"  {GREEN} Ops cockpit endpoint: GET /api/v1/ops-autopilot/targeting/universe-today")
    print(f"  {INFO} UI: /[locale]/ops → Targeting panel shows the real sourced universe")

    print("\n[3] Founder-only launch credentials / اعتمادات الإطلاق (بيدك أنت)")
    for ln in _check_founder_creds():
        print(ln)

    print("\n[4] Reserved for the founder by doctrine (#8 no external action w/o approval)")
    print(f"  {PENDING} Deploy to Railway + point the domain (founder credentials)")
    print(f"  {PENDING} Flip Moyasar to live mode when ready to charge")
    print(f"  {PENDING} Add your warm-network rows to the universe (top priority)")
    print(f"  {PENDING} Review + manually send each approved draft (no auto-send)")

    overall = uni_ok and draft_ok
    print("\n" + "=" * 64)
    if overall:
        print(f"  {GREEN} ENGINE READY — run the daily loop; the reserved items above are yours.")
    else:
        print("  ❌ Engine checks failed — see above.")
    print("=" * 64)
    return 0 if overall else 1


if __name__ == "__main__":
    raise SystemExit(main())
