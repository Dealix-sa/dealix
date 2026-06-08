#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any

try:
    import yaml
except Exception as exc:
    raise SystemExit("Install dependency: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[2]
OUT_ROOT = ROOT / "founder_os" / "output"
CONFIG = ROOT / "founder_os" / "config" / "segments.yaml"
LADDER = ROOT / "founder_os" / "config" / "service_ladder.yaml"
TEMPLATES = ROOT / "founder_os" / "templates" / "outreach.yaml"
MANUAL = ROOT / "founder_os" / "manual_import"

def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def slug(v: str) -> str:
    v = (v or "").strip().lower()
    return re.sub(r"[^a-z0-9\u0600-\u06FF]+", "-", v).strip("-") or "target"

def render(t: str, d: dict[str, Any]) -> str:
    for k, v in d.items():
        t = t.replace("{{" + k + "}}", str(v or ""))
    return t

def today_dir() -> Path:
    p = OUT_ROOT / dt.date.today().isoformat()
    p.mkdir(parents=True, exist_ok=True)
    return p

def google_text_search(query: str, limit: int) -> list[dict[str, Any]]:
    key = os.getenv("GOOGLE_MAPS_API_KEY") or os.getenv("GOOGLE_SEARCH_API_KEY")
    if not key:
        return []

    url = "https://places.googleapis.com/v1/places:searchText"
    body = json.dumps({"textQuery": query, "languageCode": "ar", "regionCode": "SA"}, ensure_ascii=False).encode("utf-8")
    field_mask = ",".join([
        "places.displayName",
        "places.formattedAddress",
        "places.internationalPhoneNumber",
        "places.nationalPhoneNumber",
        "places.websiteUri",
        "places.rating",
        "places.userRatingCount",
        "places.googleMapsUri",
        "places.businessStatus"
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
    except urllib.error.HTTPError as e:
        sys.stderr.write("Google Places HTTP error: " + e.read().decode("utf-8", errors="ignore") + "\n")
        return []
    except Exception as e:
        sys.stderr.write(f"Google Places error: {e}\n")
        return []

    rows = []
    for p in payload.get("places", [])[:limit]:
        name = p.get("displayName", {})
        rows.append({
            "company_name": name.get("text", "") if isinstance(name, dict) else str(name),
            "phone": p.get("internationalPhoneNumber") or p.get("nationalPhoneNumber") or "",
            "website": p.get("websiteUri", ""),
            "address": p.get("formattedAddress", ""),
            "rating": p.get("rating", ""),
            "user_rating_count": p.get("userRatingCount", ""),
            "google_maps_uri": p.get("googleMapsUri", ""),
            "source": "google_places",
        })
    return rows

def manual_rows() -> list[dict[str, Any]]:
    rows = []
    if not MANUAL.exists():
        return rows
    for path in MANUAL.glob("*.csv"):
        with path.open("r", encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                r["source"] = f"manual:{path.name}"
                rows.append(r)
    return rows

def score(row: dict[str, Any], priority: int) -> int:
    s = 40 + max(0, 6 - int(priority)) * 5
    if row.get("phone"): s += 20
    if row.get("website"): s += 10
    try:
        n = int(float(row.get("user_rating_count") or 0))
        if n >= 100: s += 15
        elif n >= 30: s += 8
    except Exception:
        pass
    try:
        r = float(row.get("rating") or 0)
        if 0 < r < 4.0: s += 10
        elif r >= 4.5: s += 5
    except Exception:
        pass
    return min(100, s)

def collect(segment_ids: list[str], per_segment: int) -> list[dict[str, Any]]:
    cfg = load_yaml(CONFIG)
    manual = manual_rows()
    rows = []

    for sid, seg in cfg["segments"].items():
        if segment_ids and sid not in segment_ids:
            continue

        candidates = []
        for q in seg.get("google_queries", []):
            if len(candidates) >= per_segment:
                break
            candidates.extend(google_text_search(q, per_segment - len(candidates)))

        if len(candidates) < per_segment:
            for m in manual:
                if len(candidates) >= per_segment:
                    break
                if (m.get("segment") or "") in ("", sid, seg.get("name_ar", "")):
                    candidates.append(m)

        if not candidates:
            for i in range(1, per_segment + 1):
                candidates.append({
                    "company_name": f"Research Target {seg['name_ar']} #{i}",
                    "phone": "",
                    "website": "",
                    "address": cfg.get("default_city", "Riyadh"),
                    "rating": "",
                    "user_rating_count": "",
                    "google_maps_uri": "",
                    "source": "research_placeholder",
                })

        for c in candidates[:per_segment]:
            r = dict(c)
            r.update({
                "date": dt.date.today().isoformat(),
                "segment": sid,
                "segment_name_ar": seg.get("name_ar", ""),
                "pain_angle": seg.get("pain_angle", ""),
                "transformation_angle": seg.get("transformation_angle", ""),
                "core_offer": seg.get("core_offer", ""),
                "high_ticket_offer": seg.get("high_ticket_offer", ""),
                "priority_score": score(r, seg.get("priority", 5)),
                "status": "draft_ready" if r.get("phone") or r.get("website") else "research_needed",
                "next_action": "review_and_send" if r.get("phone") or r.get("website") else "find_public_contact",
                "owner": "Sami",
            })
            rows.append(r)

    rows.sort(key=lambda x: int(x["priority_score"]), reverse=True)
    return rows

def write_csv(out: Path, rows: list[dict[str, Any]]) -> None:
    fields = [
        "date","segment","segment_name_ar","company_name","phone","website","address","rating","user_rating_count",
        "google_maps_uri","source","priority_score","pain_angle","transformation_angle","core_offer","high_ticket_offer",
        "status","next_action","owner"
    ]
    with (out / "daily_targets.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def write_drafts(out: Path, rows: list[dict[str, Any]], limit: int) -> None:
    tpl = load_yaml(TEMPLATES)
    ddir = out / "drafts"
    ddir.mkdir(exist_ok=True)

    index = ["# Daily Outreach Drafts", ""]
    for i, r in enumerate(rows[:limit], 1):
        data = {
            "company_name": r["company_name"],
            "pain_angle": r["pain_angle"],
            "core_offer": r["core_offer"],
        }
        body = [
            f"# {r['company_name']}",
            "",
            f"- Segment: {r['segment_name_ar']}",
            f"- Phone: {r.get('phone','')}",
            f"- Website: {r.get('website','')}",
            f"- Score: {r['priority_score']}",
            f"- Core offer: {r['core_offer']}",
            f"- High ticket offer: {r['high_ticket_offer']}",
            "",
            "## WhatsApp First Touch",
            render(tpl["whatsapp_first_touch"], data),
            "",
            "## WhatsApp Follow-up 1",
            render(tpl["whatsapp_followup_1"], data),
            "",
            "## WhatsApp Follow-up 2",
            render(tpl["whatsapp_followup_2"], data),
            "",
            "## Email Subject",
            render(tpl["email_subject"], data),
            "",
            "## Email Body",
            render(tpl["email_body"], data),
            "",
            "## Call Script",
            tpl["call_script"],
        ]
        filename = f"{i:02d}_{slug(r['company_name'])}.md"
        (ddir / filename).write_text("\n".join(body), encoding="utf-8")
        index.append(f"{i}. {r['company_name']} — score {r['priority_score']} — `{filename}`")
    (out / "OUTREACH_INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")

def write_proposals(out: Path, rows: list[dict[str, Any]], limit: int) -> None:
    pdir = out / "proposal_stubs"
    pdir.mkdir(exist_ok=True)
    for r in rows[:limit]:
        body = f"""# Proposal Stub — {r['company_name']}

## Situation
{r['pain_angle']}

## Transformation Angle
{r['transformation_angle']}

## Recommended First Offer
{r['core_offer']}

## Expansion Offer
{r['high_ticket_offer']}

## 14-Day Pilot
1. Map workflow and leaks.
2. Build lead/follow-up board.
3. Add message templates.
4. Create management report.
5. Train team and review first week.

## Success Metrics
- Response time
- Follow-up completion
- Overdue follow-ups
- Bookings/proposals
- Lost reasons
- Weekly executive report

## Commercial Direction
Start with diagnostic or starter system, then expand to command center after proof.
"""
        (pdir / f"{slug(r['company_name'])}_proposal_stub.md").write_text(body, encoding="utf-8")

def write_report(out: Path, rows: list[dict[str, Any]]) -> None:
    seg_counts: dict[str, int] = {}
    for r in rows:
        seg_counts[r["segment"]] = seg_counts.get(r["segment"], 0) + 1

    lines = [
        "# Dealix Founder Daily Business Report",
        "",
        f"Date: {dt.date.today().isoformat()}",
        "",
        "## Summary",
        f"- Targets generated: {len(rows)}",
        f"- Draft ready: {sum(1 for r in rows if r['status'] == 'draft_ready')}",
        f"- Research needed: {sum(1 for r in rows if r['status'] == 'research_needed')}",
        "",
        "## Segment Mix",
    ]
    for k, v in seg_counts.items():
        lines.append(f"- {k}: {v}")

    lines += [
        "",
        "## Top 10",
        "| # | Company | Segment | Score | Offer | Next Action |",
        "|---:|---|---|---:|---|---|",
    ]
    for i, r in enumerate(rows[:10], 1):
        lines.append(f"| {i} | {r['company_name']} | {r['segment']} | {r['priority_score']} | {r['core_offer']} | {r['next_action']} |")

    lines += [
        "",
        "## Founder Actions Today",
        "- Review top 20 drafts.",
        "- Send only reviewed messages manually.",
        "- Book discovery calls.",
        "- Generate proposal stubs for qualified replies.",
        "- Update statuses before end of day.",
        "",
        "## Do Not Do",
        "- Do not auto-send cold messages.",
        "- Do not commit private customer data.",
        "- Do not promise guaranteed revenue.",
    ]
    (out / "DAILY_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--segments", default="clinics,training_centers,agencies,restaurants,real_estate")
    ap.add_argument("--per-segment", type=int, default=8)
    ap.add_argument("--draft-limit", type=int, default=20)
    ap.add_argument("--proposal-limit", type=int, default=5)
    args = ap.parse_args()

    out = today_dir()
    segments = [s.strip() for s in args.segments.split(",") if s.strip()]
    rows = collect(segments, args.per_segment)
    write_csv(out, rows)
    write_drafts(out, rows, args.draft_limit)
    write_proposals(out, rows, args.proposal_limit)
    write_report(out, rows)

    print(f"Founder Business OS generated: {out}")
    print(f"Targets: {len(rows)}")
    print(f"Report: {out / 'DAILY_REPORT.md'}")
    print(f"CSV: {out / 'daily_targets.csv'}")

if __name__ == "__main__":
    main()
