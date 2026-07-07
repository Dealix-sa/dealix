# Daily Targeting Machine — SOP

> Draft-only. No live send anywhere in this loop. This is the founder's morning
> routine for the Saudi Opportunity Command Room.

## Daily steps (≈15 minutes)

1. **Add authorized seed rows** (optional). Append companies to
   `data/opportunity_graph/companies.seed.csv`. Only use sources you are allowed
   to use: manual research, CSV/Sheet exports, public exhibitor lists, your own
   CRM, MISA/Invest Saudi references. **No scraping, no purchased lists.**
2. **Seed the graph:**
   ```bash
   python scripts/commercial/seed_saudi_opportunity_graph.py
   ```
3. **Run the daily cycle (draft-only):**
   ```bash
   python scripts/commercial/run_daily_opportunity_targeting.py --mode draft-only --limit 50
   ```
4. **Generate the report (and weekly proof pack on Sundays):**
   ```bash
   python scripts/commercial/generate_daily_command_report.py --weekly-proof-pack
   ```
5. **Review the report:**
   `reports/opportunity_command/daily/<today>.md`
6. **Clear the approval queue** — approve, revise, or reject each pending draft
   (see approval workflow below).

## Expected outputs

| File | Meaning |
|---|---|
| `data/opportunity_graph/opportunities.json` | Scored + segmented companies |
| `data/opportunity_graph/outreach_drafts.json` | Draft messages (pending by default) |
| `data/opportunity_graph/approvals.json` | Append-only decision audit log |
| `reports/opportunity_command/daily/<date>.md` | Daily command report |
| `reports/opportunity_command/weekly/<date>_proof_pack.md` | Weekly proof pack |

All generated files are gitignored; only `companies.seed.csv` is committed.

## Founder review process

For each `hot` / `warm` company:

1. Read the drafted message and its `risk_notes`.
2. Confirm the signal is real and the channel is appropriate.
3. Approve, revise, or reject.
4. If you send it yourself (manually, via your own LinkedIn/email/WhatsApp),
   record the manual send so the audit log stays accurate.

## Approval workflow (API or Python)

```bash
# List pending drafts
curl -H "X-Admin-API-Key: $ADMIN_KEY" \
  https://api.dealix.me/api/v1/opportunity-command/drafts?status=pending

# Approve
curl -X POST -H "X-Admin-API-Key: $ADMIN_KEY" -H "Content-Type: application/json" \
  -d '{"actor":"Sami Assiri"}' \
  https://api.dealix.me/api/v1/opportunity-command/draft/<draft_id>/approve

# Record a MANUAL send (only after you sent it yourself)
curl -X POST -H "X-Admin-API-Key: $ADMIN_KEY" -H "Content-Type: application/json" \
  -d '{"human_sender":"Sami Assiri"}' \
  https://api.dealix.me/api/v1/opportunity-command/draft/<draft_id>/mark-sent
```

## No-live-send rule

- The system **generates drafts only**. It has no automated send path.
- `mark-sent` records that a **human** sent an **approved** draft. It never
  contacts anyone.
- `OUTBOUND_MODE=draft_only` and all `*_SEND_ENABLED` flags remain `false`.
- No cold WhatsApp blasts, no LinkedIn automation, no scraping.
