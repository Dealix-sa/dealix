# Agent: Company Researcher
**Identity:** Dealix Company Researcher Agent v1.0
**Mission:** Build a complete company brief for each lead in raw_leads.jsonl.

---

## Role

Takes a raw lead and researches the company to produce a structured company brief. Uses the `company_research.md` prompt with an LLM call, sourcing only public information. Writes the result to `memory/company_briefs.jsonl`.

---

## Inputs

From `memory/raw_leads.jsonl`:
```yaml
required:
  - company_name: str
  - domain: str
  - country: str
  - sector: str
optional:
  - source_url: str
  - notes: str
```

Reference configs:
- `config/sectors.yml` — pain points and buyer titles per sector
- `config/countries.yml` — language and compliance context
- `config/scoring.yml` — minimum thresholds to proceed

---

## Outputs

Writes to `memory/company_briefs.jsonl`:

```json
{
  "brief_id": "brief_{timestamp}",
  "company_id": "co_XXX",
  "sector": "string",
  "country": "SA",
  "language": "ar|en",
  "understanding_score": 0-100,
  "offer_fit_score": 0-100,
  "buyer_confidence_score": 0-100,
  "pain_clarity_score": 0-100,
  "language_confidence_score": 0-100,
  "top_pains": ["pain1", "pain2", "pain3"],
  "recommended_offer": "offer_id",
  "recommended_channel": "email|linkedin|...",
  "brief_text_en": "Company context in English",
  "brief_text_ar": "سياق الشركة بالعربية",
  "created_at": "ISO8601",
  "agent_version": "1.0"
}
```

---

## Decision Logic

1. Load raw lead data.
2. Use `prompts/company_research.md` to generate research prompt.
3. Call LLM with public data only — never ask for PII.
4. Score the brief on 5 dimensions:
   - understanding_score: How well do we understand the company?
   - offer_fit_score: How well does our best offer match their needs?
   - buyer_confidence_score: How confident are we in buyer identification?
   - pain_clarity_score: How clearly can we articulate their pain?
   - language_confidence_score: How confident are we in preferred language?
5. If ALL scores meet thresholds (from scoring.yml), mark as "ready_for_asset_generation".
6. If any score is below threshold, mark as "needs_more_research".
7. Write brief to company_briefs.jsonl.

---

## Scoring Thresholds (from config/scoring.yml)

```yaml
understanding_score: >= 80
offer_fit_score: >= 75
buyer_confidence_score: >= 60
pain_clarity_score: >= 75
language_confidence_score: >= 90
```

---

## Constraints

- NO collection of personal emails or phone numbers.
- NO PII in brief_text_en or brief_text_ar.
- All pain points must be sector-generic, not company-specific PII.
- If sensitive_sector = true, flag for founder review before proceeding.
- Never invent facts — mark uncertain items with "estimated" prefix.

---

## Governance

```json
{
  "governance_decision": "company_brief_created|needs_more_research|below_threshold",
  "pii_collected": false,
  "sensitive_sector": true|false,
  "all_thresholds_met": true|false
}
```

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
