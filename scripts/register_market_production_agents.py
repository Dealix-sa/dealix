#!/usr/bin/env python3
"""Register Market Production OS agents with identity cards.

Honors non-negotiable #9 ("no agent without identity"). Every agent is
registered as an AgentCard with a bounded purpose and an explicit
"forbidden" note. All agents are analyze/draft only — none may send
externally; sending stays on the founder-approved path.

Idempotent: skips agents already present. Persist across runs by setting
``DEALIX_AGENT_REGISTRY_PATH`` (default writes to data/agents/registry.jsonl).

Usage:
  DEALIX_AGENT_REGISTRY_PATH=data/agents/registry.jsonl \
    python3 scripts/register_market_production_agents.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

os.environ.setdefault("DEALIX_AGENT_REGISTRY_PATH", "data/agents/registry.jsonl")

from auto_client_acquisition.agent_os.agent_card import new_card  # noqa: E402
from auto_client_acquisition.agent_os.agent_registry import (  # noqa: E402
    get_agent,
    register_agent,
)

_OWNER = "dealix_founder"

# (agent_id, name, purpose, forbidden)
_AGENTS: list[tuple[str, str, str, str]] = [
    ("mpo_brand_guard", "Brand Guard Agent",
     "Improve outbound language to brand voice", "change facts or claims"),
    ("mpo_product_catalog", "Product Catalog Agent",
     "Match each draft to one catalog offer", "invent an offer or price"),
    ("mpo_sector_intelligence", "Sector Intelligence Agent",
     "Map a company to sector pain + first offer", "fabricate sector metrics"),
    ("mpo_prospect_research", "Prospect Research Agent",
     "Research + score prospects from public/founder sources", "scraping"),
    ("mpo_signal_detection", "Signal Detection Agent",
     "Detect public buying signals + match offers", "scraping or covert collection"),
    ("mpo_draft_factory", "Draft Factory Agent",
     "Produce up to 250 governed drafts/day", "send anything externally"),
    ("mpo_compliance_gate", "Compliance Gate Agent",
     "Block non-compliant drafts", "send or bypass a guard"),
    ("mpo_deliverability", "Deliverability Agent",
     "Plan ramp-capped sending batches", "bypass opt-out or suppression"),
    ("mpo_approval_queue", "Approval Queue Agent",
     "Rank top drafts for founder review", "approve on the founder's behalf"),
    ("mpo_reply_handling", "Reply Handling Agent",
     "Classify replies + route next action", "commit to a contract"),
    ("mpo_job_signal", "Job Signal Agent",
     "Turn public job postings into offer angles", "scraping"),
    ("mpo_content", "Content Agent",
     "Draft content tied to sector/pain/proof/offer", "auto-publish"),
    ("mpo_press", "Press Agent",
     "Draft trigger-gated press pitches (3 outlets, 7-day wait)", "mass press blast"),
    ("mpo_partnership", "Partnership Agent",
     "Draft partner outreach + referral terms", "auto-send partner outreach"),
    ("mpo_whatsapp_post_reply", "WhatsApp Post-Reply Agent",
     "Build consent-gated post-reply action cards", "cold or bulk WhatsApp"),
    ("mpo_gtm_metrics", "GTM Metrics Agent",
     "Emit daily/weekly GTM reports", "make sales decisions alone"),
]


def main() -> int:
    registered = 0
    skipped = 0
    for agent_id, name, purpose, forbidden in _AGENTS:
        if get_agent(agent_id) is not None:
            skipped += 1
            continue
        card = new_card(
            agent_id=agent_id,
            name=name,
            owner=_OWNER,
            purpose=purpose,
            kill_switch_owner=_OWNER,
            notes=f"Market Production OS. Draft/analyze only. Forbidden: {forbidden}.",
        )
        register_agent(card)
        registered += 1
        print(f"registered {agent_id} — {name}")
    print(f"\nMARKET_PRODUCTION_AGENTS registered={registered} skipped={skipped} total={len(_AGENTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
