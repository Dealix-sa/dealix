"""File-backed Opportunity Graph store for safe local/CI runs."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .models import CompanyRecord, OpportunityRecord, SignalRecord
from .scoring import score_opportunity


class OpportunityGraphStore:
    def __init__(self, root: Path | str = "data/company_os") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.path = self.root / "opportunity_graph.json"

    def write(self, payload: dict[str, Any]) -> Path:
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return self.path

    def read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"companies": [], "signals": [], "opportunities": []}
        return json.loads(self.path.read_text(encoding="utf-8"))


def seed_dealix_opportunities(limit: int = 50) -> dict[str, Any]:
    """Create deterministic seed opportunities for the first internal proof run."""

    seed_rows = [
        ("clinic-riyadh-001", "Riyadh Specialty Clinic", "clinics", "Revenue Command Pilot", "Likely patient inquiry and WhatsApp follow-up leakage", 84),
        ("training-001", "Riyadh Training Center", "training_centers", "Revenue Command Pilot", "Enrollment leads often need structured follow-up", 78),
        ("saas-uk-001", "UK B2B SaaS entering MENA", "saas_market_entry", "Saudi Market Access Sprint", "Foreign SaaS needs Saudi account and partner mapping", 82),
        ("b2b-services-001", "Local B2B Services Firm", "b2b_services", "Revenue Proof Sprint", "Proposal and follow-up discipline can be improved", 72),
        ("supplier-001", "Industrial Supplier", "partnerships", "Partner & Distributor Desk", "Potential Saudi distributor or channel partnership need", 69),
        ("b2g-ready-001", "Enterprise Tech Vendor", "b2g_readiness", "B2G Readiness Sprint", "Needs readiness assets, not risky relationship claims", 75),
    ]
    rows = seed_rows[: max(1, min(len(seed_rows), limit))]
    companies: list[CompanyRecord] = []
    signals: list[SignalRecord] = []
    opportunities: list[OpportunityRecord] = []
    for index, (company_id, name, sector, offer, reason, base_score) in enumerate(rows, start=1):
        companies.append(CompanyRecord(id=company_id, name=name, sector=sector, confidence=0.75))
        signals.append(
            SignalRecord(
                id=f"sig-{company_id}",
                company_id=company_id,
                signal_type="seed_market_signal",
                description=reason,
                confidence=0.75,
            )
        )
        scored = score_opportunity(
            fit=base_score,
            signal=base_score - 3,
            urgency=70,
            value=75,
            access=65,
            risk=10,
        )
        opportunities.append(
            OpportunityRecord(
                id=f"opp-{index:03d}",
                company_id=company_id,
                company_name=name,
                vertical=sector,
                offer_match=offer,
                reason=reason,
                score=scored,
                evidence=["seeded_for_internal_founder_proof_run"],
            )
        )
    return {
        "companies": [asdict(item) for item in companies],
        "signals": [asdict(item) for item in signals],
        "opportunities": [asdict(item) for item in opportunities],
    }
