"""GEO recommendations escalate priority as visibility weakens."""

from __future__ import annotations

from dealix.hermes.ai_visibility_product.geo_recommendations import recommend
from dealix.hermes.ai_visibility_product.trust_signal_score import TrustSignalScore


def test_absent_band_returns_critical_priority() -> None:
    s = TrustSignalScore(customer_id="cust_1", mentions=0, citations=0, score=0.0, band="absent")
    rec = recommend(s)
    assert rec.priority == "critical"
    assert rec.actions
