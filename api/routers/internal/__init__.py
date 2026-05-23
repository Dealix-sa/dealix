"""Dealix Execution & Market Launch Command System — internal endpoints.

All routers in this package are admin-key gated and read from
<private_ops>/ paths (configured via DEALIX_PRIVATE_OPS env var).

They surface non-public state for the Founder Console / Launch
Command Center: readiness, blockers, risks, revenue forecast,
learning summary. They never trigger external sends.
"""
