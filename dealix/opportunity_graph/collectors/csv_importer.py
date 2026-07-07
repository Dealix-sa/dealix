"""Import companies from a founder-provided CSV into OpportunityCompany rows.

Tolerant of missing columns and empty files. Deterministic ids are derived
from the company name + website so re-importing the same seed is idempotent.
"""

from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path

from dealix.opportunity_graph.schemas import OpportunityCompany

# Accepted CSV headers → OpportunityCompany fields.
_FIELD_MAP = {
    "name": "name",
    "company": "name",
    "website": "website",
    "url": "website",
    "country": "country",
    "city": "city",
    "sector": "sector",
    "industry": "sector",
    "company_type": "company_type",
    "type": "company_type",
    "source": "source",
    "source_url": "source_url",
    "saudi_signal": "saudi_signal",
    "signal": "saudi_signal",
    "signal_type": "signal_type",
    "signal_date": "signal_date",
    "buyer_persona": "buyer_persona",
    "persona": "buyer_persona",
    "pain_hypothesis": "pain_hypothesis",
    "pain": "pain_hypothesis",
    "offer_match": "offer_match",
    "offer": "offer_match",
    "estimated_deal_size": "estimated_deal_size",
    "deal_size": "estimated_deal_size",
    "consent_to_contact": "consent_to_contact",
    "consent": "consent_to_contact",
}

_TRUEISH = {"1", "true", "yes", "y", "نعم"}


def _stable_id(name: str, website: str) -> str:
    basis = f"{name.strip().lower()}|{website.strip().lower()}"
    digest = hashlib.sha1(basis.encode("utf-8")).hexdigest()[:12]
    return f"co_{digest}"


def _row_to_company(row: dict[str, str]) -> OpportunityCompany | None:
    mapped: dict[str, str] = {}
    for raw_key, raw_val in row.items():
        if raw_key is None:
            continue
        key = _FIELD_MAP.get(raw_key.strip().lower())
        if key and str(raw_val or "").strip():
            mapped[key] = str(raw_val).strip()
    name = mapped.get("name", "").strip()
    if not name:
        return None
    consent = mapped.pop("consent_to_contact", "").strip().lower() in _TRUEISH
    return OpportunityCompany(
        id=_stable_id(name, mapped.get("website", "")),
        consent_to_contact=consent,
        **mapped,
    )


def import_companies_csv(path: str | Path) -> list[OpportunityCompany]:
    p = Path(path)
    if not p.is_file():
        return []
    text = p.read_text(encoding="utf-8-sig")
    return _parse_csv_text(text)


def _parse_csv_text(text: str) -> list[OpportunityCompany]:
    if not text.strip():
        return []
    reader = csv.DictReader(io.StringIO(text))
    companies: list[OpportunityCompany] = []
    seen: set[str] = set()
    for row in reader:
        company = _row_to_company(row)
        if company is None or company.id in seen:
            continue
        seen.add(company.id)
        companies.append(company)
    return companies
