"""Founder daily review report rendering.

Turns a GenerationResult into the founder-facing bundle:
  founder_review.csv / .md, top_50_priority.md, compliance_report.json,
  daily_metrics.json, next_actions.md
"""

from __future__ import annotations

import csv
import io
import json
from collections import Counter
from pathlib import Path
from typing import Any

from dealix.commercial_launch.engine import GenerationResult, OUTPUTS_DIR

CSV_FIELDS = [
    "draft_id", "company_name", "vertical", "country", "city", "channel",
    "language", "buyer_persona", "buyer_title", "offer", "quality_score",
    "compliance_score", "risk_level", "research_required", "status",
    "send_allowed", "external_send_blocked", "requires_founder_approval", "subject",
]


def _priority_score(d: dict[str, Any]) -> float:
    risk_penalty = {"low": 0, "medium": 6, "high": 18}.get(d.get("risk_level", "low"), 0)
    research_penalty = 8 if d.get("research_required") else 0
    return d.get("quality_score", 0) + d.get("compliance_score", 0) - risk_penalty - research_penalty


def _summary(result: GenerationResult) -> dict[str, Any]:
    accepted = result.accepted
    by_vertical = Counter(d["vertical"] for d in accepted)
    by_channel = Counter(d["channel"] for d in accepted)
    by_language = Counter(d["language"] for d in accepted)
    by_risk = Counter(d.get("risk_level", "low") for d in accepted)
    avg_q = round(sum(d["quality_score"] for d in accepted) / len(accepted), 1) if accepted else 0
    avg_c = round(sum(d["compliance_score"] for d in accepted) / len(accepted), 1) if accepted else 0
    return {
        "run_date": result.run_date,
        "total_accepted": len(accepted),
        "total_rejected": len(result.rejected),
        "by_vertical": dict(by_vertical),
        "by_channel": dict(by_channel),
        "by_language": dict(by_language),
        "by_risk": dict(by_risk),
        "avg_quality_score": avg_q,
        "avg_compliance_score": avg_c,
        "used_real_leads": result.used_real_leads,
        "research_required_count": sum(1 for d in accepted if d.get("research_required")),
    }


def render_csv(result: GenerationResult) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CSV_FIELDS, extrasaction="ignore")
    w.writeheader()
    for d in sorted(result.accepted, key=_priority_score, reverse=True):
        w.writerow(d)
    return buf.getvalue()


def _draft_summary_line(d: dict[str, Any]) -> str:
    return f"{d.get('subject','')[:90]}"


def render_founder_md(result: GenerationResult) -> str:
    s = _summary(result)
    accepted = result.accepted
    ranked = sorted(accepted, key=_priority_score, reverse=True)
    top50 = ranked[:50]
    top_opps = ranked[:10]
    top_risks = sorted(accepted, key=lambda d: ({"high": 0, "medium": 1, "low": 2}[d.get("risk_level", "low")], -_priority_score(d)))[:10]
    needs_research = [d for d in accepted if d.get("research_required")][:15]

    L: list[str] = []
    L.append(f"# Founder Daily Review — {result.run_date}")
    L.append("")
    L.append("> **REVIEW-ONLY.** Nothing in this queue has been sent. The system does not "
             "send email, LinkedIn, WhatsApp, or any external message. You review, approve, "
             "and send manually.")
    L.append("")
    L.append("## Summary")
    L.append(f"- **Drafts ready for review:** {s['total_accepted']}")
    L.append(f"- **Drafts rejected by gates:** {s['total_rejected']}")
    L.append(f"- **Avg quality score:** {s['avg_quality_score']} / 100")
    L.append(f"- **Avg compliance score:** {s['avg_compliance_score']} / 100")
    L.append(f"- **Using real seed leads:** {'yes' if s['used_real_leads'] else 'NO — placeholders, research_required'}")
    L.append(f"- **Drafts needing research:** {s['research_required_count']}")
    if result.warnings:
        L.append("")
        L.append("### ⚠️ Warnings")
        for wn in result.warnings:
            L.append(f"- {wn}")
    L.append("")
    L.append("## Vertical distribution")
    for k, v in sorted(s["by_vertical"].items(), key=lambda kv: -kv[1]):
        L.append(f"- {k}: {v}")
    L.append("")
    L.append("## Channel distribution")
    for k, v in sorted(s["by_channel"].items(), key=lambda kv: -kv[1]):
        L.append(f"- {k}: {v}")
    L.append("")
    L.append("## Top 50 drafts (by priority)")
    L.append("")
    L.append("| # | Company | Vertical | Channel | Lang | Q | C | Risk | Subject |")
    L.append("|---|---------|----------|---------|------|---|---|------|---------|")
    for i, d in enumerate(top50, 1):
        L.append(f"| {i} | {d['company_name']} | {d['vertical']} | {d['channel']} | {d['language']} | "
                 f"{d['quality_score']} | {d['compliance_score']} | {d['risk_level']} | {_draft_summary_line(d)} |")
    L.append("")
    L.append("## Top 10 opportunities")
    for i, d in enumerate(top_opps, 1):
        L.append(f"{i}. **{d['company_name']}** ({d['vertical']}, {d['channel']}) — {d['pain_angle']}")
    L.append("")
    L.append("## Top 10 risks to watch")
    for i, d in enumerate(top_risks, 1):
        L.append(f"{i}. **{d['company_name']}** — risk={d['risk_level']}, "
                 f"compliance={d['compliance_score']} ({d['vertical']}, {d['channel']})")
    L.append("")
    L.append("## Drafts needing extra research")
    if needs_research:
        for d in needs_research:
            L.append(f"- {d['company_name']} ({d['vertical']}) — enrich buyer + company before send")
    else:
        L.append("- None — all drafts are tied to enriched leads.")
    L.append("")
    L.append("## Rejected drafts (why)")
    rej_reasons = Counter()
    for d in result.rejected:
        for r in d.get("reject_reason", ["below_threshold"]):
            rej_reasons[r] += 1
    if rej_reasons:
        for r, n in rej_reasons.most_common():
            L.append(f"- {r}: {n}")
    else:
        L.append("- None.")
    L.append("")
    L.append("## Founder recommendation for today")
    L.append(_recommendation(s))
    L.append("")
    L.append("## Go / No-Go by channel")
    L.append("- **Cold email:** GO for drafting. NO-GO for sending until SPF/DKIM/DMARC + warmup ramp are signed off.")
    L.append("- **Follow-up:** GO for drafting. Send only where a genuine prior touch exists.")
    L.append("- **LinkedIn:** GO for manual drafting only. NO-GO for any automation/auto-connect.")  # safety-audit-allow
    L.append("- **Website forms:** GO for drafting. Founder submits manually.")
    L.append("- **WhatsApp:** NO-GO for cold outreach. Inbound/opt-in reply templates only.")
    L.append("")
    return "\n".join(L)


def _recommendation(s: dict[str, Any]) -> str:
    if not s["used_real_leads"]:
        return ("Enrich the highest-priority placeholder companies with real buyer "
                "names and a verified business email before any manual send. Start with "
                "the top 50 list and the two strongest verticals "
                f"({_top_two(s['by_vertical'])}).")
    return ("Work the top 50 list first. Personalise each draft with one real, specific "
            f"detail before sending manually. Lead with {_top_two(s['by_vertical'])} today.")


def _top_two(d: dict[str, int]) -> str:
    items = sorted(d.items(), key=lambda kv: -kv[1])[:2]
    return ", ".join(k for k, _ in items) if items else "your strongest vertical"


def render_top50_md(result: GenerationResult) -> str:
    ranked = sorted(result.accepted, key=_priority_score, reverse=True)[:50]
    L = [f"# Top 50 Priority Drafts — {result.run_date}", "",
         "> Review-only. Founder sends manually. Each row is one draft.", ""]
    for i, d in enumerate(ranked, 1):
        L.append(f"### {i}. {d['company_name']} — {d['vertical']}")
        L.append(f"- **Buyer:** {d['buyer_title']} ({d['buyer_persona']})")
        L.append(f"- **Channel:** {d['channel']} · **Language:** {d['language']} · **Offer:** {d['offer']}")
        L.append(f"- **Draft summary:** {d['subject']}")
        L.append(f"- **Why this lead matters:** {d['pain_angle']}")
        L.append(f"- **Risk:** {d['risk_level']} (quality {d['quality_score']}, compliance {d['compliance_score']})")
        action = "Enrich buyer + verify email, then send manually" if d.get("research_required") else "Personalise one detail, then send manually"
        L.append(f"- **Recommended manual action:** {action}")
        L.append("")
    return "\n".join(L)


def render_compliance_report(result: GenerationResult) -> dict[str, Any]:
    accepted = result.accepted
    flagged = [
        {"draft_id": d["draft_id"], "compliance_score": d["compliance_score"], "reasons": d.get("_compliance_reasons", [])}
        for d in accepted if d.get("_compliance_reasons")
    ]
    return {
        "run_date": result.run_date,
        "drafts_checked": len(accepted),
        "min_compliance_score": min((d["compliance_score"] for d in accepted), default=0),
        "all_have_opt_out": all(("stop" in (d["body"].lower()) or "إيقاف" in d["body"]) for d in accepted),
        "all_external_send_blocked": all(d["external_send_blocked"] is True for d in accepted),
        "all_send_allowed_false": all(d["send_allowed"] is False for d in accepted),
        "flagged_drafts": flagged,
        "rejected_count": len(result.rejected),
    }


def render_daily_metrics(result: GenerationResult) -> dict[str, Any]:
    s = _summary(result)
    s["targets"] = result.targets
    s["target_total_minimum"] = 400
    s["target_met"] = result.total_accepted >= 400
    return s


def render_next_actions(result: GenerationResult) -> str:
    s = _summary(result)
    L = [f"# Next Actions — {result.run_date}", "",
         "1. Open `top_50_priority.md` and review the top 50 drafts.",
         "2. For each draft you approve, personalise one real detail.",
         "3. Send manually from your own inbox / LinkedIn / form. The system does **not** send.",
         "4. Log replies in your CRM and mark followed-up leads.",
         "5. Before any cold-email batch, confirm SPF/DKIM/DMARC + suppression list owner.",
         ""]
    if not s["used_real_leads"]:
        L.append("6. ⚠️ No real leads loaded — enrich placeholders in "
                 "`data/commercial_seed_leads.jsonl` before sending anything.")
    return "\n".join(L)


def write_review_bundle(result: GenerationResult, base_dir: Path | None = None) -> dict[str, str]:
    out = (base_dir or OUTPUTS_DIR) / result.run_date
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}

    (out / "founder_review.csv").write_text(render_csv(result), encoding="utf-8")
    paths["founder_review_csv"] = str(out / "founder_review.csv")

    (out / "founder_review.md").write_text(render_founder_md(result), encoding="utf-8")
    paths["founder_review_md"] = str(out / "founder_review.md")

    (out / "top_50_priority.md").write_text(render_top50_md(result), encoding="utf-8")
    paths["top_50_priority"] = str(out / "top_50_priority.md")

    (out / "compliance_report.json").write_text(
        json.dumps(render_compliance_report(result), ensure_ascii=False, indent=2), encoding="utf-8")
    paths["compliance_report"] = str(out / "compliance_report.json")

    (out / "daily_metrics.json").write_text(
        json.dumps(render_daily_metrics(result), ensure_ascii=False, indent=2), encoding="utf-8")
    paths["daily_metrics"] = str(out / "daily_metrics.json")

    (out / "next_actions.md").write_text(render_next_actions(result), encoding="utf-8")
    paths["next_actions"] = str(out / "next_actions.md")

    return paths
