#!/usr/bin/env python3
"""Generate the Dealix growth experiment backlog (idempotent JSONL append)."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.growth._common import (  # noqa: E402
    DATA_DIR,
    append_jsonl_unique,
    ensure_dirs,
    now_iso,
)

_OUT = DATA_DIR / "experiments.jsonl"

# Starter experiments. Each is a hypothesis with two variants and a decision rule.
_EXPERIMENTS: list[dict[str, Any]] = [
    {
        "id": "exp_score_cta_label",
        "hypothesis": "Naming the CTA 'Business OS Score' lifts tool starts.",
        "variant_a": "CTA: Business OS Score",
        "variant_b": "CTA: Free Diagnostic",
        "metric": "tool_start_rate",
        "decision_rule": "Ship winner if lift >= 15% over 2 weeks.",
    },
    {
        "id": "exp_sector_hero_pain",
        "hypothesis": "Leading with sector pain raises page-to-tool conversion.",
        "variant_a": "Hero: sector pain first",
        "variant_b": "Hero: outcome framing first",
        "metric": "page_to_tool_rate",
        "decision_rule": "Ship winner if lift >= 10% over 1000 sessions.",
    },
    {
        "id": "exp_nurture_day0_subject",
        "hypothesis": "Result-focused subject beats curiosity subject on day 0.",
        "variant_a": "Subject: result-focused",
        "variant_b": "Subject: curiosity-focused",
        "metric": "email_open_rate",
        "decision_rule": "Ship winner if open lift >= 5 points.",
    },
    {
        "id": "exp_sprint_price_anchor",
        "hypothesis": "Showing the 499 SAR anchor raises sprint inquiries.",
        "variant_a": "Anchor: 499 SAR visible",
        "variant_b": "Anchor: price on request",
        "metric": "sprint_inquiry_rate",
        "decision_rule": "Ship winner if inquiries lift >= 12%.",
    },
    {
        "id": "exp_proof_post_format",
        "hypothesis": "Pattern-plus-metric posts outperform pure-pattern posts.",
        "variant_a": "Post: pattern + anonymized metric",
        "variant_b": "Post: pattern only",
        "metric": "post_save_rate",
        "decision_rule": "Ship winner if saves lift >= 20%.",
    },
    {
        "id": "exp_tool_input_count",
        "hypothesis": "Fewer inputs raise tool completion without hurting quality.",
        "variant_a": "Inputs: 4 fields",
        "variant_b": "Inputs: 6 fields",
        "metric": "tool_completion_rate",
        "decision_rule": "Ship 4-field if completion lift >= 10% and band stable.",
    },
    {
        "id": "exp_calendar_cta_day",
        "hypothesis": "Thursday CTA posts convert better than Tuesday CTA posts.",
        "variant_a": "CTA post on Thursday",
        "variant_b": "CTA post on Tuesday",
        "metric": "post_to_tool_rate",
        "decision_rule": "Ship winner if conversion lift >= 8%.",
    },
    {
        "id": "exp_diagnostic_followup_timing",
        "hypothesis": "A 24-hour follow-up beats a 72-hour follow-up.",
        "variant_a": "Follow-up at 24h",
        "variant_b": "Follow-up at 72h",
        "metric": "diagnostic_booking_rate",
        "decision_rule": "Ship winner if bookings lift >= 10%.",
    },
    {
        "id": "exp_partner_first_offer",
        "hypothesis": "Co-branded diagnostic beats flat referral fee as a first offer.",
        "variant_a": "Offer: co-branded diagnostic",
        "variant_b": "Offer: flat referral fee",
        "metric": "partner_activation_rate",
        "decision_rule": "Ship winner if activations lift >= 15%.",
    },
    {
        "id": "exp_template_gate",
        "hypothesis": "Gating a free template behind a tool start raises qualified leads.",
        "variant_a": "Template: gated by tool start",
        "variant_b": "Template: open download",
        "metric": "qualified_lead_rate",
        "decision_rule": "Ship gated if qualified rate lift >= 10%.",
    },
    {
        "id": "exp_arabic_first_copy",
        "hypothesis": "Arabic-first hero copy lifts engagement for local owners.",
        "variant_a": "Copy: Arabic first",
        "variant_b": "Copy: bilingual split",
        "metric": "scroll_depth",
        "decision_rule": "Ship winner if depth lift >= 8%.",
    },
    {
        "id": "exp_proof_trust_line",
        "hypothesis": "An explicit no-guarantee trust line raises sprint trust signals.",
        "variant_a": "Trust line present",
        "variant_b": "Trust line absent",
        "metric": "sprint_inquiry_rate",
        "decision_rule": "Ship trust line if inquiries non-negative and trust survey up.",
    },
    {
        "id": "exp_score_band_naming",
        "hypothesis": "Neutral band names beat alarmist band names.",
        "variant_a": "Bands: neutral (Developing/Partial)",
        "variant_b": "Bands: alarmist (At Risk/Critical)",
        "metric": "diagnostic_booking_rate",
        "decision_rule": "Ship neutral if bookings non-negative and complaints lower.",
    },
    {
        "id": "exp_newsletter_repurpose",
        "hypothesis": "Repurposing build logs into newsletter sections raises replies.",
        "variant_a": "Newsletter: build-log section",
        "variant_b": "Newsletter: framework section",
        "metric": "newsletter_reply_rate",
        "decision_rule": "Ship winner if replies lift >= 10%.",
    },
    {
        "id": "exp_founder_voice_note",
        "hypothesis": "A founder voice-note script lifts nurture engagement.",
        "variant_a": "Asset: founder voice note",
        "variant_b": "Asset: text-only message",
        "metric": "nurture_engagement_rate",
        "decision_rule": "Ship winner if engagement lift >= 12%.",
    },
]


def build_records() -> list[dict[str, Any]]:
    """Return backlog records sorted by id, each stamped with status and created."""
    created = now_iso()
    records = [
        {**exp, "status": "backlog", "created": created} for exp in _EXPERIMENTS
    ]
    return sorted(records, key=lambda r: r["id"])


def main() -> int:
    """Append unique backlog experiments and print a summary line."""
    ensure_dirs()
    records = build_records()
    added, skipped = append_jsonl_unique(_OUT, records, key="id")
    print(
        f"experiments: added {added}, skipped {skipped} "
        f"(total candidates {len(records)}) -> {_OUT}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
