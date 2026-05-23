# Copywriting Rules

Dealix copy is evidence-forward. Every sentence is defensible against the no-guarantee rule. Marketing fluff is not a style choice; it is a policy violation.

**Source of truth:** `$PRIVATE_OPS/copy_lint_rules.csv`
**Owner:** Brand Guardian (`docs/ai/BRAND_GUARDIAN_AGENT.md`) + Marketing Lead
**Trust gate:** A1 — rule changes require monthly review.

## The four rules

1. **No hype.** Concrete nouns, named verbs. Replace adjectives with measurements.
2. **No guarantee.** No "guaranteed", no "definitely", no "you will". Use "case-safe pattern", "estimated", "evidenced".
3. **Evidence first.** Every quantitative claim carries a citation or an Estimated tag.
4. **Bilingual parallel.** EN and AR are parallel rewrites, not translations.

## Banned words and phrases

| Banned | Use instead |
|--------|-------------|
| Transform your business | Evidence the bottleneck in your revenue factory |
| Supercharge | Increase measured throughput |
| AI-powered | Trust-gated AI execution |
| 10x your sales | Improve case-safe conversion pattern |
| Guaranteed | Evidenced |
| Effortless | With approval gates |
| Game-changing | Operationally significant |
| Revolutionary | New |
| Cutting-edge | Current generation |
| Synergy | Combined |

## Banned framings

| Banned framing | Why |
|----------------|-----|
| "X% of buyers..." without source | Fabricated stat risk |
| "Our customers see Y% conversion" without verified attribution | Guarantee creep |
| "Limited time" without a real expiry | Manufactured urgency |
| "Trusted by leading enterprises" without named, consented logos | Hollow proof |

## Required framings

| Pattern | Example |
|---------|---------|
| Estimate vs verified | "Estimated 4 qualified conversations per week; verified figures shared with active clients." |
| Source citation | "Per ZATCA's 2024 e-invoicing guidance..." |
| Anti-promise | "We do not guarantee revenue. We guarantee a factory." |
| Disclosure | "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" |

## Lint pipeline

1. Regex pass: banned words flagged.
2. Classifier pass: claim-safety risk scored.
3. Citation density: every numeric token must have a citation or tag.
4. Bilingual parity: paragraphs aligned, length within ±20%.
5. Disclosure: mandatory line present where numbers appear.

A lint failure blocks publish. The Brand Guardian agent enforces these rules.

## Failure modes

- **False positive lint:** legitimate copy blocked by overzealous regex. Detection: producer feedback. Recovery: rule tuning; founder review.
- **Bypass:** a draft is published without lint. Detection: weekly audit. Recovery: pull; re-publish through pipeline; root cause filed.
- **Silent drift:** approved phrases gradually become "guarantee-flavoured". Detection: quarterly copy audit. Recovery: re-tune rules; re-train Brand Guardian.

## Recovery path

If lint and human review disagree consistently, the founder freezes auto-pass logic until the rules are reconciled.

## Metrics

- Lint pass rate.
- False-positive rate (sampled).
- Drift incidents per quarter (target: 0).
- Citation density score.

## Disclaimer

Copy is rhetoric. Outcomes are determined by the Revenue Factory and the client's market. Dealix does not guarantee revenue. Estimated value is not Verified value.
