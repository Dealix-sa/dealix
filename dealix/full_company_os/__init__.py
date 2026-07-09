"""Dealix Full Company OS.

A safe, draft-only orchestration layer for running Dealix as a founder-first
Saudi B2B Company OS. This package intentionally contains no external send,
payment capture, production mutation, or secret-reading behavior.
"""

from .kernel import FullCompanyOS, RunConfig, run_daily_cycle

__all__ = ["FullCompanyOS", "RunConfig", "run_daily_cycle"]
