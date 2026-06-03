# Engineering Architecture

## Purpose
Outline how Dealix's code is organized so anyone (or any sub-agent) can navigate it.

## Top-level modules
- `control_plane/` — priority router, control tower, strategic decision engine.
- `ops_runtime/` — runtime engines for business audit, execution assurance, finance, productization.
- `scripts/` — operator-facing scripts (verify_*, generate_*, audit_*, export_*, bootstrap_*).
- `schemas/` — JSON Schemas for canonical data shapes.
- `docs/` — operating doctrine; the source of truth.
- `.github/workflows/` — CI; every verifier runs here.

## Naming conventions
- Verifiers: `verify_<system>.py`.
- Generators: `generate_<artifact>.py`.
- Auditors: `audit_<system>.py`.
- Bootstrap: `bootstrap_<scope>.py`.

## Dependency direction
- `scripts/` may depend on `ops_runtime/` and `control_plane/`.
- `ops_runtime/` may depend on `control_plane/`.
- `control_plane/` depends only on the standard library + `schemas/`.

## Testing
- Tests live in `tests/`.
- A test exists for every non-trivial verifier and runtime module.
- The implementation sprint pack ships with verifier scripts that exit 0/1 — those are themselves tests.

## Configuration
- Behavior driven by command-line flags + environment variables.
- No magic constants buried in modules — declare at top of file.

## Anti-patterns
- One giant module.
- Mixing operator scripts and runtime engines.
- Re-exporting types just to "be safe".
- Adding feature flags that we never flip.

## Future state
- `saas/` module appears only after the SaaS gate.
- `agents/` module if/when we ship customer-facing agents.
