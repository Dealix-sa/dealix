"""Deterministic segment classification for the Saudi Opportunity Graph.

Maps a company's fields to one of the eight Dealix segments. Pure and
order-sensitive: the first matching rule wins, so the most specific rules
come first.
"""

from __future__ import annotations

from typing import Any

from dealix.opportunity_graph.schemas import Segment


def _text(fields: dict[str, Any]) -> str:
    parts = [
        fields.get("name"),
        fields.get("sector"),
        fields.get("company_type"),
        fields.get("saudi_signal"),
        fields.get("signal_type"),
        fields.get("pain_hypothesis"),
        fields.get("offer_match"),
        fields.get("buyer_persona"),
    ]
    return " ".join(str(p or "") for p in parts).lower()


def segment_company(fields: dict[str, Any]) -> Segment:
    blob = _text(fields)
    company_type = str(fields.get("company_type") or "").lower()
    country = str(fields.get("country") or "").lower()
    sector = str(fields.get("sector") or "").lower()

    is_foreign = company_type == "foreign" or (
        bool(country) and not any(g in country for g in ("saudi", "ksa"))
    )
    is_saudi = company_type == "saudi" or any(g in country for g in ("saudi", "ksa"))

    # ── B2G / government readiness ─────────────────────────────────────
    if any(k in blob for k in ("b2g", "government", "ministry", "authority", "public sector", "tender", "rfp")):
        return "b2g_readiness_candidate"

    # ── RHQ / partner / vendor ─────────────────────────────────────────
    if company_type in ("partner", "vendor") or any(
        k in blob for k in ("rhq", "regional headquarters", "reseller", "system integrator")
    ):
        return "rhq_vendor_or_partner_candidate"

    # ── Event / expo / tourism suppliers ───────────────────────────────
    if any(k in blob for k in ("event", "expo", "exhibition", "tourism", "hospitality", "leap", "conference")):
        return "event_expo_tourism_supplier"

    # ── Foreign plays ──────────────────────────────────────────────────
    if is_foreign:
        if any(k in blob for k in ("distributor", "reseller", "channel partner", "supplier needing")):
            return "foreign_supplier_needing_distributor"
        if any(k in blob for k in ("saas", "ai", "software", "platform", "healthtech", "fintech")):
            return "foreign_saas_ai_entering_saudi"
        if any(k in blob for k in ("supplier", "manufacturer", "industrial")):
            return "foreign_supplier_needing_distributor"

    # ── Saudi revenue-recovery plays ───────────────────────────────────
    if is_saudi:
        if any(k in sector or k in blob for k in ("clinic", "dental", "medical center", "healthcare")):
            return "saudi_clinic_revenue_leak"
        if any(
            k in sector or k in blob
            for k in ("training", "academy", "agency", "consult", "legal", "accounting", "b2b service", "logistics", "contractor")
        ):
            return "saudi_training_or_b2b_service_growth"

    return "not_fit"
