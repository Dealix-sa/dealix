# 016 — Remove the founder's personal Gmail from the public landing site

- **Finding:** `landing/index.html` publishes the founder's personal Gmail
  address (`sami.assiri11@gmail.com`) in two places visible to every site
  visitor and every search engine/crawler:
  - `landing/index.html:50` — schema.org `Organization` JSON-LD structured
    data: `"contactPoint": {"@type": "ContactPoint", "contactType":
    "sales", "email": "sami.assiri11@gmail.com", ...}`.
  - `landing/index.html:849` — page footer: `<a
    href="mailto:sami.assiri11@gmail.com">sami.assiri11@gmail.com</a>`.
  A personal Gmail address as the public "sales" contact point undermines
  the professional/enterprise trust positioning the rest of the site
  argues for (PDPL/SAMA/NCA compliance messaging, "Trust Center" links,
  etc. elsewhere in the same footer) and ties the founder's personal
  identity to every inbound sales inquiry indefinitely. The repo already
  uses company-domain addresses elsewhere on the same site — this is a
  two-line consistency fix, not a new convention.
- **Category:** doctrine / privacy
- **Wave:** maintenance
- **Effort:** S   **Confidence:** HIGH
- **Written against commit:** aae97bcefcf73e74aef8c75ac593238dc1ed690e

## Drift check (run first)
```bash
git rev-parse HEAD   # if != aae97bcefcf73e74aef8c75ac593238dc1ed690e, re-read landing/index.html before editing
```

## Context (inlined)
- File in scope: `landing/index.html` (static marketing site, separate
  from `apps/web/`).
- Company-domain addresses already used elsewhere in `landing/*.html`
  (confirmed via `grep -rohE "[a-zA-Z0-9._%+-]+@dealix\.(me|sa)"
  landing/*.html | sort | uniq -c`): `sami@dealix.me` (2 uses, founder
  contact), `sales@dealix.sa` (4 uses, matches the `contactType: "sales"`
  semantics of the JSON-LD block), `hello@dealix.me`, `founder@dealix.me` /
  `founder@dealix.sa`. Use these existing conventions — do not invent a
  new address.
- Current state, `landing/index.html:50`:
    ```html
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": "sami.assiri11@gmail.com", "availableLanguage": ["Arabic","English"]}
    ```
- Current state, `landing/index.html:849`:
    ```html
    <div><h4>تواصل</h4><ul><li><a href="mailto:sami.assiri11@gmail.com">sami.assiri11@gmail.com</a></li><li><a href="/diagnostic.html">ابدأ الفحص المجاني</a></li></ul></div>
    ```

## Steps
1. In `landing/index.html:50`, replace the JSON-LD `contactPoint.email`
   value with `sales@dealix.sa` (already used elsewhere on the same site
   with matching `contactType: "sales"` semantics):
    ```html
    "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "email": "sales@dealix.sa", "availableLanguage": ["Arabic","English"]}
    ```
   **Gate:** `grep -n "sami.assiri11@gmail.com" landing/index.html` → no
   output after this step and step 2 combined.
2. In `landing/index.html:849`, replace both the `href` and the visible
   link text with `sami@dealix.me` (preserves the "reach the founder
   directly" intent already used elsewhere on the site, without exposing
   a personal Gmail):
    ```html
    <div><h4>تواصل</h4><ul><li><a href="mailto:sami@dealix.me">sami@dealix.me</a></li><li><a href="/diagnostic.html">ابدأ الفحص المجاني</a></li></ul></div>
    ```
   **Gate:** `grep -n "sami@dealix.me" landing/index.html` → 1 match.
3. Search the rest of `landing/` and the repo generally for any other
   occurrence of the personal Gmail address that this plan's two-file
   scope might have missed:
   `grep -rln "sami.assiri11@gmail.com" --include="*.html" --include="*.json" --include="*.md" .`
   For any additional hit outside `landing/index.html`, apply the same
   company-domain substitution (sales context → `sales@dealix.sa`;
   founder-direct context → `sami@dealix.me`).
   **Gate:** command output reviewed and empty (or every hit fixed).

## Done criteria (machine-checkable)
- [ ] `grep -rn "sami.assiri11@gmail.com" .` → no output repo-wide
- [ ] `python3 -c "import json,re; html=open('landing/index.html').read(); [json.loads(m) for m in re.findall(r'<script type=\"application/ld\\+json\">(.*?)</script>', html, re.S)]"` → no exception (confirms the edited JSON-LD block is still valid JSON)
- [ ] `make full-repo-test` → all required gates PASS

## Out of scope (do not touch)
- Do not touch `apps/web/` — separate frontend, not in scope.
- Do not remove or restructure the footer's other columns/links.
- Do not change the `contactType` or any other JSON-LD field besides
  `email`.

## STOP conditions
- If `landing/index.html:50` or `:849` no longer match the excerpts above
  → STOP, re-run drift check; the page may have already been corrected.
- If `sami.assiri11@gmail.com` appears anywhere the founder may be
  actively using it for live correspondence in a way a search-and-replace
  could break (e.g. a signed contract template, not just marketing copy)
  → STOP that specific instance and report rather than substituting
  automatically.
