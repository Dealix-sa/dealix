"""
Citation assets — pieces of content designed to be quoted by AI engines.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CitationAsset:
    asset_id: str
    title: str
    canonical_url: str
    structured_data_present: bool
    machine_readable_summary: str
    last_verified_iso: str


def is_citation_ready(asset: CitationAsset) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if not asset.canonical_url:
        issues.append("missing_canonical_url")
    if not asset.structured_data_present:
        issues.append("missing_structured_data")
    if len(asset.machine_readable_summary.split()) < 40:
        issues.append("summary_too_short")
    if not asset.last_verified_iso:
        issues.append("missing_last_verified")
    return not issues, issues
