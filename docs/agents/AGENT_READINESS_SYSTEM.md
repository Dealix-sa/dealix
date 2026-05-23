# Agent Readiness System

## Purpose
Decide when an AI agent is ready to support Dealix workflows.

## Agent Levels

### L0 — Prompt Only
Manual prompt, no tools.

### L1 — Draft Assistant
Generates drafts only.

### L2 — Internal Analyst
Reads private ops and generates internal insights.

### L3 — Workflow Assistant
Suggests next actions and updates internal reports.

### L4 — Controlled Tool User
Runs safe internal tools with logs.

### L5 — Governed Automation
Runs approved low-risk workflows with monitoring.

## Not Allowed Now
- autonomous outbound
- autonomous client commitments
- autonomous pricing changes
- autonomous refunds
- autonomous public publishing
- autonomous sensitive data export

## Required Before Agent Release
- purpose
- inputs
- outputs
- risk level
- approval class
- eval rubric
- logging
- disable path
- data boundary review

## Evidence
- agent registry
- eval results
- approval log
- incident log
