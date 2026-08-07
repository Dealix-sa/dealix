# AI Task Routing

Default: deterministic. Opt-in routing per task is below.

| Task | Preferred provider | Fallback chain |
| --- | --- | --- |
| outreach_draft (AR) | MiniMax | Kimi → deterministic |
| outreach_draft (EN) | OpenAI | Kimi → deterministic |
| proposal_section | OpenAI | Kimi → deterministic |
| objection_response | Kimi | OpenAI → deterministic |
| translation_ar_en | MiniMax | Kimi → deterministic |
| proof_report_summary | DeepSeek | OpenAI → deterministic |
| client_status_summary | DeepSeek | OpenAI → deterministic |
| sales_call_summary | OpenAI | Kimi → deterministic |
| compliance_review | DeepSeek | OpenAI → deterministic |
| weakness_hypothesis | Kimi | DeepSeek → deterministic |
| lead_scoring_explanation | DeepSeek | OpenAI → deterministic |
| market_research_summary | Kimi | OpenAI → deterministic |

Routing decisions are logged in `business/_data/ai_audit_log.json`.
