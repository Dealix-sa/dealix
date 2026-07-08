# Dealix Autonomous Company OS — Full Connector Run

This runbook defines how Dealix should execute founder commands that mention GitHub, Slack, Airtable, Google Contacts, and the Dealix Autonomous Company OS skill.

## Default mode

`draft-only` is the default and safest operating mode.

Dealix may create internal files, reports, import seeds, draft briefs, approval queues, and PR updates. Dealix must not send external messages, mutate production systems, charge customers, publish claims, or merge PRs unless the exact action is approved by the founder.

## Execution map

| Layer | Purpose | Connector surface | Safety rule |
|---|---|---|---|
| Company Brain | Decide commercial thesis and daily objective | GitHub docs/report | Internal only |
| Opportunity Graph | Rank segments and prospects | Airtable seed/CSV/JSON | No invented contacts |
| Agent Team | CEO, Scout, Offer, Risk, Delivery, Proof, Product, Self-Improvement | GitHub runner/report | Draft-only |
| Approval Center | Separate safe internal actions from risky external actions | Airtable board + GitHub CSV fallback | Founder approval required |
| Slack Brief | Founder/team operating summary | Slack draft/canvas | Do not post unless approved |
| Contacts Radar | Warm/opt-in contact discovery | Google Contacts | No cold outreach |
| Proof Loop | Evidence of what happened | GitHub reports/artifacts | No fake proof |
| Self-Improvement | Update scoring/playbooks from outcomes | GitHub docs/report | Evidence-based only |

## First commercial wedge

Dealix should sell a specific operating result before selling the full platform:

**Revenue Command Room / Command Sprint**

Plain-language value:

> Dealix gives the business owner one daily command room showing what happened, who needs follow-up, what message should be reviewed, what proof exists, and what the next approved action is.

## Connector-specific execution

### GitHub

GitHub is the durable source of truth. Every serious execution should produce one or more of:

- branch or PR updates
- docs/runbooks
- scripts/runners
- workflows
- verification files
- generated reports or seed files

Current continuation target: PR #879, branch `feat/dealix-autonomous-company-os-execution-spine`.

### Slack

Slack should be used as an internal command surface only:

- create a canvas for the daily operating brief, or
- create a draft message in an approved internal channel.

No Slack message should be sent automatically to a channel without explicit approval.

### Airtable

Preferred live board tables:

1. Approval Queue
2. Opportunity Graph
3. Connector Runs
4. Proof Log
5. Self-Improvement Notes

If Airtable base/table access is unavailable, the runner generates CSV seeds under `reports/dealix_autonomous_company_os/`.

### Google Contacts

Contacts are only a warm-contact radar. Search results are not consent.

Allowed sources:

- known founder contacts
- inbound requests
- referrals
- opted-in prospects
- existing client/vendor relationships

Forbidden:

- invented contacts
- scraped contacts
- cold WhatsApp automation
- mass email or SMS

## How to run locally

```bash
python scripts/commercial/run_dealix_autonomous_company_os.py --limit 4
```

Expected outputs:

```text
reports/dealix_autonomous_company_os/latest.json
reports/dealix_autonomous_company_os/latest.md
reports/dealix_autonomous_company_os/airtable_approval_queue_seed.csv
reports/dealix_autonomous_company_os/airtable_opportunity_graph_seed.csv
```

## Approval statuses

- `Internal`: safe internal planning/reporting.
- `Pending Founder Review`: draft is ready but cannot be executed externally.
- `Approved`: founder explicitly approved the exact action.
- `Blocked`: forbidden or unsafe under current mode.

## Stop conditions

The runner halts if any of these are true:

- `EXTERNAL_SEND_ENABLED=true`
- `LIVE_OUTBOUND_ENABLED=true`
- `WHATSAPP_AUTO_SEND=true`
- `EMAIL_AUTO_SEND=true`
- `SMS_AUTO_SEND=true`
- `LINKEDIN_AUTO_SEND=true`
- `AUTO_MERGE_ENABLED=true`
- `AUTO_DEPLOY_ENABLED=true`
- `LIVE_PAYMENT_CAPTURE_ENABLED=true`

## Definition of done for this layer

- Skill exists under `skills/dealix-autonomous-company-os/`.
- Runner creates a complete daily operating packet.
- Workflow runs the runner in safe draft-only mode.
- PR body documents connector status and safety guarantees.
- Airtable fallback seeds exist through generated CSVs.
- Google Contacts is treated as warm-contact radar only.
- Slack is internal draft/canvas only.
