#!/usr/bin/env python3
from pathlib import Path
import csv
import datetime as dt
import html

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reports" / "command_room"
OUT.mkdir(parents=True, exist_ok=True)

def read(path):
    p = ROOT / path
    if not p.exists():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

prospects = read("ledgers/prospects.csv")
outreach = read("ledgers/outreach_log.csv")
replies = read("ledgers/reply_log.csv")
deals = read("ledgers/deals_pipeline.csv")

ready = [r for r in prospects if r.get("email") and r.get("source_url")]
sectors = {}
for r in prospects:
    sectors[r.get("sector") or "unknown"] = sectors.get(r.get("sector") or "unknown", 0) + 1

cards = [
    ("Prospects", len(prospects)),
    ("Ready to contact", len(ready)),
    ("Outreach log", len(outreach)),
    ("Replies", len(replies)),
    ("Deals", len(deals)),
]

cards_html = "".join(f"<div class='card'><b>{html.escape(k)}</b><span>{v}</span></div>" for k, v in cards)
sector_html = "".join(f"<li>{html.escape(k)}: {v}</li>" for k, v in sectors.items())

page = f"""<!doctype html>
<html lang="ar" dir="rtl">
<meta charset="utf-8">
<title>Dealix Founder Command Room</title>
<style>
body{{font-family:Arial;margin:32px;background:#0b1020;color:#f8fafc}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}}
.card{{background:#111827;border:1px solid #334155;border-radius:18px;padding:20px}}
.card span{{display:block;font-size:32px;margin-top:12px;color:#38bdf8}}
</style>
<h1>Dealix Founder Command Room</h1>
<p>{dt.datetime.now().isoformat()}</p>
<div class="grid">{cards_html}</div>
<h2>Sector Breakdown</h2>
<ul>{sector_html}</ul>
<h2>Next Actions</h2>
<ol>
<li>راجع outbox اليوم.</li>
<li>أكد source_url.</li>
<li>أرسل يدويًا.</li>
<li>حدّث ledgers.</li>
</ol>
</html>"""

(OUT / "index.html").write_text(page, encoding="utf-8")
print(OUT / "index.html")
