# Dealix — AI Operating Systems for Saudi B2B

Dealix is a daily operating system for Saudi B2B founders and teams.
It connects revenue, follow-up, decisions, compliance, and client delivery
into one platform — replacing scattered tools with disciplined AI operations.

---

## Quick Start (5 steps)

### Option A: Automated Setup

**Windows (PowerShell):**
```powershell
git clone https://github.com/Dealix-sa/dealix.git
cd dealix
powershell -ExecutionPolicy Bypass -File scripts/setup_local.ps1
```

**macOS / Linux:**
```bash
git clone https://github.com/Dealix-sa/dealix.git
cd dealix
bash scripts/setup_local.sh
```

### Option B: Manual Setup

```bash
# 1. Clone and install
git clone https://github.com/Dealix-sa/dealix.git
cd dealix
npm install

# 2. Configure environment
#    Copy values from docs/ops/ENVIRONMENT_VARIABLES.md into .env
#    Minimum: DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix

# 3. Start MySQL (Docker)
docker compose up -d mysql

# 4. Push database schema
npm run db:push

# 5. Verify everything
npm run check && npm run build && npm run production-check
```

Expected result: `LAUNCH DECISION: GO`

### Option C: Full Docker (no local Node/MySQL needed)

```bash
docker compose up --build
```

This starts MySQL + the production app on `http://localhost:3000`.

---

## Prerequisites

| Tool | Version | Required |
|------|---------|----------|
| Node.js | 20+ | Yes |
| Python | 3.11+ | For operational scripts |
| Docker | 24+ | For containerized deployment |
| MySQL | 8.0+ | Or use Docker Compose |

---

## Core Systems

| System | What It Does |
|--------|-------------|
| **Revenue Command Room OS** | Pipeline, drafts, follow-ups, founder daily actions |
| **Company Brain OS** | Signals, risks, decisions, opportunities with discipline |
| **WhatsApp Follow-up OS** | WhatsApp Cloud API + templates + approval before send |
| **AI Trust & Compliance OS** | PDPL + SDAIA + human review gates |
| **Client Delivery OS** | intake -> diagnosis -> blueprint -> sprint -> proof |

---

## Safety Defaults

All outbound communication is **draft-only** by default.
No message leaves the system without human approval.

```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
WHATSAPP_AGENT_MODE=dry_run
```

To verify safety at any time:
```bash
npm run outbound-dry
```

---

## Development

```bash
npm run dev        # Start dev server with HMR
npm run check      # TypeScript type-check
npm run build      # Production build
npm run preview    # Preview production build locally
```

---

## Daily Operations

```bash
npm run company-day        # Launch check + revenue engine + war room
npm run command-room       # Revenue command room generation
npm run full-revenue-day   # Revenue + outreach + war room sequence
npm run brain-day          # Governance + revenue scorecard
npm run client-day         # Client delivery workflow
npm run outbound-dry       # Safety gate verification
npm run production-check   # Full launch readiness check
```

---

## Environment Variables

Full reference: [`docs/ops/ENVIRONMENT_VARIABLES.md`](docs/ops/ENVIRONMENT_VARIABLES.md)

**Required:**
```env
DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix
NODE_ENV=development
PORT=3000
```

**WhatsApp (when ready):**
```env
WHATSAPP_ACCESS_TOKEN=your_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_id
WHATSAPP_WEBHOOK_VERIFY_TOKEN=your_verify_token
```

---

## Project Structure

```
api/                  Hono + tRPC backend
  boot.ts             Server entry point
  router.ts           Root tRPC router
  booking-router.ts   Booking management
  brain-router.ts     Brain OS operations
  command-room-router.ts  Revenue command room
  whatsapp-router.ts  WhatsApp integration
src/                  React + Vite frontend
  pages/              Main application pages
  sections/           Homepage sections
  components/ui/      shadcn/ui components
db/                   Drizzle ORM schema
scripts/              Operational engines and checks
  setup_local.sh      Unix setup script
  setup_local.ps1     Windows setup script
docs/                 Brand, ops, compliance docs
  ops/                Operational guides
  compliance/         PDPL + SDAIA documentation
business/products/    Product definitions and packaging
clients/_template/    Client delivery templates
company_os/           Reports, ledgers, operating artifacts
```

---

## Deployment

### Docker Compose (Recommended)

```bash
# Production with MySQL
docker compose up --build -d

# Check health
docker compose ps
docker compose logs app
```

### Manual Production

```bash
npm run build
NODE_ENV=production node dist/boot.js
```

### Pre-deployment Checklist

See [`docs/ops/GO_LIVE_CHECKLIST.md`](docs/ops/GO_LIVE_CHECKLIST.md) for the complete go-live checklist.

---

## Architecture

```
Browser
  |
  v
React SPA (Vite) ---- Static assets (dist/public/)
  |
  v
tRPC Client
  |
  v
Hono Server + tRPC Router (dist/boot.js)
  |
  +---> booking-router     --> MySQL (Drizzle ORM)
  +---> command-room-router --> MySQL (Drizzle ORM)
  +---> brain-router        --> MySQL (Drizzle ORM)
  +---> whatsapp-router     --> WhatsApp Cloud API (draft_only)
  |
  v
MySQL 8.0 (PlanetScale compatible)
```

---

## Compliance and Trust

- [`docs/compliance/PDPL_CHECKLIST.md`](docs/compliance/PDPL_CHECKLIST.md) — Saudi Personal Data Protection Law
- [`docs/compliance/SDAIA_AI_COMPLIANCE.md`](docs/compliance/SDAIA_AI_COMPLIANCE.md) — SDAIA AI Ethics

Operating principles:
- Human approval before all outbound communication
- Minimal necessary data handling
- Audit-friendly event logging
- No fabricated ROI claims or testimonials

---

## Product Positioning

Dealix is for B2B teams that already have leads, WhatsApp conversations,
spreadsheets, and delivery workflows — but lack prioritization,
reliable follow-up, decision visibility, and compliance-safe AI operations.

See [`business/products/PRICING_AND_PACKAGING.md`](business/products/PRICING_AND_PACKAGING.md) for packaging details.

---

## License

Proprietary — Dealix-sa
