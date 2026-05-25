from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CompanyProfile:
    name: str
    url: str
    description: str
    industry: str
    locale: str = "ar-SA"
    same_as: list[str] = field(default_factory=list)
    logo_url: str = ""
    founder: str = ""


def company_profile_jsonld(p: CompanyProfile) -> dict[str, object]:
    if not p.name or not p.url:
        raise ValueError("CompanyProfile requires name and url")
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": p.name,
        "url": p.url,
        "description": p.description,
        "industry": p.industry,
        "inLanguage": p.locale,
        "sameAs": list(p.same_as),
        "logo": p.logo_url,
        "founder": {"@type": "Person", "name": p.founder} if p.founder else None,
    }
