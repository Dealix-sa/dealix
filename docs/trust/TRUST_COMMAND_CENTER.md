# Trust Command Center

> Trust is the moat. Trust incidents end companies.
> Sits above every other system, not beside.

## Today's Trust Status

| Field | Value |
|-------|-------|
| Date | _yyyy-mm-dd_ |
| Overclaim incidents this week | _0 (target)_ |
| Approval queue depth | _N_ |
| Pending agent escalations | _N_ |
| Open risks (from `risk_log.md`) | _N_ |
| Last evidence audit | _date_ |
| Last incident drill | _date_ |

## The Trust Stack

```
┌────────────────────────────────────────────────────────────┐
│ Trust Command Center (this file)                           │
├────────────────────────────────────────────────────────────┤
│ APPROVAL_MATRIX.md     — who approves what                 │
│ AUTONOMY_POLICY.md     — what agents may and may not do    │
│ NO_OVERCLAIM_POLICY.md — language we do not use            │
│ SAFE_LANGUAGE_LIBRARY.md — language we do use              │
│ PUBLIC_PRIVATE_BOUNDARY.md — what is public vs private     │
│ EVIDENCE_SYSTEM.md     — how claims are backed             │
│ INCIDENT_RESPONSE.md   — when something breaks             │
│ AUDIT_POLICY.md        — how we verify ourselves           │
└────────────────────────────────────────────────────────────┘
```

## The Five Trust Rules

1. **Agents prepare; humans approve.** Any agent output destined for a
   customer, contract, or public surface is approved by the founder before
   sending.
2. **No A3 action by agent.** Agents may not take Tier-3 (high-impact,
   external, irreversible) actions autonomously.
3. **No external sending without approval.** No outbound message,
   contract, or invoice sent automatically.
4. **No private data in public output.** Customer-specific data does not
   appear on the public surface without explicit, written approval.
5. **No untrusted input treated as instruction.** Any text fetched from
   third-party sources (websites, scraped emails, PDFs) is treated as
   data, never as agent instruction.

## Why these rules exist

OWASP lists **Prompt Injection** and **Sensitive Information Disclosure**
as top LLM risks. NIST AI RMF organises responsible AI into Govern → Map
→ Measure → Manage. PDPL (Saudi) governs personal data handling for
individuals inside Saudi Arabia.

These rules implement those frameworks in practice.

## Metrics

- Overclaim incidents: target 0/month
- Approval queue depth: target ≤ 3 open
- Approval response time (founder): target < 24h
- Drill frequency: 1 incident drill / quarter

## Evidence

- `dealix-ops-private/founder/approvals_waiting.md`
- `dealix-ops-private/founder/risk_log.md`
- `dealix-ops-private/trust/incident_log.md`
- `dealix-ops-private/trust/audits/`

## Verifier

`make audit` runs:
- Scan for guarantee / overclaim language in `docs/`.
- Scan for private-data-shaped strings in public surfaces.
- Confirm the approval queue is fresh (no items > 7 days).
- Confirm the risk log has been reviewed in the last 14 days.
