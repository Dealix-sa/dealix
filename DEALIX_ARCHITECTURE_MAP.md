# Dealix Architecture Map
## Public Product Layer
- api/ -> FastAPI backend and routers.
- apps/web/ -> web application.
- landing/ -> public website and sales pages.
- integrations/ -> external providers.
- db/ -> models, repositories, and source of truth.
## Intelligence Layer
- auto_client_acquisition/ -> acquisition workflows.
- autonomous_growth/ -> growth automation.
- dealix/agents/ -> AI decision and generation agents.
- evals/ -> quality tests and rubrics.
## Trust Layer
- dealix/trust/ -> policy, approvals, audit.
- dealix/registers/ -> no-overclaim and Saudi compliance registers.
- docs/trust/ -> governance policies.
## Operating Layer
- scripts/ -> verification scripts.
- tests/ -> automated tests.
- readiness/ -> stage gates and scorecards.
- .github/workflows/ -> CI/CD.
## Commercial Layer
- docs/offers/ -> what Dealix sells.
- docs/delivery/ -> how Dealix delivers.
- docs/public_sales/ -> public sales material.
## Private Ops Layer
The following must live outside the public repo:
- real clients
- real leads
- outreach queues
- call notes
- payment receipts
- pricing experiments
- private prompts
- confidential GTM strategy
