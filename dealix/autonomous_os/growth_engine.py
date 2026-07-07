"""
Growth Engine — the commercial brain of the Autonomous OS.

Given a light context signal (pipeline counts, warm-list size, recent proof
assets) it proposes prioritised, *draft-only* commercial actions mapped to the
Dealix offer ladder. It answers: "given where we are, what is the highest-
leverage commercial draft to prepare today?" — never "send this".

All outputs are hypotheses framed with "we expect / the goal is / we will
measure" language — no guaranteed-ROI claims, no fabricated numbers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# Dealix offer ladder (id -> label, indicative price band in SAR).
OFFER_LADDER: dict[str, dict[str, Any]] = {
    "free_diagnostic": {"label": "Free Diagnostic", "band": "0"},
    "micro_sprint": {"label": "Micro Sprint", "band": "499"},
    "data_pack": {"label": "Data Pack", "band": "1,500"},
    "managed_ops": {"label": "Managed Ops", "band": "2,999-4,999/mo"},
    "transformation_diagnostic_sprint": {
        "label": "Transformation Diagnostic Sprint",
        "band": "7,500-25,000",
    },
    "custom_enterprise": {"label": "Custom Enterprise System", "band": "25,000-100,000+"},
}


@dataclass
class GrowthContext:
    """Minimal signal used to prioritise. All optional with safe defaults so
    the engine runs even with no CRM data available."""

    warm_leads: int = 0
    active_conversations: int = 0
    proposals_outstanding: int = 0
    proof_assets_ready: int = 0
    booked_sprints: int = 0

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> "GrowthContext":
        d = d or {}
        return cls(
            warm_leads=int(d.get("warm_leads", 0) or 0),
            active_conversations=int(d.get("active_conversations", 0) or 0),
            proposals_outstanding=int(d.get("proposals_outstanding", 0) or 0),
            proof_assets_ready=int(d.get("proof_assets_ready", 0) or 0),
            booked_sprints=int(d.get("booked_sprints", 0) or 0),
        )


@dataclass
class GrowthAction:
    title: str
    rationale: str
    offer: str
    priority: int
    kind: str  # internal | external_draft
    channel: str | None = None
    kpis: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "rationale": self.rationale,
            "offer": self.offer,
            "offer_label": OFFER_LADDER.get(self.offer, {}).get("label", self.offer),
            "price_band_sar": OFFER_LADDER.get(self.offer, {}).get("band", ""),
            "priority": self.priority,
            "kind": self.kind,
            "channel": self.channel,
            "kpis": self.kpis,
        }


class GrowthEngine:
    """Deterministic commercial prioritiser. Draft-only recommendations."""

    def recommend(self, ctx: GrowthContext) -> list[GrowthAction]:
        actions: list[GrowthAction] = []

        # 1. If proof assets exist but no sprints booked, package proof into a
        #    sprint proposal — highest commercial leverage.
        if ctx.proof_assets_ready > 0 and ctx.booked_sprints == 0:
            actions.append(
                GrowthAction(
                    title="Draft Transformation Sprint proposals from ready proof assets",
                    rationale=(
                        "We have proof assets and no booked sprint yet; the goal is to "
                        "convert existing evidence into concrete sprint proposals we can "
                        "review and send after approval."
                    ),
                    offer="transformation_diagnostic_sprint",
                    priority=95,
                    kind="internal",
                    kpis=["proposals_drafted", "sprint_bookings"],
                )
            )

        # 2. Outstanding proposals with active conversations -> follow-up drafts.
        if ctx.proposals_outstanding > 0 and ctx.active_conversations > 0:
            actions.append(
                GrowthAction(
                    title="Prepare approval-gated follow-up drafts for open proposals",
                    rationale=(
                        "Open proposals with live conversations decay without follow-up; "
                        "we will prepare per-account WhatsApp/email follow-up drafts for "
                        "founder approval (no auto-send)."
                    ),
                    offer="transformation_diagnostic_sprint",
                    priority=85,
                    kind="external_draft",
                    channel="whatsapp",
                    kpis=["reply_rate", "proposals_advanced"],
                )
            )

        # 3. Warm leads but few conversations -> low-friction entry offer draft.
        if ctx.warm_leads > 0 and ctx.active_conversations < ctx.warm_leads:
            actions.append(
                GrowthAction(
                    title="Draft Free Diagnostic invitations for warm, opted-in leads",
                    rationale=(
                        "Warm opted-in leads are under-activated; the goal is to draft "
                        "Free Diagnostic invitations (draft-only, approval-first) to open "
                        "conversations without any cold outreach."
                    ),
                    offer="free_diagnostic",
                    priority=70,
                    kind="external_draft",
                    channel="whatsapp",
                    kpis=["diagnostics_booked"],
                )
            )

        # 4. Always-on: keep the proof/content engine warm (internal, safe).
        actions.append(
            GrowthAction(
                title="Draft one new proof/content asset (bilingual AR/EN)",
                rationale=(
                    "A steady proof/content cadence compounds trust; we will draft one "
                    "reviewable asset today and measure engagement after approval."
                ),
                offer="data_pack",
                priority=40,
                kind="internal",
                kpis=["assets_drafted", "engagement"],
            )
        )

        actions.sort(key=lambda a: -a.priority)
        return actions
