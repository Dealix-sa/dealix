# AI Output Quality Bar

Before any output is forwarded to the founder for review, it must clear:

## Content checks
- [ ] No banned claims (`scripts/lib/ai_eval.check_no_banned_claims`).
- [ ] No autosend language (`check_no_autosend`).
- [ ] review_status = pending_human_review.

## Tone checks
- AR: Saudi business register, no colloquial slang in customer-facing artifacts.
- EN: executive register, ≤ 100 words for first-touch outreach.

## Truthfulness checks
- Every number traces to a source.
- Every quote is verbatim or marked `[paraphrased]`.

## Brand voice checks
- Direct, not promotional.
- No "synergy", "best-in-class", "game-changer" filler.
- Founder voice, not bot voice.

## Failure mode
Output failing any check: discarded; deterministic fallback regenerated.
