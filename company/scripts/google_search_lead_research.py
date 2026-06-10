#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "company" / "lead_research"

SEGMENTS = {
    "clinics": ["عيادات أسنان الرياض واتساب", "عيادات تجميل الرياض واتساب"],
    "training_centers": ["مراكز تدريب الرياض دورات تسجيل واتساب"],
    "agencies": ["وكالات تسويق الرياض", "شركات تسويق رقمي الرياض"],
    "restaurants": ["مطاعم الرياض تقييمات", "كافيهات الرياض تقييمات"],
    "real_estate": ["مكاتب عقار الرياض واتساب", "شركات عقار الرياض"],
}

def search(query: str, limit: int = 5) -> list[dict]:
    key = os.getenv("GOOGLE_SEARCH_API_KEY")
    cx = os.getenv("GOOGLE_SEARCH_CX")
    if not key or not cx:
        return []

    url = "https://www.googleapis.com/customsearch/v1?" + urllib.parse.urlencode({
        "key": key,
        "cx": cx,
        "q": query,
        "num": min(limit, 10),
    })

    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"Search failed: {query}: {e}")
        return []

    rows = []
    for item in data.get("items", []):
        rows.append({
            "date": dt.date.today().isoformat(),
            "query": query,
            "title": item.get("title", ""),
            "link": item.get("link", ""),
            "snippet": item.get("snippet", ""),
            "source": "google_custom_search",
        })
    return rows

def main() -> None:
    out = OUT_ROOT / dt.date.today().isoformat()
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    for segment, queries in SEGMENTS.items():
        for q in queries:
            found = search(q, 5)
            if not found:
                found = [{
                    "date": dt.date.today().isoformat(),
                    "query": q,
                    "title": f"Research Target {segment}",
                    "link": "",
                    "snippet": "Manual research needed.",
                    "source": "placeholder",
                }]
            for r in found:
                r["segment"] = segment
                r["pain_angle"] = {
                    "clinics": "استفسارات وحجوزات وتقييمات تحتاج متابعة منظمة",
                    "training_centers": "leads الدورات تحتاج تسجيل ومتابعة وتقرير",
                    "agencies": "تقارير العملاء والمهام تحتاج Command Center",
                    "restaurants": "التقييمات والشكاوى تحتاج Review Intelligence",
                    "real_estate": "leads والعروض العقارية تحتاج pipeline ومتابعة",
                }.get(segment, "تحتاج نظام تشغيل")
                r["recommended_offer"] = {
                    "clinics": "WhatsApp Revenue OS + Review Intelligence OS",
                    "training_centers": "Growth Engine OS",
                    "agencies": "Client Command Center OS",
                    "restaurants": "Review Intelligence OS",
                    "real_estate": "Sales Pipeline OS",
                }.get(segment, "Diagnostic Sprint")
                rows.append(r)

    csv_path = out / "web_lead_research.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        fields = ["date", "segment", "query", "title", "link", "snippet", "source", "pain_angle", "recommended_offer"]
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    md = ["# Dealix Web Lead Research", "", f"Date: {dt.date.today().isoformat()}", ""]
    md.append("| # | Segment | Target | Pain | Offer | Link |")
    md.append("|---:|---|---|---|---|---|")
    for i, r in enumerate(rows[:30], 1):
        md.append(f"| {i} | {r['segment']} | {r['title']} | {r['pain_angle']} | {r['recommended_offer']} | {r['link']} |")

    md_path = out / "WEB_LEAD_RESEARCH.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")

    print(csv_path)
    print(md_path)

if __name__ == "__main__":
    main()
