# Brand Guardian Agent

| Field | Value |
|---|---|
| Agent ID | `brand_guardian` |
| Scope | Validate every customer-facing surface against Dealix brand system |
| Tools | Read: brand docs, tokens, drafts. Write: rewrite suggestions, audit events. No external |
| Data access | Brand tokens, drafts, asset registry |
| Output contract | Brand-check pass / fail + diff + audit event |
| Approval class | Internal-only; no external action |
| Eval suite | Voice eval, visual conformance eval, bilingual symmetry eval |
| Kill switch | Global agent kill switch |
| Audit | Every pass / fail / suggested rewrite recorded |
| Owner | Founder |
| Allowed write targets | Audit log, draft annotations, `assets/brand/misuse-log.md` |
| Never-auto actions | Publishing, sending, modifying brand assets without founder approval |

## Responsibilities

1. Block drafts that violate `DEALIX_BRAND_VOICE.md`.
2. Block visual assets that violate `DEALIX_LOGO_USAGE.md`.
3. Flag accessibility regressions before release.
4. Maintain `assets/brand/misuse-log.md`.
5. Run weekly brand audit and report to the founder.

## Failure modes

- Voice eval mis-classifies → operator override; counter-example added to eval set.
- Bilingual symmetry false-positive → escalation; spec refinement.

## Why this matters

The Brand Guardian is the **trust gate for messaging**. A loose Brand Guardian becomes a credibility leak.
