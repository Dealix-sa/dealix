# Analytics and Events Plan

## Goals
- Measure conversion from visit to book
- Track which pages drive proposals
- Monitor daily operator health

## Tools
- Plausible or Google Analytics (privacy-first preferred)
- Internal event log via API

## Events
| Event | Trigger | Owner |
|-------|---------|-------|
| page_view | Route change | Frontend |
| cta_click | Button click | Frontend |
| book_attempt | /book submit | Frontend |
| lead_captured | POST /api/v1/leads | Backend |
| proposal_generated | script run | Backend |
| outreach_draft_created | script run | Backend |

## Privacy
- No PII in analytics
- Respect opt-out
- PDPL-compliant
