# Dependency Policy

## Purpose
Control dependencies so Dealix does not become fragile or insecure.

## Rules
- Add dependencies only when needed.
- Prefer standard library for simple scripts.
- Pin dependencies when production use begins.
- Review dependency purpose before adding.
- Remove unused dependencies.
- Enable Dependabot alerts.
- Review security updates weekly.

## Before Adding Dependency
Ask:
1. What problem does it solve?
2. Can standard library solve it?
3. Is it maintained?
4. Does it add security risk?
5. Is it required for revenue, delivery, trust, or founder leverage?

## Evidence
- requirements.txt
- Dependabot alerts
- GitHub security tab
