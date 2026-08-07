# Proof item schema

```json
{
  "id": "p-...",
  "title": "Plain-language statement (e.g., 'Lead response time dropped from 8h to 90min')",
  "evidence": "Where this is observable (e.g., 'CRM response_time field, weekly average week-23 2026')",
  "date": "YYYY-MM-DD",
  "customerConsent": true,
  "publicShareable": false,
  "demo": false
}
```

Rules:
- `evidence` must be specific enough that a third party could verify.
- `customerConsent=true` required before any external use.
- `publicShareable=true` requires written customer sign-off referencing the specific item.
