"""Cross-cutting, repo-wide constants | ثوابت مشتركة على مستوى المستودع.

This module holds small, literal values that many independent subsystems
need to agree on byte-for-byte — starting with the canonical bilingual
disclaimer. It intentionally has NO other dependencies (no settings, no
DB, no I/O) so any module — API routers, CLI scripts, doc generators,
sales asset renderers — can import it without pulling in unrelated
machinery or creating an import cycle.

Do not add business logic here. This file is for literal constants only.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Canonical disclaimer
# ---------------------------------------------------------------------------
#
# Before this constant existed, at least two materially different English
# disclaimer strings were in independent use across the codebase:
#
#   (a) "Estimated value is not Verified value / القيمة التقديرية ليست
#        قيمة مُتحقَّقة" — used in ~17 code files and ~104 docs, and is the
#        exact wording docs/LAUNCH_MASTER_PLAN.md (the canonical 90-day
#        plan) uses in its own text and in its own launch-readiness gate
#        checklist ("الإفصاح / Disclosure").
#   (b) "Estimated outcomes are not guaranteed outcomes / النتائج
#        التقديرية ليست نتائج مضمونة" — used in ~20 code files (notably
#        auto_client_acquisition/proof_architecture_os/proof_pack_render.py)
#        and ~12 docs.
#
# (a) was chosen as canonical: it already has the broader footprint, it is
# the wording docs/LAUNCH_MASTER_PLAN.md itself specifies as the required
# disclosure line, and "value" is a broader umbrella than "outcomes" —
# it covers estimated revenue/savings figures and scores generically,
# not only promised results. Consolidating (b)'s ~20 code-file consumers
# onto this constant is a deliberately separate, incremental migration
# (see the module-level TODO markers left at each (b) call site as they
# are migrated) — this file only introduces the constant; it does not by
# itself change any consumer's behavior.
CANONICAL_DISCLAIMER_EN = "Estimated value is not Verified value"
CANONICAL_DISCLAIMER_AR = "القيمة التقديرية ليست قيمة مُتحقَّقة"

# The combined bilingual line, exactly as it appears at the end of
# docs/LAUNCH_MASTER_PLAN.md and across the majority of existing
# customer-facing docs: "<EN> / <AR>".
CANONICAL_DISCLAIMER_BILINGUAL = (
    f"{CANONICAL_DISCLAIMER_EN} / {CANONICAL_DISCLAIMER_AR}"
)

__all__ = [
    "CANONICAL_DISCLAIMER_AR",
    "CANONICAL_DISCLAIMER_BILINGUAL",
    "CANONICAL_DISCLAIMER_EN",
]
