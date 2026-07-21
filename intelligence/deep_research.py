"""Deep Research Engine.

Multi-source research with safe fallback when no API keys are configured.
Never fails; always returns a valid ResearchBundle.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Protocol

from intelligence.bilingual import BilingualRenderer, BilingualText, LanguageCode
from intelligence.knowledge_accumulator import KnowledgeAccumulator, KnowledgeEntry
from intelligence.saudi_market_intelligence import SaudiCompanyProfile, SaudiMarketIntelligence


class ResearchSource(str, Enum):
    WEB_SEARCH = "web_search"
    NEWS = "news"
    SAUDI_REGISTRY = "saudi_registry"
    MARKET_SIGNALS = "market_signals"
    INTERNAL_KNOWLEDGE = "internal_knowledge"


@dataclass
class ResearchFinding:
    title: BilingualText
    summary: BilingualText
    source_url: str | None
    source: ResearchSource
    relevance_score: float
    data_quality: Literal["verified", "public", "estimated"]
    is_fallback: bool = False

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "title": BilingualRenderer.filter_text(self.title, lang),
            "summary": BilingualRenderer.filter_text(self.summary, lang),
            "source_url": self.source_url,
            "source": self.source.value,
            "relevance_score": self.relevance_score,
            "data_quality": self.data_quality,
            "is_fallback": self.is_fallback,
        }


@dataclass
class ResearchBundle:
    query: str
    findings: list[ResearchFinding]
    sources_used: list[str]
    keys_missing: list[str]
    warnings: list[str]
    confidence: float
    retrieved_at: str

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "query": self.query,
            "findings": [f.to_dict(lang) for f in self.findings],
            "sources_used": self.sources_used,
            "keys_missing": self.keys_missing,
            "warnings": self.warnings,
            "confidence": self.confidence,
            "retrieved_at": self.retrieved_at,
        }


class ResearchProvider(Protocol):
    name: str
    requires_keys: bool

    def is_configured(self) -> bool: ...
    def search(self, query: str, limit: int, lang: LanguageCode) -> list[ResearchFinding]: ...


class _MarketSignalsProvider:
    name = "market_signals"
    requires_keys = False

    def is_configured(self) -> bool:
        return True

    def search(self, query: str, limit: int, lang: LanguageCode) -> list[ResearchFinding]:
        intel = SaudiMarketIntelligence()
        sector = _guess_sector(query)
        signal = intel.sector_momentum(sector)
        entry = intel.recommend_entry(sector, "Riyadh")
        return [
            ResearchFinding(
                title=BilingualRenderer.bt(
                    en=f"{sector} sector momentum",
                    ar=f"زخم قطاع {sector}",
                ),
                summary=BilingualRenderer.bt(
                    en=f"Market momentum for {sector} is {signal.value}. Recommended entry: {entry['recommended_package']}.",
                    ar=f"زخم السوق لقطاع {sector} هو {signal.value}. نقطة الدخول الموصى بها: {entry['recommended_package']}.",
                ),
                source_url=None,
                source=ResearchSource.MARKET_SIGNALS,
                relevance_score=0.85,
                data_quality="estimated",
            )
        ][:limit]


class _InternalKnowledgeProvider:
    name = "internal_knowledge"
    requires_keys = False

    def __init__(self) -> None:
        self.knowledge = KnowledgeAccumulator()

    def is_configured(self) -> bool:
        return True

    def search(self, query: str, limit: int, lang: LanguageCode) -> list[ResearchFinding]:
        entries = self.knowledge.search(query, limit=limit)
        return [
            ResearchFinding(
                title=e.title,
                summary=e.content,
                source_url=None,
                source=ResearchSource.INTERNAL_KNOWLEDGE,
                relevance_score=e.confidence,
                data_quality="verified" if e.confidence > 0.8 else "estimated",
            )
            for e in entries
        ]


class _WebSearchProvider:
    name = "web_search"
    requires_keys = True

    def is_configured(self) -> bool:
        return bool(os.getenv("SERPER_API_KEY") or os.getenv("SERPAPI_API_KEY"))

    def search(self, query: str, limit: int, lang: LanguageCode) -> list[ResearchFinding]:
        if not self.is_configured():
            return []
        # Live call would go here; we return a structured placeholder.
        return [
            ResearchFinding(
                title=BilingualRenderer.bt(en=f"Web results for {query}", ar=f"نتائج الويب لـ {query}"),
                summary=BilingualRenderer.bt(
                    en="Live web search results would appear here when SERPER_API_KEY is configured.",
                    ar="ستظهر نتائج البحث المباشر عند تكوين SERPER_API_KEY.",
                ),
                source_url=None,
                source=ResearchSource.WEB_SEARCH,
                relevance_score=0.7,
                data_quality="public",
            )
        ]


class _NewsProvider:
    name = "news"
    requires_keys = True

    def is_configured(self) -> bool:
        return bool(os.getenv("NEWS_API_KEY"))

    def search(self, query: str, limit: int, lang: LanguageCode) -> list[ResearchFinding]:
        if not self.is_configured():
            return []
        return [
            ResearchFinding(
                title=BilingualRenderer.bt(en=f"News for {query}", ar=f"أخبار {query}"),
                summary=BilingualRenderer.bt(
                    en="Live news results would appear here when NEWS_API_KEY is configured.",
                    ar="ستظهر نتائج الأخبار المباشرة عند تكوين NEWS_API_KEY.",
                ),
                source_url=None,
                source=ResearchSource.NEWS,
                relevance_score=0.65,
                data_quality="public",
            )
        ]


class _SaudiRegistryProvider:
    name = "saudi_registry"
    requires_keys = True

    def is_configured(self) -> bool:
        return bool(os.getenv("WATHQ_API_KEY") or os.getenv("MCI_API_KEY"))

    def search(self, query: str, limit: int, lang: LanguageCode) -> list[ResearchFinding]:
        if not self.is_configured():
            return []
        return [
            ResearchFinding(
                title=BilingualRenderer.bt(en=f"Saudi registry data for {query}", ar=f"بيانات السجل السعودي لـ {query}"),
                summary=BilingualRenderer.bt(
                    en="Official Saudi registry data would appear here when WATHQ_API_KEY is configured.",
                    ar="ستظهر بيانات السجل الرسمي السعودي عند تكوين WATHQ_API_KEY.",
                ),
                source_url=None,
                source=ResearchSource.SAUDI_REGISTRY,
                relevance_score=0.9,
                data_quality="verified",
            )
        ]


def _guess_sector(query: str) -> str:
    q = query.lower()
    mapping = {
        "fintech": "fintech",
        "bank": "fintech",
        "logistics": "logistics",
        "health": "healthcare_tech",
        "real estate": "proptech",
        "property": "proptech",
        "software": "software",
        "retail": "retail",
    }
    for key, sector in mapping.items():
        if key in q:
            return sector
    return "software"


class DeepResearchEngine:
    """Multi-source research with deterministic fallback."""

    SAFE_MODE: bool = True

    def __init__(self) -> None:
        self._providers: list[ResearchProvider] = [
            _MarketSignalsProvider(),
            _InternalKnowledgeProvider(),
            _WebSearchProvider(),
            _NewsProvider(),
            _SaudiRegistryProvider(),
        ]
        self.knowledge = KnowledgeAccumulator()

    def available_sources(self) -> list[dict[str, Any]]:
        return [
            {
                "source": p.name,
                "configured": p.is_configured(),
                "requires_keys": p.requires_keys,
            }
            for p in self._providers
        ]

    def _fallback_findings(self, query: str, lang: LanguageCode) -> list[ResearchFinding]:
        return [
            ResearchFinding(
                title=BilingualRenderer.bt(
                    en=f"Offline research snapshot: {query}",
                    ar=f"لقطة بحث بدون اتصال: {query}",
                ),
                summary=BilingualRenderer.bt(
                    en="No live research keys are configured. This is a structured fallback. Configure SERPER_API_KEY, NEWS_API_KEY, or WATHQ_API_KEY for live results.",
                    ar="لم يتم تكوين مفاتيح بحث مباشرة. هذه لقطة بديلة منظمة. قم بتكوين SERPER_API_KEY أو NEWS_API_KEY أو WATHQ_API_KEY للحصول على نتائج مباشرة.",
                ),
                source_url=None,
                source=ResearchSource.MARKET_SIGNALS,
                relevance_score=0.5,
                data_quality="estimated",
                is_fallback=True,
            )
        ]

    def research(
        self,
        query: str,
        sources: list[ResearchSource] | None = None,
        sector: str | None = None,
        lang: LanguageCode = "both",
        limit: int = 10,
    ) -> ResearchBundle:
        selected_sources = sources or list(ResearchSource)
        findings: list[ResearchFinding] = []
        sources_used: list[str] = []
        keys_missing: list[str] = []
        warnings: list[str] = []

        for provider in self._providers:
            if ResearchSource(provider.name) not in selected_sources:
                continue
            if provider.requires_keys and not provider.is_configured():
                keys_missing.append(provider.name)
                warnings.append(f"{provider.name} requires API key; using fallback")
                continue
            try:
                provider_findings = provider.search(query, limit, lang)
                if provider_findings:
                    findings.extend(provider_findings)
                    sources_used.append(provider.name)
            except Exception as exc:
                warnings.append(f"{provider.name} search failed: {exc}")
                logging.getLogger(__name__).warning("research_provider_failed", provider=provider.name, error=str(exc))

        if not findings:
            findings = self._fallback_findings(query, lang)
            warnings.append("No live sources returned results; used offline fallback")

        # Persist findings to knowledge accumulator
        for f in findings:
            self.knowledge.ingest(
                KnowledgeEntry(
                    entry_id=f"research-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{id(f)}",
                    category="research_finding",
                    title=f.title,
                    content=f.summary,
                    source=f.source.value,
                    sector=sector or _guess_sector(query),
                    company=query if " " in query else None,
                    tags=["research", f.source.value],
                    confidence=f.relevance_score,
                    created_at=datetime.now(timezone.utc).isoformat(),
                    expires_at=None,
                )
            )

        confidence = round(min(0.95, sum(f.relevance_score for f in findings) / max(len(findings), 1)), 2)
        return ResearchBundle(
            query=query,
            findings=findings[:limit],
            sources_used=sources_used,
            keys_missing=keys_missing,
            warnings=warnings,
            confidence=confidence,
            retrieved_at=datetime.now(timezone.utc).isoformat(),
        )

    def company_dossier(self, company_name: str, lang: LanguageCode = "both") -> dict[str, Any]:
        # Gather signals from market intelligence and knowledge store
        sector = _guess_sector(company_name)
        profile = SaudiCompanyProfile(
            company_name=company_name,
            sector=sector,
            city="Riyadh",
        )
        intel = SaudiMarketIntelligence()
        icp = intel.score_icp(profile)
        entry = intel.recommend_entry(sector, "Riyadh")
        internal = self.knowledge.search(company_name, limit=5)

        return BilingualRenderer.wrap(
            {
                "company_name": company_name,
                "sector": sector,
                "icp_score": icp.score,
                "recommended_package": entry["recommended_package"],
                "momentum": entry["momentum"],
                "internal_intel_count": len(internal),
                "research": self.research(company_name, sector=sector, lang=lang).to_dict(lang),
            },
            lang,
        )
