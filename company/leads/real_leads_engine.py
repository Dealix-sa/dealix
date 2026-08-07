#!/usr/bin/env python3
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
TODAY = dt.date.today().isoformat()
OUT = ROOT / "company" / "runtime" / "places" / TODAY
OUT.mkdir(parents=True, exist_ok=True)

SEGMENTS = {
    "clinics": {
        "name_ar": "عيادات ومراكز طبية",
        "queries": [
            "عيادات أسنان في الرياض",
            "عيادات تجميل في الرياض",
            "عيادات جلدية في الرياض",
            "مراكز علاج طبيعي في الرياض",
        ],
        "pain": "الاستفسارات والحجوزات والتقييمات تحتاج متابعة منظمة",
        "offer": "WhatsApp Revenue OS + Review Intelligence OS",
    },
    "training_centers": {
        "name_ar": "مراكز تدريب",
        "queries": [
            "مراكز تدريب في الرياض",
            "معاهد تدريب في الرياض",
            "دورات تدريبية في الرياض",
        ],
        "pain": "استفسارات الدورات تحتاج تسجيل ومتابعة وتقرير واضح",
        "offer": "Growth Engine OS",
    },
    "agencies": {
        "name_ar": "وكالات تسويق",
        "queries": [
            "وكالات تسويق في الرياض",
            "شركات تسويق رقمي في الرياض",
            "وكالة دعاية واعلان في الرياض",
        ],
        "pain": "تقارير العملاء والمهام والتسليم تحتاج Command Center",
        "offer": "Client Command Center OS",
    },
    "restaurants": {
        "name_ar": "مطاعم وكافيهات",
        "queries": [
            "مطاعم في الرياض",
            "كافيهات في الرياض",
            "مطاعم عائلية في الرياض",
        ],
        "pain": "التقييمات والشكاوى تحتاج Review Intelligence وقرارات تشغيلية",
        "offer": "Review Intelligence OS",
    },
    "real_estate": {
        "name_ar": "عقار وخدمات B2B",
        "queries": [
            "مكاتب عقار في الرياض",
            "شركات عقار في الرياض",
            "شركات خدمات اعمال في الرياض",
        ],
        "pain": "العملاء والعروض يحتاجون pipeline ومتابعة منظمة",
        "offer": "Sales Pipeline OS",
    },
}

FIELDS = [
    "date",
    "segment",
    "segment_name_ar",
    "company_name",
    "phone",
    "website",
    "address",
    "rating",
    "user_rating_count",
    "google_maps_uri",
    "source_query",
    "pain_angle",
    "recommended_offer",
    "priority_score",
    "next_action",
]

def text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return str(value.get("text") or value.get("languageCode") or "")
    return str(value)

def score(row: dict[str, str]) -> int:
    value = 45
    if row.get("phone"):
        value += 20
    if row.get("website"):
        value += 10
    try:
        count = int(float(row.get("user_rating_count") or 0))
        if count >= 100:
            value += 15
        elif count >= 30:
            value += 8
    except (ValueError, TypeError):
        pass
    try:
        rating = float(row.get("rating") or 0)
        if 0 < rating < 4.0:
            value += 10
        elif rating >= 4.5:
            value += 5
    except (ValueError, TypeError):
        pass
    return min(value, 100)

def places_search(query: str, limit: int = 8) -> list[dict[str, Any]]:
    key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        return []

    url = "https://places.googleapis.com/v1/places:searchText"
    body = json.dumps(
        {"textQuery": query, "languageCode": "ar", "regionCode": "SA"},
        ensure_ascii=False,
    ).encode("utf-8")

    field_mask = ",".join([
        "places.displayName",
        "places.formattedAddress",
        "places.nationalPhoneNumber",
        "places.internationalPhoneNumber",
        "places.websiteUri",
        "places.rating",
        "places.userRatingCount",
        "places.googleMapsUri",
        "places.businessStatus",
    ])

    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": key,
            "X-Goog-FieldMask": field_mask,
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print("Google Places HTTP error:", exc.read().decode("utf-8", errors="ignore"))
        return []
    except Exception as exc:
        print("Google Places error:", exc)
        return []

    return payload.get("places", [])[:limit]

def build_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    seen: set[str] = set()

    for segment, cfg in SEGMENTS.items():
        for query in cfg["queries"]:
            for place in places_search(query, limit=8):
                name = text(place.get("displayName"))
                if not name:
                    continue

                key = name.strip().lower()
                if key in seen:
                    continue
                seen.add(key)

                row = {
                    "date": TODAY,
                    "segment": segment,
                    "segment_name_ar": cfg["name_ar"],
                    "company_name": name,
                    "phone": text(place.get("internationalPhoneNumber") or place.get("nationalPhoneNumber")),
                    "website": text(place.get("websiteUri")),
                    "address": text(place.get("formattedAddress")),
                    "rating": text(place.get("rating")),
                    "user_rating_count": text(place.get("userRatingCount")),
                    "google_maps_uri": text(place.get("googleMapsUri")),
                    "source_query": query,
                    "pain_angle": cfg["pain"],
                    "recommended_offer": cfg["offer"],
                    "priority_score": "0",
                    "next_action": "review_and_send_manually",
                }
                row["priority_score"] = str(score(row))
                rows.append(row)

    rows.sort(key=lambda r: int(r["priority_score"]), reverse=True)
    return rows

def write_outputs(rows: list[dict[str, str]]) -> None:
    csv_path = OUT / "real_leads.csv"
    with csv_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    report = [
        "# Dealix Real Leads Report",
        "",
        f"Date: {TODAY}",
        f"Real leads found: {len(rows)}",
        "",
        "| # | Company | Segment | Score | Phone | Website | Offer |",
        "|---:|---|---|---:|---|---|---|",
    ]

    for i, r in enumerate(rows[:30], start=1):
        report.append(
            f"| {i} | {r['company_name']} | {r['segment_name_ar']} | {r['priority_score']} | {r['phone']} | {r['website']} | {r['recommended_offer']} |"
        )

    (OUT / "REAL_LEADS_REPORT.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"Real leads CSV: {csv_path}")
    print(f"Real leads report: {OUT / 'REAL_LEADS_REPORT.md'}")
    print(f"Count: {len(rows)}")

def main() -> None:
    rows = build_rows()
    if not rows:
        print("No real leads returned. Make sure GOOGLE_MAPS_API_KEY is available in this shell or GitHub Actions.")
    write_outputs(rows)

if __name__ == "__main__":
    main()
