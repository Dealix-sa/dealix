# Contact Form Queue Machine

| Field | Value |
|---|---|
| Purpose | Queue accounts where the right channel is a partner-website contact form completed by a human operator |
| Inputs | account scores, partner registry |
| Outputs | `contact_form_queue.csv` |
| Approval class | Manual operator action only |
| Trust gate | Robots.txt / ToS-check, brand check |
| Owner | Distribution Operator |
| KPI | Reply rate, complaint rate |
| Failure mode | ToS violation → row blocked permanently |

## Draft contract

```yaml
queue: contact_form_queue
fields:
  - draft_id
  - account_id
  - form_url
  - tos_check               # pass | fail | manual_review
  - name_to_use
  - email_to_use
  - subject_en
  - subject_ar
  - body_en
  - body_ar
  - status
  - created_at
  - source
```

## Operator rules

- Use the operator's real name and Dealix email.
- Never submit identical bodies to multiple forms.
- Never auto-fill a form via headless browser; this queue is human-completed only.
