"""
Generates the daily Founder Review Report in Markdown.
"""

from __future__ import annotations
from collections import defaultdict
from datetime import datetime, timezone


def generate_report(
    date_str: str,
    stats: dict,
    approved: list[dict],
    rejected: list[dict],
) -> str:
    """Build a Markdown founder report from pipeline run statistics and draft lists."""
    top_drafts = sorted(approved, key=lambda d: d.get("quality_score", 0), reverse=True)[:25]

    by_country: dict[str, list] = defaultdict(list)
    by_sector: dict[str, list] = defaultdict(list)
    for d in approved:
        by_country[d.get("country", "unknown")].append(d)
        by_sector[d.get("sector", "unknown")].append(d)

    def avg_score(items: list[dict]) -> float:
        scores = [i.get("quality_score", 0) for i in items]
        return round(sum(scores) / len(scores), 1) if scores else 0.0

    country_rows = ""
    for country, items in sorted(by_country.items()):
        top_sector = max(
            set(d.get("sector", "") for d in items),
            key=lambda s: sum(1 for d in items if d.get("sector") == s),
            default="",
        )
        country_rows += f"| {country} | {len(items)} | {avg_score(items)} | {top_sector} |\n"

    sector_rows = ""
    for sector, items in sorted(by_sector.items()):
        angles = set(d.get("angle", "") for d in items if d.get("angle"))
        best_angle = sorted(angles, key=lambda a: sum(1 for d in items if d.get("angle") == a), reverse=True)
        sector_rows += f"| {sector} | {len(items)} | {avg_score(items)} | {best_angle[0] if best_angle else '-'} |\n"

    top_rows = ""
    for i, d in enumerate(top_drafts, 1):
        top_rows += (
            f"| {i} | {d.get('company', '-')} | {d.get('country', '-')} | "
            f"{d.get('sector', '-')} | {d.get('language', '-')} | "
            f"{d.get('offer', '-')} | {d.get('quality_score', 0)} | {d.get('channel', '-')} |\n"
        )

    risks = []
    for d in rejected[:10]:
        reason = d.get("reject_reason") or "unknown"
        risks.append(f"- {d.get('company', 'unknown')} ({d.get('country', '?')}): {reason}")
    risk_section = "\n".join(risks) if risks else "- None flagged"

    email_count = sum(1 for d in approved if d.get("channel") == "email")
    linkedin_count = sum(1 for d in approved if d.get("channel") == "linkedin")
    form_count = sum(1 for d in approved if d.get("channel") == "website_form")
    hold_count = len(approved) - email_count - linkedin_count - form_count

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    return f"""# Dealix GCC Draft Factory — Founder Report
**Date:** {date_str}
**Generated:** {generated_at}

---

## Production Summary

| Metric | Count |
|---|---:|
| Qualified companies | {stats.get('qualified_companies', 0)} |
| Arabic drafts generated | {stats.get('arabic_drafts', 0)} |
| English drafts generated | {stats.get('english_drafts', 0)} |
| Follow-up drafts | {stats.get('followup_drafts', 0)} |
| Rejected (quality/compliance) | {stats.get('rejected_drafts', 0)} |
| **Founder-ready drafts** | **{stats.get('founder_ready', 0)}** |

---

## By Country

| Country | Drafts | Avg Score | Top Sector |
|---|---:|---:|---|
{country_rows}
---

## By Sector

| Sector | Drafts | Avg Score | Best Angle |
|---|---:|---:|---|
{sector_rows}
---

## Top 25 Founder-Ready Drafts

| # | Company | Country | Sector | Lang | Offer | Score | Channel |
|---|---|---|---|---|---|---:|---|
{top_rows}
---

## Send Recommendation

- **Email:** {email_count} drafts ready (pending your approval)
- **LinkedIn:** {linkedin_count} drafts ready
- **Website forms:** {form_count} drafts ready
- **Hold / needs more research:** {hold_count}

---

## Risk Flags

{risk_section}

---

## Tomorrow Strategy

- Review top 25 above and approve sends
- Update suppression list with any opt-outs
- Check reply rates from yesterday's sends
- Adjust angle weights based on reply learning log
"""
