"""Pitch drafting — output only. Never send."""

from __future__ import annotations


def draft_partner_pitch(
    *,
    partner_name: str,
    partner_type: str,
    offer_name: str,
    pain: str,
    commercial_model: str,
) -> str:
    return (
        f"Subject: {offer_name} for {partner_name}\n\n"
        f"Hi {partner_name} team,\n\n"
        f"As a {partner_type} partner, your clients face: {pain}.\n"
        f"Dealix's {offer_name} ships a white-label revenue stream you can resell.\n\n"
        f"Commercial model: {commercial_model}.\n\n"
        f"If you'd like, we can run a 30-minute walkthrough next week.\n\n"
        f"— Sami, Dealix\n"
    )
