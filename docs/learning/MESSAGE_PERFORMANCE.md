# Message Performance — أداء الرسائل

## Purpose
Track outreach message reply rates by sector, channel, and variant. Build the sector-by-message matrix that informs future pack composition.

## Owner
Head of Delivery.

## Inputs
- Client-reported reply data at 30-day check-in.
- Message variant metadata from each sprint's pack.
- Sector and channel labels from the lead table.

## Outputs
- Sector-by-channel matrix of reply rates with sample size.
- Variant-level reply rate trends.
- Quarterly recommendation: which variants to retire, which to promote.

## Rules (numbered)
1. Reply data is captured only when the client reports it. We do not infer or track recipient behavior.
2. Every cell has a sample size; cells with fewer than 30 messages are flagged "low confidence".
3. Reply rates are observed ranges, never promises.
4. Aggregate data is anonymized; no client-identifiable cells.
5. Variants are retired when they consistently underperform on at least 100 messages across at least 3 sprints.
6. New variants enter the matrix as experiments per `EXPERIMENT_SYSTEM.md`.

## Metrics
- Cells with sample size greater than or equal to 30 (target greater than or equal to 60 percent of cells).
- Variants retired per quarter.
- Variants promoted per quarter.

## Cadence
Updated monthly. Reviewed quarterly.

## Evidence (paths)
- `docs/learning/registers/message_performance/<month>.md`

## Verifier
Head of Delivery.

## Runtime Command
`make learning.messages.update` pulls the latest client-reported data and refreshes the matrix.

## Matrix shape

Rows: sector codes from the intake list.

Columns: channel x variant. Example columns: email_v1, email_v2, form_v1, form_v2, association_v1, association_v2.

Cells: observed reply rate range across sprints, sample size, last updated.

Example cell: `12-18% (n=240, last 6 sprints, updated 2026-05-01)`.

## Variant card

Each active variant has a card with:
- Variant ID (channel + version).
- Variant text (template form).
- Sectors where it has been used.
- Sample size and reply rate range.
- Notes on what makes it work or not.
- Status: active | experimental | retired.

## Operating substance
Message performance is a Dealix operating asset that compounds over sprints. Each sprint adds messages-times-recipients of observation. After 50 sprints, the matrix becomes a real artifact that informs proposal scoping.

We track ranges, not point estimates. Reply rate ranges across sprints are honest about variance; point estimates are not. When we show this data to a future client, we show "observed range was X to Y over N sprints", never "expect X percent".

The flag on low-confidence cells is the honesty layer. A cell with 12 messages and a 17 percent reply rate is anecdotal; flagging it as low-confidence prevents misuse. The flag goes away when sample size crosses 30.

Variant retirement is a discipline. Old variants accumulate; without retirement, the pack template bloats. Quarterly review retires variants that have consistently underperformed and promotes variants that have outperformed in their sectors.

Client-reported only. We do not track recipient open or click rates, because that would require sending infrastructure Dealix does not operate. We do not infer reply rates from indirect signals. We ask the client at 30-day check-in.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
