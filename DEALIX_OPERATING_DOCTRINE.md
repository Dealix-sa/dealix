# Dealix Operating Doctrine

Dealix is a Saudi-founded AI revenue intelligence company that turns customer data into paid commercial outcomes. This doctrine is the constitution of the Company OS. Every system, agent, and decision must comply with it.

## Purpose
Define the five operating loops, the AI/Founder split, and the non-negotiable rules that govern Dealix as a company. Every contributor, every agent, every CI check must enforce this doctrine.

## Owner
Sami (Founder, CEO).

## Review Cadence
Quarterly. Re-read every Monday during the CEO Loop. Re-ratified on every major strategy shift.

## Inputs
- Weekly Intelligence Review.
- Customer evidence (payments, delivery outcomes, feedback).
- Friction log and failure modes.
- Founder strategic decisions.

## Outputs
- The doctrine itself.
- Updates to operating loops, autonomy policy, and approval matrix.
- Rule changes broadcast to all sub-agents.

## Rules
- AI prepares. Founder approves. No outbound action is taken without explicit founder sign-off until autonomy graduates that surface.
- No automation may degrade customer trust to chase speed.
- Public assets contain no private customer data; private ops contain no marketing claims that are not proven.
- Every paid outcome must be reproducible: source data → DQ score → proof pack.

---

## The Five Operating Loops

Dealix runs on five compounding loops. They are the heartbeat of the company.

### 1. Revenue Loop
- Surface qualified accounts → score → outreach draft → founder approves → response → proposal → paid.
- Owner: Sales OS.
- Cadence: Daily.
- Evidence: `docs/revenue/PIPELINE_STAGES.md`, private `pipeline/pipeline_tracker.csv`.

### 2. Delivery Loop
- Paid customer → kickoff → 7-day Revenue Intelligence Sprint → proof pack → retainer offer.
- Owner: Delivery OS.
- Cadence: Per customer, plus weekly review.
- Evidence: `docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md`, `docs/delivery/revenue_sprint/QA_CHECKLIST.md`.

### 3. Trust Loop
- Every AI action → autonomy level → approval matrix → approval log → audit.
- Owner: Trust OS.
- Cadence: Daily.
- Evidence: `docs/trust/AUTONOMY_POLICY.md`, `docs/trust/APPROVAL_MATRIX.md`.

### 4. Learning Loop
- Every week, surface what happened, what worked, what failed, what bottleneck, what will change.
- Owner: Learning OS.
- Cadence: Weekly.
- Evidence: `docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md`.

### 5. CEO Loop
- Founder reviews money, sales, delivery, trust, and decisions every day.
- Owner: Founder OS.
- Cadence: Daily.
- Evidence: `docs/founder/DAILY_COMMAND_BRIEF.md`, `docs/founder/WEEKLY_CEO_REVIEW.md`.

---

## AI / Founder Split

| Surface | Autonomy | Who Acts |
|---|---|---|
| Lead scoring | L3 Auto | AI |
| Outreach drafts | L1 Assisted | AI prepares → Founder approves |
| Outbound send | L0 Manual | Founder |
| Proposal pricing | L1 Assisted | AI prepares → Founder approves |
| Payment requests | L0 Manual | Founder |
| Delivery research | L2 Semi-Auto | AI executes → Founder reviews |
| Customer-facing reports | L1 Assisted | AI drafts → Founder signs |
| Public website edits | L1 Assisted | AI prepares → Founder approves |
| Account or money changes | L4 Prohibited | Founder only |

AI prepares. Founder approves. This phrase is the entire operating split until autonomy graduates a surface.

## Metrics
- Number of operating loops with green status this week.
- Percentage of AI actions that pass approval matrix on the first review.
- Number of doctrine violations caught and resolved.

## Evidence
- `scripts/verify_company_os_deep.py` confirms doctrine integrity.
- Weekly CEO review confirms all five loops ran.
- Approval log confirms autonomy policy was enforced.

## Last Reviewed
2026-05-23
