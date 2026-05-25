# Security, Reliability & Supply Chain Operating System

## Purpose
Protect Dealix code, workflows, secrets, data boundaries, automation, and software supply chain.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly for security checks, monthly for hardening.

## Core Principle
Dealix should be safe to change, safe to run, and safe to scale.

## Security Domains
1. GitHub branch protection.
2. Required status checks.
3. Secret scanning and push protection.
4. Dependency monitoring.
5. Public/private data boundary.
6. Supply chain integrity.
7. Automation permission control.
8. AI and agent safety.
9. Incident response.
10. Release discipline.

## Rules
- No merge to main if required checks fail.
- No secrets in Git.
- No real client data in public repo.
- No autonomous external actions.
- No A3 automation.
- No dependency added without reason.
- No release without passing audit.
- No public claim without trust review.

## Evidence
- GitHub Actions green.
- branch protection active.
- security workflow results.
- public safety scanner.
- OpenSSF Scorecard result.
- dependency review.
- incident log.
