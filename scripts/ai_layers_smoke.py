"""AI Layers smoke test — runs the full 9-layer pipeline against a synthetic
context and verifies every result carries a governance_decision.

Usage:
    python scripts/ai_layers_smoke.py [--json]

Exits 0 on success, non-zero on doctrine violation.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Allow running this script from any cwd.
_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.ai_layers import (  # noqa: E402
    AI_LAYERS,
    LayerContext,
    run_pipeline,
)


def _synthetic_ctx() -> LayerContext:
    return LayerContext(
        customer_id="smoke_co",
        payload={
            # lead_scoring signals
            "title_founder_exec": True,
            "b2b_company": True,
            "crm_or_pipeline": True,
            "uses_or_plans_ai": True,
            "saudi_or_gcc": True,
            # account_scoring
            "account_name": "Smoke Account",
            "icp_signals": {
                "saudi_b2b": True,
                "size_50_500_emp": True,
                "has_data_owner": True,
                "uses_crm": True,
                "has_ai_budget": True,
            },
            "readiness_signals": {
                "data_available": True,
                "owner_present": True,
                "accepts_governance": True,
                "workflow_pain_clear": True,
            },
            "estimated_acv_sar": 5_000,
            # content_generation
            "topic": "Revenue Intelligence Sprint",
            "audience": "fintech",
            "cta": "Reply to schedule a free diagnostic.",
            "locales": ["ar", "en"],
            # decision_passport
            "action": "send_diagnostic_email",
            "evidence_refs": ["proof://pack/PP-smoke"],
            "risk_class": "L1",
            # compliance_reasoning
            "contains_pii": False,
            "lawful_basis": None,
            "data_classification": "internal",
            "processing_region": "sa",
            # proof_curation
            "sector": "saas",
            "stage": "diagnosis",
            "artifacts": [
                {
                    "id": "PE-1",
                    "type": "proof_example",
                    "tier": "verified",
                    "source_ref": "proof://1",
                    "summary": "case-safe pattern",
                },
                {
                    "id": "SR-1",
                    "type": "scoring_rule",
                    "tier": "observed",
                    "source_ref": "rule://1",
                    "summary": "scoring rule",
                },
            ],
            # customer_health
            "adoption_pct": 75,
            "usage_last_7d": 8,
            "friction_high_severity_14d": 1,
            "last_value_event_tier": "observed",
            # growth_signals
            "signals": [
                {
                    "kind": "warm_intro",
                    "timestamp": "2026-05-22T10:00:00Z",
                    "account_hint": "Smoke",
                    "source_ref": "intro://founder/2026-05-22",
                },
                {
                    "kind": "referral",
                    "timestamp": "2026-05-23T10:00:00Z",
                    "account_hint": "Smoke2",
                    "source_ref": "ref://founder/2026-05-23",
                },
            ],
            # executive_intelligence inputs (composite mode)
            "customer_health_composite": 75,
            "proof_artifact_count_sourced": 2,
            "growth_signal_acceptance_pct": 100,
            "compliance_overall": "ALLOW",
            "partnership_active_count": 1,
        },
        source_refs=("founder://warm_list/smoke",),
        actor="ai-layers-smoke",
        external_action_requested=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit JSON result")
    args = parser.parse_args()

    ctx = _synthetic_ctx()
    result = run_pipeline(ctx)

    # Doctrine: every layer must have a governance_decision.
    missing: list[str] = []
    for layer_name in AI_LAYERS:
        r = result.results.get(layer_name)
        if r is None or not r.governance_decision:
            missing.append(layer_name)

    if args.json:
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"Layers run: {len(result.layers_run)}")
        print(f"Overall decision: {result.overall_decision}")
        print(f"Blocked layers: {list(result.blocked_layers)}")
        for layer_name, r in result.results.items():
            print(f"  - {layer_name}: {r.governance_decision} (ok={r.ok})")

    if missing:
        print(f"\nDOCTRINE VIOLATION: missing governance_decision on: {missing}",
              file=sys.stderr)
        return 2

    if result.overall_decision == "BLOCK":
        print("\nSMOKE BLOCK: pipeline overall_decision=BLOCK (review per-layer)",
              file=sys.stderr)
        return 1

    print("\nAI_LAYERS_SMOKE_VERDICT=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
