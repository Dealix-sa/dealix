# Banned Claims Policy

## Hard ban (refuse and log)
- "Guaranteed X" or "X guaranteed"
- "نضمن" + variants
- "100% money-back" + variants
- "We promise results"
- "ROI guaranteed"
- "Risk-free outcome"
- "Pay only if you win"
- Any fake testimonial / case study

## Soft ban (flag for founder edit)
- Numbers without source attribution.
- Aspirational language ("revolutionary", "best-in-class").
- "Industry-leading" without comparison data.
- "Most companies" without citation.

## Enforcement
- `scripts/lib/ai_safety.py` checks prompts pre-call.
- `scripts/lib/ai_eval.py` checks outputs post-call.
- `tests/test_no_guaranteed_revenue_claims.py` checks committed content.

## Override
- There is no founder override for hard bans.
- Soft bans can be overridden case-by-case in the audit log.
