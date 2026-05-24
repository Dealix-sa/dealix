"""Contract: forbidden phrases from DO_NOT_SAY.md are absent from the Hypergrowth Layer.

Globs all new P0+P1 docs and asserts none contain the doctrine-forbidden
phrases. The policy file itself (`docs/founder/DO_NOT_SAY.md`) is exempt
because it must quote the phrases for enforcement.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

DOC_GLOBS = [
    "docs/founder/*.md",
    "docs/finance/*.md",
    "docs/metrics/*.md",
    "docs/people/*.md",
    "docs/strategy/DEALIX_GOAL_TREE.md",
    "docs/strategy/NORTH_STAR_METRIC.md",
    "docs/strategy/KPI_DEFINITION_DICTIONARY.md",
    "docs/strategy/BEACHHEAD_SECTOR_SCORECARD.md",
    "docs/strategy/STRATEGIC_ACCOUNT_LIST.md",
    "docs/revenue/REVENUE_LEADERSHIP_SYSTEM.md",
    "docs/revenue/PIPELINE_REVIEW_RHYTHM.md",
    "docs/revenue/DEAL_DESK_SYSTEM.md",
    "docs/revenue/PRICING_COUNCIL.md",
    "docs/revenue/WIN_LOSS_REVIEW.md",
    "docs/revenue/CLOSE_PLAN_TEMPLATE.md",
    "docs/revenue/PAYMENT_CAPTURE_OS.md",
    "docs/revenue/REVENUE_FACTORY_LIVE_DATA.md",
    "docs/enterprise/ENTERPRISE_SALES_MOTION.md",
    "docs/enterprise/PROCUREMENT_READINESS.md",
    "docs/enterprise/STAKEHOLDER_MAP.md",
    "docs/enterprise/SECURITY_REVIEW_PACKET.md",
    "docs/enterprise/ENTERPRISE_PROPOSAL_FLOW.md",
    "docs/enterprise/MULTI_THREADING_SYSTEM.md",
]

EXEMPT = {"docs/founder/DO_NOT_SAY.md"}

FORBIDDEN = [
    r"guaranteed revenue",
    r"guaranteed roi",
    r"we guarantee",
    r"we will pay you back",
    r"auto[- ]send",
    r"automated outreach",
    r"\bscraped\b",
    r"we transfer funds on behalf of",
    r"نضمن",
    r"مضمون",
]


def _collect_docs() -> list[Path]:
    out: list[Path] = []
    for pattern in DOC_GLOBS:
        out.extend(ROOT.glob(pattern))
    return [p for p in out if str(p.relative_to(ROOT)).replace("\\", "/") not in EXEMPT]


@pytest.mark.parametrize("doc", _collect_docs(), ids=lambda p: str(p.relative_to(ROOT)))
def test_no_forbidden_phrases(doc: Path) -> None:
    text = doc.read_text(encoding="utf-8").lower()
    hits = [pat for pat in FORBIDDEN if re.search(pat, text, flags=re.IGNORECASE)]
    assert not hits, f"{doc.relative_to(ROOT)} contains forbidden phrases: {hits}"


def test_at_least_one_doc_present() -> None:
    """Sanity: the doctrine test would silently pass if no docs match. Catch that."""
    docs = _collect_docs()
    assert docs, "No P0/P1 docs found — the layer is empty or globs are broken"
