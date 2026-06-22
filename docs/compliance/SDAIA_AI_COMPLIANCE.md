# SDAIA AI Compliance Operating Notes — Dealix v1.1

## Purpose
This document maps Dealix operating behavior to practical AI governance expectations for Saudi enterprise sales under SDAIA guidelines.

**Last Updated:** 2026-06-23
**Version:** 1.1
**Compliance Level:** Governance-Aware (not formally certified)

---

## Governance Position

**Dealix AI Role:**
- Analyze business data
- Suggest next actions
- Structure information
- Draft communications

**Dealix AI Limitation:**
- Dealix does NOT make autonomous decisions
- Dealix does NOT replace human judgment
- Dealix does NOT guarantee specific outcomes
- All AI outputs require human review before action

---

## Required Operating Controls

### 1. Human Oversight
- [x] Founder or reviewer approval before sensitive outbound
- [x] Draft queues remain visible before send
- [x] Brain outputs are framed as inputs to a human decision process
- [x] No fully automated decision-making without human-in-the-loop
- [x] Escalation paths defined for uncertain AI outputs

### 2. Transparency
- [x] AI-generated content is reviewable
- [x] Decision context is visible through metrics, assumptions, and next actions
- [x] Message templates and conversation flows are observable in the system
- [x] All AI-generated content tagged with `[AI]` marker
- [x] System explains why suggestions are made (when possible)

### 3. Accountability
- [x] Decision and risk records can be tied to owners
- [x] Approval actions are explicit and logged
- [x] System defaults bias toward control rather than automation
- [x] Audit trail maintained for all AI-assisted actions
- [x] Clear responsibility assignment (owner field on all records)

### 4. Risk Management
- [x] Outbound defaults remain restricted (`draft_only`)
- [x] Failed message and webhook events are trackable
- [x] Operational risks can be logged in Brain OS
- [x] Risk scores visible on prospects and deals
- [x] Bottleneck alerts configured for pipeline stages

### 5. Fairness and Appropriate Use
- [x] Signals and scoring focus on business context, not protected characteristics
- [x] Teams review prompts, drafts, and selection logic periodically
- [x] No deceptive claims or fabricated outcomes
- [x] No discrimination in lead prioritization (no gender, religion, nationality bias)
- [x] ICP scoring based on firmographic data only

### 6. Data Quality
- [x] AI inputs validated before processing
- [x] Confidence scores displayed on AI suggestions
- [x] Low-confidence outputs flagged for extra review
- [x] Data enrichment sources documented

---

## WhatsApp Governance

| Control | Status | Implementation |
|---------|--------|----------------|
| Official Cloud API only | ✅ | WHATSAPP_ACCESS_TOKEN configured |
| Webhook verification | ✅ | WHATSAPP_WEBHOOK_VERIFY_TOKEN required |
| Template approval | ✅ | Manual submission + Meta approval required |
| Live send disabled | ✅ | WHATSAPP_SEND_ENABLED=false |
| Message review | ✅ | Draft queue + approval workflow |
| User consent | ✅ | Collected at booking time |
| Audit logging | ✅ | All messages tracked in DB |

---

## Commercial Guidance

### ✅ Describe Dealix As:
- governed
- reviewable
- approval-gated
- compliance-aware
- human-in-the-loop
- auditable
- transparency-focused

### ❌ Do NOT Describe Dealix As:
- fully autonomous
- guaranteed compliant (no formal certification)
- guaranteed ROI generating
- replacing management judgment
- making decisions for you
- a replacement for legal/compliance review

---

## AI Prompts and Templates

All AI prompts and templates used in Dealix:

1. **Lead Qualification Prompts** — Focus on business pain and fit
2. **Draft Generation Prompts** — Include review reminders
3. **Signal Detection Prompts** — Flag low-confidence results
4. **Decision Support Prompts** — Always suggest human validation

**Prompt Review Schedule:** Quarterly

---

## Safety Architecture

```
User Input → Validation Gate → AI Processing → Draft Queue
                                                    ↓
                                          Human Review
                                                    ↓
                                          Approval/Rejection
                                                    ↓
                                          Send (if approved)
                                                    ↓
                                          Audit Log
```

### Safety Gates
1. **Input Validation** — Reject malformed data
2. **Compliance Check** — Block sensitive content
3. **Draft Creation** — Require human review
4. **Send Gate** — Block without explicit approval
5. **Audit Trail** — Log all actions

---

## Monitoring and Reporting

### AI System Metrics
- Draft generation rate
- Approval rate vs rejection rate
- AI confidence score distribution
- Response time (AI processing)

### Governance Metrics
- Human review completion rate
- Time-to-approval (average)
- Escalation frequency
- Safety incident count

### Monthly Review Required
1. Review AI output samples
2. Check for bias in scoring
3. Update prompts if needed
4. Document any incidents

---

## Contact

**AI Governance Lead:** Sami (Founder)
**Email:** samim@dealix.sa
**Review Cadence:** Quarterly

---

*This document reflects Dealix's commitment to responsible AI use in Saudi B2B sales. Not a substitute for legal advice.*
