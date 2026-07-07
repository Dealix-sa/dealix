# Dealix Tool Stack Ranking

Mode: draft-only, approval-first

## Ranking

| Rank | Priority | Score | Tool | Category | Safe next action |
|---:|---|---:|---|---|---|
| 1 | P0 | 38 | [Ollama](https://github.com/ollama/ollama) | local_llm | Document private Ollama worker pattern. |
| 2 | P0 | 34 | [markitdown](https://github.com/microsoft/markitdown) | document_processing | Add to local document ingestion workflow. |
| 3 | P0 | 33 | [n8n](https://github.com/n8n-io/n8n) | workflow_automation | Pilot local n8n workflow for approval cards. |
| 4 | P0 | 30 | [LangGraph](https://github.com/langchain-ai/langgraph) | agent_orchestration | Prototype daily strategy graph. |
| 5 | P0 | 29 | [Dify](https://github.com/langgenius/dify) | agent_builder | Evaluate as visual builder for Dealix Command Room. |
| 6 | P0 | 26 | [Firecrawl](https://github.com/firecrawl/firecrawl) | web_intelligence | Add as research adapter with source policy. |
| 7 | P1 | 30 | [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | local_rag_chat | Pilot for internal Dealix docs only. |
| 8 | P1 | 29 | [Open WebUI](https://github.com/open-webui/open-webui) | local_llm_ui | Defer until Ollama worker policy exists. |
| 9 | P1 | 29 | [Bitwarden Server](https://github.com/bitwarden/server) | secrets_management | Document secrets handling baseline. |
| 10 | P1 | 28 | [LlamaIndex](https://github.com/run-llama/llama_index) | data_rag_agents | Use for internal docs retrieval prototype. |
| 11 | P1 | 28 | [Twenty](https://github.com/twentyhq/twenty) | crm | Defer until lead volume justifies CRM. |
| 12 | P1 | 28 | [Cal.com](https://github.com/calcom/cal.com) | scheduling | Integrate after first landing page CTA. |
| 13 | P1 | 28 | [Metabase](https://github.com/metabase/metabase) | bi_dashboard | Use after Postgres reporting tables exist. |
| 14 | P1 | 28 | [Ragas](https://github.com/explodinggradients/ragas) | llm_eval | Add eval stage to RAG workflows. |
| 15 | P1 | 28 | [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) | audit_telemetry | Use for production-grade logging later. |
| 16 | P1 | 28 | [Qdrant](https://github.com/qdrant/qdrant) | vector_database | Evaluate with pgvector; choose one. |
| 17 | P1 | 28 | [Unstructured](https://github.com/Unstructured-IO/unstructured) | document_processing | Use with markitdown comparison. |
| 18 | P1 | 27 | [Aider](https://github.com/Aider-AI/aider) | coding_agent | Use for local development on small fixes. |
| 19 | P1 | 26 | [Langfuse](https://github.com/langfuse/langfuse) | llm_observability | Evaluate with Phoenix; choose one. |
| 20 | P1 | 25 | [Phoenix](https://github.com/Arize-ai/phoenix) | llm_observability | Pilot on synthetic strategy runs. |
| 21 | P1 | 24 | [CrewAI](https://github.com/crewAIInc/crewAI) | agent_orchestration | Compare against LangGraph for simple team workflows. |
| 22 | P1 | 24 | [LangChain](https://github.com/langchain-ai/langchain) | agent_framework | Adopt selectively behind internal interfaces. |
| 23 | P1 | 21 | [Mem0](https://github.com/mem0ai/mem0) | agent_memory | Prototype memory only on synthetic data. |
| 24 | P2 | 28 | [PrivateGPT](https://github.com/zylon-ai/private-gpt) | private_rag | Evaluate for sensitive/offline use. |
| 25 | P2 | 26 | [PostHog](https://github.com/PostHog/posthog) | product_analytics | Install only after product routes stabilize. |
| 26 | P2 | 26 | [Vaultwarden](https://github.com/dani-garcia/vaultwarden) | secrets_management | Use only if managed Bitwarden is not chosen. |
| 27 | P2 | 25 | [Temporal](https://github.com/temporalio/temporal) | workflow_engine | Defer until workflows require retries/state durability. |
| 28 | P2 | 24 | [RAGFlow](https://github.com/infiniflow/ragflow) | rag | Defer until first paid client knowledge base. |
| 29 | P2 | 24 | [Tabby](https://github.com/TabbyML/tabby) | coding_assistant | Defer until local dev environment stabilizes. |
| 30 | P2 | 24 | [Playwright](https://github.com/microsoft/playwright) | browser_automation | Use for dealix.me smoke tests. |
| 31 | P2 | 22 | [Haystack](https://github.com/deepset-ai/haystack) | rag_orchestration | Evaluate only if RAGFlow is too heavy. |
| 32 | P2 | 20 | [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) | repo_memory | Evaluate with synthetic repo subset. |
| 33 | P2 | 19 | [Langflow](https://github.com/langflow-ai/langflow) | agent_builder | Use only if Dify is not enough. |
| 34 | P2 | 19 | [EvolutionAPI](https://github.com/evolution-foundation/evolution-api) | whatsapp | Keep disabled until approval center and suppression list exist. |
| 35 | P2 | 19 | [OpenClaw](https://github.com/openclaw/openclaw) | team_ai_assistant | Evaluate after core Strategy OS exists. |
| 36 | P2 | 19 | [AutoGen](https://github.com/microsoft/autogen) | agent_orchestration | Compare with LangGraph/CrewAI later. |
| 37 | P2 | 18 | [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | skills_library | Mine for safe skill patterns. |
| 38 | P2 | 15 | [Browser-use](https://github.com/browser-use/browser-use) | browser_automation | Research safe use cases only. |
| 39 | P3 | 19 | [Appwrite](https://github.com/appwrite/appwrite) | backend_platform | Keep as future alternative, not current migration. |
| 40 | P3 | 19 | [developer-roadmap](https://github.com/kamranahmedse/developer-roadmap) | team_roadmaps | Use for team growth docs. |
| 41 | P3 | 19 | [System Design 101](https://github.com/ByteByteGoHq/system-design-101) | architecture_reference | Use for engineering quality checklist. |
| 42 | P3 | 16 | [last30days-skill](https://github.com/mvanhorn/last30days-skill) | market_research | Use as skill inspiration only. |
| 43 | P3 | 14 | [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | video_content | Use as content lab after proof packs. |
| 44 | P3 | 14 | [OpenMontage](https://github.com/calesthio/OpenMontage) | video_content | Evaluate later against MoneyPrinterTurbo. |
| 45 | P3 | 13 | [Hermes Agent](TBD) | local_agent_runtime | Resolve exact repo/package before adoption. |
| 46 | P3 | 11 | [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) | autonomous_agents | Keep as reference, not production dependency. |
| 47 | P3 | 11 | [SalesGPT](https://github.com/filip-michalsky/SalesGPT) | sales_agents | Use patterns only; do not enable live agent. |
| 48 | P3 | 10 | [Agent-Reach](https://github.com/Panniantong/Agent-Reach) | internet_intelligence | Keep as reference until source policy exists. |
| 49 | P3 | 9 | [SuperAGI](https://github.com/TransformerOptimus/SuperAGI) | autonomous_agents | Reference only. |
| 50 | P3 | 8 | [pi-mono](TBD) | agent_monorepo_reference | Resolve exact repo before adoption. |

## P0 tools

- **Ollama**: Run private classification, summarization, and cheap draft generation.
- **markitdown**: Convert PDFs, docs, decks, and client files into analysis-ready markdown.
- **n8n**: Approval queues, daily runs, safe connector orchestration.
- **LangGraph**: Core candidate for Strategy Execution OS state machines.
- **Dify**: Build internal agents for research, scoring, and proposal drafts.
- **Firecrawl**: Lead intelligence and market snapshots from allowed sources.

## Blocked by default

- cold_whatsapp_blast
- mass_linkedin_automation
- terms_violating_scraping
- fake_proof
- guaranteed_revenue_claims
- government_access_claims
- hardcoded_secrets
- public_llm_endpoint
