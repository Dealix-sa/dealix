# Supply Chain Security System

## Purpose
Reduce risk from dependencies, GitHub Actions, builds, and automation.

## Reference Principles
- Use trusted GitHub Actions.
- Pin action versions when possible.
- Keep dependency list minimal.
- Run security scans.
- Track provenance later when releases matter.
- Avoid secrets in workflows unless required.

## Current Controls
- required GitHub checks
- public safety scanner
- no autonomous external action scanner
- data boundary scanner
- compile checks
- Dependabot alerts
- OpenSSF Scorecard later

## SLSA Direction
Dealix should gradually move toward stronger build integrity:
- version-controlled workflows
- reproducible build scripts where useful
- provenance later for released artifacts
- minimal trusted build steps

## Rule
Do not add complex CI/CD before there is a product release need.
