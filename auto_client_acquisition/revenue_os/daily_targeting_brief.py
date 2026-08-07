"""Daily Targeting Brief — ranked, governed dossiers + draft-only outreach.

Integration layer over :mod:`target_company_intelligence`. Loads operator-declared
companies (from a YAML file the founder fills from their own CRM / network — never
scraped), builds deterministic dossiers, ranks by priority, and assembles a
bilingual brief with draft-only outreach queued for human approval.

No network, no DB, no LLM. Every number is an estimate from declared inputs only.
"""

from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

import yaml

from auto_client_acquisition.revenue_os.target_company_intelligence import (
    build_company_dossier,
    build_target_company_draft,
)

_PLACEHOLDER_PREFIX = "REPLACE:"


def load_target_companies(path: str) -> list[dict[str, Any]]:
    """Load companies from a YAML file with a top-level ``companies:`` list.

    Rows whose ``company_name`` is empty or starts with ``REPLACE:`` are skipped
    (placeholders the operator has not yet filled in).
    """
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    rows = data.get("companies") or []
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        name = str(row.get("company_name") or "").strip()
        if not name or name.startswith(_PLACEHOLDER_PREFIX):
            continue
        out.append(dict(row))
    return out


def _summarize(targets: list[dict[str, Any]]) -> dict[str, Any]:
    """Deterministic roll-up over the ranked dossiers."""
    if not targets:
        return {
            "avg_icp_fit": 0.0,
            "count_by_priority_band": {},
            "count_by_recommended_offer": {},
            "top_weakness_codes": [],
        }
    avg_icp = round(
        sum(int(t["icp_fit"]["score"]) for t in targets) / len(targets), 1
    )
    band_counts: dict[str, int] = {}
    offer_counts: dict[str, int] = {}
    weakness_counts: dict[str, int] = {}
    for t in targets:
        band_counts[t["priority_band"]] = band_counts.get(t["priority_band"], 0) + 1
        offer = t["recommended_offer"]
        offer_counts[offer] = offer_counts.get(offer, 0) + 1
        for w in t["weaknesses"]:
            weakness_counts[w["code"]] = weakness_counts.get(w["code"], 0) + 1
    top_weaknesses = [
        code
        for code, _ in sorted(
            weakness_counts.items(), key=lambda kv: (-kv[1], kv[0])
        )
    ]
    return {
        "avg_icp_fit": avg_icp,
        "count_by_priority_band": band_counts,
        "count_by_recommended_offer": offer_counts,
        "top_weakness_codes": top_weaknesses,
    }


def build_daily_targeting_brief(
    companies: list[dict[str, Any]],
    *,
    top_n: int = 10,
    date_iso: str | None = None,
    icp_sectors: frozenset[str] | None = None,
    icp_cities: frozenset[str] | None = None,
) -> dict[str, Any]:
    """Build dossiers for all companies, rank by priority, draft top_n (draft-only)."""
    brief_date = date_iso or date.today().isoformat()

    scored: list[dict[str, Any]] = []
    for idx, company in enumerate(companies):
        dossier = build_company_dossier(
            company, icp_sectors=icp_sectors, icp_cities=icp_cities
        )
        scored.append({"idx": idx, "company": company, "dossier": dossier})

    # Stable sort: priority desc, original order preserved on ties.
    scored.sort(key=lambda item: (-int(item["dossier"]["priority_score"]), item["idx"]))

    selected = scored[: max(0, top_n)]
    targets: list[dict[str, Any]] = []
    for item in selected:
        draft = build_target_company_draft(
            item["company"],
            item["dossier"],
            include_whatsapp_draft=False,
        )
        target = dict(item["dossier"])
        target["draft"] = draft
        targets.append(target)

    summary = _summarize(targets)

    return {
        "date": brief_date,
        "total_targets": len(companies),
        "shown": len(targets),
        "generated_at": datetime.now(UTC).isoformat(),
        "summary": summary,
        "targets": targets,
        "governance_footer_ar": (
            "مسودات فقط — تتطلب موافقة بشرية. لا جمع خارجي، لا إرسال تلقائي. "
            "كل الأرقام تقديرية وليست ضمانات."
        ),
        "governance_footer_en": (
            "Draft-only — requires human approval. No scraping, no auto-send. "
            "All numbers are estimates, not guarantees."
        ),
        "disclaimer_ar": (
            "نقاط الضعف فرضيات تشغيلية من بيانات معلنة فقط — ليست حقائق مؤكدة "
            "عن شركات حقيقية."
        ),
        "disclaimer_en": (
            "Weaknesses are operator hypotheses from declared inputs only — not "
            "verified facts about real companies."
        ),
    }


def _md_escape(text: Any) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ")


def render_brief_markdown(brief: dict[str, Any]) -> str:
    """Render a bilingual markdown brief with a ranked table + per-target sections."""
    lines: list[str] = []
    lines.append(f"# Daily Targeting Brief — {brief['date']}")
    lines.append("")
    lines.append(
        f"Total targets: {brief['total_targets']} · Shown: {brief['shown']} · "
        f"Generated: {brief['generated_at']}"
    )
    lines.append("")
    summary = brief["summary"]
    lines.append(
        f"Avg ICP fit (estimate): {summary['avg_icp_fit']} · "
        f"Bands: {summary['count_by_priority_band']} · "
        f"Offers: {summary['count_by_recommended_offer']}"
    )
    lines.append("")
    lines.append("## Ranked targets")
    lines.append("")
    lines.append(
        "| Company | Sector | Priority | ICP fit | Recommended offer | Top weakness |"
    )
    lines.append("|---|---|---|---|---|---|")
    for t in brief["targets"]:
        top_weakness = t["weaknesses"][0]["code"] if t["weaknesses"] else "-"
        lines.append(
            f"| {_md_escape(t['company_name'])} | {_md_escape(t['sector'])} | "
            f"{t['priority_band']} | {t['icp_fit']['score']} (est.) | "
            f"{t['recommended_offer']} | {top_weakness} |"
        )
    lines.append("")
    lines.append("## Targets detail")
    lines.append("")
    for t in brief["targets"]:
        lines.append(f"### {t['company_name']} — {t['priority_band']}")
        lines.append("")
        lines.append(f"- Why now (AR): {t['why_now_ar']}")
        lines.append(f"- Why now (EN): {t['why_now_en']}")
        lines.append(f"- Recommended offer: {t['recommended_offer']}")
        lines.append(
            f"- ICP fit (estimate): {t['icp_fit']['score']} · "
            f"Data quality completeness (estimate): "
            f"{t['data_quality']['completeness_pct']}%"
        )
        lines.append("")
        draft = t.get("draft", {})
        lines.append("**مسودة — تتطلب موافقة / DRAFT — requires approval**")
        lines.append("")
        if draft.get("angle_ar"):
            lines.append(f"- Angle (AR): {draft['angle_ar']}")
        if draft.get("angle_en"):
            lines.append(f"- Angle (EN): {draft['angle_en']}")
        if draft.get("email_ar"):
            lines.append("")
            lines.append("```")
            lines.append(str(draft["email_ar"]))
            lines.append("")
            lines.append(str(draft.get("email_en", "")))
            lines.append("```")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"_{brief['governance_footer_ar']}_")
    lines.append("")
    lines.append(f"_{brief['governance_footer_en']}_")
    lines.append("")
    lines.append(f"_{brief['disclaimer_ar']}_")
    lines.append("")
    lines.append(f"_{brief['disclaimer_en']}_")
    return "\n".join(lines)


def brief_to_dict(brief: dict[str, Any]) -> dict[str, Any]:
    """Identity passthrough — the brief is already a plain dict."""
    return brief


__all__ = [
    "brief_to_dict",
    "build_daily_targeting_brief",
    "load_target_companies",
    "render_brief_markdown",
]
