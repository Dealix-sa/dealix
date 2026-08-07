# Command Center and Sales Agent API

## Purpose

These APIs make the Dealix Strategic Command Center usable from the frontend and future client portals.

Baseline mode remains `draft_only`. These endpoints do not send email, WhatsApp, SMS, or any external communication.

## GET /api/command-center

Returns the current strategic command center payload:

- north star
- daily targets
- revenue lane
- targeting lane
- sales agent lane
- company brain lane
- delivery lane
- safety gates

### Example

```bash
curl http://localhost:3100/api/command-center
```

## POST /api/sales-agent/draft

Generates a company-specific sales draft, discovery questions, pain hypothesis, recommended offer, and negotiation guardrails.

### Request

```json
{
  "company": "Sample Riyadh B2B Company",
  "sector": "b2b_services",
  "city": "Riyadh",
  "senderIdentity": "Dealix Sales Assistant",
  "sourceUrl": "manual_review_required"
}
```

### Response

```json
{
  "mode": "draft_only",
  "requiresApproval": true,
  "externalSendEnabled": false,
  "company": "Sample Riyadh B2B Company",
  "recommendedOffer": "Revenue Command Room OS",
  "draftAr": "..."
}
```

## Identity policy

Allowed sender identities:

- Dealix Sales Assistant
- Dealix team
- authorized sales assistant for the company

Named executive identity requires explicit owner approval.

## Safety policy

- No external send from these APIs.
- Every output is a draft.
- Founder or owner review is required.
- No fake ROI or fake proof.
- Email scale requires sender authentication and unsubscribe handling.
- WhatsApp requires opt-in and approved template before production use.
