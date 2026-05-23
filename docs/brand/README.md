# Dealix Brand-Growth Operating Layer — Entry Point

This folder is the entry point to Dealix's **Market Domination
Operating Layer**: a brand-led, founder-controlled, trust-gated, AI-
native Saudi B2B Revenue Operating System.

## Layers (in order)

1. [Brand System](DEALIX_BRAND_SYSTEM.md)
   ([visual](DEALIX_VISUAL_IDENTITY.md) ·
    [logo](DEALIX_LOGO_USAGE.md) ·
    [color](DEALIX_COLOR_SYSTEM.md) ·
    [typography](DEALIX_TYPOGRAPHY.md) ·
    [voice](DEALIX_BRAND_VOICE.md) ·
    [marketing assets](DEALIX_MARKETING_ASSET_GUIDE.md) ·
    [accessibility](DEALIX_ACCESSIBILITY_GUIDE.md))
2. [Category & Positioning](../positioning/)
3. [Market Intelligence](../intelligence_market/)
4. [Distribution War Machine](../growth/DISTRIBUTION_WAR_MACHINE.md)
5. [Revenue Factory](../revenue/REVENUE_FACTORY_OS.md)
6. [Product Marketing](../product/)
7. [Marketing OS](../marketing/DEALIX_MARKETING_OS.md)
8. [AI Agent OS](../ai/AGENT_REGISTRY.md)
9. [Performance Loop](../performance/PERFORMANCE_IMPROVEMENT_OS.md)

## Verify

```bash
make brand-system
make growth-system
make marketing-system
make product-distribution
make brand-growth-operating-layer
```

## Build the founder console

```bash
npm --prefix apps/web ci
npm --prefix apps/web run build
```

## Internal API endpoints

- `GET /api/v1/internal/brand/summary`
- `GET /api/v1/internal/growth/targeting`
- `GET /api/v1/internal/marketing/summary`
- `GET /api/v1/internal/product/distribution`

All read-only; all `source=fallback` until the runtime ledgers are
wired; none reach an external system.
