# Dealix Commercial Identity Standards

## Overview

This document defines the canonical commercial identity for Dealix as a Saudi-first AI Business Operating System. Use it to keep all public-facing materials, code, scripts, and documentation consistent.

---

## Organization identity

| Item | Value |
|---|---|
| Company name | Dealix |
| Legal entity | Dealix Software LLC (planned) |
| GitHub org | `Dealix-sa` |
| Repository | `Dealix-sa/dealix` |
| Website | `https://dealix.me` |
| GitHub Pages | `https://dealix-sa.github.io/dealix` |
| Contact | `hello@dealix.me` |

### Canonical GitHub URLs

- Repository: `https://github.com/Dealix-sa/dealix`
- Issues: `https://github.com/Dealix-sa/dealix/issues`
- Actions: `https://github.com/Dealix-sa/dealix/actions`
- Security: `https://github.com/Dealix-sa/dealix/security`

---

## Brand positioning

### One-liner

> Dealix is a Saudi-first AI Business Operating System.

### Tagline

> Revenue + Proof + Command for Saudi companies.

### Sub-line

> PDPL-native · ZATCA-aware · Approval-first

### Core promise

AI explores, analyzes, and recommends. Deterministic workflows execute. Humans approve critical external commitments.

---

## What Dealix is (elevator pitch)

Dealix helps Saudi B2B companies turn commercial intent into governed revenue execution. It combines Saudi lead intelligence, productized AI services, and an approval-first trust layer so founders and revenue teams can grow with evidence instead of guesswork.

It is **not** a generic CRM, chatbot, or blind sales automation tool.

---

## Key product language

Use these terms consistently across landing pages, decks, and documentation:

| Term | Meaning |
|---|---|
| Revenue OS | First commercial wedge: lead, pipeline, outreach, proof |
| Proof Engine | Audit trails, evidence packs, before/after artifacts |
| Command Room | Executive command surface for founders |
| Trust Gate | Approval-first control point before external commitments |
| Service Pack | Productized AI delivery offering |
| Pilot | First paid engagement, typically SAR 2,500–7,500 |

---

## Visual identity (minimal)

- **Primary color:** Deep Saudi green `#006C35` on white
- **Accent:** Warm gold `#C5A059`
- **Type:** Clean sans-serif (Inter / IBM Plex Sans / system)
- **Tone:** Professional, credible, restrained — never hype-driven
- **Icons:** Avoid emojis in production commercial materials

---

## Repository hygiene

### Never commit

- Real customer or prospect data
- API keys, secrets, credentials
- Large archives (`.zip`, `.tar.xz`, `.rar`, `.7z`)
- Session export artifacts (`*_EXPORT*`, `*_BUNDLE*`, `*_PATCH*`)
- Runtime state snapshots generated during agent sessions

### Always commit

- Canonical product data under `data/commercial/`
- Bilingual templates under `data/templates/`
- Documentation updates reflecting current identity
- Tests and verification scripts

---

## External references

- [README.md](../README.md)
- [Platform Source of Truth](docs/00_platform_truth/PLATFORM_SOURCE_OF_TRUTH.md)
- [Production Readiness Checklist](docs/ops/PRODUCTION_READINESS_CHECKLIST.md)
- [Commercial Go-Live Gate](docs/ops/COMMERCIAL_GO_LIVE_GATE.md)
- [Trust Engine](../trust/)

---

*Last updated: 2026-07-21. Maintained by the Dealix engineering team.*
