# CEO Dashboard Spec

The CEO Dashboard is the user-facing view of the Control Plane. The
backing data is `control_plane/company_state.py`.

## Sections

### 1. Revenue
- cash collected
- MRR
- pipeline value
- proposals pending

### 2. Sales
- leads
- contacted
- replies
- calls
- proposals

### 3. Delivery
- active clients
- due reports
- QA pending
- overdue

### 4. Trust
- approvals waiting
- A3 blocked
- incidents
- claims review

### 5. Product
- CI status
- bugs
- release candidate
- customer-requested features

### 6. Learning
- best sector
- best message
- latest experiment
- next decision

### 7. CEO Queue
- approve
- reject
- defer
- kill

## Implementation Notes

- The 7 sections map 1:1 onto the dataclasses in
  `control_plane/company_state.py`.
- The CEO Queue section is rendered from `founder/decision_queue.md` in
  the private founder repo (template lives in
  `docs/founder/DECISION_QUEUE_TEMPLATE.md`).
