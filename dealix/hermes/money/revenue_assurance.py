"""Revenue Assurance — block phantom revenue."""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.money.revenue_streams import RevenueEvent


@dataclass(frozen=True)
class RevenueQuality:
    score: float
    margin_term: float
    repeatability_term: float
    retainer_term: float
    moat_term: float
    partner_term: float
    delivery_burden_term: float


@dataclass
class RevenueAssurance:
    """Doctrine: revenue is not real until it is paid AND verified."""

    def verify(self, event: RevenueEvent, *, payment_confirmed: bool, invoice_linked: bool) -> RevenueEvent:
        if not payment_confirmed or not invoice_linked:
            return event
        return event.model_copy(update={"verified": True})

    @staticmethod
    def quality_score(
        *,
        margin_ratio: float,
        repeatability: float,
        retainer_potential: float,
        data_moat: float,
        partner_potential: float,
        delivery_burden: float,
    ) -> RevenueQuality:
        margin = max(0.0, min(margin_ratio, 1.0)) * 0.25
        repeat = max(0.0, min(repeatability, 1.0)) * 0.20
        retainer = max(0.0, min(retainer_potential, 1.0)) * 0.20
        moat = max(0.0, min(data_moat, 1.0)) * 0.15
        partner = max(0.0, min(partner_potential, 1.0)) * 0.10
        burden = max(0.0, min(delivery_burden, 1.0)) * 0.10
        score = round(margin + repeat + retainer + moat + partner - burden, 4)
        return RevenueQuality(
            score=score,
            margin_term=margin,
            repeatability_term=repeat,
            retainer_term=retainer,
            moat_term=moat,
            partner_term=partner,
            delivery_burden_term=burden,
        )
