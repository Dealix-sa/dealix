# `frontend/messages` — i18n conventions

Locale dictionaries for `next-intl`. One file per locale; the JSON shape
must stay identical across locales (missing key → runtime warning).

## The `ops.*` unified namespace (M12)

The cockpit's governed-control surfaces use a single top-level `ops`
namespace, grouped by surface. Add new cockpit strings here — don't
sprinkle inline `locale === "ar"` ternaries into components.

```
ops.governed.title
ops.governed.refresh
ops.governed.scheduler.{running,stopped,nextRun,lastDay,start,stopKill,runNow}
ops.governed.log.{title,empty,blockedSuffix}
```

Usage in a client component:

```tsx
import { useTranslations } from "next-intl";

const t  = useTranslations("ops.governed");
const ts = useTranslations("ops.governed.scheduler");
// ...
<h3>{t("title")}</h3>
<Button>{ts("stopKill")}</Button>
```

## Why not migrate the existing legacy namespaces?

`nav.*`, `opsHub.*`, `opsPages.*`, `targeting.*`, `warRoom.*` etc. are
left untouched on purpose — a big-bang rename would create merge churn
and silent missing-key warnings across the cockpit. Migrate components
to `ops.*` opportunistically as they're touched.

## Adding a key

1. Add the key under `ops.<surface>.<key>` in **both** `en.json` and
   `ar.json` (identical shape, different copy).
2. Reference via `useTranslations("ops.<surface>")`.
3. Build (`npm run build`) and watch the dev server log for missing-key
   warnings — they're loud and easy to spot.
