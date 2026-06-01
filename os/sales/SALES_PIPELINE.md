# Dealix — Sales Pipeline OS
# نظام Pipeline المبيعات

**Version:** 1.0

---

## Pipeline Stages

```
Lead → Researched → Offer Routed → Channel Pack Ready → Contacted →
Replied → Call Booked → Discovery Done → Proposal Sent →
Won → Onboarding → Delivery → Retainer → Expansion
```

### Stage Definitions

| Stage | What it means | Exit criteria |
|-------|---------------|---------------|
| Lead | Company identified, not yet researched | Research complete |
| Researched | Company scored, signals documented | fit_score calculated, tier assigned |
| Offer Routed | Offer and channel selected | offer_router output confirmed |
| Channel Pack Ready | Brief + draft prepared, scored ≥ 82 | Persuasion dossier complete |
| Contacted | At least one message sent | Founder approved + sent |
| Replied | Company responded (any reply) | Reply classified |
| Call Booked | Discovery call scheduled | Calendar invite confirmed |
| Discovery Done | Discovery call completed | Call notes documented |
| Proposal Sent | Written proposal sent | Founder approved + sent |
| Won | Deal agreed, invoice issued | Invoice sent |
| Onboarding | Kickoff done, scope signed | Scope document signed |
| Delivery | Active build | QA checklist and delivery gates |
| Retainer | Ongoing monthly engagement | Monthly health check |
| Expansion | Expanding to more departments/workflows | Expansion scope defined |
| Lost | Deal not won | Lost reason documented |
| Nurture | Good fit, not ready now | Follow up in 60 days |
| Archived | Poor fit or permanently no | No follow-up |

---

## Stage Transition Rules

- **Lead → Researched:** company_scorer must run, fit_score must be documented
- **Researched → Offer Routed:** offer_router must run, route documented
- **Offer Routed → Channel Pack Ready:** persuasion dossier must score ≥ 82
- **Channel Pack Ready → Contacted:** founder must approve the send
- **Contacted → Replied:** actual reply received (not bounce/auto-reply)
- **Replied → Call Booked:** positive reply that leads to meeting
- **Call Booked → Discovery Done:** call completed, notes documented
- **Discovery Done → Proposal Sent:** proposal prepared + founder approved
- **Proposal Sent → Won:** deal verbally agreed, invoice issued
- **Won → Onboarding:** kickoff done, scope signed, 50% upfront collected
- **Onboarding → Delivery:** active build started, delivery gates initialized
- **Delivery → Retainer:** project delivered (QA passed, UAT signed), retainer agreed
- **Retainer → Expansion:** expansion scope identified and agreed

---

## Pipeline Health Metrics

Track weekly:
- Companies in each stage (count)
- Average days per stage
- Stage conversion rates
- Weekly new companies entering pipeline
- Weekly wins
- Pipeline value by tier (estimated — not verified)

**Weekly targets:**
- 20+ new companies in "Researched"
- 5+ in "Channel Pack Ready"
- 5+ messages sent
- 1+ calls booked
- 1 proposal per week

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
