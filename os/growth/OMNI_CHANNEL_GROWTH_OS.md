# Dealix — Omni-Channel Growth OS
# نظام النمو متعدد القنوات

**Version:** 1.0 | **Scope:** GCC B2B | **Owner:** Founder

---

## Strategic Frame

Dealix does not do mass outreach. Every message is a precision move — researched, scored, personalized, and approved before sending. The goal is not volume; it is qualified pipeline.

**Core doctrine:**
- No cold WhatsApp automation
- No LinkedIn automation
- No scraping
- All external sends require founder approval
- Every message must score ≥ 82/100 on the persuasion rubric before queuing

---

## Daily Targets

| Metric | Target | Max |
|--------|--------|-----|
| New companies researched | 20 | 30 |
| Briefs prepared | 10 | 20 |
| Messages queued for approval | 10 | 20 |
| Messages approved and sent | 5 | 15 |
| Follow-ups sent | 5 | 10 |
| Proposals prepared | 1 | 3 |
| Discovery calls booked | 1 | 2 |

**Note:** These are operational maximums. Quality always beats volume.

---

## Channel Strategy by Market

### KSA (Priority 1 — Arabic Primary)

| Channel | Use | Limit/Day |
|---------|-----|-----------|
| Email | Primary outreach — formal Arabic | 15 |
| Website Form | Conservative sectors (legal, accounting) | 5 |
| Phone Intro | FM, maintenance, contracting | 8 calls |
| Referral | Legal, accounting (highest conversion) | 3 asks |
| LinkedIn (manual) | Consulting, international | 8 msgs |

### UAE (Priority 1 — English Primary)

| Channel | Use | Limit/Day |
|---------|-----|-----------|
| LinkedIn (manual) | International companies, consulting | 10 msgs |
| Executive Email | VP-level contacts | 5 |
| Partner Referral | Via established partners | 5 |
| Email | Standard B2B outreach | 10 |

---

## The Research → Brief → Send Loop

```
1. RESEARCH (free action, no approval)
   └── Find company on LinkedIn / website
   └── Identify sector, buyer title, growth signals
   └── Score company (company_scorer) → tier A/B

2. BRIEF PREPARATION (free action, no approval)
   └── Route offer (offer_router)
   └── Route channels (channel_router)
   └── Build persuasion dossier (persuasion_dossier)
   └── Score dossier → must be ≥ 82

3. FOUNDER APPROVAL (required for all sends)
   └── Review brief + draft in Daily Brief
   └── Approve → message queued for send
   └── Reject → revise and re-score

4. SEND (founder executes manually)
   └── Email draft → founder sends
   └── LinkedIn message → founder sends manually
   └── Phone call → founder calls using prepared brief
```

---

## Anti-Ban Enforcement

All outreach passes through `anti_ban_guardian.py` before queuing:

- Minimum 14 days between contacts to same company
- Message similarity < 72% vs recent sends
- Email: pause if bounce > 5%, spam > 0.3%
- LinkedIn: manual only, max 10 connections + 8 messages/day
- WhatsApp: NEVER cold; opt-in only

---

## Weekly Growth Rhythm

| Day | Activity |
|-----|----------|
| Sunday | Research 20 new companies, brief top 10 |
| Monday | Send 10 drafts (founder approved), follow up on replies |
| Tuesday | Proposal prep, discovery calls |
| Wednesday | Content + LinkedIn (manual posts), nurture follow-ups |
| Thursday | Weekly pipeline review, prepare next week's research list |

---

## Growth Metrics Dashboard (Weekly)

Track these every week:
- Companies researched
- Briefs prepared and scored
- Messages sent (by channel)
- Reply rate per channel
- Meetings booked
- Proposals sent
- Won / Lost this week
- MRR and one-time revenue

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
