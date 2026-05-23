# Suppression List Policy

> The list of contacts we will never send to, automated or manual.
> Enforced by `dealix/trust/suppression.py`.

## What The List Is

A monotonic (additions-only) list of identifiers (email, LinkedIn URL, phone, company domain) that Dealix and any agent/automation must check before any external send.

Stored at `trust/suppression_list.csv` (private repo) with schema:
```
identifier_type, identifier_value, added_at, reason, source, owner
```

## What Adds A Contact To Suppression

Any of:
1. Explicit "remove me", "stop", "no thanks", "not interested" reply
2. "Unsubscribe" clicked (if email)
3. 3 unanswered messages over 60+ days (auto-suppress)
4. Negative public mention of Dealix from this contact
5. Prior incident logged in `trust/data_incidents.md` involving this contact
6. Company asks for opt-out (covers all individuals at company)
7. Pre-revenue / disqualifier (per `ICP_STRATEGY.md`)
8. Direct competitor

## What The Code Does

Every send function calls:
```python
from dealix.trust.suppression import is_suppressed
if is_suppressed(identifier):
    raise SuppressionViolation(identifier, reason)
```

The function blocks the send before any external API call happens.

## Identifier Normalization

- Emails: lowercase, strip whitespace, normalize plus-tags
- LinkedIn URLs: extract the canonical profile slug
- Phones: E.164 format
- Company domains: lowercase, remove protocols, remove paths

All checks normalize before comparison.

## Cross-Identifier Linking

When a contact opts out via one channel (email), we suppress them across all channels we have for them:
- Linked records in pipeline tracker get suppression flag
- Future messages on any channel are blocked

## Removal From Suppression (almost never)

The list is monotonic by default. Removal requires:
- Explicit written request from the contact (saved as evidence)
- 90-day waiting period
- Founder + advisor signoff
- Logged in `trust/suppression_removals.csv` (auditable)

There is no UI button to remove someone. There is intentional friction.

## Audit Discipline

- Daily: any new auto-suppression noted in Daily Brief Trust section
- Weekly: count of suppressions added; trend
- Monthly: spot-check 5 random entries against actual interaction history
- Quarterly: review false-positive rate of auto-suppression heuristics

## Failure Modes To Prevent

- **Bypassed check** — every send must call `is_suppressed`. Test enforces this for known send paths.
- **List drift** — duplicate entries with different formatting. Normalization handles this.
- **Stale list** — list never gets stale (additions-only). Verify it's loaded fresh every day.
- **Cross-team leak** — list lives in private repo only. Never copied to public.

## Reporting

If a customer asks "am I on your suppression list?":
- Confirm or deny
- Provide the reason
- Provide the date added
- Do not negotiate

If a customer asks to be added: add immediately + confirm.

## What This Policy Refuses

- "One-time exception" sends
- "But this is a different campaign" justifications
- "Their assistant said yes, the boss is on suppression but should be fine"
- Re-engaging suppressed contacts via a different agent / contractor
- Any UI / tool that bypasses the code-level check
