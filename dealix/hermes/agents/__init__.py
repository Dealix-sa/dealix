"""
Hermes built-in agents.

Each agent is a small, deterministic Python module that the Orchestrator
can call without LLM latency. LLM-backed variants can wrap these later.
"""

__all__ = [
    "founder_brief",
    "opportunity_mapper",
    "trust_checker",
    "asset_builder",
]
