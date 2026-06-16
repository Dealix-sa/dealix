#!/usr/bin/env python3
"""Dealix Command Room — offline founder dashboard for daily outreach.

Doctrine-safe by design:
  * Read-only. Reads the local outreach log + today's generated drafts and
    renders a single self-contained HTML file. It never sends anything.
  * Stdlib only — no third-party dependencies, no network, no external assets.
  * The rendered HTML opens directly in any browser (file://), works offline.

Usage:
    python3 scripts/dealix_command_room.py
    python3 scripts/dealix_command_room.py --log data/outreach/outreach_log.csv
    python3 scripts/dealix_command_room.py --dry-run

Input:
    data/outreach/outreach_log.csv            (founder-maintained; falls back
    data/outreach/outreach_log.template.csv    to the tracked template)

Output:
    reports/command_room/index.html           (self-contained dashboard)
"""
from __future__ import annotations

import argparse
import csv
import html
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = REPO_ROOT / "data" / "outreach" / "outreach_log.csv"
TEMPLATE_LOG = REPO_ROOT / "data" / "outreach" / "outreach_log.template.csv"
OUTREACH_REPORTS = REPO_ROOT / "reports" / "outreach"
OUTBOUND_DIR = REPO_ROOT / "data" / "outbound"
OUT_HTML = REPO_ROOT / "reports" / "command_room" / "index.html"

# Controlled Live Outbound CSV paths
OUTBOUND_CONTACTS = OUTBOUND_DIR / "contacts.csv"
OUTBOUND_MESSAGES = OUTBOUND_DIR / "messages.csv"
OUTBOUND_EVENTS = OUTBOUND_DIR / "events.csv"
OUTBOUND_PIPELINE = OUTBOUND_DIR / "deals_pipeline.csv"

# Dealix brand colors (see brand/brand-colors.css and the visual identity guide).
PRIMARY = "#1B5E3B"
ACCENT = "#C9A94C"
DARK = "#0D2818"

STATUSES = ("drafted", "sent", "reply", "meeting", "won", "lost")
FUNNEL = ("drafted", "sent", "reply", "meeting", "won")

STATUS_LABELS: dict[str, str] = {
    "drafted": "مسودة / Drafted",
    "sent": "أُرسلت / Sent",
    "reply": "رد / Reply",
    "meeting": "اجتماع / Meeting",
    "won": "صفقة / Won",
    "lost": "خسارة / Lost",
}

SECTOR_LABELS: dict[str, str] = {
    "real_estate": "العقار / Real Estate",
    "clinic": "العيادات / Clinics",
    "logistics": "اللوجستيات / Logistics",
    "training": "التدريب / Training",
    "marketing_agency": "وكالات التسويق / Agencies",
    "b2b_services": "خدمات الأعمال / B2B",
}


def resolve_log(log: Path) -> tuple[Path, bool]:
    """Return the log path to read and whether it is the fallback template."""
    if log.exists():
        return log, False
    return TEMPLATE_LOG, True


def read_log(log: Path) -> list[dict[str, str]]:
    """Read the outreach log CSV, skipping comment lines (starting with #)."""
    rows: list[dict[str, str]] = []
    with log.open(encoding="utf-8") as fh:
        reader = csv.DictReader(r for r in fh if not r.lstrip().startswith("#"))
        for row in reader:
            clean = {(k or "").strip(): (v or "").strip() for k, v in row.items()}
            if not clean.get("company") or not clean.get("status"):
                continue
            clean["status"] = clean["status"].lower()
            clean["replied"] = clean.get("replied", "").lower()
            rows.append(clean)
    return rows


def latest_drafts_dir() -> Path | None:
    """Return the most recent reports/outreach/<date>/ folder, if any."""
    if not OUTREACH_REPORTS.exists():
        return None
    dated = sorted(
        (p for p in OUTREACH_REPORTS.iterdir() if p.is_dir()),
        key=lambda p: p.name,
    )
    return dated[-1] if dated else None


def count_ready_drafts(drafts_dir: Path | None) -> int:
    """Count generated draft emails (markdown files, excluding the digest)."""
    if drafts_dir is None:
        return 0
    return sum(
        1
        for p in drafts_dir.glob("*.md")
        if not p.name.startswith("_")
    )


def read_csv_if_exists(path: Path) -> list[dict[str, str]]:
    """Read a CSV file if it exists, otherwise return empty list."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def compute_outbound_stats() -> dict[str, object]:
    """Compute stats from the controlled live outbound CSV store."""
    messages = read_csv_if_exists(OUTBOUND_MESSAGES)
    events = read_csv_if_exists(OUTBOUND_EVENTS)
    pipeline = read_csv_if_exists(OUTBOUND_PIPELINE)

    stats: dict[str, int] = {
        "queued": 0,
        "sent": 0,
        "failed": 0,
        "replied": 0,
        "opted_out": 0,
        "draft": 0,
        "approved": 0,
    }
    for msg in messages:
        status = (msg.get("status") or "").lower()
        if status in stats:
            stats[status] += 1

    for event in events:
        event_type = (event.get("event_type") or "").lower()
        if event_type == "reply":
            stats["replied"] += 1
        elif event_type == "opt_out":
            stats["opted_out"] += 1

    meetings = sum(1 for p in pipeline if (p.get("stage") or "").lower() == "meeting")
    proposals = sum(1 for p in pipeline if (p.get("stage") or "").lower() == "proposal")
    next_actions = [
        {
            "company": p.get("company_name", "—"),
            "stage": p.get("stage", "—"),
            "next_action": p.get("next_action", "—"),
            "next_action_at": p.get("next_action_at", "—"),
        }
        for p in pipeline
        if p.get("next_action")
    ]

    return {
        **stats,
        "meetings": meetings,
        "proposals": proposals,
        "next_actions": next_actions,
        "limits": {
            "email_daily_limit": 25,
            "email_sent_today": stats["sent"],
            "email_remaining": max(0, 25 - stats["sent"]),
            "whatsapp_daily_limit": 10,
            "whatsapp_sent_today": 0,  # tracked separately when live
            "whatsapp_remaining": 10,
        },
    }


def compute_kpis(rows: list[dict[str, str]], ready_drafts: int) -> dict[str, object]:
    """Compute the Command Room KPIs from log rows + today's ready drafts + outbound store."""
    by_status: dict[str, int] = dict.fromkeys(STATUSES, 0)
    by_sector: dict[str, dict[str, int]] = {}
    for row in rows:
        status = row["status"]
        if status in by_status:
            by_status[status] += 1
        sector = row.get("sector") or "unknown"
        bucket = by_sector.setdefault(sector, {"total": 0, "reply": 0, "won": 0})
        bucket["total"] += 1
        if status in ("reply", "meeting", "won"):
            bucket["reply"] += 1
        if status == "won":
            bucket["won"] += 1

    sent = by_status["sent"] + by_status["reply"] + by_status["meeting"] + by_status["won"] + by_status["lost"]
    replies = by_status["reply"] + by_status["meeting"] + by_status["won"]
    reply_rate = round((replies / sent) * 100, 1) if sent else 0.0

    funnel = {
        "drafted": len(rows),
        "sent": sent,
        "reply": replies,
        "meeting": by_status["meeting"] + by_status["won"],
        "won": by_status["won"],
    }

    outbound = compute_outbound_stats()

    return {
        "ready_drafts": ready_drafts,
        "total": len(rows),
        "sent": sent,
        "replies": replies,
        "meetings": by_status["meeting"] + by_status["won"],
        "won": by_status["won"],
        "lost": by_status["lost"],
        "reply_rate": reply_rate,
        "by_status": by_status,
        "by_sector": by_sector,
        "funnel": funnel,
        "outbound": outbound,
    }


def _kpi_card(label: str, value: object, color: str) -> str:
    return (
        '<div class="card">'
        f'<div class="kpi" style="color:{color}">{html.escape(str(value))}</div>'
        f'<div class="kpi-label">{html.escape(label)}</div>'
        "</div>"
    )


def _funnel_rows(funnel: dict[str, int]) -> str:
    top = funnel.get("drafted", 0) or 1
    out: list[str] = []
    for stage in FUNNEL:
        count = funnel.get(stage, 0)
        pct = round((count / top) * 100)
        out.append(
            '<div class="funnel-row">'
            f'<span class="funnel-name">{html.escape(STATUS_LABELS[stage])}</span>'
            f'<span class="funnel-bar"><span class="funnel-fill" style="width:{pct}%"></span></span>'
            f'<span class="funnel-count">{count}</span>'
            "</div>"
        )
    return "\n".join(out)


def _sector_rows(by_sector: dict[str, dict[str, int]]) -> str:
    if not by_sector:
        return '<tr><td colspan="4" class="muted">لا توجد بيانات بعد / No data yet</td></tr>'
    out: list[str] = []
    for sector, bucket in sorted(by_sector.items(), key=lambda kv: kv[1]["total"], reverse=True):
        label = SECTOR_LABELS.get(sector, sector)
        total = bucket["total"]
        replies = bucket["reply"]
        won = bucket["won"]
        rate = round((replies / total) * 100) if total else 0
        out.append(
            "<tr>"
            f"<td>{html.escape(label)}</td>"
            f"<td>{total}</td>"
            f"<td>{replies} ({rate}%)</td>"
            f"<td>{won}</td>"
            "</tr>"
        )
    return "\n".join(out)


def _outbound_status_cards(outbound: dict[str, object]) -> str:
    cards = [
        ("في الطابور / Queued", outbound.get("queued", 0), ACCENT),
        ("أُرسلت / Sent", outbound.get("sent", 0), PRIMARY),
        ("فاشلة / Failed", outbound.get("failed", 0), "#c44"),
        ("ردود / Replies", outbound.get("replied", 0), ACCENT),
        ("إلغاء اشتراك / Opt-outs", outbound.get("opted_out", 0), "#c44"),
        ("اجتماعات / Meetings", outbound.get("meetings", 0), PRIMARY),
        ("عروض / Proposals", outbound.get("proposals", 0), PRIMARY),
    ]
    return "\n".join(_kpi_card(label, value, color) for label, value, color in cards)


def _limits_rows(limits: dict[str, int]) -> str:
    email_pct = round((limits["email_sent_today"] / limits["email_daily_limit"]) * 100) if limits["email_daily_limit"] else 0
    wa_pct = round((limits["whatsapp_sent_today"] / limits["whatsapp_daily_limit"]) * 100) if limits["whatsapp_daily_limit"] else 0
    return f"""
    <div class="limit-row">
      <span>Email</span>
      <span class="limit-bar"><span class="limit-fill" style="width:{email_pct}%"></span></span>
      <span>{limits['email_sent_today']} / {limits['email_daily_limit']} ({limits['email_remaining']} remaining)</span>
    </div>
    <div class="limit-row">
      <span>WhatsApp</span>
      <span class="limit-bar"><span class="limit-fill" style="width:{wa_pct}%"></span></span>
      <span>{limits['whatsapp_sent_today']} / {limits['whatsapp_daily_limit']} ({limits['whatsapp_remaining']} remaining)</span>
    </div>
    """


def _next_action_rows(actions: list[dict[str, str]]) -> str:
    if not actions:
        return '<tr><td colspan="4" class="muted">لا توجد إجراءات قادمة / No upcoming actions</td></tr>'
    out: list[str] = []
    for action in actions[:10]:
        out.append(
            "<tr>"
            f"<td>{html.escape(str(action.get('company', '—')))}</td>"
            f"<td>{html.escape(str(action.get('stage', '—')))}</td>"
            f"<td>{html.escape(str(action.get('next_action', '—')))}</td>"
            f"<td>{html.escape(str(action.get('next_action_at', '—')))}</td>"
            "</tr>"
        )
    return "\n".join(out)


def render_html(kpis: dict[str, object], source_note: str) -> str:
    """Render the self-contained Command Room HTML page."""
    today = date.today().isoformat()
    by_sector = kpis["by_sector"]  # type: ignore[assignment]
    funnel = kpis["funnel"]  # type: ignore[assignment]
    outbound = kpis["outbound"]  # type: ignore[assignment]
    limits = outbound.get("limits", {})  # type: ignore[assignment]

    cards = "\n".join([
        _kpi_card("مسودات جاهزة اليوم / Ready today", kpis["ready_drafts"], ACCENT),
        _kpi_card("إجمالي السجل / Total logged", kpis["total"], PRIMARY),
        _kpi_card("أُرسلت / Sent", kpis["sent"], PRIMARY),
        _kpi_card("ردود / Replies", kpis["replies"], ACCENT),
        _kpi_card("اجتماعات / Meetings", kpis["meetings"], ACCENT),
        _kpi_card("صفقات / Won", kpis["won"], PRIMARY),
        _kpi_card("نسبة الرد / Reply rate", f"{kpis['reply_rate']}%", ACCENT),
    ])

    return f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dealix — غرفة القيادة / Command Room</title>
<style>
  :root {{
    --primary: {PRIMARY};
    --accent: {ACCENT};
    --dark: {DARK};
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    font-family: "Tajawal", "Noto Kufi Arabic", "Segoe UI", system-ui, sans-serif;
    background: var(--dark);
    color: #f4f6f4;
    line-height: 1.6;
  }}
  header {{
    background: linear-gradient(135deg, var(--primary), var(--dark));
    border-bottom: 3px solid var(--accent);
    padding: 28px 20px;
  }}
  header h1 {{ margin: 0; font-size: 1.6rem; }}
  header .sub {{ color: var(--accent); margin-top: 6px; font-size: .95rem; }}
  main {{ max-width: 960px; margin: 0 auto; padding: 20px; }}
  .grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 14px;
    margin-bottom: 28px;
  }}
  .card {{
    background: #11331f;
    border: 1px solid rgba(201,169,76,.25);
    border-radius: 14px;
    padding: 18px;
    text-align: center;
  }}
  .kpi {{ font-size: 2.1rem; font-weight: 800; }}
  .kpi-label {{ font-size: .85rem; color: #b9c7bd; margin-top: 4px; }}
  section {{
    background: #11331f;
    border: 1px solid rgba(201,169,76,.18);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 22px;
  }}
  section h2 {{
    margin: 0 0 16px;
    font-size: 1.15rem;
    color: var(--accent);
    border-bottom: 1px solid rgba(201,169,76,.2);
    padding-bottom: 8px;
  }}
  .funnel-row {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
  .funnel-name {{ flex: 0 0 38%; font-size: .9rem; }}
  .funnel-bar {{ flex: 1; background: rgba(255,255,255,.08); border-radius: 8px; height: 18px; overflow: hidden; }}
  .funnel-fill {{ display: block; height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent)); }}
  .funnel-count {{ flex: 0 0 36px; text-align: left; font-weight: 700; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 10px 8px; text-align: right; border-bottom: 1px solid rgba(255,255,255,.07); font-size: .9rem; }}
  th {{ color: var(--accent); font-weight: 700; }}
  .muted {{ color: #8aa192; text-align: center; }}
  footer {{ text-align: center; padding: 18px; color: #7e9486; font-size: .8rem; }}
  .note {{ background: rgba(201,169,76,.1); border: 1px solid rgba(201,169,76,.3);
           border-radius: 10px; padding: 12px 14px; font-size: .85rem; margin-bottom: 22px; }}
  .limit-row {{ display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }}
  .limit-row > span:first-child {{ flex: 0 0 80px; font-size: .9rem; }}
  .limit-bar {{ flex: 1; background: rgba(255,255,255,.08); border-radius: 8px; height: 18px; overflow: hidden; max-width: 320px; }}
  .limit-fill {{ display: block; height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent)); }}
  .limit-row > span:last-child {{ flex: 0 0 160px; font-size: .85rem; color: #b9c7bd; text-align: left; }}
  @media (max-width: 520px) {{
    .funnel-name {{ flex: 0 0 46%; font-size: .8rem; }}
    header h1 {{ font-size: 1.3rem; }}
  }}
</style>
</head>
<body>
<header>
  <h1>غرفة القيادة — Dealix Command Room</h1>
  <div class="sub">لوحة المتابعة اليومية للاستهداف · Daily outreach dashboard · {today}</div>
</header>
<main>
  <div class="note">المصدر / Source: {html.escape(source_note)} — هذه اللوحة للقراءة فقط ولا ترسل أي شيء. Read-only, sends nothing.</div>

  <div class="grid">
    {cards}
  </div>

  <section>
    <h2>القمع / Funnel</h2>
    {_funnel_rows(funnel)}
  </section>

  <section>
    <h2>حسب القطاع / By sector</h2>
    <table>
      <thead>
        <tr><th>القطاع / Sector</th><th>إجمالي / Total</th><th>ردود / Replies</th><th>صفقات / Won</th></tr>
      </thead>
      <tbody>
        {_sector_rows(by_sector)}
      </tbody>
    </table>
  </section>

  <section>
    <h2>الإرسال الخارجي المحكوم / Controlled Outbound</h2>
    <div class="grid">
      {_outbound_status_cards(outbound)}
    </div>
  </section>

  <section>
    <h2>حدود الإرسال اليومية / Daily Limits</h2>
    {_limits_rows(limits)}
  </section>

  <section>
    <h2>الإجراءات التالية / Next Actions</h2>
    <table>
      <thead>
        <tr><th>الشركة / Company</th><th>المرحلة / Stage</th><th>الإجراء / Action</th><th>الموعد / Due</th></tr>
      </thead>
      <tbody>
        {_next_action_rows(outbound.get("next_actions", []))}
      </tbody>
    </table>
  </section>
</main>
<footer>
  Dealix — نظام تشغيل الإيرادات. كل المسودات تنتظر مراجعتك. لا إرسال تلقائي.<br>
  Generated offline · {today}
</footer>
</body>
</html>
"""


def print_summary(kpis: dict[str, object], out_path: Path) -> None:
    """Print a short bilingual-leaning Arabic summary to stdout."""
    outbound = kpis.get("outbound", {})
    print("غرفة القيادة — Dealix Command Room")
    print(f"  مسودات جاهزة اليوم: {kpis['ready_drafts']}")
    print(f"  إجمالي السجل:        {kpis['total']}")
    print(f"  أُرسلت:               {kpis['sent']}")
    print(f"  ردود:                 {kpis['replies']}")
    print(f"  اجتماعات:             {kpis['meetings']}")
    print(f"  صفقات (won):          {kpis['won']}")
    print(f"  نسبة الرد:            {kpis['reply_rate']}%")
    print("  — Controlled Outbound —")
    print(f"    queued:    {outbound.get('queued', 0)}")
    print(f"    sent:      {outbound.get('sent', 0)}")
    print(f"    failed:    {outbound.get('failed', 0)}")
    print(f"    replies:   {outbound.get('replied', 0)}")
    print(f"    opt-outs:  {outbound.get('opted_out', 0)}")
    print(f"    meetings:  {outbound.get('meetings', 0)}")
    print(f"    proposals: {outbound.get('proposals', 0)}")
    print(f"  اللوحة: {out_path}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Dealix Command Room — offline outreach dashboard")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG, help="Path to the outreach log CSV")
    ap.add_argument("--dry-run", action="store_true", help="Compute and print KPIs without writing HTML")
    args = ap.parse_args()

    log_path, used_template = resolve_log(args.log)
    if used_template:
        print(f"[تنبيه] لا يوجد سجل حقيقي ({args.log}) — استخدمت القالب: {log_path}")

    rows = read_log(log_path)
    drafts_dir = latest_drafts_dir()
    ready = count_ready_drafts(drafts_dir)
    kpis = compute_kpis(rows, ready)

    source_note = f"{log_path.name}" + (" (template)" if used_template else "")

    if args.dry_run:
        print("[dry-run] لن تُكتب اللوحة. ملخص المؤشرات:")
        print_summary(kpis, OUT_HTML)
        return 0

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(render_html(kpis, source_note), encoding="utf-8")
    print_summary(kpis, OUT_HTML)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
