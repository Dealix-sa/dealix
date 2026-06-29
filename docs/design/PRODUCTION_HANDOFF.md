# Dealix Design Production Handoff Checklist

Before converting a design artifact into production UI, confirm:

```text
Artifact:
Source brief:
Business owner:
Engineering owner:
Reviewed by:
Approval state:
Safety status:
Claims status:
Data sensitivity status:
Production route/component:
Rollback plan:
```

## Engineering checks

- Existing route/component inspected
- No unnecessary dependencies added
- Responsive behavior considered
- Accessibility baseline checked
- No secrets or sensitive data included
- Runtime build command identified
- Generated artifact separated from production until approved

## Commercial checks

- Business outcome clear
- Next action clear
- Claims reviewed
- Assumptions labeled
- Proof available or marked missing
- Client-facing language approved

## Safety checks

- No live outbound implication without gates
- No fake ROI or fake customer proof
- No hidden automation claims
- Human approval state visible where needed
