# Tool Stack

## MVP (now)

| Area | Tools |
|------|-------|
| Backend | FastAPI, Pydantic, SQLAlchemy |
| DB | Postgres |
| Frontend | Next.js, Tailwind, shadcn/ui |
| Data | stdlib CSV + pandas where already used in repo |
| Reports | Markdown/Jinja paths via reporting modules |
| Testing | pytest |
| Quality | ruff (repo), optional mypy slices |

## After first 3 customers

| Area | Tools |
|------|-------|
| LLM Gateway | LiteLLM (if adopted) |
| Observability | Langfuse (optional) |
| Product analytics | PostHog (optional) |
| Vector store | pgvector / Qdrant |
| RAG | LlamaIndex or Haystack (evaluate) |
| Workers | ARQ / existing queue |

## Enterprise

Temporal, IdP/RBAC, S3-compatible object storage, OpenTelemetry, SIEM hooks — phased.

## Why Data + Governance first

AI initiatives fail without AI-ready data practices (metadata, governance, proportionality).

Reference: [Gartner press release — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
