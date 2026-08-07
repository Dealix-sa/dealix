# Tech Debt Register

| ID | Location | Issue | Fix |
|----|----------|-------|-----|
| TD-01 | scripts/import_leads.py | Hardcodes API URL, no local pipeline | Create local-first import_leads_csv.py |
| TD-02 | apps/web/ | node_modules missing, build fails | Document npm install step; add CI |
| TD-03 | business/ | Only 2 markdown files, no schemas | Create full schema + data layer |
| TD-04 | scripts/ | No shared lib, path duplication | Create scripts/lib/ |
| TD-05 | apps/web/app/ | No outreach-lab, operator, legal, pipeline pages | Add pages |
| TD-06 | apps/web/app/api/ | No health/commercial-os route | Add route.ts |
| TD-07 | .env.example | Missing connector placeholders | Add GOOGLE_PLACES_API_KEY, WHATSAPP_BUSINESS_TOKEN, etc. |
| TD-08 | tests/ | Missing 6 unit tests for new commercial layer | Add tests |
| TD-09 | docs/ | Missing deploy, security, PDF docs | Add docs |
| TD-10 | connectors/ | Directory does not exist | Create safe stubs |
