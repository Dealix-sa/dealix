"""Generate the Weekly Growth War Room review — evidence-only.

Reads from <private_ops>/ and writes:
  <private_ops>/founder/weekly_growth_review.md

Surfaces what moved / stalled / Kill-Fix-Scale decisions for the week.
Never claims guaranteed revenue.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8", newline="") as fh:
            return list(csv.DictReader(fh))
    except (OSError, csv.Error):
        return []


def _parse_date(s: str) -> date | None:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(s.split("T")[0][:10], "%Y-%m-%d").date()
        except ValueError:
            continue
    return None


def _within_week(rows: list[dict[str, str]], days: int = 7) -> list[dict[str, str]]:
    cutoff = date.today() - timedelta(days=days)
    out = []
    for r in rows:
        d = _parse_date(r.get("date", "") or r.get("created_at", ""))
        if d and d >= cutoff:
            out.append(r)
    return out


def _bullet(items: list[str]) -> str:
    return "\n".join(f"- {x}" for x in items) if items else "- (لا شيء — nothing)"


def _section(title_ar: str, title_en: str, body: str) -> str:
    return f"## {title_ar} — {title_en}\n\n{body}\n"


def generate(private_ops: Path) -> str:
    cash = _read_csv(private_ops / "finance" / "cash_collected.csv")
    proposals = _read_csv(private_ops / "sales" / "proposal_log.csv")
    meetings = _read_csv(private_ops / "sales" / "meetings.csv")
    experiments = _read_csv(private_ops / "learning" / "experiments.csv")
    decisions = _read_csv(private_ops / "learning" / "decisions.csv")
    sector_log = _read_csv(private_ops / "learning" / "sector_learning.csv")
    message_log = _read_csv(private_ops / "learning" / "message_learning.csv")

    week_cash = _within_week(cash)
    week_props = _within_week(proposals)
    week_meets = _within_week(meetings)
    week_exps = _within_week(experiments)

    cash_sum = sum(float(r.get("amount_sar", 0) or 0) for r in week_cash)
    moved = [
        f"كاش هذا الأسبوع: {cash_sum:.0f} SAR (rows: {len(week_cash)})",
        f"Proposals مرسلة: {len(week_props)}",
        f"اجتماعات: {len(week_meets)}",
    ]

    stalled_proposals = [
        p for p in proposals
        if p.get("status", "").lower() in {"sent", "verbal_yes"}
        and (date.today() - (_parse_date(p.get("date", "")) or date.today())).days >= 7
    ]
    stalled = [f"Proposals stalled ≥7 يوم: {len(stalled_proposals)}"]

    sectors = Counter()
    for r in proposals:
        sec = (r.get("sector") or "unknown").strip()
        if r.get("status", "").lower() == "paid":
            sectors[sec] += 1
    best_sector = sectors.most_common(1)[0][0] if sectors else "غير محدد"
    worst_sectors = [s for s in {p.get("sector", "") for p in proposals} if s and sectors[s] == 0]
    worst_sector = worst_sectors[0] if worst_sectors else "غير محدد"

    channels = Counter()
    for r in meetings:
        ch = (r.get("channel") or "unknown").strip()
        channels[ch] += 1
    best_channel = channels.most_common(1)[0][0] if channels else "غير محدد"

    message_perf = sorted(
        message_log,
        key=lambda r: float(r.get("reply_rate", 0) or 0),
        reverse=True,
    )
    best_message = (
        message_perf[0].get("insight", "")[:160] if message_perf else "لم تُسجَّل رسائل بعد"
    )

    objections = Counter()
    for r in proposals:
        obj = (r.get("objection") or "").strip()
        if obj:
            objections[obj] += 1
    top_objections = [f"{k}: {v}" for k, v in objections.most_common(3)]

    decisions_open = [d for d in decisions if d.get("status", "open").lower() == "open"]
    kfs_decisions = [
        f"[{d.get('decision', '?').upper()}] {d.get('subject', '?')}"
        for d in _within_week(decisions)
        if d.get("decision", "").lower() in {"kill", "fix", "scale"}
    ]

    target_next = "Pick ONE measurable target (e.g., ≥1 paid customer in sector X by next Monday)."

    sections = [
        f"# Weekly Growth War Room — {date.today().isoformat()}",
        "",
        f"_Generated: {_now_iso()}_",
        f"_Source: {private_ops}_",
        "",
        _section("ما تحرَّك", "What moved", _bullet(moved)),
        _section("ما توقَّف", "What stalled", _bullet(stalled)),
        _section("أفضل قطاع", "Best sector", _bullet([best_sector])),
        _section("أسوأ قطاع", "Worst sector", _bullet([worst_sector])),
        _section("أفضل قناة", "Best channel", _bullet([best_channel])),
        _section("أفضل رسالة", "Best message", _bullet([best_message])),
        _section("الاعتراضات الأشيع", "Top objections", _bullet(top_objections)),
        _section(
            "التجارب المغلقة",
            "Experiments closed",
            _bullet([f"{e.get('experiment_id','?')}: {e.get('result','')[:120]}" for e in week_exps]),
        ),
        _section("قرارات Kill / Fix / Scale", "Kill / Fix / Scale decisions", _bullet(kfs_decisions)),
        _section("هدف الأسبوع القادم", "Next-week target", _bullet([target_next])),
        "",
        "---",
        "",
        "_No guaranteed outcomes. All numbers observed-only. Update decisions.csv if you accept any KFS calls._",
    ]

    return "\n".join(sections)


def write_review(private_ops: Path) -> Path:
    target = private_ops / "founder" / "weekly_growth_review.md"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(generate(private_ops), encoding="utf-8")
    return target


def _empty_template(reason: str) -> str:
    return (
        f"# Weekly Growth War Room — {date.today().isoformat()}\n\n"
        f"_PRIVATE_OPS unavailable: {reason}_\n\n"
        "See docs/growth/WEEKLY_GROWTH_WAR_ROOM.md\n"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Dealix Weekly Growth Review.")
    parser.add_argument(
        "--private-ops",
        default=os.environ.get("PRIVATE_OPS") or os.environ.get("DEALIX_PRIVATE_OPS"),
    )
    parser.add_argument("--print", action="store_true")
    args = parser.parse_args(argv)

    if not args.private_ops:
        sys.stderr.write("[warn] PRIVATE_OPS not set — emitting template.\n")
        sys.stdout.write(_empty_template("not set"))
        return 0

    private_ops = Path(args.private_ops).expanduser().resolve()
    if not private_ops.exists():
        sys.stderr.write(f"[warn] PRIVATE_OPS missing: {private_ops}\n")
        sys.stdout.write(_empty_template(str(private_ops)))
        return 0

    out = write_review(private_ops)
    sys.stdout.write(f"[ok] wrote {out}\n")
    if args.print:
        sys.stdout.write(out.read_text(encoding="utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
