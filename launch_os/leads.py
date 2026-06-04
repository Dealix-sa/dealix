"""Synthetic Saudi B2B lead generation across the first 5 verticals.

IMPORTANT: every lead produced here is *synthetic* — fabricated placeholder
companies built from a deterministic combination of vertical, city and an
index. No scraping, no real PII, no purchased lists. The ``.example`` seed
file documents the schema; the generator fans it out to >=400 deterministically
so the draft factory and tests are reproducible.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from pathlib import Path

# The first 5 verticals for commercial launch (Saudi B2B).
VERTICALS: tuple[dict[str, str], ...] = (
    {"key": "logistics", "name_en": "Logistics & Last-Mile", "name_ar": "اللوجستيات والتوصيل"},
    {"key": "contracting", "name_en": "Contracting & Construction", "name_ar": "المقاولات والإنشاءات"},
    {"key": "healthcare", "name_en": "Private Clinics & Healthcare", "name_ar": "العيادات والرعاية الصحية"},
    {"key": "prof_services", "name_en": "Professional Services", "name_ar": "الخدمات المهنية"},
    {"key": "manufacturing", "name_en": "Industrial & Manufacturing", "name_ar": "الصناعة والتصنيع"},
)

CITIES: tuple[dict[str, str], ...] = (
    {"en": "Riyadh", "ar": "الرياض"},
    {"en": "Jeddah", "ar": "جدة"},
    {"en": "Dammam", "ar": "الدمام"},
    {"en": "Khobar", "ar": "الخبر"},
    {"en": "Makkah", "ar": "مكة"},
    {"en": "Madinah", "ar": "المدينة"},
    {"en": "Tabuk", "ar": "تبوك"},
    {"en": "Abha", "ar": "أبها"},
)

# Generic, clearly-fictional company stems per vertical.
_STEMS: dict[str, tuple[str, ...]] = {
    "logistics": ("Masar", "Tariq", "Shahin", "Rakeb", "Nuqta"),
    "contracting": ("Binaa", "Rukn", "Asas", "Imaar", "Qaaim"),
    "healthcare": ("Shifa", "Afyah", "Sehhah", "Tabib", "Raha"),
    "prof_services": ("Mizan", "Rased", "Daleel", "Khibrah", "Manhaj"),
    "manufacturing": ("Sabb", "Masna", "Wared", "Faulad", "Taqa"),
}


@dataclass
class Lead:
    """A synthetic B2B account. No real contact data; no send fields."""

    lead_id: str
    company: str
    company_ar: str
    vertical: str
    vertical_name_en: str
    vertical_name_ar: str
    city: str
    city_ar: str
    employees_band: str
    source: str = "synthetic_placeholder"
    icp_score: int = 0
    stage: str = "new"
    consent_status: str = "not_collected"
    notes: str = ""
    # Deliberately NO email / phone / contact-person fields: this dataset is a
    # PDPL-safe placeholder and must never carry routable contact data.
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def _icp_score(seed: str) -> int:
    """Deterministic pseudo-ICP score in the 40-95 band."""
    h = int(hashlib.sha256(seed.encode()).hexdigest(), 16)
    return 40 + (h % 56)


def _band(idx: int) -> str:
    bands = ("11-50", "51-200", "201-500", "500+")
    return bands[idx % len(bands)]


def generate_leads(count: int = 420) -> list[Lead]:
    """Generate ``count`` deterministic synthetic leads, fanned across verticals.

    Order is round-robin over verticals so every vertical is represented even
    for small counts.
    """
    leads: list[Lead] = []
    i = 0
    while len(leads) < count:
        v = VERTICALS[i % len(VERTICALS)]
        city = CITIES[i % len(CITIES)]
        stems = _STEMS[v["key"]]
        stem = stems[(i // len(VERTICALS)) % len(stems)]
        n = i + 1
        lead_id = f"LEAD-{n:05d}"
        company = f"{stem} {v['name_en'].split(' & ')[0]} Co. #{n:04d}"
        company_ar = f"شركة {stem} لـ{v['name_ar']} #{n:04d}"
        seed = f"{lead_id}:{stem}:{v['key']}:{city['en']}"
        leads.append(
            Lead(
                lead_id=lead_id,
                company=company,
                company_ar=company_ar,
                vertical=v["key"],
                vertical_name_en=v["name_en"],
                vertical_name_ar=v["name_ar"],
                city=city["en"],
                city_ar=city["ar"],
                employees_band=_band(i),
                icp_score=_icp_score(seed),
                tags=[v["key"], city["en"].lower(), "synthetic"],
            )
        )
        i += 1
    return leads


def write_seed_example(path: Path, count: int = 20) -> int:
    """Write a small ``.example`` JSONL seed file documenting the schema."""
    path.parent.mkdir(parents=True, exist_ok=True)
    leads = generate_leads(count)
    with path.open("w", encoding="utf-8") as fh:
        for lead in leads:
            fh.write(json.dumps(lead.to_dict(), ensure_ascii=False) + "\n")
    return len(leads)
