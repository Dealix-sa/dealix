"""Company Brain for the founder-first Dealix run.

The Company Brain is deliberately static by default so the foundation can run
in CI without secrets, live connectors, or external dependencies. Later PRs can
hydrate it from Drive, CRM, or a tenant database.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(slots=True)
class CompanyBrain:
    client_id: str
    name: str
    positioning: str
    primary_offer: str
    offers: list[str] = field(default_factory=list)
    ideal_customers: list[str] = field(default_factory=list)
    verticals: list[str] = field(default_factory=list)
    tone: str = "direct, Saudi-first, practical, proof-based"
    goals: list[str] = field(default_factory=list)
    restrictions: list[str] = field(default_factory=list)
    proof_assets: list[str] = field(default_factory=list)
    prohibited_claims: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_default_dealix_brain() -> CompanyBrain:
    """Return the safe default brain for Dealix's internal 14-day proof run."""

    return CompanyBrain(
        client_id="dealix",
        name="Dealix",
        positioning=(
            "Saudi B2B AI-native Company OS that helps companies discover, "
            "prioritize, draft, approve, execute safely, prove, and improve "
            "growth work without replacing their CRM."
        ),
        primary_offer="Revenue Command Pilot / Saudi Market Access Sprint",
        offers=[
            "Saudi Opportunity Snapshot",
            "Revenue Proof Sprint",
            "Revenue Command Pilot",
            "Saudi Market Access Sprint",
            "Partner & Distributor Desk",
            "B2G Readiness Sprint",
            "AI Company OS Setup",
            "Proof Pack / Executive Reporting",
        ],
        ideal_customers=[
            "Saudi clinics and medical centers losing WhatsApp or inquiry follow-up",
            "Training and consulting centers with unmanaged leads",
            "B2B service companies with weak follow-up discipline",
            "Foreign SaaS or B2B companies exploring Saudi market entry",
            "Suppliers needing partner or distributor mapping",
            "Companies that need B2G readiness without risky relationship claims",
        ],
        verticals=[
            "clinics",
            "training_centers",
            "saas_market_entry",
            "b2b_services",
            "logistics",
            "b2g_readiness",
            "partnerships",
        ],
        goals=[
            "Run Dealix internally for 14 days before selling full SaaS",
            "Generate qualified opportunities, drafts, approvals, and proof logs",
            "Create first paid Snapshot, Sprint, or Pilot without live automation risk",
            "Convert learning events into better targeting, offers, and playbooks",
        ],
        restrictions=[
            "draft_only_mode_required",
            "human_approval_required_for_external_actions",
            "no_cold_whatsapp",
            "no_mass_spam",
            "no_live_payment_capture",
            "no_production_mutation",
            "no_secret_exposure",
            "no_prohibited_scraping",
        ],
        proof_assets=[
            "daily_company_os_report",
            "approval_queue",
            "draft_queue",
            "proof_ledger",
            "self_improvement_report",
            "weekly_proof_pack",
        ],
        prohibited_claims=[
            "guaranteed revenue",
            "guaranteed B2G win",
            "government access",
            "fake client result",
            "fake ROI",
            "automated sending without approval",
        ],
    )
