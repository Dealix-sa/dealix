# Worker Mesh OS

## Purpose
Run Dealix as a mesh of safe internal workers on the server.

## Worker Classes

### A. Intelligence Workers
- market discovery
- sector discovery
- lead discovery
- signal detection
- competitor monitoring

### B. Commercial Workers
- lead scoring
- outreach drafting
- approval queue building
- follow-up scheduling
- reply routing
- sample generation
- proposal drafting
- payment capture

### C. Delivery Workers
- client workspace creation
- delivery checklist
- QA scoring
- handoff generation
- feedback request

### D. Trust Workers
- policy evaluator
- suppression check
- no-overclaim scan
- sensitive data check
- approval routing

### E. Finance Workers
- proposal value tracking
- payment follow-up
- MRR update
- margin calculation
- pricing review

### F. CEO Workers
- sales cockpit
- approval center
- stoplight report
- board KPI stack
- war room report

## Execution Rules
- Workers may prepare.
- Workers may route.
- Workers may score.
- Workers may draft.
- Workers may not make external commitments without approval.

## Queue Upgrade Path
Cron → Redis Queue → Durable Workflows.
