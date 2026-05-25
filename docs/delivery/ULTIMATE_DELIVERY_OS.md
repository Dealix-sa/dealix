# Ultimate Delivery OS

> Turn paid work into client value, proof, retention, and referrals.
> A payment is not the end of a deal. It is the start of the proof loop.

---

## 1. Purpose

Convert every paid engagement into:
1. **Value** the client can measure.
2. **Proof** Dealix can re-use.
3. **Retention** that compounds.
4. **Referrals** that seed inbound demand.

A delivery that produces (1) but not (2), (3), (4) is half a delivery. The Delivery OS exists so that no engagement leaks any of the four.

---

## 2. Delivery flow

```
Payment / PO / written approval
   │
   ▼
Client workspace          (clients/<handle>/)
   │
   ▼
Intake                    (kickoff doc, expectations, contacts)
   │
   ▼
Delivery plan             (scope, milestones, owners, dates)
   │
   ▼
Delivery work             (the actual work, in the workspace)
   │
   ▼
QA                        (checklist, founder sign-off)
   │
   ▼
Handoff                   (artifacts, walkthrough, evidence)
   │
   ▼
Feedback                  (structured, recorded)
   │
   ▼
Retainer ask              (if applicable)
   │
   ▼
Proof approval            (case study / testimonial / sample)
   │
   ▼
Referral ask              (one warm intro per delighted customer)
   │
   ▼
Productization learning   (what to make reusable next time)
```

Every node above produces a file in `clients/<handle>/` (see §3) and an event in the event log.

---

## 3. Required artifacts (per client workspace)

Every paid engagement creates a workspace at `clients/<handle>/` with these files. Each file has an owner, a template, and a "definition of done".

| File                  | Owner    | Definition of done                                                          |
|------------------------|----------|------------------------------------------------------------------------------|
| `client_os.md`         | Founder  | One-pager: who, what, why, success criteria, comms cadence.                  |
| `intake.md`            | Delivery | Stakeholders, decision-makers, constraints, data access.                     |
| `delivery_plan.md`     | Delivery | Milestones with dates, owners, dependencies, exit criteria.                  |
| `lead_table.csv`       | Delivery | (For lead-related engagements) source records with provenance.               |
| `qa_checklist.md`      | Founder  | Filled QA checklist with pass/fail per item.                                 |
| `delivery_report.md`   | Delivery | What was delivered, before/after metrics, links to artifacts.                |
| `handoff.md`           | Delivery | Walkthrough notes, training materials, "how to use it without us".           |
| `feedback.md`          | Delivery | Structured feedback (NPS, what went well, what to fix).                      |
| `health_score.md`      | Delivery | Computed score with components; updated weekly.                              |
| `proof_approval.md`    | Founder  | Customer's written approval to publish, signed (PDF/email link).             |
| `renewal.md`           | Founder  | Renewal terms, decision date, next-step trigger.                             |

A workspace missing any file at the appropriate stage **blocks** progression to the next stage.

---

## 4. Stage-by-stage contract

### 4.1 Payment / PO / written approval
- The only entry into Delivery.
- Recorded by `finance_events` and `payment_capture_queue`.
- No work begins without one of: cleared payment, signed PO, or written approval from the agreed signatory.

### 4.2 Client workspace
- Created by `delivery-intake` worker.
- Seeds `clients/<handle>/client_os.md` and `intake.md` templates.
- Adds the client to `delivery_queue`.

### 4.3 Intake
- Founder + client agree on scope and stakeholders.
- `intake.md` is filled within 48 hours of payment.
- Calendar holds for the next two milestones are placed.

### 4.4 Delivery plan
- Milestones, dates, owners.
- Each milestone has an exit criterion.
- The plan is reviewed at the **first** check-in; not before.

### 4.5 Delivery work
- All artifacts live in the workspace, not in personal drives or chats.
- Daily standup is **not** required. Weekly written update **is**.
- Scope changes only via `change_request.md` (with founder approval).

### 4.6 QA
- Founder runs the QA checklist before handoff.
- QA records: `qa_status = pass | fail`, notes, date.
- A fail returns the engagement to the previous stage; it does not skip handoff.

### 4.7 Handoff
- A scheduled handoff call.
- `handoff.md` written within 48 hours of the call.
- Handoff includes: artifacts, walkthrough recording (if applicable), training material, and the "operate without us" instructions.

### 4.8 Feedback
- Structured feedback form requested within 7 days of handoff.
- Stored in `feedback.md` with: NPS (0–10), top-1 keep, top-1 fix.
- Negative feedback (NPS ≤ 6) triggers a founder review within 48 hours.

### 4.9 Health score
- Computed weekly by `health-score` worker.
- Components: NPS, response latency, payment status, engagement signals, last contact.
- Color: green / amber / red. Red triggers a founder action.

### 4.10 Retainer ask
- Only proposed if health is green and feedback is positive.
- Offered after the **second** delivered milestone, never before.
- Logged in `retention_queue`.

### 4.11 Proof approval
- Founder drafts a proof asset (case study / testimonial / sample report).
- Customer approves in writing (email + signed PDF acceptable).
- Approval stored in `proof_approval.md` and `proof_library`.
- Publishing is A3 (see Trust Plane); no proof goes public without a written, signed approval.

### 4.12 Referral ask
- One warm intro is requested per delighted customer (NPS ≥ 9).
- Asked once, in person or in writing, with a specific suggested intro (not "anyone who might be interested").

### 4.13 Productization learning
- After each engagement, a 15-minute review answers:
  1. Which step did we do twice? → candidate for a template.
  2. Which step did we do three times? → candidate for a worker.
  3. Which step was painful? → candidate for tooling.
- Logged into `docs/product/ULTIMATE_PRODUCT_PLATFORM.md` candidate list.

---

## 5. SLAs

| Event                                    | SLA                  |
|------------------------------------------|----------------------|
| Payment → workspace created              | ≤ 4 working hours    |
| Workspace → intake call scheduled        | ≤ 24 working hours   |
| Intake → delivery plan written           | ≤ 48 working hours   |
| Stage transition → status update         | within 24 hours      |
| Handoff call → handoff doc written       | ≤ 48 hours           |
| Feedback request → response chase        | weekly until reply   |
| Negative feedback (NPS ≤ 6) → founder review | ≤ 48 hours       |

SLA breaches surface on `/delivery` as amber/red flags.

---

## 6. Quality gates (the QA checklist core)

Every engagement passes these checks before handoff. Engagement-specific items extend this list.

- [ ] Scope as agreed in `delivery_plan.md` is delivered.
- [ ] All data has provenance recorded.
- [ ] No personal data leaked into shareable artifacts.
- [ ] No external claim made beyond what we can prove.
- [ ] Artifacts are bilingual (AR + EN) where the customer is bilingual.
- [ ] All file links resolve.
- [ ] Founder has reviewed and signed the QA checklist.

---

## 7. Cross-cutting integrations

- **Trust Plane:** publishing proof is A3; any external communication about a client is A2; sending an artifact is A2.
- **Finance OS:** the engagement's economics (price, hours, AI/tool cost, margin) are recorded as `finance_events`.
- **Product Platform:** every reused artifact becomes a template candidate.
- **Worker Mesh:** every stage transition writes to `delivery_queue` and emits an event.

---

## 8. Failure modes the Delivery OS prevents

| Failure mode                                       | Prevention                                                       |
|----------------------------------------------------|------------------------------------------------------------------|
| Work starts before payment.                        | `payment / PO / written approval` is the only entry.             |
| Scope expands silently.                            | `change_request.md` with founder approval; no other path.        |
| Handoff is informal; client doesn't know how to use it. | `handoff.md` is gated; QA blocks until present.             |
| Feedback is never collected; we don't learn.       | `feedback.md` is required at L6 exit.                            |
| Customer says "yes" to a case study verbally; we publish; they complain. | `proof_approval.md` with written approval; A3.    |
| One person leaves and the engagement collapses.    | Everything in the workspace; nothing in heads.                   |

---

## 9. Rule

> **Delivery is not complete until feedback and next commercial path are handled.**

A green QA + a handoff call are necessary but not sufficient. Without recorded feedback and a logged commercial decision (retainer / referral / pause), the engagement remains **open**.
