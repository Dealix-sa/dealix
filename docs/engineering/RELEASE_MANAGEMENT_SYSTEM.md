# Release Management System

## Purpose
Control how Dealix changes are built, checked, merged, and released.

## Current Release Type
Internal operating system.

## Release Rules
- Every PR must pass required checks.
- Every new system must have verifier.
- Every automation must have approval class.
- Every data change must respect schemas.
- No secrets or private data in public repo.
- No external automation without trust gate.

## Release Levels
R0 = docs only.
R1 = internal script.
R2 = private ops generator.
R3 = dashboard/local output.
R4 = internal automation.
R5 = customer-facing feature later.

## Required Before R4
- verifier
- logs
- rollback/disable path
- data boundary check
- trust approval if needed
