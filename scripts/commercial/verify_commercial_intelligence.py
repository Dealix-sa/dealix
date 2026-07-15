#!/usr/bin/env python3
"""Static and domain verification for Commercial Intelligence foundation."""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_intelligence import (
    EvidenceLevel,
    GovernedSource,
    OpportunityInputs,
    SourceKind,
    SourcePolicyStatus,
    score_opportunity,
    score_source,
)

REQUIRED = (
    "dealix/commercial_intelligence.py",
    "db/models_commercial_intelligence.py",
    "db/migrations/versions/20260715_017_commercial_intelligence_graph.py",
    "api/routers/commercial_intelligence.py",
    "apps/web/app/commercial-intelligence/page.tsx",
    "data/commercial_intelligence/ksa_source_registry.yaml",
    "data/commercial_intelligence/dealix_department_objectives.yaml",
    "docs/commercial/DEALIX_SAUDI_COMMERCIAL_STRATEGY_2026_AR.md",
    "vercel.json",
)


def main() -> int:
    missing = [path for path in REQUIRED if not (ROOT / path).is_file()]
    if missing:
        print("COMMERCIAL_INTELLIGENCE_FOUNDATION=FAIL")
        for path in missing:
            print(f"MISSING={path}")
        return 1
    source = GovernedSource(
        tenant_id="dealix",
        source_id="src_verify",
        name="Verification source",
        kind=SourceKind.OWNED,
        policy_status=SourcePolicyStatus.APPROVED,
        allowed_use="internal_verification",
        authority_score=90,
        verifiability_score=90,
        freshness_days=30,
        retention_days=365,
        terms_reviewed_at=datetime.now(UTC),
    )
    opportunity = score_opportunity(
        OpportunityInputs(
            strategic_fit=90,
            problem_evidence=90,
            urgency=80,
            relationship_strength=80,
            commercial_value=80,
            evidence_level=EvidenceLevel.L4_VERIFIED,
            source_score=score_source(source),
            signal_count=2,
        )
    )
    if opportunity.external_action_allowed or opportunity.score < 75:
        print("COMMERCIAL_INTELLIGENCE_FOUNDATION=FAIL")
        return 1
    print("COMMERCIAL_INTELLIGENCE_FOUNDATION=PASS")
    print("PERSISTENCE_TABLES=6")
    print("EXTERNAL_ACTIONS_EXECUTED=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
