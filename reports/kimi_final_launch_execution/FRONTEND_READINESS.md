# FRONTEND LAUNCH READINESS REPORT

## Frontend Structure
| Property | `frontend/` (Canonical) | `apps/web/` (Legacy) |
|----------|------------------------|----------------------|
| Next.js | 15.1.3 | 15.1.3 |
| React | 19.0.0 | 19.0.0 |
| TypeScript | 5.6.3 | 5.6.3 |
| Tailwind | 3.4.14 | 3.4.0 |
| i18n | next-intl 3.22.0 | ❌ None |
| Port | 3000 | 3100 |
| UI Components | Radix UI full suite | Minimal |
| Charts | Recharts | ❌ None |
| Forms | react-hook-form + zod | ❌ None |
| Animations | framer-motion | ❌ None |

## Surfaces in `frontend/` (Canonical)
| Route | Purpose | Auth |
|-------|---------|------|
| `/[locale]/` | Public landing (CommercialLaunchHome) | Public |
| `/[locale]/dealix-diagnostic` | Diagnostic tool | Public |
| `/[locale]/risk-score` | Risk assessment | Public |
| `/[locale]/proof-pack` | Proof pack | Public |
| `/[locale]/learn/[slug]` | Learning center | Public |
| `/[locale]/partners` | Partners page | Public |
| `/[locale]/business-now` | 8 pillars + strategy | Public |
| `/[locale]/cloud` | Dealix Cloud UI | Public |
| `/[locale]/ops` | Ops hub (admin key) | Admin API Key |
| `/[locale]/ops/founder` | Founder 90-min cockpit | Admin API Key |
| `/[locale]/ops/command-room` | Command room | Admin API Key |
| `/[locale]/ops/war-room` | War room | Admin API Key |
| `/[locale]/ops/marketing` | Marketing ops | Admin API Key |
| `/[locale]/ops/sales` | Sales ops | Admin API Key |
| `/[locale]/ops/evidence` | Evidence board | Admin API Key |
| `/[locale]/ops/approvals` | Approval center | Admin API Key |

## SEO Surfaces
| File | Purpose |
|------|---------|
| `frontend/src/app/robots.ts` | robots.txt |
| `frontend/src/app/sitemap.ts` | XML sitemap |
| `frontend/app/[locale]/layout.tsx` | Metadata, OG tags |

## CTA Path Verification
| CTA | Target Route | Backend API | Status |
|-----|-------------|-------------|--------|
| "Get Diagnostic" | `/dealix-diagnostic` | `POST /api/v1/diagnostic/intent` | ✅ |
| "Book Demo" | External Calendly | `CALENDLY_URL` | ✅ |
| "Submit Lead" | `/` form | `POST /api/v1/leads` | ✅ |
| "View Pricing" | `/pricing` (redirects) | `GET /api/v1/business/pricing` | ✅ |

## `apps/web/` Assessment
**Status**: Legacy supplementary app with minimal pages.
**Unique pages to preserve**:
- `/control-plane` → Candidate for merge into `frontend/[locale]/ops/`
- `/data-room` → Candidate for merge
- `/proof-vault` → `frontend/` already has `/proof-pack`
- `/war-room` → `frontend/` already has `/ops/war-room`

**Recommendation**: Deprecate `apps/web/` after merging unique pages. Do not delete until merge confirmed.

## Acceptance
| Check | Status |
|-------|--------|
| `frontend/package.json` scripts valid | ✅ |
| `apps/web/package.json` scripts valid | ✅ |
| Arabic/English i18n configured | ✅ (frontend/ only) |
| Sitemap exists | ✅ |
| Robots.txt exists | ✅ |
| CTA paths match backend APIs | ✅ |
| No overclaims in public copy | ✅ (verified against CLAIMS_EVIDENCE_MATRIX) |

## P0: Build Verification Required
**Frontend build not yet run** — requires `npm install`.
This is documented as environment-only, not a code defect.

## Verdict: ✅ FRONTEND STRUCTURE READY (build verification needed)
