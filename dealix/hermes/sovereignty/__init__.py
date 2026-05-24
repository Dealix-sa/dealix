"""Sovereignty Module — Sami's authority over the entire kernel.

This module is intentionally tiny in API but absolute in power:

* ``levels`` defines the S0..S5 scale.
* ``classifier`` decides what level any action sits at.
* ``approval_rules`` declares which levels can auto-run vs. need approval.
* ``kill_switch`` halts execution globally or per-domain.
* ``sovereign_memory`` is the protected long-term memory only Sami writes.
* ``decision_journal`` is the append-only log of every sovereign decision.
* ``capital_allocation`` enforces 'no SAR moves without sovereign approval'.

Hard rule: anything classified S4 or S5 NEVER executes autonomously.
"""

from dealix.hermes.sovereignty.approval_rules import (
    ApprovalDecision,
    ApprovalRules,
)
from dealix.hermes.sovereignty.capital_allocation import (
    CapitalAllocation,
    CapitalLedger,
)
from dealix.hermes.sovereignty.classifier import SovereigntyClassifier
from dealix.hermes.sovereignty.decision_journal import (
    DecisionJournal,
    JournalEntry,
)
from dealix.hermes.sovereignty.kill_switch import KillSwitch, KillScope
from dealix.hermes.sovereignty.levels import SovereigntyLevel
from dealix.hermes.sovereignty.sovereign_memory import SovereignMemory

__all__ = [
    "ApprovalDecision",
    "ApprovalRules",
    "CapitalAllocation",
    "CapitalLedger",
    "SovereigntyClassifier",
    "DecisionJournal",
    "JournalEntry",
    "KillSwitch",
    "KillScope",
    "SovereigntyLevel",
    "SovereignMemory",
]
