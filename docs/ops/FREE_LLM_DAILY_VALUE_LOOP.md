# Free LLM Daily Value Loop

This playbook turns the Free LLM Provider Radar into a daily Dealix commercial operating rhythm. It is designed to increase founder output, reduce AI operating cost, and create more approved commercial actions every day. It does not guarantee revenue.

## Operating rule

Use free providers for non-confidential acceleration only. Do not place customer private data, legal files, secrets, production logs, contracts, or private financial material into free tiers unless a provider has been separately approved.

## Daily loop

1. Run provider radar for coding:

```bash
python scripts/ops/free_llm_provider_radar.py --task coding
```

Use the result for repo work, bug fixes, tests, refactors, and integration planning.

2. Run provider radar for Arabic and Saudi drafts:

```bash
python scripts/ops/free_llm_provider_radar.py --task arabic
```

Use the result for bilingual wording, Saudi B2B positioning, objections, and proposal copy. Human review is required.

3. Run provider radar for batch work:

```bash
python scripts/ops/free_llm_provider_radar.py --task batch
```

Use the result for non-confidential daily drafts, content variants, proposal skeletons, ICP notes, and follow-up plans.

4. Run the Dealix Daily Operator:

```bash
python scripts/dealix_daily_operator.py --mode demo
```

This refreshes scoring, outreach drafts, follow-up queue, prospect pack, proposal, CEO brief, and pipeline report.

5. Review top actions and approve manually.

No external message should move without the Dealix approval path.

## Commercial use cases

### 1. More daily prospecting at lower cost

Use free providers to prepare non-confidential drafts, channel variants, and objections. The human-approved output becomes daily outbound work.

### 2. Faster proposal preparation

Use free providers to create first-pass proposal outlines, value bullets, industry language, and objection handling. Final proposal claims must be verified.

### 3. Faster repo progress

Use free providers for issue analysis, test generation, refactor plans, and documentation. This increases product velocity without increasing paid model spend.

### 4. Arabic/Saudi positioning

Use Arabic-capable providers for tone, local phrasing, sector-specific language, and founder messages. Final client-facing language must be reviewed.

### 5. Content and proof packaging

Use free providers to draft LinkedIn posts, landing page variants, case-study skeletons, demo notes, and proof bullets. Do not claim outcomes without evidence.

### 6. Daily founder command

Each morning, choose the provider stack for the day, then use the daily operator output to decide which accounts receive a draft, follow-up, proposal, or demo call request.

## Provider-to-task map

- Coding: OpenRouter, Groq, Cerebras, GitHub Models, Cloudflare Workers AI.
- Arabic: Cohere, Google AI Studio, Groq Arabic-capable models, Cloudflare Workers AI.
- Batch drafts: Groq, Cerebras, Cloudflare Workers AI, OpenRouter.
- Edge experiments: Cloudflare Workers AI, Vercel AI Gateway.
- Sensitive work: approved paid/private/local providers only.

## 90-minute daily block

1. 10 minutes: run radar and choose providers.
2. 20 minutes: run daily operator and review generated files.
3. 20 minutes: select top 5 accounts.
4. 20 minutes: improve drafts, objections, and proposal CTA.
5. 20 minutes: founder approval and controlled commercial action.

## Weekly maintenance

- Review `cheahjs/free-llm-api-resources` for changed limits and providers.
- Update `data/ai/free_llm_provider_registry.json`.
- Remove providers that changed policy or became unsuitable.
- Keep all keys in `.env` or a secret manager only.

## Success metrics

Track these weekly:

- number of safe drafts prepared;
- number of approved commercial actions;
- number of proposals prepared;
- number of discovery calls requested;
- number of experiments completed without paid model spend;
- paid AI cost avoided;
- time from idea to approved action.
