import os
from pathlib import Path

from scripts.measure_vercel_source_payload import measure

ROOT = Path(os.environ.get("DEALIX_REPO_ROOT", Path(__file__).resolve().parents[1]))
TENANT_TABLES = {
    "commercial_intelligence_sources",
    "commercial_intelligence_signals",
    "commercial_department_objectives",
    "commercial_strategic_relationships",
    "commercial_intelligence_opportunities",
    "commercial_opportunity_signals",
}


def test_all_commercial_intelligence_tables_have_rls_policy() -> None:
    policies = (ROOT / "db/rls_policies.py").read_text(encoding="utf-8")
    assert all(f'"{table}"' in policies for table in TENANT_TABLES)


def test_sales_router_registers_commercial_intelligence() -> None:
    registry = (ROOT / "api/routers/domains/sales/__init__.py").read_text(encoding="utf-8")
    assert "commercial_intelligence" in registry
    assert "commercial_intelligence.router" in registry


def test_migration_has_real_evidence_edges_and_linear_parent() -> None:
    migration = (
        ROOT / "db/migrations/versions/20260715_017_commercial_intelligence_graph.py"
    ).read_text(encoding="utf-8")
    assert 'down_revision: Union[str, None] = "20260715_016_company_targeting"' in migration
    assert '"commercial_opportunity_signals"' in migration
    assert 'sa.ForeignKey("commercial_intelligence_signals.id"' in migration
    assert 'sa.ForeignKey("commercial_intelligence_opportunities.id"' in migration


def test_router_has_no_external_dispatch_path() -> None:
    router = (ROOT / "api/routers/commercial_intelligence.py").read_text(encoding="utf-8")
    assert '"external_action_allowed": False' in router
    assert '"/opportunities/{opportunity_id}/buyer-decision-plan"' in router
    assert "PricingDecision.CATALOG_RECONCILIATION_REQUIRED" in router
    for forbidden in ("send_email(", "send_whatsapp(", "dispatch_provider(", "charge_customer("):
        assert forbidden not in router


def test_commercial_intelligence_ui_exposes_internal_buyer_decision_plan() -> None:
    page = (ROOT / "apps/web/app/commercial-intelligence/page.tsx").read_text(encoding="utf-8")
    api_client = (ROOT / "apps/web/lib/api.ts").read_text(encoding="utf-8")

    assert "Buyer Decision Spine · Internal draft" in page
    assert "postCommercialIntelligenceBuyerDecisionPlan" in page
    assert "price_included" in page
    assert "external_action_allowed" in page
    assert "/buyer-decision-plan" in api_client


def test_vercel_source_input_is_within_budget() -> None:
    result = measure()
    assert result["within_source_budget"] is True
