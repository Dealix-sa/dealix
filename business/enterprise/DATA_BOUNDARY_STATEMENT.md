# Dealix Data Boundary Statement

## What Dealix touches

- Customer-provided lead lists, CRM exports, WhatsApp transcripts (only if customer shares them), reviews, public website content, and customer-supplied reports.

## What Dealix never touches

- Personal data outside the scope written in the SOW.
- Customer financial data (Dealix does not process card data; payments go through customer's PCI-compliant processor).
- Customer internal employee performance reviews.
- Anything the customer marks "off-limits" in the kickoff workshop.

## Where data lives

- Operational data: customer-owned systems remain the system of record.
- Dealix workspace: short-lived processing zone, retained per SOW.
- Backups: encrypted, regional, rotated.

## Sub-processors

- PaaS hosting (regional choice).
- LLM providers (opt-in only).

## Customer rights

- Right to inspect Dealix workspace data.
- Right to request deletion within 30 days of SOW termination.
- Right to receive a final data return (CSV + JSON exports).

## How the boundary is enforced

- Code-level: `scripts/check_tenant_boundaries.py`, `scripts/check_public_pages_no_private_data.py`.
- Process-level: kickoff workshop produces a written "in-scope / out-of-scope" matrix attached to the SOW.
