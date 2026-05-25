# Security Baseline

## Purpose
Define the minimum security standard for Dealix.

## Required GitHub Settings
- Branch protection on main.
- Pull request required before merge.
- Required status checks.
- Secret scanning enabled.
- Push protection enabled.
- Dependabot alerts enabled.
- Dependabot security updates enabled.
- No force pushes to main.
- No direct bypass unless emergency.

## Required Repo Controls
- .gitignore protects private/local outputs.
- public safety scanner passes.
- no autonomous external actions scanner passes.
- data boundary verifier passes.
- compile checks pass.
- master blueprint verifier passes.

## Required Private Ops Controls
- private ops not public.
- no API keys in markdown/csv.
- client data stays private.
- payment records stay private.
- approval log exists.
- incident log exists.

## Rule
If security baseline fails, stop product expansion.
