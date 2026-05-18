#!/usr/bin/env python3
"""Scaffold weekly decision board (3 questions) — no invented KPIs."""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.paths import FOUNDER_WEEKLY_ONE_DECISION_YAML, REPO_ROOT  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ICP_YAML = REPO_ROOT / "dealix/config/icp_agency_wedge.yaml"
CACHE_YAML = REPO_ROOT / "dealix/transformation/business_now_cache.yaml"


def _scaffold() -> dict:
    icp = "وكالات B2B — Motion A"
    if ICP_YAML.is_file():
        data = yaml.safe_load(ICP_YAML.read_text(encoding="utf-8")) or {}
        icp = data.get("wedge_ar") or data.get("summary_ar") or icp
    focus = ""
    if CACHE_YAML.is_file():
        cache = yaml.safe_load(CACHE_YAML.read_text(encoding="utf-8")) or {}
        focus = str(cache.get("commercial_focus") or cache.get("focus_ar") or "")[:200]
    week = datetime.now(UTC).strftime("%Y-%m-%d")
    return {
        "week_iso": week,
        "launch_mode": "soft",
        "active_phase": 1,
        "one_decision_ar": "[املأ: قرار واحد للأسبوع]",
        "why_this_phase_ar": focus or "[من business_now_cache]",
        "icp_focus_ar": icp,
        "weakest_soaen_link_ar": "Evidence — سجّل أحداثاً حقيقية في evidence CSV",
        "evidence_before_scale_ar": "أول payment_received + proof_pack_delivered",
        "no_build_acknowledged": True,
        "success_by_friday_ar": "[نتيجة قابلة للتحقق يوم الجمعة]",
        "evidence_events_to_log": ["message_sent_manual"],
        "blocked_by": "",
        "next_week_phase_hint": None,
    }


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--write", action="store_true")
    args = p.parse_args()

    scaffold = _scaffold()
    if args.write:
        existing: dict = {}
        if FOUNDER_WEEKLY_ONE_DECISION_YAML.is_file():
            existing = yaml.safe_load(
                FOUNDER_WEEKLY_ONE_DECISION_YAML.read_text(encoding="utf-8")
            ) or {}
        for key, val in scaffold.items():
            if key not in existing or not str(existing.get(key) or "").strip():
                existing[key] = val
        FOUNDER_WEEKLY_ONE_DECISION_YAML.write_text(
            yaml.safe_dump(existing, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        print(f"WROTE {FOUNDER_WEEKLY_ONE_DECISION_YAML}")
    else:
        print(yaml.safe_dump(scaffold, allow_unicode=True, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
