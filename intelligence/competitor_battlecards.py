"""
Competitor Battlecards

Generates quick-reference competitive positioning for Saudi B2B sales.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Battlecard:
    competitor_name: str
    their_strength: str
    their_weakness: str
    dealix_differentiator: str
    talk_track: str
    objection_response: str


class CompetitorBattlecards:
    """Battlecard library for common Saudi B2B competitors."""

    CARDS: dict[str, Battlecard] = {
        "generic_crm": Battlecard(
            competitor_name="Generic CRM",
            their_strength="Broad feature set and brand recognition",
            their_weakness="Not built for Saudi market; weak Arabic/PDPL support",
            dealix_differentiator="Saudi-first AI Operating System with approval-first governance",
            talk_track="CRM tracks deals. Dealix helps you win Saudi deals with intelligence and proof.",
            objection_response="If you need a global CRM, keep it. Dealix sits on top and makes your Saudi revenue engine work.",
        ),
        "ai_chatbot_vendor": Battlecard(
            competitor_name="AI Chatbot Vendor",
            their_strength="Quick deployment of conversational bots",
            their_weakness="No revenue execution; generic responses",
            dealix_differentiator="AI recommends; deterministic workflows execute; humans approve commitments",
            talk_track="Chatbots answer questions. Dealix turns conversations into qualified revenue.",
            objection_response="A chatbot is a feature. Dealix is your commercial operating system.",
        ),
        "lead_database": Battlecard(
            competitor_name="Lead Database",
            their_strength="Large contact databases",
            their_weakness="Static data; no Saudi context or scoring",
            dealix_differentiator="Saudi ICP scoring, enrichment, and governed outreach in one flow",
            talk_track="Lists don't close deals. Scored, enriched Saudi prospects with a playbook do.",
            objection_response="You can buy data. Dealix gives you data + strategy + execution discipline.",
        ),
        "consulting_firm": Battlecard(
            competitor_name="Traditional Consulting Firm",
            their_strength="High-touch advisory and reputation",
            their_weakness="Slow, expensive, hard to productize",
            dealix_differentiator="Productized AI services with measurable delivery and repeatable pilots",
            talk_track="Consulting gives you a deck. Dealix gives you a running revenue engine.",
            objection_response="Use consultants for transformation. Use Dealix for repeatable Saudi revenue growth.",
        ),
    }

    def get(self, competitor_key: str) -> Battlecard:
        if competitor_key not in self.CARDS:
            return Battlecard(
                competitor_name=competitor_key,
                their_strength="Unknown",
                their_weakness="Unknown",
                dealix_differentiator="Dealix is Saudi-first, approval-first, and proof-driven.",
                talk_track="Let's focus on your specific use case and compare outcomes.",
                objection_response="We can run a pilot so you compare real results.",
            )
        return self.CARDS[competitor_key]

    def list_competitors(self) -> list[str]:
        return list(self.CARDS.keys())

    def to_dict(self, card: Battlecard) -> dict[str, Any]:
        return {
            "competitor_name": card.competitor_name,
            "their_strength": card.their_strength,
            "their_weakness": card.their_weakness,
            "dealix_differentiator": card.dealix_differentiator,
            "talk_track": card.talk_track,
            "objection_response": card.objection_response,
        }
