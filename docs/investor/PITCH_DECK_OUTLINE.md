# Pitch Deck Outline — مخطط عرض المستثمر

## Purpose
Outline only. The deck itself is not built until three proof artifacts are in hand: 1 paid sprint signed, 1 sprint delivered with verified outcome, 1 written client feedback. Building the deck before these is premature.

## Owner
Founder. Drafted only when proof artifacts exist.

## Inputs
- `docs/investor/COMPANY_OVERVIEW.md` (one-pager).
- `docs/investor/MARKET_THESIS.md`.
- `docs/investor/FINANCIAL_MODEL.md` (summary).
- `docs/investor/ROADMAP.md`.
- `docs/investor/RISK_REGISTER.md`.
- 1 named case study (Track A) or strongly anonymized Track B.

## Outputs
- This outline (what slides, what claim, what evidence).
- Deck built only after gate.

## Gate — Deck Built Only When All Three Are True
1. At least 1 paid sprint signed (commercial proof of conversion).
2. At least 1 paid sprint delivered with verified outcome (proof of delivery).
3. At least 1 written client feedback in the proof library (proof of retention signal).

## Outline (Max 10 Slides)
| # | Slide | Claim | Evidence required |
|---|---|---|---|
| 1 | What is Dealix | Identity + what we sell | Company overview |
| 2 | Proof status | Gates passed + active | Operating evidence |
| 3 | Market thesis | Five claims summarized | Sector reports + public data |
| 4 | Product / Service | Sprint + sector report + specialist | Sample deliverables |
| 5 | Case study | One verified outcome | Track A or B case study |
| 6 | Productization ladder | Where we are on 3→5→10 | Productization command center snapshot |
| 7 | Financials | Last 6 months actuals + 12-month plan | Financial model summary |
| 8 | Team and roadmap | Current org + triggered roles | Role map + roadmap |
| 9 | Risks | Top 5 risks + mitigations | Risk register |
| 10 | The ask | Specific use of funds + kill criteria | Cash plan |

## Rules
1. No deck before all three gate conditions met.
2. No slide without an evidence link.
3. Max 10 slides; longer decks are vanity.
4. Every projected number labelled "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة".
5. No client names without written approval.
6. Use of funds is specific (named hires, named tools, named markets).
7. Kill criteria appear on the ask slide.

## Metrics
- Deck readiness: 3 gates true/false.
- Slides with evidence (target 100%).
- Investor meetings held using the deck.
- Investor follow-up rate.

## Cadence
- Built once gate is passed.
- Refreshed every 90 days while active.

## Evidence
- `evidence/investor/deck/<version>/` with slide-by-slide source links.

## Verifier
Founder.

## Runtime Command
`make pitch-deck-gate` — verifies the three gate conditions, refuses deck build if any fails.

## Arabic Summary — ملخص عربي
مخطط عرض المستثمر، لا يُبنى قبل: سباق مدفوع موقَّع، سباق مُسلَّم بنتيجة مُتحقَّقة، تغذية راجعة عميل مكتوبة. عشر شرائح بحد أقصى. كل ادعاء بدليل. القيم التقديرية ليست مُتحقَّقة.
