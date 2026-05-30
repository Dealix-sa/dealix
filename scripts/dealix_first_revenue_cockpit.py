#!/usr/bin/env python3
"""Founder First-Revenue Cockpit — one daily command that says what to do today.

Ties the already-shipped pieces (warm-list close-packet engine, qualification,
and the existing ledgers/accessors) into a single bilingual (AR+EN)
"First-Revenue Action Board". It tells the founder, deterministically:

  1. Warm-list readiness — who is ready to close right now and the exact
     command to generate their packets.
  2. Pipeline snapshot — honest counts from the real ledgers (leads waiting,
     proof events, capital assets, renewals due, friction). Empty is shown as
     zero/empty; nothing is fabricated.
  3. Today's top 3 revenue actions — derived only from the state above, each
     with the concrete command to run.

Reused entry points (no new business logic invented here):
- scripts.dealix_warm_list_packets.read_rows / _row_to_prospect / _resolve_csv /
  _DECISION_BADGE — warm-list CSV parsing + per-row prospect mapping, mirrored
  exactly so the two scripts cannot diverge.
- auto_client_acquisition.sales_os.qualification.qualify — the verdict.
- The same ledgers/accessors dealix_pm_daily.py reads: lead_inbox,
  friction_log, payment_ops.renewal_scheduler, proof_ledger, capital_os.

Doctrine constraints honored:
- No outreach is sent. The cockpit only points to draft-generating commands.
- No invented KPIs or revenue. Only real ledger reads; absent data degrades to
  honest zeros/empties. Estimated value is labeled, never presented as verified.
- Reject / refer-out / doctrine-violating warm-list rows are excluded from the
  "ready-to-close" set.
- Bilingual (Arabic primary, English secondary).

The core (build_cockpit) is a pure function over its inputs (the warm-list rows
and an injectable pipeline reader) so it can be tested offline without network
or subprocess.

Usage:
    python scripts/dealix_first_revenue_cockpit.py
    python scripts/dealix_first_revenue_cockpit.py --csv data/warm_list.csv.template \\
        --out data/activation_pack/first_revenue_cockpit_DEMO.md
    python scripts/dealix_first_revenue_cockpit.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.dealix_warm_list_packets import (  # noqa: E402
    _DECISION_BADGE,
    _resolve_csv,
    _row_to_prospect,
    read_rows,
)

# Decisions that constitute a real, offer-bearing engagement the founder can
# close now. Mirrors the warm-list packet writer: reject / refer_out yield no
# offer, and any doctrine violation forces a reject in the core regardless.
_READY_DECISIONS: frozenset[str] = frozenset({"accept", "reframe"})
_DIAGNOSTIC_DECISIONS: frozenset[str] = frozenset({"diagnostic_only"})

# A lead is "waiting" once it has been untouched for longer than this.
_LEAD_WAIT_HOURS: int = 24
# Upper bound on leads read in one pass; counts at this cap are reported as "N+".
_LEAD_READ_LIMIT: int = 1000

_DISCLAIMER_LINE = (
    "Estimated value is not Verified value / "
    "القيمة التقديرية ليست قيمة مُتحقَّقة"
)

# Stable section anchors (used by the renderer and asserted by the test).
_SECTION_WARM = "1. Warm-list readiness / جاهزية القائمة الدافئة"
_SECTION_PIPELINE = "2. Pipeline snapshot / لقطة خط الأنابيب"
_SECTION_ACTIONS = "3. Today's top 3 revenue actions / أهم 3 إجراءات إيراد اليوم"


def _now() -> datetime:
    return datetime.now(UTC)


def _today_label() -> str:
    return _now().strftime("%Y-%m-%d")


# ── Warm-list readiness (pure) ────────────────────────────────────────────────


def assess_warm_list(rows: list[dict[str, str]], *, channel: str = "whatsapp") -> dict[str, Any]:
    """Qualify every warm-list row and bucket it.

    Pure: no I/O, no network. Reuses the warm-list row->prospect mapping and
    runs qualify() exactly as the packet generator does, then buckets each row
    into ready / diagnostic_only / skip. A row is "ready" only when its decision
    yields an offer (accept/reframe) AND it carries no doctrine violation; a
    reject, refer-out, or doctrine-violating row is always a skip.
    """
    from auto_client_acquisition.sales_os.qualification import qualify

    ready: list[dict[str, Any]] = []
    diagnostic: list[dict[str, Any]] = []
    skip: list[dict[str, Any]] = []

    for row in rows:
        prospect = _row_to_prospect(row, channel=channel)
        result = qualify(
            raw_request_text=str(prospect.get("raw_request_text") or ""),
            sector=str(prospect.get("sector") or ""),
            city=str(prospect.get("city") or ""),
            **prospect["signals"],
        )
        decision = result.decision
        violations = list(result.doctrine_violations)
        entry = {
            "name": prospect.get("decision_maker") or "(name?)",
            "company": prospect.get("company") or "Unknown",
            "decision": decision,
            "badge": _DECISION_BADGE.get(decision, decision.upper()),
            "score": int(result.score),
            "recommended_offer": result.recommended_offer,
            "doctrine_violations": violations,
        }
        if violations or decision not in (_READY_DECISIONS | _DIAGNOSTIC_DECISIONS):
            # Any doctrine violation, reject, or refer-out is always a skip.
            skip.append(entry)
        elif decision in _DIAGNOSTIC_DECISIONS:
            diagnostic.append(entry)
        else:  # accept / reframe with no violations
            ready.append(entry)

    return {
        "total": len(rows),
        "ready_count": len(ready),
        "diagnostic_count": len(diagnostic),
        "skip_count": len(skip),
        "ready": ready,
        "diagnostic": diagnostic,
        "skip": skip,
    }


# ── Pipeline accessors (I/O, each isolated + fail-safe) ───────────────────────


def _leads_waiting() -> dict[str, Any]:
    """Leads untouched for > _LEAD_WAIT_HOURS, read from the real lead_inbox.

    lead_inbox records carry `received_at` and a `status`; a lead still in the
    `new` state past the cutoff is waiting. Returns an honest zero on any error.
    """
    try:
        from auto_client_acquisition import lead_inbox

        records = lead_inbox.list_leads(limit=_LEAD_READ_LIMIT)
        # If the store returned exactly the read cap, the true count may be
        # higher; flag it so the number is reported as "N+" rather than implying
        # an exact total we did not actually read.
        truncated = len(records) >= _LEAD_READ_LIMIT
        cutoff = _now() - timedelta(hours=_LEAD_WAIT_HOURS)
        items: list[dict[str, Any]] = []
        for rec in records:
            if str(rec.get("status") or "new") not in ("new", "contacted"):
                continue
            stamp = rec.get("received_at") or rec.get("created_at") or ""
            try:
                received = datetime.fromisoformat(str(stamp))
                if received.tzinfo is None:
                    received = received.replace(tzinfo=UTC)
            except Exception:
                continue
            if received < cutoff:
                items.append(
                    {
                        "company": rec.get("company") or rec.get("email") or "(lead)",
                        "sector": rec.get("sector") or "",
                        "received_at": received.isoformat(),
                    }
                )
        return {"count": len(items), "items": items[:5], "truncated": truncated}
    except Exception:
        return {"count": 0, "items": [], "truncated": False}


def _recent_proof_events() -> dict[str, Any]:
    try:
        from auto_client_acquisition.proof_ledger.file_backend import get_default_ledger

        events = get_default_ledger().list_events(limit=10)
        items = [
            {
                "event_type": str(getattr(e, "event_type", "")),
                "customer_handle": str(getattr(e, "customer_handle", "")),
                "created_at": str(getattr(e, "created_at", "")),
            }
            for e in events[:5]
        ]
        return {"count": len(events), "items": items}
    except Exception:
        return {"count": 0, "items": []}


def _capital_this_week() -> dict[str, Any]:
    try:
        from auto_client_acquisition.capital_os.capital_ledger import list_assets

        assets = list_assets(limit=200)
        cutoff = _now() - timedelta(days=7)
        recent: list[dict[str, Any]] = []
        for a in assets:
            try:
                created = datetime.fromisoformat(str(getattr(a, "created_at", "")))
                if created.tzinfo is None:
                    created = created.replace(tzinfo=UTC)
            except Exception:
                continue
            if created >= cutoff:
                recent.append(
                    {
                        "asset_type": str(getattr(a, "asset_type", "")),
                        "owner": str(getattr(a, "owner", "")),
                    }
                )
        return {"count": len(recent), "items": recent[:5]}
    except Exception:
        return {"count": 0, "items": []}


def _renewals_due() -> dict[str, Any]:
    try:
        from auto_client_acquisition.payment_ops.renewal_scheduler import list_due

        due = list_due()
        items = [
            {
                "customer_id": str(getattr(s, "customer_id", "")),
                "plan": str(getattr(s, "plan", "")),
                "amount_sar": getattr(s, "amount_sar", 0),
            }
            for s in due[:10]
        ]
        return {"count": len(due), "items": items}
    except Exception:
        return {"count": 0, "items": []}


def _friction_high(customer_id: str) -> dict[str, Any]:
    try:
        from auto_client_acquisition.friction_log.aggregator import aggregate

        agg = aggregate(customer_id=customer_id, window_days=7).to_dict()
        by_sev = agg.get("by_severity") or {}
        return {
            "total": int(agg.get("total") or 0),
            "high": int(by_sev.get("high") or 0),
            "top_3_kinds": agg.get("top_3_kinds") or [],
        }
    except Exception:
        return {"total": 0, "high": 0, "top_3_kinds": []}


def _retainer_eligible() -> dict[str, Any]:
    """Retainer-eligible accounts.

    adoption_os exposes scoring helpers (adoption_score, retainer_readiness) but
    there is no per-account adoption ledger to iterate in this repo, so there is
    nothing real to count. Rather than fabricate accounts, this degrades to an
    honest empty with an explicit note. Wire an adoption ledger to populate it.
    """
    return {
        "count": 0,
        "items": [],
        "note": "no_adoption_ledger_wired",
    }


def read_pipeline(customer_id: str = "dealix_internal") -> dict[str, Any]:
    """Read every pipeline signal from the real ledgers. Honest zeros on absence."""
    return {
        "leads_waiting_24h_plus": _leads_waiting(),
        "recent_proof_events": _recent_proof_events(),
        "capital_assets_this_week": _capital_this_week(),
        "renewals_due_next_7d": _renewals_due(),
        "friction_high_7d": _friction_high(customer_id),
        "retainer_eligible": _retainer_eligible(),
    }


# ── Top-3 actions (pure, deterministic) ───────────────────────────────────────


def _top_actions(
    warm: dict[str, Any],
    pipeline: dict[str, Any],
    *,
    csv_label: str,
    is_demo: bool,
) -> list[dict[str, str]]:
    """Derive up to 3 concrete revenue actions purely from the state above.

    Each action carries a bilingual title and the exact command to run. Order is
    deterministic: closing ready warm contacts first, then follow-ups on
    waiting leads / due renewals, then proof publication, with stable fallbacks.
    """
    actions: list[dict[str, str]] = []
    demo_flag = " (DEMO)" if is_demo else ""

    ready_n = warm["ready_count"]
    if ready_n > 0:
        actions.append(
            {
                "ar": f"أنشئ حُزَم الإغلاق لـ {ready_n} جهة دافئة جاهزة.",
                "en": f"Generate close packets for the {ready_n} ready warm contact(s).",
                "command": f"python scripts/dealix_warm_list_packets.py --csv {csv_label}",
            }
        )

    leads_n = pipeline["leads_waiting_24h_plus"]["count"]
    renewals_n = pipeline["renewals_due_next_7d"]["count"]
    if leads_n > 0:
        actions.append(
            {
                "ar": f"تابع {leads_n} عميل محتمل ينتظر أكثر من {_LEAD_WAIT_HOURS} ساعة.",
                "en": f"Follow up the {leads_n} lead(s) waiting > {_LEAD_WAIT_HOURS}h.",
                "command": "python scripts/dealix_pm_daily.py",
            }
        )
    if renewals_n > 0:
        actions.append(
            {
                "ar": f"أكِّد {renewals_n} تجديد retainer مستحق هذا الأسبوع.",
                "en": f"Confirm {renewals_n} retainer renewal(s) due this week.",
                "command": (
                    "python -c \"from auto_client_acquisition.payment_ops."
                    "renewal_scheduler import list_due; print(list_due())\""
                ),
            }
        )

    proof_n = pipeline["recent_proof_events"]["count"]
    if proof_n == 0 and len(actions) < 3:
        actions.append(
            {
                "ar": "انشر Proof Pack واحدة أو ملخّص حالة آمن مستحق.",
                "en": "Publish 1 Proof Pack / case-safe summary if one is due.",
                "command": (
                    "python scripts/dealix_close_packet_generator.py --help "
                    "(then send the matched proposal section manually)"
                ),
            }
        )

    friction_high = pipeline["friction_high_7d"]["high"]
    if friction_high > 0 and len(actions) < 3:
        actions.append(
            {
                "ar": f"عالج {friction_high} حدث احتكاك عالي الخطورة قبل توسعة العرض.",
                "en": (
                    f"Resolve {friction_high} high-severity friction event(s) "
                    "before expanding the offer."
                ),
                "command": "python scripts/dealix_pm_daily.py --json",
            }
        )

    if warm["diagnostic_count"] > 0 and len(actions) < 3:
        dn = warm["diagnostic_count"]
        actions.append(
            {
                "ar": f"حوّل {dn} جهة (تشخيص فقط) إلى تشخيص مجاني مُجدوَل.",
                "en": f"Move the {dn} diagnostic-only contact(s) into a scheduled free diagnostic.",
                "command": f"python scripts/dealix_warm_list_packets.py --csv {csv_label}",
            }
        )

    if not actions:
        actions.append(
            {
                "ar": f"يوم هادئ{demo_flag}: تواصل مع جهتين دافئتين ووثّق أصلاً واحداً قابلاً لإعادة الاستخدام.",
                "en": f"Quiet day{demo_flag}: reach out to 2 warm contacts and log 1 reusable asset.",
                "command": "python scripts/dealix_founder_daily_brief.py",
            }
        )

    return actions[:3]


# ── Core ──────────────────────────────────────────────────────────────────────


def build_cockpit(
    rows: list[dict[str, str]],
    *,
    csv_label: str,
    is_demo: bool = False,
    channel: str = "whatsapp",
    customer_id: str = "dealix_internal",
    pipeline_reader: Callable[[str], dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Assemble the full cockpit board as a machine-readable dict.

    Pure with respect to the warm list: `rows` are qualified deterministically.
    The pipeline side is read through `pipeline_reader` (defaults to the real
    ledger reader); inject a stub in tests to keep the build fully offline. The
    rendered bilingual markdown lives under the `markdown` key.
    """
    reader = pipeline_reader or read_pipeline
    warm = assess_warm_list(rows, channel=channel)
    pipeline = reader(customer_id)
    actions = _top_actions(warm, pipeline, csv_label=csv_label, is_demo=is_demo)

    cockpit = {
        "generated_at": _now().isoformat(),
        "date": _today_label(),
        "is_demo": is_demo,
        "csv_label": csv_label,
        "is_estimate": True,
        "warm_list": warm,
        "pipeline": pipeline,
        "top_actions": actions,
        "disclaimer": _DISCLAIMER_LINE,
    }
    cockpit["markdown"] = render_markdown(cockpit)
    return cockpit


# ── Renderer (bilingual markdown) ─────────────────────────────────────────────


def render_markdown(cockpit: dict[str, Any]) -> str:
    warm = cockpit["warm_list"]
    pipe = cockpit["pipeline"]
    csv_label = cockpit["csv_label"]
    lines: list[str] = []

    lines.append(f"# First-Revenue Action Board / لوحة إجراءات أول إيراد · {cockpit['date']}")
    lines.append("")
    if cockpit["is_demo"]:
        lines.append(
            "> **DEMO DATA / بيانات تجريبية** — generated from the warm-list "
            "template, not the founder's real list."
        )
        lines.append("")
    lines.append(f"_Generated: {cockpit['generated_at']}_")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 1 — warm-list readiness
    lines.append(f"## {_SECTION_WARM}")
    lines.append("")
    lines.append(
        f"- **Ready to close / جاهز للإغلاق (ACCEPT/REFRAME):** {warm['ready_count']}"
    )
    lines.append(
        f"- **Diagnostic-only / تشخيص فقط:** {warm['diagnostic_count']}"
    )
    lines.append(
        f"- **Skip / تخطٍّ (reject/refer-out/doctrine):** {warm['skip_count']}"
    )
    lines.append("")
    if warm["ready"]:
        lines.append("**Ready contacts / جهات جاهزة:**")
        lines.append("")
        lines.append("| Name / الاسم | Company / الشركة | Decision / القرار | Score / الدرجة |")
        lines.append("|---|---|---|---|")
        for r in warm["ready"]:
            lines.append(
                f"| {r['name']} | {r['company']} | {r['badge']} | {r['score']}/100 |"
            )
        lines.append("")
        lines.append(
            "Next command / الأمر التالي (generates DRAFT packets only — never auto-sends):"
        )
        lines.append("")
        lines.append("```")
        lines.append(f"python scripts/dealix_warm_list_packets.py --csv {csv_label}")
        lines.append("```")
    else:
        lines.append(
            "_No ready-to-close contacts in this list. Reject / refer-out / "
            "doctrine rows are excluded. / لا توجد جهات جاهزة للإغلاق._"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # Section 2 — pipeline snapshot
    lines.append(f"## {_SECTION_PIPELINE}")
    lines.append("")
    leads = pipe["leads_waiting_24h_plus"]
    proof = pipe["recent_proof_events"]
    cap = pipe["capital_assets_this_week"]
    ren = pipe["renewals_due_next_7d"]
    fr = pipe["friction_high_7d"]
    ret = pipe["retainer_eligible"]
    leads_label = f"{leads['count']}+" if leads.get("truncated") else str(leads["count"])
    lines.append(
        f"- Leads waiting > {_LEAD_WAIT_HOURS}h / عملاء ينتظرون: **{leads_label}**"
    )
    lines.append(f"- Recent proof events / أحداث إثبات حديثة: **{proof['count']}**")
    lines.append(f"- Capital assets this week / أصول رأسمالية هذا الأسبوع: **{cap['count']}**")
    lines.append(f"- Renewals due next 7d / تجديدات مستحقة: **{ren['count']}**")
    lines.append(
        f"- High-severity friction (7d) / احتكاك عالي الخطورة: **{fr['high']}** "
        f"(total / الإجمالي: {fr['total']})"
    )
    ret_note = "" if ret["count"] else f" — _{ret.get('note', '')}_"
    lines.append(
        f"- Retainer-eligible accounts / حسابات مؤهلة للـ retainer: **{ret['count']}**{ret_note}"
    )
    lines.append("")
    if leads["items"]:
        lines.append("Waiting leads / عملاء بالانتظار:")
        for it in leads["items"]:
            lines.append(f"  - {it['company']} ({it.get('sector', '')}) — {it['received_at']}")
        lines.append("")
    if all(
        v == 0
        for v in (leads["count"], proof["count"], cap["count"], ren["count"], fr["total"], ret["count"])
    ):
        lines.append(
            "_All pipeline ledgers are empty — honest zeros, nothing fabricated. "
            "/ جميع السجلات فارغة — أصفار صادقة، بلا تلفيق._"
        )
        lines.append("")
    lines.append("---")
    lines.append("")

    # Section 3 — top 3 actions
    lines.append(f"## {_SECTION_ACTIONS}")
    lines.append("")
    for i, a in enumerate(cockpit["top_actions"], start=1):
        lines.append(f"{i}. **{a['ar']}**")
        lines.append(f"   _{a['en']}_")
        lines.append("   ```")
        lines.append(f"   {a['command']}")
        lines.append("   ```")
        lines.append("")
    lines.append("---")
    lines.append("")

    # Footer
    lines.append("## Disclaimer / إخلاء مسؤولية")
    lines.append(f"- _{cockpit['disclaimer']}_")
    lines.append(
        "- _Cockpit only. No outreach is sent; every command above produces a "
        "DRAFT the founder reviews and sends manually. / لوحة فقط؛ لا إرسال._"
    )
    lines.append("")
    return "\n".join(lines)


# ── CLI ───────────────────────────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Founder First-Revenue Cockpit — one daily board of what to do today "
            "to get revenue. Reads the warm list + real ledgers; sends nothing."
        )
    )
    parser.add_argument(
        "--csv",
        default="data/warm_list.csv",
        help=(
            "Warm-list CSV (name,role,company,sector,relationship,city,"
            "linkedin_url,notes). Falls back to the template (DEMO) if missing."
        ),
    )
    parser.add_argument(
        "--out",
        default="",
        help=(
            "Output markdown path "
            "(default data/founder_briefs/first_revenue_cockpit_<today>.md)."
        ),
    )
    parser.add_argument(
        "--customer",
        default="dealix_internal",
        help="Customer id used to scope the friction aggregate.",
    )
    parser.add_argument(
        "--json",
        dest="json_out",
        action="store_true",
        help="Print the machine-readable JSON cockpit to stdout instead of markdown.",
    )
    args = parser.parse_args(argv)

    csv_path, is_demo = _resolve_csv(args.csv)
    if not csv_path.exists():
        print(f"CSV not found at {csv_path} and no template fallback available.")
        print("Copy the template: cp data/warm_list.csv.template data/warm_list.csv")
        return 1

    rows = read_rows(csv_path)
    if not rows:
        print(f"Warm list is empty — fill {csv_path} with at least 1 contact, then re-run.")
        return 1

    # The command surfaced to the founder should reference the resolved CSV.
    csv_label = args.csv if not is_demo else "data/warm_list.csv.template"

    cockpit = build_cockpit(
        rows,
        csv_label=csv_label,
        is_demo=is_demo,
        customer_id=args.customer,
    )

    if args.json_out:
        machine = {k: v for k, v in cockpit.items() if k != "markdown"}
        print(json.dumps(machine, ensure_ascii=False, indent=2))
        return 0

    out_path = (
        Path(args.out)
        if args.out
        else REPO_ROOT / "data" / "founder_briefs" / f"first_revenue_cockpit_{_today_label()}.md"
    )
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(cockpit["markdown"] + "\n", encoding="utf-8")

    label = " (DEMO)" if is_demo else ""
    print(f"OK: processed {len(rows)} warm contact(s) from {csv_path}{label}")
    print(f"  ready to close: {cockpit['warm_list']['ready_count']}")
    print(f"  diagnostic-only: {cockpit['warm_list']['diagnostic_count']}")
    print(f"  skip (reject/refer-out/doctrine): {cockpit['warm_list']['skip_count']}")
    print(f"  board: {out_path}")
    print(cockpit["markdown"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
