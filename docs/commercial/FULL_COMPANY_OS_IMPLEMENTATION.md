# Dealix Full Company OS Implementation

## Product statement

Dealix is a founder-first Saudi B2B Company OS. It prepares daily work for revenue, market access, partnerships, negotiation, proof, and self-improvement while keeping every external action under human approval.

The simplest customer-facing statement:

> Dealix understands your company, identifies who to follow up with and why, prepares the messages, offers, negotiation notes, reports, and proof packs, then sends everything to your team for approval before any external contact.

## Core flow

```text
Safety tripwire
-> Company Brain
-> Safe target intake
-> Opportunity scoring
-> Offer matching
-> Draft generation
-> Approval queue
-> Proof log
-> Self-improvement recommendations
-> Daily report
```

## Autonomy levels

| Level | Name | Meaning |
|---:|---|---|
| 0 | Observe | Read and summarize only. |
| 1 | Analyze | Classify, rank, and prioritize. |
| 2 | Draft | Generate messages, offers, reports, and proof drafts. |
| 3 | Internal execute | Write reports, queues, local artifacts, and proof logs. |
| 4 | Repo execute | Open branches/PR drafts and run tests only when explicitly allowed. |
| 5 | External execute | Sending, publishing, payments, production mutation. Blocked in this implementation. |

## Safety tripwire

The runner refuses to operate if any dangerous live-action flag is enabled:

```text
EXTERNAL_SEND_ENABLED
LIVE_OUTBOUND_ENABLED
AUTO_SEND_ENABLED
WHATSAPP_SEND_ENABLED
EMAIL_SEND_ENABLED
LINKEDIN_AUTOPOST_ENABLED
PAYMENT_CAPTURE_ENABLED
PRODUCTION_MUTATION_ENABLED
PR_AUTO_MERGE_ENABLED
```

It also refuses non-draft outbound mode.

## Offer ladder

The kernel uses the current Dealix commercial ladder:

1. Saudi Opportunity Snapshot
2. Revenue Proof Sprint 499 SAR
3. Revenue Command Pilot
4. Saudi Market Access Sprint
5. Revenue Command Room Retainer
6. AI Company OS Setup
7. B2G Readiness Sprint
8. Partner / Distributor Desk

## Output files

A run writes:

```text
reports/full_company_os/<date>/bundle.json
reports/full_company_os/<date>/opportunities.json
reports/full_company_os/<date>/drafts.json
reports/full_company_os/<date>/approvals.json
reports/full_company_os/<date>/proof.json
reports/full_company_os/<date>/improvements.json
reports/full_company_os/<date>/daily.md
reports/full_company_os/latest.json
reports/full_company_os/latest.md
```

## Runner

```bash
python scripts/commercial/run_full_company_os.py --client dealix --mode draft-only --limit 50
```

## Verifier

```bash
python scripts/commercial/verify_full_company_os.py
```

The verifier checks:

- required files exist,
- live send/payment/production mutation functions were not introduced in this slice,
- the runner creates outputs,
- drafts exist and remain pending founder review,
- approval queue exists,
- proof log exists.

## How this connects to the bigger Dealix plan

This is the small safe nucleus for the broader Dealix Autonomous Company OS:

- Production Trust remains the first gate.
- Money Now remains manual-close and proof-first.
- Client Acquisition Queue can feed better target cards later.
- Conversation and Negotiation Engine can consume the scored opportunities later.
- Self-Improvement can learn from approvals, rejections, replies, meetings, and proof logs later.
- Controlled-live outbound must be a separate PR with rate limits, opt-out, audit logs, and explicit founder approval.

## Non-goals for this PR

- No SaaS client portal yet.
- No CRM mutation.
- No Gmail send.
- No WhatsApp send.
- No live checkout.
- No paid ads.
- No scraping adapters.
- No external connector mutation.

## First 14-day internal proof target

Use this runner on Dealix itself before selling the full system:

```text
500 companies observed
100 qualified companies
50 draft messages
20 founder approvals
10 manual sends or approved sends
5 replies
2 meetings
1 paid pilot or offer
1 proof pack
20 learning events
5 internal improvements
```

These are tracking goals only. Actual numbers must come from evidence.
