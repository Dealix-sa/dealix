"""Convert a market trend signal into a proposed Offer skeleton."""

from __future__ import annotations

from dealix.hermes.core.schemas import Signal


class TrendToOffer:
    def propose(self, signal: Signal) -> dict:
        sector = signal.payload.get("sector", "general")
        intent = signal.payload.get("intent", "offer")
        return {
            "buyer": f"{sector} CEO/CFO",
            "pain": signal.summary,
            "promise": f"Convert {signal.payload.get('kind','signal')} into measurable revenue.",
            "deliverables": ["Diagnostic", "Pilot pack", "First 30 targets"],
            "metric": "qualified meetings within 30 days",
            "upsell": "Managed Ops retainer",
            "trust_risks": ["data scope", "external send"],
            "domain": signal.domain,
            "intent": intent,
        }


__all__ = ["TrendToOffer"]
