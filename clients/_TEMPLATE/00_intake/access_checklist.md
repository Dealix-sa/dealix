# Access Checklist

> Before diagnosis can begin, confirm every access path is open. No access = no diagnosis.

## Systems

| System | URL / endpoint | Access type | Owner | Granted? | Notes |
|--------|----------------|-------------|-------|----------|-------|
| CRM |                | read / write |       | [ ]      |       |
| ERP / finance |        | read         |       | [ ]      |       |
| Data warehouse / BI |   | read         |       | [ ]      |       |
| Production database |    | read / limited |     | [ ]      |       |
| Cloud console (AWS/GCP/Azure) | | read | | [ ] | |
| Ticketing / support desk | | read | | [ ] | |

## Data

| Dataset | Source | Format | Last refresh | Sensitivity | Granted? |
|---------|--------|--------|--------------|-------------|----------|
|         |        |        |              | public / internal / confidential | [ ] |

## People

- [ ] Sponsor available for kickoff within 5 business days
- [ ] Day-to-day contact identified and reachable
- [ ] Subject-matter experts named for each in-scope workflow
- [ ] Data owner named and contactable

## Legal / compliance

- [ ] NDA / MSA signed
- [ ] Data processing agreement (DPA) in place
- [ ] PDPL / GDPR posture confirmed
- [ ] Data residency requirement documented
- [ ] AI usage disclosure approved by client legal

## Tools we bring

- [ ] Project workspace created (`scripts/delivery/create_client_workspace.py`)
- [ ] Diagnostic workspace provisioned
- [ ] Secure channel for sharing credentials established
- [ ] Version-controlled evidence folder agreed

## Acceptance gate

Access is sufficient to start diagnosis only when **all systems in scope are granted read access** and **the sponsor has confirmed the kickoff date**.