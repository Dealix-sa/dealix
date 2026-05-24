"""
UI philosophy — §109.

Pure data declaring the command-first sections of the Sovereign UI.
No rendering happens here; the surface is consumed by a separate
front-end.
"""

from __future__ import annotations


UI_PAGE_QUESTIONS: tuple[str, ...] = (
    "What is making money right now?",
    "What needs my decision today?",
    "What is at risk and why?",
    "What did the system create that I can reuse?",
    "What is the next best action for revenue?",
)


UI_SECTIONS: tuple[dict[str, str], ...] = (
    {"id": "money_command", "title": "Money Command",
     "purpose": "Cash, pipeline, stuck deals, next best action."},
    {"id": "approval_center", "title": "Approval Center",
     "purpose": "Every pending decision that needs Sami."},
    {"id": "agent_ops", "title": "Agent Ops",
     "purpose": "Runs, tools, anomalies, kill switches."},
    {"id": "value_loop", "title": "Value Loop",
     "purpose": "Customer / partner / venture outcomes."},
    {"id": "intelligence", "title": "Intelligence",
     "purpose": "What works — sectors, messages, offers, prices."},
    {"id": "sovereign_floor", "title": "Sovereign Floor",
     "purpose": "Security mode, incidents, sovereign-only memory."},
)
