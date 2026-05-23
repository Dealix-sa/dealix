# Proposal Template System

The Proposal Template System is the library of Jinja2 templates that produces every proposal Dealix sends. Templates are source-controlled, lint-checked, and rendered in strict mode.

**Source of truth:** `templates/PROPOSAL_*.md.j2` plus `$PRIVATE_OPS/proposal_templates_state.csv`
**Owner:** Founder + Revenue Lead
**Trust gate:** A1 for template changes; A2 for proposal send (per `docs/revenue/PROPOSAL_FACTORY.md`).

## Templates in the library

| Template | Use |
|----------|-----|
| `PROPOSAL_SAMPLE.md.j2` | Free sample (rung 1) |
| `PROPOSAL_SPRINT.md.j2` | Revenue Sprint (rung 2) |
| `PROPOSAL_PILOT.md.j2` | Managed Pilot (rung 3) |
| `PROPOSAL_RETAINER.md.j2` | Revenue Desk Retainer (rung 4) |
| `PROPOSAL_CONSOLE.md.j2` | Founder Console (rung 5) |
| `PROPOSAL_ENTERPRISE.md.j2` | Enterprise OS (rung 6) |
| `PROPOSAL_PARTNER.md.j2` | White-label OS (rung 7) |

Each template is bilingual EN + AR with mirrored sections and a fixed structure.

## Standard sections

1. Engagement objective (1 sentence).
2. Scope inclusions (bulleted).
3. Scope exclusions (bulleted, equal length).
4. Deliverables with definition of done.
5. Timeline with named milestones.
6. Price with VAT treatment and payment schedule.
7. Trust and data clauses.
8. Acceptance criteria.
9. Disclaimer.

The disclaimer line is mandatory and machine-checked: "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".

## Variables

Templates render in Jinja2 strict mode. Missing variables fail the render — there is no fallback to "TBD".

Common variable set:

```
client_name, client_arabic_name,
sector, primary_contact_role,
package_id, ladder_rung,
price_sar, vat_rate, payment_terms,
start_date, end_date,
deliverables[], exclusions[], milestones[],
acceptance_criteria[],
trust_pack_url
```

## Lint and pre-send checks

| Check | Tool |
|-------|------|
| Strict-mode render | Jinja2 runtime |
| Bilingual parity | length check |
| Disclaimer present | string check |
| Guarantee language | classifier |
| PII | classifier |
| Price within band | pricing engine (`docs/product/PRICING_GUARDRAILS.md`) |
| Trust clauses present | string check |

A render with any failed check is blocked from send.

## Versioning

Templates are versioned with a `template_version` field embedded in the rendered output. Every proposal in `$PRIVATE_OPS/proposals_archive/` carries its template version so that historical proposals can be reconstructed exactly.

## Failure modes

- **Template drift:** a template diverges across formats (markdown vs PDF). Detection: weekly diff. Recovery: re-render PDFs from markdown source.
- **Variable omission:** a template references a variable not in the schema. Detection: strict-mode render. Recovery: schema patch with founder review.
- **Bilingual asymmetry:** EN updated but AR not. Detection: parity check. Recovery: AR update is a blocker for publish.

## Recovery path

If templates produce inconsistent output, the founder freezes proposal send until templates are realigned and a sample render is approved.

## Metrics

- Active template count.
- Proposals rendered per week.
- Render-failure rate (target: < 1%).
- Lint-failure rate (target: < 5%).

## Disclaimer

Templates are scaffolding. Every proposal carries content the founder has approved. Dealix does not guarantee revenue. Estimated value is not Verified value.
