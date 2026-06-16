"""Commercial orchestrator — the missing connective tissue that chains
existing primitives into one daily loop:

    prospects → ICP score → consent/doctrine gate → bilingual draft → queue

Everything it calls already exists and is independently tested:
- `auto_client_acquisition.icp_scorer`            (deterministic fit score)
- `auto_client_acquisition.commercial_orchestrator.outreach`  (draft render)
- `auto_client_acquisition.commercial_orchestrator.draft_queue` (durable queue)

Doctrine:
- COMPANY-LEVEL only. The pipeline never reads or emits personal PII.
- A draft is produced ONLY for an on-ICP, consent-flagged company, and it is
  always queued with `approval_required=True`. NOTHING is sent here.
- Pure composition + one append to the draft queue. No network, no LLM.
"""
from __future__ import annotations

import csv
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from auto_client_acquisition.commercial_orchestrator import draft_queue
from auto_client_acquisition.commercial_orchestrator.outreach import (
    OutreachContext,
    render_outreach_draft,
)
from auto_client_acquisition.icp_scorer import ICPFilter, LeadSignals, score_lead

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_DEFAULT_DATASET = "data/leads/saudi_b2b_prospects.csv"

# Band ordering for the min-band gate.
_BAND_RANK = {"cold": 0, "cool": 1, "warm": 2, "hot": 3}

# Dealix default ICP frame for the Saudi B2B target set. Matching the curated
# dataset's sectors/regions/sizes yields a warm-or-better fit, which is the
# intended behaviour for an on-ICP target frame.
DEFAULT_ICP = ICPFilter(
    target_sectors=[
        "real_estate", "logistics", "healthcare", "training", "engineering",
        "construction", "facilities_management", "marketing_agency", "ecommerce",
        "food_and_beverage", "wholesale_distribution", "manufacturing",
        "professional_services", "insurance", "automotive", "hospitality",
        "oil_gas_services", "technology", "project_management", "education",
        "fintech", "agritech", "b2b_services",
    ],
    target_regions=["Central", "Western", "Eastern", "Northern", "Southern", "Qassim"],
    target_size_bands=["small", "mid", "large", "enterprise"],
    preferred_tech=[],
)


def dataset_path() -> Path:
    """Resolve the prospect dataset path (override via DEALIX_LEAD_DATASET_PATH)."""
    p = Path(os.environ.get("DEALIX_LEAD_DATASET_PATH", _DEFAULT_DATASET))
    if not p.is_absolute():
        p = _REPO_ROOT / p
    return p


def load_prospects(path: str | Path | None = None) -> list[dict[str, Any]]:
    """Load the curated prospect CSV into a list of dicts. Returns [] if absent."""
    p = Path(path) if path else dataset_path()
    if not p.exists():
        return []
    with p.open("r", encoding="utf-8") as f:
        return [dict(row) for row in csv.DictReader(f)]


def _to_signals(p: dict[str, Any]) -> LeadSignals:
    region = (p.get("region") or "").strip() or (p.get("city") or "").strip()
    website = (p.get("website") or "").strip()
    return LeadSignals(
        sector=(p.get("sector") or "").strip() or None,
        region=region or None,
        size_band=(p.get("size_band") or "").strip() or None,
        has_domain=bool(website),
        has_email=False,   # company-level frame carries no personal email
        has_linkedin=False,
    )


@dataclass
class ChainResult:
    generated: int = 0
    skipped: int = 0
    drafts: list[dict[str, Any]] = field(default_factory=list)
    skipped_rows: list[dict[str, Any]] = field(default_factory=list)

    def summary(self) -> dict[str, Any]:
        by_sector: dict[str, int] = {}
        by_band: dict[str, int] = {}
        for d in self.drafts:
            by_sector[d.get("sector", "?")] = by_sector.get(d.get("sector", "?"), 0) + 1
            by_band[d.get("icp_band", "?")] = by_band.get(d.get("icp_band", "?"), 0) + 1
        return {
            "generated": self.generated,
            "skipped": self.skipped,
            "by_sector": by_sector,
            "by_band": by_band,
        }


def run_acquisition_to_drafts(
    prospects: list[dict[str, Any]] | None = None,
    *,
    icp: ICPFilter | None = None,
    min_band: str = "warm",
    enqueue_drafts: bool = True,
) -> ChainResult:
    """Score each prospect, and for on-ICP companies render a bilingual
    first-touch draft and queue it for founder approval.

    Args:
        prospects: list of prospect dicts. Defaults to the curated dataset.
        icp: ICP frame. Defaults to ``DEFAULT_ICP``.
        min_band: minimum ICP band that earns a draft ("warm" by default).
        enqueue_drafts: when True, persist each draft to the durable queue.

    Returns a ``ChainResult``. No external send ever happens here.
    """
    if prospects is None:
        prospects = load_prospects()
    icp = icp or DEFAULT_ICP
    threshold = _BAND_RANK.get(min_band, 2)
    result = ChainResult()

    for p in prospects:
        company = (p.get("company_name") or "").strip()
        if not company:
            result.skipped += 1
            result.skipped_rows.append({"reason": "missing_company_name", "row": p})
            continue

        scored = score_lead(_to_signals(p), icp)
        if _BAND_RANK.get(scored["band"], 0) < threshold:
            result.skipped += 1
            result.skipped_rows.append(
                {"reason": "below_min_band", "company": company,
                 "band": scored["band"], "score": scored["score"]}
            )
            continue

        rendered = render_outreach_draft(OutreachContext(
            company_name=company,
            sector=(p.get("sector") or "").strip(),
            city=(p.get("city") or "").strip(),
            name_ar=(p.get("name_ar") or "").strip(),
            pain_hypothesis_en=(p.get("pain_hypothesis_en") or "").strip(),
            pain_hypothesis_ar=(p.get("pain_hypothesis_ar") or "").strip(),
            icp_band=scored["band"],
        ))

        draft = {
            "kind": "outreach",
            "channel": "email",                     # suggested; founder confirms
            "company_name": company,
            "name_ar": (p.get("name_ar") or "").strip(),
            "sector": (p.get("sector") or "").strip(),
            "city": (p.get("city") or "").strip(),
            "region": (p.get("region") or "").strip(),
            "size_band": (p.get("size_band") or "").strip(),
            "icp_score": scored["score"],
            "icp_band": scored["band"],
            "offer": "free_ai_ops_diagnostic",
            "subject_en": rendered["subject_en"],
            "subject_ar": rendered["subject_ar"],
            "body_md": rendered["body_md"],
            "consent_status": (p.get("consent_status") or "required_before_contact").strip(),
            "source_type": (p.get("source_type") or "").strip(),
            "source_url": (p.get("source_url") or "").strip(),
        }

        if enqueue_drafts:
            draft = draft_queue.enqueue(draft)
        result.drafts.append(draft)
        result.generated += 1

    return result


__all__ = [
    "ChainResult",
    "DEFAULT_ICP",
    "dataset_path",
    "load_prospects",
    "run_acquisition_to_drafts",
]
