# Page Map — Dealix Public Website — خريطة الصفحات

Every public route on the Dealix website (Next.js, `apps/web`), its purpose, its primary CTA, and bilingual status. AR/EN status legend: **Ready** = approved copy loaded; **Draft** = copy in deck, pending review; **Mirror** = content mirrors the EN/AR counterpart.

## Route table — جدول المسارات

| Route | Purpose — الغرض | Primary CTA | AR status | EN status |
|---|---|---|---|---|
| `/` | Arabic-first home; positioning, problem, solution, verticals | Request AI Workflow Audit | Ready | Mirror at `/en` |
| `/en` | English home for GCC / international readers | Request AI Workflow Audit | Mirror | Ready |
| `/commercial` | Commercial overview: offer ladder, how engagements work | Book Diagnostic | Draft | Draft |
| `/services` | Service scope: audit, pilot, department OS, retainer | Book Diagnostic | Draft | Draft |
| `/pricing` | Offer ladder in SAR with scope per tier | Start Pilot | Draft | Draft |
| `/trust` | Approval-first, human-in-the-loop, PDPL-aware posture, no blind automation | Request AI Workflow Audit | Draft | Draft |
| `/launch` | Launch status, what is live, what is review-only | Book Diagnostic | Draft | Draft |
| `/contact` | Contact and intake; routes to founder review queue | Book Diagnostic | Draft | Draft |
| `/status` | System and service status | (none — informational) | Mirror | Ready |
| `/verticals` | Index of the five priority sectors | Book Diagnostic | Draft | Draft |
| `/verticals/facilities-management` | FM workflow patterns and offers | Request AI Workflow Audit | Draft | Draft |
| `/verticals/contracting-project-controls` | Contracting and project controls patterns | Request AI Workflow Audit | Draft | Draft |
| `/verticals/real-estate-property-ops` | Real estate and property operations patterns | Request AI Workflow Audit | Draft | Draft |
| `/verticals/legal-professional-services` | Legal and professional services patterns | Request AI Workflow Audit | Draft | Draft |
| `/verticals/consulting-training-b2b` | Consulting and B2B training patterns | Request AI Workflow Audit | Draft | Draft |
| `/case-method` | The case-safe method: how Dealix documents outcomes without overclaiming | Book Diagnostic | Draft | Draft |
| `/media` | Media and social calendar planning, press posture | (none — informational) | Draft | Draft |
| `/faq` | Frequently asked questions, including the no-send governing rule | Book Diagnostic | Draft | Draft |

## CTA routing — توجيه الدعوات للفعل

All three CTAs route to founder-reviewed intake. No CTA triggers external sending.

- **Request AI Workflow Audit** → `/contact` intake → founder review queue.
- **Book Diagnostic** → `/contact` intake (diagnostic intent) → founder review queue.
- **Start Pilot** → `/contact` intake (pilot intent) → founder review queue.

## Notes — ملاحظات

- `/status`, `/media` carry no commercial CTA; they are informational.
- Internal ops surfaces (`/control-plane`, `/agents`, `/approvals`, `/sandbox`, `/self-evolving`) are not public marketing routes and are disallowed in `robots.ts`.
- AR is the default surface at `/`; EN lives at `/en`. Each vertical page must ship AR and EN in parity before its status moves to Ready.

## Related — روابط

- `docs/site-launch/02_SEO_CHECKLIST.md`
- `docs/site-launch/03_COPY_DECK_AR_EN.md`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
