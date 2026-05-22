#!/usr/bin/env python3
"""Founder reality check — single command, evidence-based truth report.

What's wired (real files), what was claimed but is absent, gate status from
the real evidence CSV, and three honest next actions. Arabic + English. No
invention. No "GREEN" without `payment_received` + `proof_pack_delivered`.

Usage:
  python3 scripts/founder_reality_check.py            # human report
  python3 scripts/founder_reality_check.py --json     # machine JSON
  python3 scripts/founder_reality_check.py --quiet    # just the verdict line

Exit code mirrors the gate: 0 when Phase 0–1 is open, 1 otherwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from dealix.commercial_ops.founder_reality_check import build_reality_check  # noqa: E402


def _line(s: str = "") -> None:
    print(s)


def _ok(b: bool) -> str:
    return "OK " if b else "-- "


def _render_human(snapshot: dict) -> None:
    verdict = snapshot.get("verdict", "UNKNOWN")
    no_build = snapshot.get("no_build_until_first_paid")
    _line(f"FOUNDER_REALITY_CHECK_VERDICT={verdict}")
    _line(
        f"no_build_until_first_paid={'true' if no_build else 'false'}"
        " (doctrine: لا بناء قبل أول دفعة حقيقية + Proof Pack)"
    )
    _line(f"generated_at={snapshot.get('generated_at')}")
    _line()

    wired = snapshot.get("wired_anchors", {})
    _line(
        f"-- WIRED ANCHORS — {wired.get('present')}/{wired.get('total')} present --"
    )
    for item in wired.get("items", []):
        _line(f"  {_ok(item['exists'])}{item['path']}")
        _line(f"     · {item['proves_ar']}")
    _line()

    absent = snapshot.get("claimed_but_absent", {})
    _line(
        f"-- CLAIMED BUT ABSENT — {absent.get('still_absent')}/"
        f"{absent.get('total_claims')} confirmed missing --"
    )
    for item in absent.get("items", []):
        marker = "(!) found locally" if item["exists"] else "absent"
        _line(f"  -- {item['path']}  [{marker}]")
        _line(f"     · {item['claim_ar']}")
    _line()

    ev = snapshot.get("evidence", {})
    _line(
        f"-- EVIDENCE TRUTH — {ev.get('real_rows')} real / "
        f"{ev.get('total_rows')} total rows --"
    )
    by_type = ev.get("by_type") or {}
    if by_type:
        for et, n in sorted(by_type.items(), key=lambda x: (-x[1], x[0])):
            _line(f"  · {et}: {n}")
    else:
        _line("  · لا توجد أحداث حقيقية بعد — السجل لا يزال (template/seed) فقط")
    _line(f"  csv: {ev.get('csv_path')}")
    _line()

    gate = snapshot.get("phase_0_1_gate", {})
    _line(f"-- PHASE 0–1 GATE — verdict={gate.get('verdict')} --")
    for b in gate.get("blockers_ar") or []:
        _line(f"  -- {b}")
    if not gate.get("blockers_ar"):
        _line("  OK gate open — proceed under no_build_after_first_paid policy")
    _line()

    weekly = snapshot.get("weekly_one_decision", {})
    _line(
        f"-- WEEKLY DECISION — verdict={weekly.get('verdict')} "
        f"(week={weekly.get('expected_week_id') or weekly.get('week_id')}) --"
    )

    gtm = snapshot.get("gtm_codification", {})
    _line(
        f"-- GTM CODIFICATION — verdict={gtm.get('verdict')} "
        f"({gtm.get('debriefs_with_notes')}/{gtm.get('target_deals')}) --"
    )

    pdpl = snapshot.get("pdpl_compliance_pass", {})
    _line(
        f"-- PDPL PASS — verdict={pdpl.get('verdict')} "
        f"({pdpl.get('done')}/{pdpl.get('total')}) --"
    )
    _line()

    actions = snapshot.get("next_actions") or []
    _line("-- NEXT 3 HONEST ACTIONS --")
    if not actions:
        _line("  OK كل البوابات مفتوحة — راجع War Room للتنفيذ اليومي")
    for i, a in enumerate(actions, 1):
        _line(f"  {i}. {a.get('title_ar')}  ({a.get('title_en')})")
        _line(f"     do: {a.get('do_ar')}")
        if a.get("doc"):
            _line(f"     doc: {a['doc']}")
    _line()

    notes = snapshot.get("honesty_notes") or {}
    _line("-- HONESTY NOTES --")
    _line(f"  payment_received real events: {notes.get('first_paid_real_events')}")
    _line(f"  proof_pack_delivered real events: {notes.get('proof_pack_real_events')}")
    _line(f"  crm_kpi_pending: {notes.get('crm_kpi_pending')}")
    _line(f"  rule: {notes.get('rule')}")


def main(argv: list[str] | None = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    as_json = "--json" in args
    quiet = "--quiet" in args
    snapshot = build_reality_check()

    if as_json:
        print(json.dumps(snapshot, ensure_ascii=False, indent=2))
    elif quiet:
        print(f"FOUNDER_REALITY_CHECK_VERDICT={snapshot.get('verdict')}")
    else:
        _render_human(snapshot)

    return 0 if snapshot.get("verdict") == "GATE_OPEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
