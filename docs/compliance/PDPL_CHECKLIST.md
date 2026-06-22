# PDPL Checklist — Dealix Saudi B2B Operating System

## Purpose
This checklist defines the minimum privacy and data handling controls required for Dealix to operate in a Saudi B2B context under the Personal Data Protection Law (PDPL).

**Last Updated:** 2026-06-23
**Version:** 1.1

---

## Core Principles

1. **Purpose Limitation** — Collect only data necessary to run the requested workflow
2. **Data Minimization** — Keep a clear business purpose for every collected field
3. **Transparency** — Avoid hidden secondary use of customer data
4. **Accountability** — Make approval, review, and outbound activity auditable
5. **Security** — Protect data with appropriate technical and organizational measures
6. **Data Subject Rights** — Enable access, correction, and deletion requests

---

## Data Categories Used in Dealix

| Category | Examples | Retention |
|----------|----------|-----------|
| Contact & Booking | Name, company, role, phone, email | Until relationship ends |
| Prospect & Pipeline | Company data, pain points, value | Until won/lost |
| Conversations | WhatsApp messages, drafts | 90 days default |
| Decisions & Risks | Brain OS records | Indefinite |
| Operational Reports | Proof artifacts, scorecards | Project-based |

---

## Required Controls

### 1. Lawful Basis and Purpose
- [x] Booking flow collects only relevant qualification inputs
- [x] Outreach and follow-up are tied to explicit business purpose
- [x] Consent signals are stored when applicable
- [x] Privacy notice provided at data collection points
- [x] No data sold or shared with third parties

### 2. Data Minimization
- [x] Default forms avoid unnecessary personal fields
- [x] Internal ledgers focus on business context, not excess personal data
- [x] Generated drafts are stored for review, not sprayed automatically
- [x] WhatsApp messages limited to business-relevant content
- [x] No collection of sensitive personal data (religion, political views, etc.)

### 3. Transparency
- [x] Users can understand what the platform is doing
- [x] AI-generated outbound is reviewable before send
- [x] Decision and risk records are visible in the operating interface
- [x] Booking confirmation includes privacy notice
- [x] All automated decisions are tagged [AI]

### 4. Retention and Review
- [x] Reports and outbox artifacts should not be committed into Git
- [x] Teams should define a retention window for conversations and drafts
- [x] Stale sensitive data should be reviewed and removed periodically
- [x] Retention policy documented: 90 days for messages, project-based for reports
- [x] Annual data review scheduled

### 5. Security and Access
- [x] Secrets remain outside the repository
- [x] Outbound defaults are disabled unless explicitly enabled
- [x] Sensitive operational changes require human review
- [x] API keys rotated periodically
- [x] Access logs maintained for audit

### 6. Data Subject Rights
- [x] Client delivery workflow must identify where data lives
- [x] Teams should be able to locate booking, contact, and conversation records
- [x] Deletion or export requests handled through controlled internal procedures
- [x] Response time for data requests: within 30 days
- [x] Data export format: JSON or CSV

---

## WhatsApp-Specific Controls

- [x] Official WhatsApp Cloud API only (no third-party wrappers)
- [x] Webhook verification token required
- [x] No live send by default (`WHATSAPP_SEND_ENABLED=false`)
- [x] Template and message events remain auditable
- [x] User consent collected before any outbound
- [x] Opt-out mechanism available
- [x] Message content reviewed before sending

---

## Technical Implementation

### Environment Variables (Safety Defaults)
```env
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
OUTBOUND_MODE=draft_only
WHATSAPP_AGENT_MODE=dry_run
EXTERNAL_SEND_ENABLED=false
```

### Database Schema Considerations
- All tables include `createdAt` and `updatedAt` for audit
- Sensitive fields encrypted at rest
- No PII stored in logs

---

## Operating Notes

1. Dealix should describe itself as **compliance-aware and reviewable**
2. Dealix should **not claim formal certification** unless that certification exists
3. Any changes to data handling must be documented and reviewed
4. Annual compliance review required

---

## Incident Response

If a data breach is suspected:
1. Immediately notify the data protection officer
2. Document the incident within 24 hours
3. Assess scope and notify affected parties if required by law
4. Implement corrective measures
5. Review and update controls

**Contact:** Sami (Founder) — samim@dealix.sa

---

*This checklist is a living document. Review quarterly or when regulations change.*
