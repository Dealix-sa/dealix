"""Growth OS integrity verifier.

Imports every Growth OS submodule, asserts core invariants, and runs
``enforce_all`` on a synthetic batch. Prints a verdict line consumable by
the bash wrapper.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path
from typing import Any

# Ensure the repository root is on sys.path when invoked directly.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _step(name: str) -> None:
    print(f"[growth_os] {name}")


def main() -> int:
    failures: list[str] = []

    try:
        _step("import subpackages")
        from dealix.growth_os import (
            abm,
            attribution,
            brand,
            case_studies,
            content_engine,
            dashboard,
            experiments,
            funnels,
            geo,
            icp,
            partners,
            revenue_assurance,
            revenue_proof,
            streams,
        )
        from dealix.growth_os import operating_rules as ops_rules
    except Exception:
        failures.append("import_failure")
        traceback.print_exc()
        print("DEALIX_GROWTH_OS_VERDICT=FAIL")
        return 1

    try:
        _step("ICP integrity")
        from dealix.growth_os.icp.matrix import ICP_MATRIX
        assert len(ICP_MATRIX) == 7, f"expected 7 ICPs, got {len(ICP_MATRIX)}"
    except Exception:
        failures.append("icp_integrity")
        traceback.print_exc()

    try:
        _step("GEO pages integrity")
        from dealix.growth_os.geo.pages_registry import GEO_PAGES
        required = {
            "/ai-governance-saudi-companies",
            "/agentic-control-plane",
            "/ai-revenue-hunter",
            "/agency-ai-white-label",
            "/ai-agents-permissions-approvals",
            "/mcp-risk-review",
        }
        assert required == set(GEO_PAGES.keys())
    except Exception:
        failures.append("geo_pages")
        traceback.print_exc()

    try:
        _step("Revenue proof doctrine")
        from dealix.growth_os.revenue_proof.proof_rules import is_real_revenue
        from dealix.growth_os.revenue_proof.revenue_record import RevenueRecord
        rec = RevenueRecord(
            record_id="rev_check",
            customer_id="cust_001",
            offer_key="x",
            amount_usd=100.0,
            status="paid",
            verification=None,
        )
        assert is_real_revenue(rec) is False, "vanity status must be rejected"
    except Exception:
        failures.append("revenue_proof_doctrine")
        traceback.print_exc()

    try:
        _step("enforce_all on sample batch")
        batch: dict[str, list[dict[str, Any]]] = {
            "campaign": [{"id": "c1"}],
            "content": [{"title": "t"}],
            "revenue": [{"record_id": "r1"}],
        }
        violations = ops_rules.enforce_all(batch)
        assert "campaign" in violations, "campaign violation expected"
        assert "content" in violations, "content violation expected"
        assert "revenue" in violations, "revenue violation expected"
    except Exception:
        failures.append("enforce_all")
        traceback.print_exc()

    try:
        _step("Streams portfolio integrity")
        from dealix.growth_os.streams.portfolio import (
            REVENUE_PORTFOLIO,
            STREAM_BUCKETS,
        )
        assert set(STREAM_BUCKETS) == {
            "fast",
            "monthly",
            "partner",
            "enterprise",
            "platform",
        }
        assert len(REVENUE_PORTFOLIO.streams) >= 25
    except Exception:
        failures.append("streams_portfolio")
        traceback.print_exc()

    try:
        _step("Brand positioning bilingual")
        from dealix.growth_os.brand.positioning import BRAND_POSITIONING
        assert BRAND_POSITIONING.hero_line.ar and BRAND_POSITIONING.hero_line.en
        assert len(BRAND_POSITIONING.audiences) == 4
    except Exception:
        failures.append("brand_positioning")
        traceback.print_exc()

    if failures:
        print(f"FAILURES={','.join(failures)}")
        print("DEALIX_GROWTH_OS_VERDICT=FAIL")
        return 1

    print("DEALIX_GROWTH_OS_VERDICT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
