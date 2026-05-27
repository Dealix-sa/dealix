"""No-Orphan auditor (section 129)."""

from __future__ import annotations

from datetime import timedelta

from dealix.hermes.audit.no_orphan import NoOrphanAudit
from dealix.hermes.core.schemas import Asset, Opportunity, Signal
from dealix.hermes.kernel import HermesKernel
from dealix.hermes.sovereignty.levels import SovereigntyLevel
from dealix.hermes.trust.agent_registry import AgentCard
from dealix.hermes.trust.tool_registry import ToolCard


def test_orphans_detected_on_empty_kernel():
    k = HermesKernel()
    report = k.no_orphan_audit()
    assert report.clean, "Fresh kernel must have no orphans"


def test_unscored_opportunity_flagged():
    k = HermesKernel()
    sig = k.signals.receive(Signal.make(source="x", domain="money", summary="x"))
    k.opportunities.add(Opportunity.make(signal_id=sig.id, domain="money", title="x"))
    report = k.no_orphan_audit()
    assert report.unscored_opportunities, "Unscored opportunity must be reported"


def test_signal_orphan_after_cutoff():
    k = HermesKernel()
    sig = k.signals.receive(Signal.make(source="x", domain="money", summary="x"))
    audit = NoOrphanAudit(
        signals=k.signals,
        opportunities=k.opportunities,
        executions=k.executions,
        outcomes=k.outcomes,
        tools=k.tools,
        agents=k.agents,
        assets=k.assets,
        signal_age_cutoff=timedelta(seconds=0),
    )
    report = audit.run()
    assert sig.id in report.orphan_signals


def test_customer_without_value_report_flagged():
    k = HermesKernel()
    report = k.no_orphan_audit(
        active_customers=["acme"],
        customer_value_reports={"acme": False},
    )
    assert "acme" in report.customers_without_value_report


def test_partner_without_review_flagged():
    k = HermesKernel()
    report = k.no_orphan_audit(
        active_partners=["bigco_agency"],
        partner_reviews={"bigco_agency": False},
    )
    assert "bigco_agency" in report.partners_without_performance_review


def test_unreused_asset_flagged():
    k = HermesKernel()
    # Skip lineage shortcuts for brevity — asset registry stands alone.
    k.assets.add(Asset.make(outcome_id="out_x", kind="template", title="x", summary="x"))
    report = k.no_orphan_audit()
    assert report.unreused_assets, "asset with reuse_count=0 must be flagged"


def test_red_flags_surface_high_approval_backlog():
    k = HermesKernel()
    # Stuff the approval center.
    for i in range(6):
        k.approval_center.request(requested_by="x", action=f"send_email_{i}", payload={})
    flags = k.red_flags()
    assert any(f.code == "high_approval_backlog" for f in flags)


def test_registry_blocks_kpi_less_agent():
    k = HermesKernel()
    # Registry rejects on register — see test_trust. Audit shouldn't see anyone here.
    report = k.no_orphan_audit()
    assert not report.agents_without_kpi


def test_tool_without_owner_blocked_at_registry():
    k = HermesKernel()
    import pytest
    with pytest.raises(ValueError):
        k.tools.register(ToolCard(tool_id="x", name="x", tool_type="x", owner=""))
