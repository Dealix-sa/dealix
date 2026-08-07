# Dealix CEO Priority Decision

## Current situation

The repository has a large number of open and draft PRs. The company risk is not lack of ideas; the risk is uncontrolled accumulation.

## Executive decision

Do not merge everything.

Start with the highest business-leverage and highest-risk items:

1. Stabilize main and stop direct main pushes.
2. Inspect PR #760 because it touches controlled live outbound.
3. Keep all outbound defaults safe unless production gates are verified.
4. Consolidate Revenue Loop from #732 / #727 / #739 / #726 into one source of truth.
5. Merge website/brand only if it improves conversion and does not break build.
6. Convert older draft PRs into backlog/docs/tests, not bulk code merges.

## Merge order

### P0 — Main governance

- No direct main pushes.
- All changes through PR.
- Keep reports small and meaningful.

### P1 — PR #760 Controlled outbound

Inspect only. Merge only if:
- default mode remains safe
- no uncontrolled external send
- tests pass
- Makefile targets work
- no secrets
- no fake claims
- WhatsApp live send is gated

### P2 — Revenue loop

Prioritize:
- #732 Resolve PR 727
- #739 daily Arabic email targeting
- #726 daily Arabic email targeting draft

Choose one canonical path. Do not duplicate.

### P3 — Website / brand

Prioritize:
- #757 only if it contains real website/brand value
- reject no-op or duplicate PRs

### P4 — Draft backlog

Older drafts should be triaged and converted into:
- docs
- tests
- backlog items
- runbooks
- product catalog
- sales assets
