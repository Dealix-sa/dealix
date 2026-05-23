"""Generate the CEO Daily Brief — bilingual, evidence-only.

Reads from <private_ops>/ tree and writes:
  <private_ops>/founder/ceo_daily_brief.md

If PRIVATE_OPS is missing, writes a clear template explaining the gap.

Non-negotiables enforced:
  - No guaranteed revenue / meeting / sales claims.
  - No external send is triggered.
  - No secrets surfaced.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return []


def _read_json(path: Path) -> dict | list | None:
    if not path.exists():
        return None
    try:
        import json
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _top(items: Iterable, n: int = 3) -> list:
    out = []
    for item in items:
        out.append(item)
        if len(out) >= n:
            break
    return out


def _section(title_ar: str, title_en: str, lines: list[str]) -> str:
    body = "\n".join(f"- {ln}" for ln in lines) if lines else "- (لا شيء — nothing today)"
    return f"## {title_ar} — {title_en}\n\n{body}\n"


def generate(private_ops: Path) -> str:
    blockers = _read_csv_rows(private_ops / "launch" / "blockers.csv")
    risks = _read_csv_rows(private_ops / "trust" / "open_risks.csv")
    machines = _read_csv_rows(private_ops / "ops" / "machine_health.csv")
    proposals = _read_csv_rows(private_ops / "sales" / "proposal_log.csv")
    approvals = _read_csv_rows(private_ops / "distribution" / "approvals.csv")
    decisions = _read_csv_rows(private_ops / "founder" / "decisions.csv")
    cash_rows = _read_csv_rows(private_ops / "finance" / "cash_collected.csv")
    today_file = private_ops / "founder" / "today.md"

    failing_machines = [m for m in machines if m.get("state", "").lower() in {"down", "degraded"}]
    high_risks = [r for r in risks if r.get("severity", "").lower() in {"high", "critical"}]
    open_blockers = [b for b in blockers if b.get("status", "open").lower() == "open"]
    pending_payments = [
        p for p in proposals
        if p.get("status", "").lower() in {"sent", "verbal_yes"} and p.get("paid", "").lower() != "true"
    ]
    pending_approvals = [a for a in approvals if a.get("status", "").lower() == "pending"]
    pending_decisions = [d for d in decisions if d.get("status", "").lower() == "open"]

    bottleneck = "غير معروف — حدد يدويًا" if not (pending_payments or open_blockers) else (
        f"{len(pending_payments)} proposals بانتظار دفع + {len(open_blockers)} blockers مفتوحة"
    )

    if open_blockers:
        top_action = f"إغلاق blocker #{open_blockers[0].get('id', '?')}: {open_blockers[0].get('description', '')[:120]}"
    elif pending_payments:
        first = pending_payments[0]
        top_action = (
            f"Follow-up على proposal {first.get('proposal_id', '?')} "
            f"للعميل {first.get('customer', '?')}"
        )
    elif failing_machines:
        m = failing_machines[0]
        top_action = f"إعادة تشغيل machine {m.get('machine_id', '?')} (state={m.get('state', '?')})"
    else:
        top_action = "اختر action واحد فقط لليوم وكتابته في today.md"

    sections = [
        f"# CEO Daily Brief — {datetime.now().strftime('%Y-%m-%d')}",
        "",
        f"_Generated: {_now_iso()}_",
        f"_Source: {private_ops}_",
        "",
        _section("Top CEO Action", "Top CEO Action", [top_action]),
        _section("اختناق الكاش", "Revenue Bottleneck", [bottleneck]),
        _section(
            "مخاطر الثقة",
            "Trust Risks",
            [f"{r.get('risk_id', '?')}: {r.get('description', '')[:120]}" for r in _top(high_risks)],
        ),
        _section(
            "Worker Failures",
            "Worker Failures",
            [f"{m.get('machine_id', '?')}: {m.get('state', '?')} ({m.get('notes', '')[:80]})"
             for m in _top(failing_machines)],
        ),
        _section(
            "Launch Blockers",
            "Launch Blockers",
            [f"{b.get('id', '?')}: {b.get('description', '')[:120]}" for b in _top(open_blockers)],
        ),
        _section(
            "Payment Follow-Ups",
            "Payment Follow-Ups",
            [f"{p.get('proposal_id', '?')} → {p.get('customer', '?')} (D+{p.get('days_open', '?')})"
             for p in _top(pending_payments)],
        ),
        _section(
            "Approved Work Ready",
            "Approved Work Ready",
            [f"{a.get('id', '?')}: {a.get('description', '')[:100]}" for a in _top(pending_approvals)],
        ),
        _section(
            "Decisions Needed",
            "Decisions Needed",
            [f"{d.get('decision_id', '?')}: {d.get('question', '')[:120]}" for d in _top(pending_decisions)],
        ),
        _section(
            "What To Ignore Today",
            "What To Ignore Today",
            [
                "LinkedIn impressions / vanity reach.",
                "أي طلب تواصل بارد.",
                "اقتراحات scope creep من proposals مغلقة.",
            ],
        ),
        "",
        "---",
        "",
        "_No guaranteed revenue, sales or meetings are claimed. All numbers are observed-only._",
    ]

    return "\n".join(sections)


def write_brief(private_ops: Path) -> Path:
    target = private_ops / "founder" / "ceo_daily_brief.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(generate(private_ops), encoding="utf-8")
    return target


def _empty_template(reason: str) -> str:
    return (
        f"# CEO Daily Brief — {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"_PRIVATE_OPS unavailable: {reason}_\n\n"
        "## Setup\n\n"
        "- Pass `PRIVATE_OPS=/path` to `make ceo-daily-brief`.\n"
        "- Or set `DEALIX_PRIVATE_OPS` env var.\n"
        "- See docs/founder/CEO_DAILY_BRIEF_SYSTEM.md\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Dealix CEO Daily Brief.")
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("PRIVATE_OPS") or os.environ.get("DEALIX_PRIVATE_OPS"),
        help="Path to private ops tree (or env PRIVATE_OPS / DEALIX_PRIVATE_OPS).",
    )
    parser.add_argument("--print", action="store_true", help="Print to stdout in addition to writing.")
    args = parser.parse_args(argv)

    if not args.private_ops:
        sys.stderr.write(
            "[warn] PRIVATE_OPS not set — writing empty template to stdout only.\n"
        )
        sys.stdout.write(_empty_template("not set"))
        return 0

    private_ops = Path(args.private_ops).expanduser().resolve()
    if not private_ops.exists():
        sys.stderr.write(f"[warn] PRIVATE_OPS path missing: {private_ops}\n")
        sys.stdout.write(_empty_template(str(private_ops)))
        return 0

    out = write_brief(private_ops)
    sys.stdout.write(f"[ok] wrote {out}\n")
    if args.print:
        sys.stdout.write(out.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
