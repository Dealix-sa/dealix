# Customer Success Playbook · دليل نجاح العميل

> What happens AFTER a customer pays. The exact rhythm from kickoff
> to renewal or churn. Bilingual. Doctrine-aligned.
>
> **Effective:** 2026-06-01

---

## Customer lifecycle stages

```
Free Diagnostic → 1 SAR Pilot → 7-day Sprint → Managed Ops → Custom AI
                                       ↓               ↓
                                  case study      partner contract
```

Every stage has:
1. **Entry trigger** — what brought them here
2. **Owner SLA** — who does what within what window
3. **Exit criteria** — what defines successful transition
4. **Failure modes** — what to watch for

---

## Stage 1: Free Diagnostic (24-48 hours)

### Entry trigger
Customer submits the 6-question form at `/[locale]/dealix-diagnostic`.

### Owner SLA
- **Founder:** read + respond within 24h
- **Agent:** generates the 1-page report
- **Founder:** approves before send (always)

### Deliverables
- 1-page bilingual report
- 3 specific observations about their situation
- 1 recommended next step (Sprint, Custom AI, or "not yet ready")
- DPA link if their answer reveals data work needed

### Exit criteria
- [ ] Customer received report
- [ ] Customer responded (any direction)
- [ ] Pipeline_tracker updated with outcome

### Common failure modes
- Customer ghosts after report → log nurture, 30-day silence
- Customer expects "free advice" stream → politely point to 1 SAR pilot
- Customer reveals incompatibility (wants autonomous send) → polite no,
  point to doctrine

---

## Stage 2: 1 SAR Pilot (5 minutes for customer, 0 for founder)

### Entry trigger
Customer pays 1 SAR via `/[locale]/checkout`.

### Owner SLA
- **System:** Moyasar webhook → receipt email within 1 minute
- **Founder:** personal follow-up within 24h ("شكرًا على التحقق من
  الـ flow. الخطوة التالية: Sprint بـ ٤٩٩ ر.س لو أردت.")

### Deliverables
- ZATCA-compliant receipt
- Receipt email
- Follow-up email from founder

### Exit criteria
- [ ] 1 SAR landed in Dealix Moyasar account
- [ ] Receipt visible to customer
- [ ] Founder follow-up sent
- [ ] Customer decision: proceed to Sprint or stop

### Failure modes
- Webhook delays → manually verify in Moyasar dashboard, replay if
  needed
- Customer didn't intend pilot, thought it was full Sprint → refund
  immediately + email apology

---

## Stage 3: 7-day Sprint (the core engagement)

### Entry trigger
Customer pays 499 SAR for `pilot_managed`.

### Owner SLA per day

#### Day 0 (within 2h of payment)
- Founder sends `day_0_welcome.md` (personalized)
- Calendly link for 20-min kickoff
- `sprint_start` API called → run_id created + checklist initialized

#### Day 1 (within 24h of payment)
- Kickoff call held (20 min)
- Founder sends `day_1_data_request.md`
- Sprint step 1 (kickoff) marked done with evidence link
- DPA URL sent
- Data upload link issued (TTL ≤ 7 days)

#### Day 2 (24-48h after payment)
- Customer uploads data
- DQ pipeline runs automatically
- Sprint step 2 (data_intake) marked done

#### Day 3 (72h after payment)
- DQ Report generated (bilingual)
- Top-10 prospects ranked
- Founder sends `day_3_intelligence_preview.md`
- Sprint step 3+4 (data_quality_report, icp_match_scoring) marked done
- 15-min review call optional

#### Day 4 (96h)
- Intelligence loop runs (enrichment + competitor brief)
- Sprint step 5 marked done

#### Day 5 (120h)
- Drafts assembly: 15 outreach + proposal drafts
- Sprint step 6 marked done
- Founder sends `day_5_draft_review.md`
- Customer reviews via `approval_center`
- Customer signoff = Sprint step 7 marked done

#### Day 6 (144h)
- Proof Pack v1 assembled (14 sections)
- Internal QA pass (founder reviews bilingual quality, no fabrication)
- Sprint step 8 marked done

#### Day 7 (168h)
- Final Proof Pack delivered
- `day_7_handoff.md` email sent
- Sprint step 9 (founder_approval_pass_2) + 10 (handoff_delivery)
  marked done
- NPS survey sent
- 3 paths offered: Managed Ops / Custom AI / End

### Deliverables (final)
- Final Proof Pack (14 sections, bilingual, downloadable)
- HubSpot CSV import
- Email templates ZIP
- WhatsApp scripts (approved only)
- Founder briefing summary (1 page)

### Exit criteria
- [ ] All 10 sprint steps marked done
- [ ] Proof Pack delivered
- [ ] NPS captured
- [ ] Customer next-action decision logged

### Common failure modes
- Data delayed → pause Sprint clock, 48h grace
- Customer rejects drafts en masse → 1-hour call to recalibrate voice
- Founder time conflict → max 1 Sprint at a time per founder (hard cap)

---

## Stage 4: Managed Revenue Ops (recurring)

### Entry trigger
Customer subscribes to Starter / Growth / Scale via `/checkout`.

### Owner SLA — monthly cadence

#### Week 1 of each month
- Founder review call (45 min)
- Top opportunities surfaced
- Last month's proof events reviewed
- New month's outreach plan agreed

#### Weekly within month
- Founder approves drafts daily (per `FOUNDER_DAILY_RUNBOOK.md`)
- Weekly progress email to customer (founder-written, not auto)
- Friction signals reviewed

#### Month-end
- Monthly Proof Pack assembled
- ZATCA receipt for the month
- NPS pulse (1 question)
- Renewal confirmation 7 days before charge

### Deliverables (monthly)
- Monthly Proof Pack (12-page bilingual report)
- Updated HubSpot data
- New proof events logged
- Monthly NPS captured

### Exit criteria
- [ ] Customer accepts renewal OR
- [ ] Customer requests cancellation → handle per REFUND_POLICY
- [ ] Customer escalates to Custom AI

### Common failure modes
- NPS drops below 7 → schedule recovery call within 48h
- 30 days of zero proof events → emergency review, possible refund
- Customer wants doctrine violation → polite no, possible offboarding

---

## Stage 5: Custom AI Engagement

### Entry trigger
Customer signs scoped engagement contract (5-25K SAR).

### Owner SLA
- Per the contract — milestone-based
- Founder reviews at each milestone before customer signoff

### Deliverables
- Per contract scope

### Exit criteria
- [ ] All milestones delivered
- [ ] Customer signs final acceptance
- [ ] Case study eligibility evaluated (per
      `CASE_STUDY_TEMPLATE.md`)

---

## NPS measurement & response

### Per touchpoint
- Sprint Day 7: NPS via email link
- Managed Ops month-end: 1-question pulse
- Custom AI milestone: per-milestone NPS

### Score interpretation
- **9-10 (Promoter):** ask permission for case study + LinkedIn quote
- **7-8 (Passive):** book 15-min call within 7 days to understand
- **0-6 (Detractor):** **24-hour recovery call mandatory**

### Detractor recovery script (24h)
1. Listen first (5 min)
2. Acknowledge specifically what failed
3. Offer concrete remediation (refund / additional Sprint / Custom
   AI credit)
4. Log full conversation in `customer_health` table
5. Follow up in 7 days with action taken

Doctrine #8 (no_silent_failures) applies — never let an NPS detractor
go silent.

---

## Renewal preparation (managed subscriptions)

### Day -14 (2 weeks before charge)
- Customer success score pulled from `compute_health`
- Proof events from past 30 days summarized
- Recommendation: smooth renewal / needs check-in / risk

### Day -7 (1 week before charge)
- Founder sends renewal confirmation email
- Customer can confirm / pause / cancel
- If "pause": 30-day skip + restart automatically

### Day 0 (charge day)
- Moyasar charges automatically
- ZATCA receipt issued
- Welcome-back email for the new cycle
- `renewal_scheduler.cycle_count` incremented

### Day +3
- Follow-up: "anything blocking your team this month?"
- New month's priorities locked

---

## Churn protocols

### Voluntary churn (customer requests cancellation)
1. Acknowledge within 24h
2. Confirm refund per `REFUND_POLICY.md`
3. Data export offered (no lock-in)
4. 30-day "we miss you" silence
5. After 90 days: 1-shot reactivation email

### Involuntary churn (we offboarded customer)
Reasons that justify:
- Customer requests doctrine violation persistently
- Customer breaches DPA
- Customer's data is fundamentally unusable

Protocol:
1. Founder emails decision with reason
2. Refund last month
3. Data exported + deleted
4. Logged in `KNOWN_LIMITATIONS.md` if pattern emerges

### Surprising churn (no signal beforehand)
This is a process failure. Postmortem within 7 days:
- What signal did we miss?
- Was NPS captured?
- Was a check-in skipped?
- What ritual change prevents this next time?

---

## Customer success metrics

| Metric | Target | Red line | Source |
|--------|--------|----------|--------|
| NPS (avg, trailing 90d) | ≥ 8 | < 7 | `customer_success_os` |
| Sprint completion rate | 100% | < 95% | `sprint_runner` tracker |
| Proof events per month per customer | ≥ 4 | 0 for 30 days | `proof_ledger` |
| Renewal rate (Managed Ops) | ≥ 90% | < 75% | `renewal_scheduler` |
| Customer-reported time saved/week | ≥ 5 hours | < 2 hours | survey |
| Days from kickoff to first proof event | ≤ 7 | > 14 | `proof_ledger` |

---

## What the founder owes every customer

1. **30-min response** during business hours
2. **No autonomous send** ever (Doctrine #1)
3. **Honest reflection** in monthly Proof Pack §8
4. **Right to cancel** without retention call
5. **Data portability** within 24h of request
6. **NPS feedback loop** that visibly changes the product
7. **Postmortem transparency** if anything breaks

This list is short on purpose. These 7 are non-negotiable.
