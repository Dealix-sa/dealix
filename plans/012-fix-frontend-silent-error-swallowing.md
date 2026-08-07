# 012 — Fix silent error-swallowing in the HR page + add a frontend smoke test

- **Finding:** `apps/web/app/[tenant]/hr/page.tsx:12-16` fetches employee
  data and swallows any fetch failure identically to an empty result:
    ```tsx
    useEffect(() => {
      fetch(`/api/v1/erp/hr/employees`, { headers: { "x-tenant-id": tenant } })
        .then((r) => r.json())
        .then((d) => { setEmployees(d); setLoading(false); })
        .catch(() => setLoading(false));
    }, [tenant]);
    ```
  A failed request (network error, 500, malformed JSON) renders the exact
  same "لا يوجد موظفين" (no employees) empty state (line 54) as a tenant
  that genuinely has zero employees — a user has no way to tell "the
  system is broken" from "you have no staff." The `+ موظف جديد` (add
  employee) button (line 26-28) also has no `onClick` handler — a dead
  control on a real, wired page. Separately, `apps/web` has **zero**
  automated tests anywhere (`*.test.*`/`*.spec.*` — none found; no
  jest/vitest/playwright config) despite ~130 routes and 147
  component/page files, and the `verify` gate (`apps/web/package.json:9-10`)
  is only `typecheck && build`, so a regression like this error-swallowing
  bug would never be caught by CI.
- **Category:** correctness / tests
- **Wave:** maintenance
- **Effort:** M   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read the files below before editing
```

## Context (inlined)
- Files in scope: `apps/web/app/[tenant]/hr/page.tsx`
- Full current file (63 lines) already quoted in the finding above and
  fetched during audit — the executor should re-read the file directly
  since it's short.
- Reference pattern to mirror (a page in this repo that already does this
  correctly): `apps/web/app/founder/command-room/page.tsx` — has explicit
  loading/error/empty states and a visible error message on fetch failure.
  Read that file's error-handling shape before writing the fix here so the
  UX pattern is consistent across the app.
- This repo has no test runner configured for `apps/web` yet — adding a
  full test framework is a larger decision (Jest vs Vitest vs Playwright)
  that should be a founder call, not something an executor silently picks.
  This plan scopes the test-coverage half narrowly: a single smoke check
  script, not a new framework.

## Steps
1. Fix `apps/web/app/[tenant]/hr/page.tsx` to track and surface fetch
   errors distinctly from an empty result:
    ```tsx
    "use client";

    import { useEffect, useState } from "react";
    import { useParams } from "next/navigation";

    export default function HRPage() {
      const params = useParams();
      const tenant = params.tenant as string;
      const [employees, setEmployees] = useState<any[]>([]);
      const [loading, setLoading] = useState(true);
      const [error, setError] = useState<string | null>(null);

      useEffect(() => {
        setError(null);
        fetch(`/api/v1/erp/hr/employees`, { headers: { "x-tenant-id": tenant } })
          .then((r) => {
            if (!r.ok) throw new Error(`HTTP ${r.status}`);
            return r.json();
          })
          .then((d) => { setEmployees(d); setLoading(false); })
          .catch((e) => { setError(String(e)); setLoading(false); });
      }, [tenant]);

      if (loading) return <div className="p-8 text-center">جاري التحميل...</div>;
      if (error) return <div className="p-8 text-center text-red-600">تعذّر تحميل بيانات الموظفين. حاول مرة أخرى لاحقاً.</div>;

      // ...rest unchanged
    ```
   Keep the rest of the JSX (the table) unchanged.
   **Gate:** `npm --prefix apps/web run typecheck` → passes.
2. Either wire the `+ موظف جديد` button to a real action, or if that
   feature genuinely doesn't exist yet, disable it visibly rather than
   leaving a dead click target:
    ```tsx
    <button
      className="bg-slate-300 text-slate-500 px-4 py-2 rounded-lg cursor-not-allowed"
      disabled
      title="قريباً"
    >
      + موظف جديد
    </button>
    ```
   Do not invent a fake "add employee" flow that doesn't call a real API —
   if there's no backend endpoint for creating an employee
   (`grep -rn "erp/hr/employees" api/routers/` to check for a POST
   handler), disabling the button honestly is the correct fix, not faking
   success.
   **Gate:** `grep -n "disabled" apps/web/app/\[tenant\]/hr/page.tsx` → 1 match (only if no POST endpoint exists; otherwise wire the real call and this gate doesn't apply — check first).
3. Add a minimal smoke-test script (no new test framework) that exercises
   this exact regression class — a Node script using the built-in
   `node:assert` that renders is out of scope for React without a runner,
   so instead add a Playwright-free static check: extend
   `apps/web/package.json`'s `verify` script is out of scope (that's a
   larger CI decision) — instead, just confirm the fix compiles and the
   error state string appears in the built output:
   `npm --prefix apps/web run build && grep -rn "تعذّر تحميل بيانات الموظفين" apps/web/.next/`
   **Gate:** grep finds the string in the build output (confirms the error
   branch is real, reachable JSX, not dead code eliminated by the bundler).

## Done criteria (machine-checkable)
- [ ] `npm --prefix apps/web run verify` → PASS (typecheck + build)
- [ ] `grep -n "catch(() => setLoading(false))" apps/web/app/\[tenant\]/hr/page.tsx` → no output (old swallow pattern removed)
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not introduce Jest/Vitest/Playwright or any new test framework/config
  in this plan — that's a bigger tooling decision for the founder.
- Do not touch any other page under `apps/web/app/` even if it has the
  same pattern — if found, report as a separate finding rather than fixing
  opportunistically (keeps this plan's diff reviewable).
- Do not implement a real "add employee" backend flow if one doesn't exist —
  disabling the button honestly is the in-scope fix.

## STOP conditions
- If `apps/web/app/[tenant]/hr/page.tsx` no longer matches the excerpt
  in the Finding above → STOP, re-run drift check.
- If a POST endpoint for creating employees already exists and the fix
  should wire the button instead of disabling it, but the request/response
  shape isn't obvious from `api/routers/` alone → STOP and report; do not
  guess a payload shape for a real mutating endpoint.
