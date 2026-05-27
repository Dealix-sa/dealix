"""Classify any action into an S-level using pattern rules.

The classifier is intentionally conservative: when in doubt, it returns
the **stricter** level. Domain modules can register additional rules at
runtime (e.g. ``customer.contract`` → S3) without editing this file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Iterable

from dealix.hermes.sovereignty.levels import SovereigntyLevel


@dataclass(frozen=True)
class Rule:
    pattern: re.Pattern[str]
    level: SovereigntyLevel
    reason: str


# Default rules — ordered from most-specific to least-specific. The
# classifier returns the **maximum** matching level so that a single
# permissive match cannot lower the floor of a strict match.
_DEFAULT_RULES: tuple[Rule, ...] = (
    # S5 — never autonomous. Money movement / signatures.
    Rule(re.compile(r"\b(wire_transfer|sign_contract|sign_on_behalf|move_funds|pay_invoice|disburse)\b", re.I),
         SovereigntyLevel.S5_NEVER_AUTONOMOUS,
         "Irreversible financial / legal action."),
    # S4 — sovereign only. Public surfaces.
    Rule(re.compile(r"\b(public_api|publish_marketplace|change_strategy|press_release|public_announcement)\b", re.I),
         SovereigntyLevel.S4_SOVEREIGN_ONLY,
         "Public-facing surface or strategic change."),
    # S3 — sovereign memo.
    Rule(re.compile(r"\b(enterprise_contract|price_quote|sla|partnership_terms|nda)\b", re.I),
         SovereigntyLevel.S3_SOVEREIGN_MEMO,
         "Pricing / contractual commitment — needs written memo."),
    # S2 — Sami approval for anything external.
    Rule(re.compile(r"\b(send_email|send_whatsapp|send_linkedin|send_external|publish_post|customer_send|proposal_send)\b", re.I),
         SovereigntyLevel.S2_SAMI_APPROVAL,
         "External-facing send — requires Sami approval."),
    # S1 — internal task / draft.
    Rule(re.compile(r"\b(create_task|draft_|prepare_|plan_|score_)\w*", re.I),
         SovereigntyLevel.S1_INTERNAL,
         "Internal, non-binding work."),
    # S0 — summaries, reads.
    Rule(re.compile(r"\b(summarize|classify|read_|fetch_|index_|listen_)\w*", re.I),
         SovereigntyLevel.S0_AUTO_SAFE,
         "Read-only / inference; no external effect."),
)


class SovereigntyClassifier:
    """Pure-function-ish classifier; safe to instantiate once and reuse."""

    def __init__(self, extra_rules: Iterable[Rule] | None = None) -> None:
        self._rules: list[Rule] = list(_DEFAULT_RULES)
        if extra_rules:
            self._rules.extend(extra_rules)

    def add_rule(self, rule: Rule) -> None:
        self._rules.append(rule)

    def classify(self, action: str) -> tuple[SovereigntyLevel, str]:
        """Return ``(level, reason)``. Defaults to S2 when nothing matches.

        Defaulting to S2 (not S0) is intentional: an unknown action is
        treated as 'needs Sami' until a rule is added. Better to ask than
        to autonomously act.
        """
        matched: list[Rule] = [r for r in self._rules if r.pattern.search(action)]
        if not matched:
            return SovereigntyLevel.S2_SAMI_APPROVAL, "Unknown action — defaulting to S2 (Sami approval)."
        best = max(matched, key=lambda r: r.level)
        return best.level, best.reason


__all__ = ["Rule", "SovereigntyClassifier"]
