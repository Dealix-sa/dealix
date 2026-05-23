# Founder Interface Data Contract

## Purpose
Define the data shape required by the founder frontend.

## CEO Summary
```json
{
  "top_action": "Approve outreach batch",
  "status": "C3 Revenue Partial",
  "risk_flags": 0,
  "cash_collected_sar": 0,
  "approved_outreach": 0,
  "positive_replies": 0,
  "proposals_due": 0,
  "payment_followups_due": 0,
  "last_updated": "2026-05-23T00:00:00Z"
}
```

## Sales Funnel
```json
{
  "lead_intelligence": 0,
  "a_leads": 0,
  "pending_approval": 0,
  "approved_outreach": 0,
  "sent": 0,
  "replies": 0,
  "positive_replies": 0,
  "samples": 0,
  "proposals": 0,
  "payment_capture": 0
}
```

## Approval Item
```json
{
  "id": "approval_001",
  "type": "outreach",
  "company": "Example Co",
  "risk_level": "Low",
  "approval_class": "A2",
  "summary": "Outbound draft for ERP lead",
  "evidence": "lead_intelligence_base.csv",
  "recommended_action": "Approve",
  "status": "Pending"
}
```

## Worker Health
```json
{
  "worker": "lead_scoring",
  "last_run": "2026-05-23T00:00:00Z",
  "status": "healthy",
  "failures_24h": 0,
  "next_run": "2026-05-23T01:00:00Z"
}
```

## Rule
Frontend must not invent numbers. If data is missing, show missing state.
