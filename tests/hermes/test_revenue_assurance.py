"""Revenue assurance doctrine."""

from __future__ import annotations

from dealix.hermes.money.revenue_assurance import RevenueAssurance
from dealix.hermes.money.revenue_streams import RevenueEvent, StreamType


def test_revenue_requires_verification():
    """No 9: لا Revenue بلا Verification."""
    event = RevenueEvent(stream=StreamType.sprint, amount_sar=4999, customer_id="c1")
    assurance = RevenueAssurance()
    unverified = assurance.verify(event, payment_confirmed=False, invoice_linked=False)
    assert unverified.verified is False

    half_verified = assurance.verify(event, payment_confirmed=True, invoice_linked=False)
    assert half_verified.verified is False

    verified = assurance.verify(event, payment_confirmed=True, invoice_linked=True)
    assert verified.verified is True


def test_revenue_quality_components():
    q = RevenueAssurance.quality_score(
        margin_ratio=0.6, repeatability=0.8, retainer_potential=0.5,
        data_moat=0.4, partner_potential=0.2, delivery_burden=0.3,
    )
    # 0.25*0.6 + 0.20*0.8 + 0.20*0.5 + 0.15*0.4 + 0.10*0.2 - 0.10*0.3
    assert 0.45 <= q.score <= 0.55
