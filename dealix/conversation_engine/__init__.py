"""Dealix launch conversation and negotiation engine.

This package generates approval-first commercial drafts for Dealix. It does not send,
publish, charge, deploy, or mutate production.
"""

from dealix.conversation_engine.engine import build_launch_packets

__all__ = ["build_launch_packets"]
