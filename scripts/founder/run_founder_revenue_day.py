#!/usr/bin/env python3
"""
Dealix Founder Revenue Day — daily orchestrator.

Produces all 10 required daily outputs:
  1. Target list status
  2. Verified prospects count
  3. Drafts generated
  4. Manual sends recommended
  5. Replies requiring action
  6. Deals pipeline movement
  7. Proposal candidates
  8. Follow-up queue
  9. Safety warnings
  10. Next 10 actions

Outputs:
  reports/founder/latest.md
  reports/founder/latest.json
  reports/command_room/index.html
  reports/command_room/data.json
  outbox/YYYY-MM-DD/ (drafts)

Usage:
    python scripts/founder/run_founder_revenue_day.py
    make founder-day
"""
from __future__ import annotations

import csv
import json
import os
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TODAY = date.today().isoformat()

PROSPECTS = ROOT / "ledgers" / "prospects.csv"
OUTREACH_LOG = ROOT / "ledgers" / "outreach_log.csv"
REPLY_LOG = ROOT / "ledgers" / "reply_log.csv"
PIPELINE = ROOT / "ledgers" / "deals_pipeline.csv"
OUTBOX = ROOT / "outbox" / TODAY
REPORTS = ROOT / "reports" / "founder"
COMMAND = ROOT / "reports" / "command_room"

for d in (OUTBOX, REPORTS, COMMAND):
    d.mkdir(parents=True, exist_ok=True)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []


def build_draft(row: dict[str, str]) -> str:
    company = (row.get("company_name") or "فريقكم").strip()
    sector = (row.get("sector") or "").strip()
    pain = (row.get("pain_hypothesis") or "").strip()
    product = (row.get("recommended_product") or "Diagnostic Sprint / Revenue Command Room OS").strip()
    angle = (row.get("dealix_angle") or "ترتيب المتابعة وتحويل الفرص إلى إيراد").strip()

    pain_line = f"\nالتحدي المبدئي: {pain}\n" if pain else ""

    return f"""السلام عليكم فريق {company}،

أنا سامي من Dealix.

نساعد الشركات في {sector or 'قطاعكم'} على تحويل فوضى المتابعة في واتساب، الإيميل، والفرص إلى نظام يومي واضح يعرف:
من يحتاج متابعة؟ ماذا نرسل؟ أين الفرص العالقة؟ وما القرار التالي؟
{pain_line}
التوصية المبدئية: {product}
زاوية البداية: {angle}

البداية عندنا تكون بتشخيص سريع من صفحة واحدة، بدون تغيير أنظمتكم الحالية، يوضح أين تضيع الفرص وكيف ممكن نبني Pilot خلال 7 أيام.

إذا مناسب، أرسل لكم نموذج مختصر.
وإذا غير مناسب، أوقف التواصل فورًا.

---
⚠️ مسودة — يحتاج مراجعة المؤسس قبل الإرسال
"""


def generate_drafts(prospects: list[dict[str, str]]) -> list[dict]:
    ready = [
        r for r in prospects
        if (r.get("verification_status") or "").lower() in {"ready_for_review", "approved_to_send"}
        and (r.get("owner_decision") or "").lower() not in {"reject", "do_not_contact"}
    ]
    drafts = []
    for idx, row in enumerate(ready[:25], 1):
        company = row.get("company_name") or f"company_{idx}"
        safe = "".join(ch if ch.isalnum() or ch in "-_" else "_" for ch in company)[:60]
        text = build_draft(row)
        path = OUTBOX / f"{idx:02d}_{safe}_draft.txt"
        path.write_text(text, encoding="utf-8")
        drafts.append({
            "rank": idx,
            "company": company,
            "sector": row.get("sector", ""),
            "product": row.get("recommended_product", ""),
            "status": row.get("verification_status", ""),
            "confidence": row.get("confidence", ""),
            "file": str(path.relative_to(ROOT)),
        })
    return drafts


def build_follow_up_queue(outreach: list[dict[str, str]]) -> list[dict]:
    today = date.today()
    queue = []
    for row in outreach:
        fu_date_str = row.get("follow_up_date") or row.get("next_followup_date") or ""
        if not fu_date_str:
            continue
        try:
            fu_date = date.fromisoformat(fu_date_str)
        except ValueError:
            continue
        if fu_date <= today + timedelta(days=2):
            queue.append({
                "company": row.get("company_name") or row.get("company", ""),
                "channel": row.get("channel", ""),
                "follow_up_date": fu_date_str,
                "overdue": fu_date < today,
                "days_until": (fu_date - today).days,
            })
    queue.sort(key=lambda x: x["follow_up_date"])
    return queue


def identify_proposal_candidates(prospects: list[dict[str, str]], replies: list[dict[str, str]]) -> list[dict]:
    warm = {
        (r.get("company_name") or "").strip().lower()
        for r in replies
        if (r.get("classification") or "").lower() in {"interested", "meeting_request"}
    }
    candidates = []
    for row in prospects:
        name_lower = (row.get("company_name") or "").strip().lower()
        if name_lower in warm or (row.get("verification_status") or "") == "approved_to_send":
            candidates.append({
                "company": row.get("company_name", ""),
                "product": row.get("recommended_product", ""),
                "confidence": row.get("confidence", ""),
            })
    return candidates[:5]


def pipeline_movers(pipeline: list[dict[str, str]]) -> list[dict]:
    recent_threshold = (date.today() - timedelta(days=7)).isoformat()
    movers = []
    for row in pipeline:
        updated = row.get("last_updated") or row.get("date") or ""
        if updated >= recent_threshold:
            movers.append({
                "company": row.get("company_name") or row.get("company", ""),
                "stage": row.get("stage") or row.get("status", ""),
                "value": row.get("deal_value_sar") or row.get("value", ""),
                "last_updated": updated,
            })
    return movers


def check_safety() -> dict:
    warnings = []
    if os.environ.get("EXTERNAL_SEND_ENABLED", "false").lower() == "true":
        if os.environ.get("OUTBOUND_MODE", "draft_only").lower() != "controlled_live":
            warnings.append("EXTERNAL_SEND_ENABLED=true but OUTBOUND_MODE is not controlled_live")
    if os.environ.get("WHATSAPP_SEND_ENABLED", "false").lower() == "true":
        if os.environ.get("WHATSAPP_ALLOW_LIVE_SEND", "false").lower() != "true":
            warnings.append("WHATSAPP_SEND_ENABLED=true but WHATSAPP_ALLOW_LIVE_SEND is not true")
    return {
        "external_send": os.environ.get("EXTERNAL_SEND_ENABLED", "false"),
        "outbound_mode": os.environ.get("OUTBOUND_MODE", "draft_only"),
        "whatsapp_live": os.environ.get("WHATSAPP_ALLOW_LIVE_SEND", "false"),
        "email_live": os.environ.get("EMAIL_SEND_ENABLED", "false"),
        "warnings": warnings,
        "gate": "PASS" if not warnings else "WARN",
    }


def write_command_room(data: dict) -> None:
    prospects = data["prospects"]
    ready = data["ready_for_review"]
    drafts_n = data["drafts_generated"]
    sends = data["recommended_manual_sends"]
    replies_n = data["replies_requiring_action"]
    pipeline_val = data.get("pipeline_total_sar", 0)
    proposals_n = len(data.get("proposal_candidates", []))
    safety = data["safety"]
    follow_ups = data.get("follow_up_queue", [])

    style = """\
body{font-family:Arial,sans-serif;margin:0;padding:24px;background:#0b1020;color:#eef2ff;direction:rtl}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:24px 0}
.card{background:#111936;padding:24px;border-radius:16px}
.card h3{margin:0 0 8px;color:#8899cc;font-size:13px;text-transform:uppercase;letter-spacing:1px}
.metric{font-size:36px;font-weight:bold;color:#ffffff}
.metric.warn{color:#ffaa44}
.metric.ok{color:#44dd88}
.metric.danger{color:#ff4466}
h1{color:#ffffff;font-size:24px}
.sub{color:#8899cc;font-size:13px}
table{width:100%;border-collapse:collapse;margin-top:12px}
th,td{padding:10px 12px;text-align:right;border-bottom:1px solid #1e2a4a;font-size:14px}
th{color:#8899cc;font-size:12px;text-transform:uppercase}
.badge{display:inline-block;padding:2px 10px;border-radius:12px;font-size:12px}
.badge.high{background:#1a3a1a;color:#44dd88}
.badge.medium{background:#2a2a1a;color:#ffcc44}
.badge.low{background:#1a1a2a;color:#8899cc}
.section{margin:32px 0}
"""

    safety_color = "ok" if safety["gate"] == "PASS" else "warn"
    def _fu_cell(r: dict) -> str:
        return "⚠️ متأخر" if r["overdue"] else f"{r['days_until']} يوم"

    follow_up_rows = "".join(
        f"<tr><td>{r['company']}</td><td>{r['follow_up_date']}</td>"
        f"<td>{_fu_cell(r)}</td></tr>"
        for r in follow_ups[:10]
    ) or "<tr><td colspan='3'>لا متابعات مجدولة للفترة القادمة</td></tr>"

    html = f"""<!doctype html>
<html lang="ar" dir="rtl">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Dealix Command Room — {TODAY}</title>
<style>{style}</style>
</head>
<body>
<h1>🎯 Dealix Founder Command Room</h1>
<p class="sub">{TODAY} — Draft-only mode — No auto-send</p>

<div class="grid">
  <div class="card"><h3>إجمالي العملاء المحتملين</h3><div class="metric">{prospects}</div></div>
  <div class="card"><h3>جاهز للمراجعة</h3><div class="metric">{ready}</div></div>
  <div class="card"><h3>مسودات اليوم</h3><div class="metric">{drafts_n}</div></div>
  <div class="card"><h3>إرسال يدوي موصى به</h3><div class="metric">{sends}</div></div>
  <div class="card"><h3>ردود تحتاج إجراء</h3><div class="metric {'warn' if replies_n > 0 else ''}">{replies_n}</div></div>
  <div class="card"><h3>قيمة الصفقات (SAR)</h3><div class="metric">{pipeline_val:,}</div></div>
  <div class="card"><h3>مرشحون للعروض</h3><div class="metric">{proposals_n}</div></div>
  <div class="card"><h3>بوابة الأمان</h3><div class="metric {safety_color}">{safety['gate']}</div></div>
</div>

<div class="section">
  <h2>📋 قائمة المتابعات القادمة</h2>
  <table>
    <thead><tr><th>الشركة</th><th>تاريخ المتابعة</th><th>الحالة</th></tr></thead>
    <tbody>{follow_up_rows}</tbody>
  </table>
</div>

<div class="section">
  <h2>🔒 وضع الأمان</h2>
  <p>الإرسال الخارجي: <strong>{safety['external_send']}</strong> |
     WhatsApp Live: <strong>{safety['whatsapp_live']}</strong> |
     وضع الإرسال: <strong>{safety['outbound_mode']}</strong></p>
  {''.join(f'<p style="color:#ffaa44">⚠️ {w}</p>' for w in safety['warnings']) or '<p style="color:#44dd88">✅ الإعدادات الافتراضية الآمنة مفعّلة</p>'}
</div>

<div class="section">
  <h2>⚡ الإجراءات العشرة التالية</h2>
  <ol>
{''.join(f"    <li>{a}</li>" for a in data.get("next_10_actions", []))}
  </ol>
</div>

<p class="sub">آخر تحديث: {TODAY} | جميع المسودات تحتاج مراجعة المؤسس قبل الإرسال</p>
</body>
</html>"""
    (COMMAND / "index.html").write_text(html, encoding="utf-8")
    (COMMAND / "style.css").write_text(style, encoding="utf-8")
    (COMMAND / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    prospects = read_csv(PROSPECTS)
    outreach = read_csv(OUTREACH_LOG)
    replies = read_csv(REPLY_LOG)
    pipeline = read_csv(PIPELINE)

    ready = [
        r for r in prospects
        if (r.get("verification_status") or "").lower() in {"ready_for_review", "approved_to_send"}
    ]

    pending_replies = [
        r for r in replies
        if (r.get("classification") or "").lower() in {"interested", "meeting_request", "need_more_info"}
        and r.get("next_action_date", "") >= date.today().isoformat()
    ]

    drafts = generate_drafts(prospects)
    follow_up = build_follow_up_queue(outreach)
    proposal_candidates = identify_proposal_candidates(prospects, replies)
    movers = pipeline_movers(pipeline)
    safety = check_safety()

    try:
        pipeline_total = sum(
            int((r.get("deal_value_sar") or r.get("value") or "0").replace(",", "").replace("SAR", "").strip())
            for r in pipeline if r.get("deal_value_sar") or r.get("value")
        )
    except Exception:
        pipeline_total = 0

    next_10 = [
        f"افتح outbox/{TODAY} وراجع أول {min(10, len(drafts))} مسودة",
        "تحقق من source_url لكل شركة قبل الإرسال",
        "أرسل يدويًا وسجّل الإرسال في outreach_log.csv",
        "راجع قائمة المتابعات المستحقة اليوم",
        f"اتصل أو راسل {len(pending_replies)} ردود تنتظر إجراء",
        "حدّث حالة الصفقات في deals_pipeline.csv",
        f"جهّز عرض أسعار لـ {len(proposal_candidates)} مرشح للعرض" if proposal_candidates else "أضف مزيدًا من العملاء المحتملين للـ ledger",
        "تحقق من بوابة الأمان قبل أي إرسال",
        "وثّق أي ردود جديدة في reply_log.csv",
        "خطّط إجراءات الغد بناءً على ردود اليوم",
    ]

    data = {
        "date": TODAY,
        "prospects_total": len(prospects),
        "ready_for_review": len(ready),
        "drafts_generated": len(drafts),
        "recommended_manual_sends": min(10, len(drafts)),
        "replies_requiring_action": len(pending_replies),
        "pipeline_total_sar": pipeline_total,
        "pipeline_movers": movers[:5],
        "proposal_candidates": proposal_candidates,
        "follow_up_queue": follow_up[:10],
        "safety": safety,
        "next_10_actions": next_10,
        "outbox": str(OUTBOX),
        "drafts": drafts,
    }

    (REPORTS / "latest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    md = f"""# Dealix Founder Revenue Day — {TODAY}

## ملخص تنفيذي

| المؤشر | القيمة |
|--------|--------|
| إجمالي العملاء المحتملين | {len(prospects)} |
| جاهز للمراجعة | {len(ready)} |
| مسودات اليوم | {len(drafts)} |
| إرسال يدوي موصى به | {min(10, len(drafts))} |
| ردود تحتاج إجراء | {len(pending_replies)} |
| مرشحون للعروض | {len(proposal_candidates)} |
| قيمة الصفقات | {pipeline_total:,} SAR |

## 🔒 وضع الأمان

- الإرسال الخارجي: `{safety['external_send']}`
- وضع الإرسال: `{safety['outbound_mode']}`
- WhatsApp Live: `{safety['whatsapp_live']}`
- بوابة الأمان: **{safety['gate']}**
{''.join(chr(10) + '⚠️ ' + w for w in safety['warnings'])}

## 📋 قائمة المتابعات القادمة

{"".join(f"- **{r['company']}** — {r['follow_up_date']} {'(متأخر ⚠️)' if r['overdue'] else ''}" + chr(10) for r in follow_up[:10]) or "لا متابعات مجدولة للفترة القادمة."}

## 🎯 مرشحون للعروض

{"".join(f"- {c['company']} — {c['product']}" + chr(10) for c in proposal_candidates) or "لا مرشحين للعروض حاليًا."}

## ⚡ الإجراءات العشرة التالية

{"".join(f"{i}. {a}" + chr(10) for i, a in enumerate(next_10, 1))}
## ملفات اليوم

- المسودات: `{OUTBOX}`
- التقرير JSON: `reports/founder/latest.json`
- غرفة القيادة: `reports/command_room/index.html`
"""
    (REPORTS / "latest.md").write_text(md, encoding="utf-8")
    write_command_room(data)

    print("FOUNDER_REVENUE_DAY_READY")
    print(f"NO_AUTO_EXTERNAL_SEND_GATE={safety['gate']}")
    print(f"Prospects:    {len(prospects)}")
    print(f"Ready:        {len(ready)}")
    print(f"Drafts:       {len(drafts)}")
    print(f"Follow-ups:   {len(follow_up)} due soon")
    print(f"Proposals:    {len(proposal_candidates)} candidates")
    print(f"Outbox:       {OUTBOX}")
    print(f"Report:       {REPORTS / 'latest.md'}")
    print(f"Command room: {COMMAND / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
