# Distribution War Machine

This is the meta-document for Dealix distribution. It defines what the
war machine is, what it is not, and how the individual machines plug into
a single approval-gated pipeline.

Wordmark: DEALIX. Tagline: INTELLIGENT DEALS. REAL GROWTH.
Positioning: Saudi B2B Revenue Operating System.

## 1. What the war machine is

The Distribution War Machine is the set of autonomous draft-producing
machines that turn ranked accounts and triggers into approval-ready
artefacts for the founder console. It produces drafts; the founder
approves; the operator sends. The machine never sends anything itself.

It is "war" only in operational discipline — coverage, cadence,
calibration. It is not aggressive in tone. Saudi B2B punishes aggression.

## 2. What it is not

- It is not an outbound automation. It does not connect to email, SMS,
  WhatsApp, or LinkedIn APIs to send.
- It is not a list scraper. Every account it touches has an attributed
  source from `LEAD_SOURCE_SYSTEM.md`.
- It is not a forecasting tool. It produces drafts and queues; pipeline
  forecasts are produced separately by the Revenue Factory.
- It is not a content firehose. Content is produced by the Content-to-
  Demand Engine under brand and trust gates.

## 3. The machines

The war machine is composed of the following machines, each with its own
document:

- `OUTBOUND_DRAFT_MACHINE.md` — universal draft factory for outbound
  messages.
- `LINKEDIN_QUEUE_MACHINE.md` — LinkedIn-specific draft queue.
- `EMAIL_DRAFT_MACHINE.md` — single-account structured email drafts.
- `CONTACT_FORM_QUEUE_MACHINE.md` — invited contact-form draft queue.
- `FOLLOW_UP_MACHINE.md` — cadence drafts after first contact.
- `REPLY_ROUTER_MACHINE.md` — inbound reply routing to the right next
  step.
- `NURTURE_MACHINE.md` — bounded nurture sequence for not-yet-ready
  accounts.
- `PARTNER_REFERRAL_MACHINE.md` — partner-introduced account handling.
- `ABM_STRATEGIC_ACCOUNT_MACHINE.md` — bespoke handling for top accounts.
- `PROOF_TO_DEMAND_MACHINE.md` — converts approved proof into outreach
  triggers.
- `CONTENT_TO_DEMAND_ENGINE.md` — content-led demand creation.
- `CHANNEL_PORTFOLIO_SYSTEM.md` — channel performance and rebalancing.
- `COMMUNITY_ECOSYSTEM_ENGINE.md` — sector community and ecosystem
  presence.
- `EVENTS_AND_PARTNERSHIP_ENGINE.md` — events, roundtables, partnership
  activations.

## 4. Pipeline shape

```
Intelligence Layer (sectors, ICPs, personas, triggers, scores)
            |
            v
   Per-Machine Draft Producer (A1/A2)
            |
            v
   Trust Gate (suppression, brand voice, no-guarantee, source check)
            |
            v
   Founder Approval Queue (Founder Console)
            |
            v
   Operator Send (manual, named, logged)
            |
            v
   Reply Router (back into Intelligence Layer)
```

Every machine in section 3 runs through this exact shape.

## 5. Approval classes

Across the war machine:

- A1 (observe / draft only): allowed.
- A2 (assist with explicit approval): allowed.
- A3 (autonomous external action): banned. Codified in
  `policies/dealix_control_policy.yaml` (rule `no_a3_auto`).

If a machine drifts toward A3 behaviour — for example, by attempting to
auto-send drafts on schedule — the Trust Guardian blocks the run and
opens an incident.

## 6. Cross-machine constraints

- Suppression list (`outreach/suppression.csv`) is checked before any
  draft is queued.
- "Guaranteed" claims are scanned by the Brand Guardian; matches block
  the draft.
- Daily volume caps are enforced per channel and per persona; exceeded
  caps require founder approval to override.
- Brand voice checks run on every draft.
- Bilingual operating reality is honoured per account.

## 7. KPIs (system-level)

- Draft Approval Rate — share of drafts approved without rewrite.
- Reply Quality Score — reply usefulness rated by operator post-reply.
- Suppression Bleed — number of suppressed identities that reached a
  draft queue (target: 0).
- Brand Voice Pass Rate — first-pass approval through brand check.
- Time-to-First-Operator-Touch — minutes from approval to operator send.

These KPIs are tracked in `distribution/channel_scorecard.csv` and
`distribution/sector_scorecard.csv` by the Performance Analyst.

## 8. Cadence

| Cadence | Activity |
|---|---|
| Daily | Draft production, approval queue review |
| Weekly | Reply quality review; cap recalibration |
| Monthly | Channel posture review; machine-by-machine audit |
| Quarterly | Cross-machine performance review |

## 9. Owners

- Operator: Distribution Operator agent.
- Approver: Founder Console.
- Auditor: Trust Guardian.
- Reviewer: Performance Analyst.

## 10. Failure modes (cross-machine)

| Failure | Recovery |
|---|---|
| Drift toward A3 | Trust Guardian halts run; incident opened |
| Brand voice degradation | Brand Guardian rewrites pipeline; root cause |
| Channel saturation | Caps lowered; reply quality re-baselined |
| Suppression bleed | Run halted; suppression check re-run |
| Approval queue backlog | Priority reordered; founder briefed |

## 11. Non-negotiables

- No automated external send. Ever.
- No guaranteed-revenue language.
- No scraping. No purchased lists.
- A3 banned. Only A1 and A2.
- Every draft traceable to a named source.

## 12. Source of truth

This document is the source of truth for the distribution layer. Each
sub-machine document refines a specific stage. Where they conflict, this
document and the policy-as-code file in `policies/` take precedence.

Distribution is the most policy-sensitive layer in Dealix. It is also the
one most likely to be optimised in directions that violate trust. The
war-machine framing exists to enforce both discipline and restraint.
