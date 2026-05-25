"""
CitationAsset — a structured asset designed to be quoted by AI answers.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CitationAsset:
    asset_id: str
    title: str
    url: str
    citation_text: str
    source_topic: str
    last_updated_iso: str
    evidence_links: tuple[str, ...] = field(default_factory=tuple)

    def schema_org(self) -> dict[str, object]:
        return {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": self.title,
            "url": self.url,
            "datePublished": self.last_updated_iso,
            "isPartOf": {"@type": "WebSite", "name": "Dealix"},
            "citation": [{"@type": "WebPage", "url": link} for link in self.evidence_links],
        }
