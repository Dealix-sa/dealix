#!/usr/bin/env python3
"""Batch Close Packet generator over the founder's whole warm list.

Reads the warm-list CSV (the same intake `warm_list_outreach.py` uses) and runs
the unified Close Packet core (`dealix_close_packet_generator.build_close_packet`)
over every contact in one pass. For each qualified contact it writes one
bilingual, founder-send-ready packet; for reject / refer-out / doctrine-violating
rows it writes no packet and records the reason in the index instead.

Reused entry points (no new business logic invented here):
- scripts.dealix_close_packet_generator.build_close_packet (pure core)
- auto_client_acquisition.sales_os.qualification.qualify (via the core)
- warm-list CSV parsing + flag inference, mirrored from warm_list_outreach.py so
  the two scripts cannot diverge.

Doctrine constraints honored:
- Nothing is auto-sent. Every packet's outreach stays a labeled DRAFT (the core
  enforces this and runs the governance pre-check).
- No packet / outreach is written for a reject, refer-out, or doctrine-violating
  row. Those rows appear in the index with the reason (and any doctrine
  violations) so the founder declines or refers out cleanly.
- No invented metrics. The bilingual disclaimers come from the core.

Offline: the core builder is a pure function over a dict (no network, no
subprocess). detect_stack is never invoked here.

Usage:
    python scripts/dealix_warm_list_packets.py
    python scripts/dealix_warm_list_packets.py \\
        --csv data/warm_list.csv.template \\
        --out-dir data/activation_pack/packets_DEMO \\
        --channel whatsapp
"""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.dealix_close_packet_generator import build_close_packet

_DEFAULT_CSV = "data/warm_list.csv"
_TEMPLATE_CSV = "data/warm_list.csv.template"
_DEFAULT_OUT_DIR = "data/outreach/packets"
_VALID_CHANNELS: tuple[str, ...] = ("linkedin", "whatsapp", "email")

# Roles that imply the owner / decision-maker is present. Mirrored from
# warm_list_outreach._qualify_contact so the two scripts never diverge.
_OWNER_ROLES: frozenset[str] = frozenset(
    {"ceo", "coo", "gm", "founder", "md", "vp"}
)

# Decisions that produce no offer, hence no packet and no outreach. Anything in
# this set is recorded in the index with a reason instead of a packet file.
_NO_PACKET_DECISIONS: frozenset[str] = frozenset({"reject", "refer_out"})

# Bilingual decision badges. Mirrors warm_list_outreach._render_contact style
# (no emojis here; this file ships in code under the no-emoji quality bar).
_DECISION_BADGE: dict[str, str] = {
    "accept": "ACCEPT / مقبول",
    "diagnostic_only": "DIAGNOSTIC_ONLY / تشخيص فقط",
    "reframe": "REFRAME / إعادة صياغة",
    "reject": "REJECT / مرفوض",
    "refer_out": "REFER_OUT / إحالة",
}

_DISCLAIMER_LINE = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة"
)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def _sanitize_filename(value: str) -> str:
    """Reduce an arbitrary label to a safe, lowercase file stem.

    Keeps alphanumerics, collapses every other character to a single
    underscore, and never returns an empty stem.
    """
    keep = [c.lower() if c.isalnum() else "_" for c in (value or "").strip()]
    slug = "".join(keep).strip("_")
    while "__" in slug:
        slug = slug.replace("__", "_")
    return slug or "contact"


def _decision_badge(decision: str) -> str:
    return _DECISION_BADGE.get(decision, decision.upper())


def _handle_from_url(value: str) -> str:
    """Extract a usable handle from a linkedin/contact URL or string.

    Used only as a filename fallback when a row has no company. Returns an
    empty string when nothing usable is present.
    """
    raw = (value or "").strip()
    if not raw:
        return ""
    # Strip protocol + host, keep the last meaningful path segment.
    tail = raw.rstrip("/").split("/")[-1]
    return _sanitize_filename(tail) if tail else ""


def _row_to_prospect(row: dict[str, str], *, channel: str) -> dict[str, Any]:
    """Map one warm-list CSV row to a Close Packet prospect dict.

    Flag inference mirrors warm_list_outreach._qualify_contact exactly:
    - owner_present: role is one of the owner-grade titles
    - pain/data/budget/retainer paths: true only for warm/active relationships
    - accepts_governance + wants_safe_methods + proof_path_visible: always true
    The row's notes (plus sector) become raw_request_text so the core's doctrine
    scan sees any forbidden request expressed in the notes.
    """
    name = (row.get("name") or "").strip()
    role = (row.get("role") or "").strip()
    company = (row.get("company") or "").strip()
    sector = (row.get("sector") or "").strip()
    relationship = (row.get("relationship") or "cold").strip().lower()
    city = (row.get("city") or "").strip()
    notes = (row.get("notes") or "").strip()

    has_owner = role.lower() in _OWNER_ROLES
    warm_or_active = relationship in ("warm", "active")
    rel_text = (notes + " " + sector).strip()

    signals = {
        "pain_clear": warm_or_active,
        "owner_present": has_owner,
        "data_available": warm_or_active,
        "accepts_governance": True,
        "has_budget": warm_or_active,
        "wants_safe_methods": True,
        "proof_path_visible": True,
        "retainer_path_visible": warm_or_active,
    }

    return {
        "company": company or name or "Unknown",
        "sector": sector or "b2b_services",
        "decision_maker": name,
        "role": role,
        "city": city or "Riyadh",
        # The core refuses to draft outreach on a cold basis; collapse the
        # relationship to the two values the core understands for warm intake.
        "relationship": "warm" if warm_or_active else "cold",
        "channel": channel,
        "warm_intro_notes": notes,
        "raw_request_text": rel_text,
        "signals": signals,
    }


def _packet_stem(row: dict[str, str], prospect: dict[str, Any]) -> str:
    """Choose a filename stem: company, else handle/contact, else name."""
    company = (row.get("company") or "").strip()
    if company:
        return _sanitize_filename(company)
    handle = _handle_from_url(row.get("linkedin_url") or row.get("contact") or "")
    if handle:
        return handle
    return _sanitize_filename(str(prospect.get("decision_maker") or "contact"))


def _no_packet_reason(packet: dict[str, Any]) -> str:
    """Human-readable reason a row gets no packet (decision-driven)."""
    violations = packet.get("doctrine_violations") or []
    decision = packet.get("decision", "")
    if violations:
        return "doctrine_violation: " + ", ".join(violations)
    if decision in _NO_PACKET_DECISIONS:
        return f"{decision} — no offer, decline/refer out politely"
    return "no packet"


def read_rows(csv_path: Path) -> list[dict[str, str]]:
    """Read non-empty warm-list rows from a CSV.

    Mirrors warm_list_outreach.main parsing: DictReader, skip rows with no
    name. Pure I/O — raises FileNotFoundError if the path is missing.
    """
    rows: list[dict[str, str]] = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not (row.get("name") or "").strip():
                continue
            rows.append(row)
    return rows


def build_packets(
    rows: list[dict[str, str]],
    *,
    channel: str = "whatsapp",
) -> list[dict[str, Any]]:
    """Run the Close Packet core over every row (pure: no I/O, no network).

    Returns one result dict per row with the keys the index + writer need:
    name, company, decision, badge, score, recommended_offer, doctrine_violations,
    write_packet (bool), reason, stem, and the full `packet` (incl. markdown).
    """
    if channel not in _VALID_CHANNELS:
        raise ValueError(f"invalid_channel:{channel}")

    results: list[dict[str, Any]] = []
    seen_stems: dict[str, int] = {}
    for row in rows:
        prospect = _row_to_prospect(row, channel=channel)
        packet = build_close_packet(prospect)
        decision = packet["decision"]
        violations = list(packet.get("doctrine_violations") or [])
        # Write a packet only when the decision yields an offer AND there is no
        # doctrine violation. (A doctrine violation already forces a reject in
        # the core, so this is belt-and-suspenders.)
        write_packet = decision not in _NO_PACKET_DECISIONS and not violations

        stem = _packet_stem(row, prospect)
        # De-duplicate filename stems so two rows never overwrite each other.
        if write_packet:
            count = seen_stems.get(stem, 0)
            seen_stems[stem] = count + 1
            if count:
                stem = f"{stem}_{count + 1}"

        q = packet["qualification"]
        results.append(
            {
                "name": prospect["decision_maker"] or "(name?)",
                "company": prospect["company"],
                "decision": decision,
                "badge": _decision_badge(decision),
                "score": int(q["score"]),
                "recommended_offer": q["recommended_offer"],
                "doctrine_violations": violations,
                "write_packet": write_packet,
                "reason": "" if write_packet else _no_packet_reason(packet),
                "stem": stem,
                "packet": packet,
            }
        )
    return results


def _render_index(
    results: list[dict[str, Any]],
    *,
    out_dir_name: str,
    is_demo: bool,
    generated: int,
    skipped: int,
) -> str:
    """Render the bilingual INDEX.md table + summary counts."""
    lines: list[str] = []
    lines.append("# Warm-list Close Packets — index / فهرس حُزَم الإغلاق")
    lines.append("")
    if is_demo:
        lines.append(
            "> **DEMO DATA / بيانات تجريبية** — generated from the warm-list "
            "template, not the founder's real list."
        )
        lines.append("")
    lines.append(f"_Generated: {_now_iso()}_")
    lines.append("")
    lines.append(
        f"**Summary / الملخص:** {generated} packet(s) generated / "
        f"تم إنشاء {generated} حزمة · {skipped} skipped / تم تخطّي {skipped}."
    )
    lines.append("")
    lines.append(
        "Reject / refer-out / doctrine-violating rows get **no packet** — "
        "decline or refer out politely. / صفوف الرفض/الإحالة/خرق العقيدة "
        "بلا حزمة — اعتذر أو أحِل بأدب."
    )
    lines.append("")
    lines.append(
        "| # | Contact / جهة الاتصال | Company / الشركة | "
        "Decision / القرار | Score / الدرجة | Offer / العرض | "
        "Packet / الحزمة |"
    )
    lines.append("|---|---|---|---|---|---|---|")

    for i, r in enumerate(results, start=1):
        if r["write_packet"]:
            packet_cell = f"[{r['stem']}_close_packet.md](./{r['stem']}_close_packet.md)"
        else:
            packet_cell = f"no packet — {r['reason']}"
        offer = r["recommended_offer"]
        lines.append(
            f"| {i} | {r['name']} | {r['company']} | {r['badge']} | "
            f"{r['score']}/100 | `{offer}` | {packet_cell} |"
        )

    lines.append("")
    lines.append(f"_Output directory: `{out_dir_name}`_")
    lines.append("")
    lines.append(f"_{_DISCLAIMER_LINE}._")
    lines.append("")
    return "\n".join(lines)


def write_outputs(
    results: list[dict[str, Any]],
    *,
    out_dir: Path,
    is_demo: bool,
) -> dict[str, Any]:
    """Write one packet per qualified row + the INDEX.md. Returns a summary.

    Pure I/O over the precomputed results. No packet is written for rows whose
    `write_packet` is False (reject / refer-out / doctrine violation).
    """
    out_dir.mkdir(parents=True, exist_ok=True)

    written_files: list[Path] = []
    skipped = 0
    for r in results:
        if not r["write_packet"]:
            skipped += 1
            continue
        path = out_dir / f"{r['stem']}_close_packet.md"
        path.write_text(r["packet"]["markdown"], encoding="utf-8")
        written_files.append(path)

    index_md = _render_index(
        results,
        out_dir_name=str(out_dir),
        is_demo=is_demo,
        generated=len(written_files),
        skipped=skipped,
    )
    index_path = out_dir / "INDEX.md"
    index_path.write_text(index_md, encoding="utf-8")

    return {
        "generated": len(written_files),
        "skipped": skipped,
        "written_files": written_files,
        "index_path": index_path,
        "is_demo": is_demo,
    }


def _resolve_csv(csv_arg: str) -> tuple[Path, bool]:
    """Resolve the CSV path, falling back to the template (DEMO) when missing.

    Returns (path, is_demo). is_demo is True when we fell back to the template
    or the caller explicitly pointed at a `.template` file.
    """
    path = Path(csv_arg)
    if not path.is_absolute():
        path = REPO_ROOT / csv_arg

    if path.exists():
        return path, path.name.endswith(".template")

    template = REPO_ROOT / _TEMPLATE_CSV
    if template.exists():
        return template, True
    return path, False  # caller handles the missing-file error


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Batch the founder Close Packet generator over the whole warm list."
        )
    )
    parser.add_argument(
        "--csv",
        default=_DEFAULT_CSV,
        help=(
            "Warm-list CSV (name,role,company,sector,relationship,city,"
            "linkedin_url,notes). Falls back to the template (DEMO) if missing."
        ),
    )
    parser.add_argument(
        "--out-dir",
        dest="out_dir",
        default=_DEFAULT_OUT_DIR,
        help="Directory for per-contact packets + INDEX.md.",
    )
    parser.add_argument(
        "--channel",
        choices=list(_VALID_CHANNELS),
        default="whatsapp",
        help="Outreach channel for the DRAFT inside each packet.",
    )
    args = parser.parse_args(argv)

    csv_path, is_demo = _resolve_csv(args.csv)
    if not csv_path.exists():
        print(f"CSV not found at {csv_path} and no template fallback available.")
        print(f"Copy the template: cp {_TEMPLATE_CSV} {args.csv}")
        return 1

    rows = read_rows(csv_path)
    if not rows:
        print(f"CSV is empty — fill {csv_path} with at least 1 contact, then re-run.")
        return 1

    results = build_packets(rows, channel=args.channel)

    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = REPO_ROOT / args.out_dir
    summary = write_outputs(results, out_dir=out_dir, is_demo=is_demo)

    label = " (DEMO)" if is_demo else ""
    print(f"OK: processed {len(rows)} contact(s) from {csv_path}{label}")
    print(f"  packets generated: {summary['generated']}")
    print(f"  skipped (reject/refer_out/doctrine): {summary['skipped']}")
    print(f"  index: {summary['index_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
