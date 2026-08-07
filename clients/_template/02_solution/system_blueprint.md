# System Blueprint

> The blueprint is the bridge between diagnosis and build. It says what we will build, why, and how it fits together — before a line of production code.

## Design principle

> Map → Design → Build → Operate → Scale. Start from the business outcome, not the tool.

## Outcome anchored to diagnosis

- **Pain addressed:**
- **Opportunity seized:**
- **Primary metric this moves:**
- **Baseline → target:**

## System overview

- **One-paragraph description:**
- **Primary users:**
- **Primary inputs:**
- **Primary outputs:**
- **Boundaries (what this system is NOT):**

## Components

| Component | Purpose | Build / buy / configure | Owner | Depends on |
|-----------|---------|--------------------------|-------|-------------|
|           |         |                          |       |             |

## Data flow

```
[source] → [ingest] → [transform] → [store] → [serve/act] → [measure]
```

- **Text narrative:**

## Integration points

| System | Direction | Data exchanged | Mode | Auth | Notes |
|--------|-----------|----------------|------|------|-------|
|        | in / out  |                | batch / real-time |      |       |

## Non-functional requirements

- **Performance (target latency / throughput):**
- **Reliability (target uptime):**
- **Security posture:**
- **Data residency:**
- **Observability:**
- **Maintainability:**

## Build vs buy vs configure decision log

| Need | Option A | Option B | Chosen | Why |
|------|----------|----------|--------|-----|
|      |          |          |        |     |

## Acceptance hook

This blueprint is not complete until `02_solution/acceptance_criteria.md` is signed.