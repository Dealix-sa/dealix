#!/usr/bin/env bash
set -euo pipefail
echo "== Dealix Full Ops Setup =="
# 1) Core control files
touch DEALIX_STAGE_STATUS.md
touch DEALIX_ARCHITECTURE_MAP.md
touch DEALIX_EXECUTION_LEDGER.md
cat > DEALIX_STAGE_STATUS.md <<'EOF'
# Dealix Stage Status
| Gate | Area | Status | Score | Evidence | Owner | Next Action |
|---|---|---:|---:|---|---|---|
| 0 | Founder Clarity | FIX | 70 | docs/company/FOUNDER_CLARITY.md | Sami | Finalize positioning |
| 1 | Offer Readiness | FIX | 70 | docs/offers/revenue_sprint/OFFER.md | Sami | Finalize pricing and scope |
| 2 | Delivery Readiness | FIX | 60 | docs/delivery/revenue_sprint/ | Sami | Finish playbook and templates |
| 3 | Product Readiness | FIX | 80 | /health, /pricing, /demo-request | System | Verify checkout/payment |
| 4 | Trust Readiness | FIX | 75 | docs/trust/APPROVAL_MATRIX.md | Sami | Review claims and data policy |
| 5 | Sales Readiness | BLOCKED | 40 | private pipeline | Sami | Send first 25 DMs |
| 6 | First Client | BLOCKED | 0 | paid delivery | Sami | Close first sprint |
| 7 | Retainer | BLOCKED | 0 | monthly client | Sami | After 3 sprints |
| 8 | Scale | BLOCKED | 0 | SOP index | Sami | After repeatability |
## Rule
A stage is not complete unless it has:
1. A file.
2. A test or verification command.
3. Evidence.
4. PASS status.
EOF
cat > DEALIX_ARCHITECTURE_MAP.md <<'EOF'
# Dealix Architecture Map
## Public Product Layer
- api/ -> FastAPI backend and routers.
- apps/web/ -> web application.
- landing/ -> public website and sales pages.
- integrations/ -> external providers.
- db/ -> models, repositories, and source of truth.
## Intelligence Layer
- auto_client_acquisition/ -> acquisition workflows.
- autonomous_growth/ -> growth automation.
- dealix/agents/ -> AI decision and generation agents.
- evals/ -> quality tests and rubrics.
## Trust Layer
- dealix/trust/ -> policy, approvals, audit.
- dealix/registers/ -> no-overclaim and Saudi compliance registers.
- docs/trust/ -> governance policies.
## Operating Layer
- scripts/ -> verification scripts.
- tests/ -> automated tests.
- readiness/ -> stage gates and scorecards.
- .github/workflows/ -> CI/CD.
## Commercial Layer
- docs/offers/ -> what Dealix sells.
- docs/delivery/ -> how Dealix delivers.
- docs/public_sales/ -> public sales material.
## Private Ops Layer
The following must live outside the public repo:
- real clients
- real leads
- outreach queues
- call notes
- payment receipts
- pricing experiments
- private prompts
- confidential GTM strategy
EOF
cat > DEALIX_EXECUTION_LEDGER.md <<'EOF'
# Dealix Execution Ledger
## Current Execution Sprint
### Completed
- Created Dealix stage status file.
- Created architecture map.
- Created execution ledger.
- Created revenue sprint offer structure.
- Created delivery structure.
- Created trust governance structure.
- Added verification scripts.
- Added CI control workflow.
### Decisions
- Revenue Sprint is the primary commercial offer.
- Dealix OS vision remains internal until revenue is proven.
- Public repo is for product, trust, docs, demo, and proof.
- Private ops repo is for clients, leads, payments, outreach, and confidential operations.
### Blockers
- Live payment verification.
- First outbound campaign.
- First paid client.
- First delivery.
- First case study.
### Next 24 Hours
- Send first 25 founder-led DMs.
- Prepare 3 free samples.
- Close first paid Revenue Sprint.
- Update stage status with real evidence.
EOF
# 2) Directory structure
mkdir -p docs/company
mkdir -p docs/offers/revenue_sprint
mkdir -p docs/offers/revenue_desk
mkdir -p docs/delivery/revenue_sprint
mkdir -p docs/delivery/revenue_desk
mkdir -p docs/trust
mkdir -p docs/public_sales
mkdir -p docs/ops
mkdir -p readiness/gates readiness/checklists readiness/scorecards
mkdir -p landing
mkdir -p scripts
mkdir -p .github/workflows
# 3) Company docs
cat > docs/company/FOUNDER_CLARITY.md <<'EOF'
# Founder Clarity
## What Dealix Is
Dealix is a Saudi-native revenue intelligence and execution system for B2B companies.
## Primary Customer
Saudi B2B companies that sell services, software, consulting, real estate, logistics, marketing, ERP, CRM, cybersecurity, payments, or business solutions.
## Primary Pain
They need more qualified opportunities, clearer prioritization, better outreach, and a repeatable revenue process.
## Primary Offer
Dealix Revenue Sprint.
## Primary Outcome
Within 7-14 days, the client receives qualified Saudi B2B opportunities, scoring, outreach messages, and an execution memo.
## What We Do Not Sell Yet
- Full enterprise OS.
- Fully autonomous sales execution.
- Guaranteed revenue.
- Legal compliance certification.
- Large SaaS subscriptions before proof.
EOF
cat > docs/company/DEALIX_POSITIONING.md <<'EOF'
# Dealix Positioning
## One-Liner
Dealix helps Saudi B2B companies identify qualified sales opportunities, prioritize leads, and prepare outreach packs within 14 days.
## Internal Positioning
Dealix is a Full-Ops Saudi Revenue Machine where AI prepares, workflows execute, trust governs, and humans approve critical moves.
## External Positioning
Qualified Saudi B2B opportunities in 14 days.
## Tagline
Intelligent Deals. Real Growth.
## Messaging Pillars
1. Saudi-native revenue operations.
2. AI-assisted opportunity intelligence.
3. Approval-first execution.
4. Evidence-backed recommendations.
5. Privacy-conscious lead operations.
EOF
cat > docs/company/ICP.md <<'EOF'
# Ideal Customer Profile
## Best-Fit Customers
- Saudi B2B companies.
- Service or software businesses.
- Average deal size above 5,000 SAR.
- Need outbound, partnerships, or enterprise leads.
- Have a clear offer but weak lead generation.
## Priority Sectors
1. Marketing and digital agencies.
2. ERP, CRM, and business software providers.
3. Payments and invoicing solution providers.
4. Cybersecurity firms.
5. Logistics companies.
6. Commercial real estate and contracting.
7. B2B consulting firms.
8. Corporate training companies.
## Avoid Initially
- B2C.
- Very small retail.
- Restaurants.
- Low-ticket offers.
- Businesses without a clear sales process.
EOF
cat > docs/company/DO_NOT_SELL_YET.md <<'EOF'
# Do Not Sell Yet
Dealix must not sell these as primary offers before enough proof exists:
- Enterprise OS.
- Fully autonomous outbound.
- Guaranteed sales.
- Guaranteed revenue.
- Legal compliance certification.
- ZATCA Phase 2 readiness unless technically verified.
- PDPL compliance unless legally reviewed.
- White-label enterprise platform before repeatable delivery.
EOF
cat > docs/company/DECISION_RULES.md <<'EOF'
# Dealix Decision Rules
## Build
Build only if it supports:
- lead generation
- sales conversion
- payment
- delivery
- proof
- retention
- trust
## Defer
Defer anything that is impressive but does not move revenue now.
## Kill
Kill anything that increases complexity without supporting the revenue path.
## Manual First
Do not automate a workflow until it has worked manually at least 3-5 times.
## Revenue Path
Lead -> Reply -> Call -> Payment -> Delivery -> Proof -> Retainer
EOF
# 4) Offer docs
cat > docs/offers/revenue_sprint/OFFER.md <<'EOF'
# Dealix Revenue Sprint
## One-Line Offer
Dealix helps Saudi B2B companies identify qualified sales opportunities, prioritize leads, and prepare outreach packs within 14 days.
## Target Customer
Saudi B2B companies selling services, software, consulting, real estate, logistics, marketing, ERP, CRM, cybersecurity, payments, or business solutions.
## Deliverables
- 30-75 qualified Saudi B2B leads.
- ICP scoring.
- Lead priority grading: A / B / C.
- Pain hypothesis per account.
- Arabic and English outreach messages.
- Follow-up cadence.
- Executive memo.
- 14-day action plan.
## Timeline
7-14 days.
## What This Is Not
- Not guaranteed sales.
- Not guaranteed revenue.
- Not legal advice.
- Not mass spam automation.
- Not a replacement for the client's sales team.
## Approval Rule
No external commitment, claim, pricing change, contract change, or sensitive data export may happen without human approval.
EOF
cat > docs/offers/revenue_sprint/PRICING.md <<'EOF'
# Revenue Sprint Pricing
## Starter
2,500 SAR
Includes:
- 30 leads.
- Lead scoring.
- Arabic outreach messages.
- Executive memo.
## Growth
4,500 SAR
Includes:
- 75 leads.
- Scoring.
- Outreach pack.
- Follow-up cadence.
- 14-day action plan.
## Managed Pilot
9,500-25,000 SAR
Includes:
- Sprint deliverables.
- Weekly optimization.
- Pipeline support.
- Meeting prep.
- Dashboard snapshot.
## Payment Rule
Work starts after one of the following:
- successful online payment,
- bank transfer confirmation,
- signed purchase order,
- written approval from the client.
EOF
cat > docs/offers/revenue_sprint/SCOPE.md <<'EOF'
# Revenue Sprint Scope
## Included
- ICP review.
- Lead research.
- Lead scoring.
- Outreach copy.
- Follow-up cadence.
- Executive summary.
- Action plan.
## Excluded
- Guaranteed replies.
- Guaranteed meetings.
- Guaranteed revenue.
- Legal advice.
- Sending messages without approval.
- Managing paid ads.
- Full CRM implementation.
- Long-term sales management unless upgraded to Managed Pilot or Revenue Desk.
EOF
cat > docs/offers/revenue_sprint/FAQ.md <<'EOF'
# Revenue Sprint FAQ
## Do you guarantee sales?
No. Dealix does not guarantee sales or revenue. Dealix provides qualified opportunities, prioritization, outreach assets, and execution guidance.
## Do you send messages for us?
Only if explicitly included in a Managed Pilot and approved by the client.
## Is this a CRM?
No. Dealix may integrate with CRM workflows, but the Revenue Sprint is an opportunity intelligence and execution package.
## Is this legal or compliance advice?
No. Dealix provides privacy-conscious and approval-first workflows, but does not provide legal advice.
## When does work start?
After payment, purchase order, bank transfer confirmation, or written approval.
EOF
cat > docs/offers/revenue_sprint/PROPOSAL_TEMPLATE.md <<'EOF'
# Revenue Sprint Proposal Template
## Client
[Client Name]
## Objective
Identify qualified Saudi B2B opportunities and prepare an actionable outreach pack within 14 days.
## Deliverables
- [30/75] qualified leads.
- Lead scoring.
- Pain hypothesis.
- Outreach messages.
- Follow-up cadence.
- Executive memo.
- 14-day action plan.
## Timeline
Start: [Date]
Delivery: [Date]
## Investment
[Amount] SAR
## Payment
Work starts after payment, purchase order, bank transfer confirmation, or written approval.
## Approval
Client approves final outreach use and any external communication.
EOF
cat > docs/offers/revenue_sprint/TERMS.md <<'EOF'
# Revenue Sprint Terms
## Start Condition
Dealix starts work after one of the following:
- successful online payment,
- bank transfer confirmation,
- signed purchase order,
- written approval from the client.
## No Guarantee
Dealix does not guarantee sales, revenue, meetings, or replies.
## Client Approval
The client is responsible for approving any outbound use of messages, lead lists, claims, or campaign execution.
## Confidentiality
Client-specific files, leads, and delivery reports must be stored in private operational storage, not in the public repo.
EOF
# 5) Delivery docs
cat > docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md <<'EOF'
# Revenue Sprint Delivery Playbook
## Day 0 - Intake
- Confirm client ICP.
- Confirm offer.
- Confirm target sectors.
- Confirm exclusions.
- Confirm delivery date.
## Day 1-2 - Research
- Gather target accounts.
- Remove irrelevant accounts.
- Remove duplicates.
- Check obvious fit.
## Day 3-4 - Scoring
- Score fit.
- Score likely pain.
- Score contactability.
- Assign A/B/C priority.
## Day 5-6 - Outreach Pack
- Draft Arabic messages.
- Draft English messages if needed.
- Draft follow-up cadence.
- Prepare CTA options.
## Day 7-10 - Executive Memo
- Summarize ICP.
- Summarize best opportunities.
- Identify top segments.
- Prepare 14-day action plan.
## Day 11-14 - QA and Handoff
- Run QA checklist.
- Verify no overclaims.
- Verify evidence.
- Deliver final report.
EOF
cat > docs/delivery/revenue_sprint/CLIENT_INTAKE.md <<'EOF'
# Revenue Sprint Client Intake
## Company
- Company name:
- Website:
- Sector:
- City:
- Contact person:
## Offer
- What do you sell?
- Average deal size:
- Best customers:
- Worst-fit customers:
- Geographic target:
## ICP
- Target sectors:
- Target company size:
- Target roles:
- Exclusions:
## Sales Context
- Current sales process:
- Current CRM:
- Main objection:
- Existing outreach:
- Preferred tone:
## Delivery
- Preferred language:
- Deadline:
- Format:
EOF
cat > docs/delivery/revenue_sprint/LEAD_TABLE_SCHEMA.md <<'EOF'
# Lead Table Schema
| Field | Required | Description |
|---|---:|---|
| company_name | Yes | Company name |
| sector | Yes | Business sector |
| website | Preferred | Company website |
| city | Preferred | Saudi city |
| contact_role | Preferred | Target role |
| fit_score | Yes | 0-100 |
| priority | Yes | A / B / C |
| pain_hypothesis | Yes | Why this company may need the offer |
| evidence | Yes | Why this lead was selected |
| outreach_message_ar | Yes | Arabic message |
| outreach_message_en | Preferred | English message |
| risk_level | Yes | Low / Medium / High |
| next_action | Yes | Recommended action |
EOF
cat > docs/delivery/revenue_sprint/REPORT_TEMPLATE.md <<'EOF'
# Revenue Sprint Report Template
## 1. Executive Summary
[Brief summary of best opportunities and recommended action.]
## 2. ICP Summary
[Client ICP and targeting logic.]
## 3. Lead List
[Lead table.]
## 4. Scoring Logic
[How leads were prioritized.]
## 5. Outreach Pack
[Arabic and English messages.]
## 6. Follow-Up Cadence
[Follow-up 1, 2, 3.]
## 7. 14-Day Action Plan
[Day-by-day execution plan.]
## 8. Risks and Assumptions
[Data limits, assumptions, exclusions.]
## 9. Next Step
[Recommended next commercial or execution step.]
EOF
cat > docs/delivery/revenue_sprint/QA_CHECKLIST.md <<'EOF'
# Revenue Sprint QA Checklist
Before delivery, verify:
## Lead Quality
- Every lead matches the ICP.
- Every lead has a clear reason for inclusion.
- Every lead has A/B/C score.
- Duplicate leads removed.
## Outreach Quality
- Messages are specific, not generic.
- No guaranteed sales claim.
- No misleading compliance claim.
- Arabic and English are professional.
## Trust
- No sensitive personal data included unnecessarily.
- Opt-out or suppression requests respected.
- Evidence included for important recommendations.
- No claim leaves without support.
## Delivery
- Executive summary included.
- Lead table included.
- Outreach pack included.
- 14-day action plan included.
- Next step clearly stated.
EOF
cat > docs/delivery/revenue_sprint/HANDOFF_TEMPLATE.md <<'EOF'
# Revenue Sprint Handoff Template
## Client
[Client Name]
## Delivered Files
- Revenue Sprint Report
- Lead Table
- Outreach Pack
- 14-Day Action Plan
## Recommended Next Step
[Next action.]
## Optional Upgrade
- Managed Pilot
- Revenue Desk monthly retainer
## Notes
[Important assumptions, exclusions, and client-specific notes.]
EOF
# 6) Trust docs
cat > docs/trust/APPROVAL_MATRIX.md <<'EOF'
# Dealix Approval Matrix
## A0 - Fully Automatic
Allowed:
- internal lead scoring
- duplicate removal
- CRM status update
- draft generation
- internal reports
## A1 - Human Review Recommended
Requires quick review:
- first outbound message
- sample pack
- public content
- lead list delivery
- proposal draft
## A2 - Human Approval Required
Requires explicit approval:
- pricing changes
- proposal sending
- client delivery
- payment terms
- public case study
- customer data export
## A3 - Never Auto-Execute
Never automatic:
- contract changes
- NDAs
- legal commitments
- regulator communication
- refunds
- sensitive data exports
- claims of guaranteed revenue
- claims of full legal compliance
EOF
cat > docs/trust/NO_OVERCLAIM_POLICY.md <<'EOF'
# No-Overclaim Policy
Dealix must not claim:
- guaranteed sales
- guaranteed revenue
- full legal compliance
- official certification
- ZATCA Phase 2 readiness unless technically verified
- PDPL compliance unless legally reviewed
Preferred language:
- PDPL-aware workflows
- approval-first operations
- evidence-backed recommendations
- Saudi-native revenue operations
- privacy-conscious lead operations
EOF
cat > docs/trust/DATA_RETENTION_POLICY.md <<'EOF'
# Data Retention Policy
## Principle
Dealix keeps only what is needed for delivery, evidence, operations, and legal/business records.
## Lead Data
Lead data should be minimized, relevant, and connected to a clear business purpose.
## Client Data
Client-specific files must live in private operational storage.
## Deletion
Data should be deleted or archived when no longer needed.
## Suppression
Opt-out or do-not-contact requests must be retained in a suppression list to prevent future outreach.
EOF
cat > docs/trust/SUPPRESSION_LIST_POLICY.md <<'EOF'
# Suppression List Policy
## Purpose
Prevent contacting people or companies that have opted out or requested no contact.
## Rule
If any person or company asks not to be contacted, they must be added to the suppression list.
## Enforcement
Before outreach or delivery, check suppression status.
## Storage
Suppression list belongs in private operational storage, not the public repo.
EOF
cat > docs/trust/INCIDENT_RESPONSE.md <<'EOF'
# Incident Response
## Incident Types
- accidental client data exposure
- wrong recipient
- leaked secret
- failed payment webhook
- misleading public claim
- unauthorized data export
## First 24 Hours
1. Stop the affected workflow.
2. Preserve evidence.
3. Identify impacted records.
4. Notify the responsible owner.
5. Remove exposed data if possible.
6. Rotate secrets if needed.
7. Write an incident note.
8. Decide corrective action.
## Owner
Founder approval is required for sensitive incidents.
EOF
cat > docs/trust/PUBLIC_REPO_SAFETY.md <<'EOF'
# Public Repo Safety
The public repo must not contain:
- real client private data
- real lead lists
- outreach queues
- call notes
- payment receipts
- bank details
- private prompts
- confidential GTM strategy
Allowed:
- public docs
- product code
- demo data
- sample templates
- high-level architecture
- trust policies
EOF
# 7) Public sales docs
cat > docs/public_sales/REVENUE_SPRINT_ONE_PAGER.md <<'EOF'
# Dealix Revenue Sprint One-Pager
## Headline
Qualified Saudi B2B opportunities in 14 days.
## What You Get
- 30-75 qualified leads.
- Lead scoring.
- Outreach messages.
- Executive memo.
- 14-day action plan.
## Best For
Saudi B2B companies that need better outbound, partnerships, and sales opportunities.
## Important
Dealix does not guarantee sales or revenue. Dealix provides opportunity intelligence and execution assets.
EOF
cat > docs/public_sales/CASE_STUDY_TEMPLATE.md <<'EOF'
# Case Study Template
## Client Type
[Sector / size / region]
## Problem
[What they struggled with.]
## Dealix Work
[What Dealix delivered.]
## Result
[Measured or qualitative result.]
## What Changed
[Before vs after.]
## Next Step
[Retainer / pilot / expansion.]
EOF
cat > docs/public_sales/PARTNER_PROGRAM.md <<'EOF'
# Dealix Partner Program
## Partner Types
- agencies
- consultants
- software vendors
- business development partners
## Model
Partners refer or resell Dealix Revenue Sprint and Managed Pilot offers.
## Requirements
- No overclaims.
- No guaranteed revenue claims.
- Client approval required.
- Clear scope and pricing.
EOF
# 8) Ops docs
cat > docs/ops/SOP_INDEX.md <<'EOF'
# SOP Index
## Revenue
- Founder outreach.
- Follow-up.
- Proposal.
- Payment verification.
## Delivery
- Intake.
- Research.
- Scoring.
- Outreach pack.
- QA.
- Handoff.
## Trust
- Approval.
- Suppression.
- No-overclaim.
- Incident response.
EOF
cat > docs/ops/DAILY_OPERATING_LOOP.md <<'EOF'
# Daily Operating Loop
Every day:
1. Review revenue dashboard.
2. Review pipeline.
3. Send founder-led outreach.
4. Prepare or improve samples.
5. Check active delivery tasks.
6. Review approvals.
7. Update execution ledger.
EOF
cat > docs/ops/WEEKLY_OPERATING_REVIEW.md <<'EOF'
# Weekly Operating Review
## Revenue
- Cash collected:
- Proposals sent:
- Calls booked:
- New paid customers:
- MRR:
## Sales
- Outbound sent:
- Replies:
- Samples sent:
- Follow-ups:
- Best message:
## Delivery
- Active clients:
- Reports delivered:
- Overdue:
- QA issues:
## Product
- CI status:
- Failed tests:
- Bugs:
- New useful feature:
## Trust
- Opt-outs:
- Approval escalations:
- Data issues:
- Claims needing evidence:
## Founder Decisions
- Build:
- Fix:
- Kill:
- Defer:
EOF
# 9) Landing page
cat > landing/revenue-sprint.html <<'EOF'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Dealix Revenue Sprint</title>
  <meta name="description" content="Qualified Saudi B2B leads, outreach packs, and execution plan within 14 days.">
  <meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
  <main>
    <h1>Qualified Saudi B2B opportunities in 14 days.</h1>
    <p>Dealix helps Saudi B2B companies identify qualified leads, prioritize opportunities, and prepare Arabic/English outreach packs.</p>
    <h2>What you get</h2>
    <ul>
      <li>30-75 qualified leads</li>
      <li>A/B/C prioritization</li>
      <li>Pain hypothesis per account</li>
      <li>Arabic and English outreach messages</li>
      <li>14-day action plan</li>
    </ul>
    <h2>Pricing</h2>
    <p>Starter from 2,500 SAR. Growth from 4,500 SAR.</p>
    <h2>Trust</h2>
    <p>Approval-first, evidence-backed, privacy-conscious revenue operations. No guaranteed sales claims.</p>
    <a href="/demo">Request a sample</a>
  </main>
</body>
</html>
EOF
# 10) Verification scripts
cat > scripts/verify_docs_complete.py <<'EOF'
from pathlib import Path
REQUIRED_FILES = [
    "DEALIX_STAGE_STATUS.md",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "docs/company/FOUNDER_CLARITY.md",
    "docs/company/DEALIX_POSITIONING.md",
    "docs/company/ICP.md",
    "docs/company/DO_NOT_SELL_YET.md",
    "docs/company/DECISION_RULES.md",
    "docs/offers/revenue_sprint/OFFER.md",
    "docs/offers/revenue_sprint/PRICING.md",
    "docs/offers/revenue_sprint/SCOPE.md",
    "docs/offers/revenue_sprint/FAQ.md",
    "docs/offers/revenue_sprint/PROPOSAL_TEMPLATE.md",
    "docs/offers/revenue_sprint/TERMS.md",
    "docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md",
    "docs/delivery/revenue_sprint/CLIENT_INTAKE.md",
    "docs/delivery/revenue_sprint/LEAD_TABLE_SCHEMA.md",
    "docs/delivery/revenue_sprint/REPORT_TEMPLATE.md",
    "docs/delivery/revenue_sprint/QA_CHECKLIST.md",
    "docs/delivery/revenue_sprint/HANDOFF_TEMPLATE.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/trust/DATA_RETENTION_POLICY.md",
    "docs/trust/SUPPRESSION_LIST_POLICY.md",
    "docs/trust/INCIDENT_RESPONSE.md",
    "docs/trust/PUBLIC_REPO_SAFETY.md",
    "docs/public_sales/REVENUE_SPRINT_ONE_PAGER.md",
    "docs/public_sales/CASE_STUDY_TEMPLATE.md",
    "docs/public_sales/PARTNER_PROGRAM.md",
    "docs/ops/SOP_INDEX.md",
    "docs/ops/DAILY_OPERATING_LOOP.md",
    "docs/ops/WEEKLY_OPERATING_REVIEW.md",
    "landing/revenue-sprint.html",
    ".github/workflows/dealix-control.yml",
]
missing = [file for file in REQUIRED_FILES if not Path(file).exists()]
if missing:
    print("Missing required files:")
    for file in missing:
        print(f"- {file}")
    raise SystemExit(1)
empty = []
for file in REQUIRED_FILES:
    path = Path(file)
    if path.exists() and path.is_file() and path.stat().st_size == 0:
        empty.append(file)
if empty:
    print("Empty required files:")
    for file in empty:
        print(f"- {file}")
    raise SystemExit(1)
print("PASS: all required Dealix control files exist and are not empty.")
EOF
cat > scripts/verify_architecture.py <<'EOF'
from pathlib import Path
ALLOWED_TOP_LEVEL = {
    ".github",
    ".claude",
    ".cursor",
    "alembic",
    "api",
    "apps",
    "auto_client_acquisition",
    "autonomous_growth",
    "clients",
    "core",
    "dashboard",
    "data",
    "db",
    "dealix",
    "demos",
    "design-skills",
    "design-systems",
    "docs",
    "evals",
    "frontend",
    "integrations",
    "landing",
    "migrations",
    "platform_core",
    "projects",
    "readiness",
    "scripts",
    "simulations",
    "supabase",
    "templates",
    "tests",
}
ALLOWED_ROOT_FILES = {
    "README.md",
    "README.ar.md",
    "QUICK_START.md",
    "DEPLOYMENT.md",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "CHANGELOG.md",
    "DASHBOARD.md",
    "DEALIX_COMPANY_OPERATIONAL_STATE.md",
    "DEALIX_READINESS.md",
    "DEALIX_STAGE_STATUS.md",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "AGENTS.md",
    "Dockerfile",
    "Procfile",
    "Makefile",
    "docker-compose.yml",
    "alembic.ini",
    "cli.py",
    "lighthouserc.js",
    "locustfile.py",
    "pyproject.toml",
    "railway.json",
    "railway.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "v3_app.py",
    ".dockerignore",
    ".editorconfig",
    ".env.example",
    ".env.staging.example",
    ".gitignore",
    ".gitleaks.toml",
    ".pa11yrc.json",
    ".pre-commit-config.yaml",
    ".secrets.baseline",
}
violations = []
for item in Path(".").iterdir():
    name = item.name
    if name == ".git":
        continue
    if item.is_dir() and name not in ALLOWED_TOP_LEVEL:
        violations.append(f"Unexpected top-level directory: {name}")
    if item.is_file() and name not in ALLOWED_ROOT_FILES:
        violations.append(f"Unexpected root file: {name}")
if violations:
    print("Architecture violations:")
    for violation in violations:
        print(f"- {violation}")
    raise SystemExit(1)
print("PASS: repository architecture matches Dealix approved map.")
EOF
cat > scripts/verify_public_safety.py <<'EOF'
import re
from pathlib import Path

SKIP_FILES = {
    "scripts/verify_public_safety.py",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "docs/trust/PUBLIC_REPO_SAFETY.md",
}

SKIP_DIR_PREFIXES = (
    ".git/",
    "node_modules/",
    ".venv/",
    "venv/",
    "dist/",
    "build/",
    "__pycache__/",
    "tests/",
)

BLOCKED_PATH_PARTS = [
    "real_leads",
    "private_pipeline_data",
    "outreach_queue_real",
    "payment_receipts_real",
    "client_call_notes",
    "customer_bank_details",
    "customer_secrets",
]

REAL_SECRET_PATTERNS = [
    re.compile(r"sk_live_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{30,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"AIza[0-9A-Za-z_\-]{30,}"),
    re.compile(r"ghp_[A-Za-z0-9]{30,}"),
    re.compile(r"gho_[A-Za-z0-9]{30,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{40,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |ENCRYPTED )?PRIVATE KEY-----"),
    re.compile(r"eyJ[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]{20,}"),
]

TEXT_EXTENSIONS = {".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".py", ".ts", ".tsx", ".js", ".html", ".env"}

violations = []

for path in Path(".").rglob("*"):
    if path.is_dir():
        continue
    rel = path.as_posix()
    if any(rel.startswith(prefix) or f"/{prefix}" in rel for prefix in SKIP_DIR_PREFIXES):
        continue
    if rel in SKIP_FILES:
        continue

    lower_path = rel.lower()
    for blocked in BLOCKED_PATH_PARTS:
        if blocked in lower_path:
            violations.append(f"Blocked path pattern: {rel}")

    if path.suffix.lower() not in TEXT_EXTENSIONS:
        continue
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        continue
    for pattern in REAL_SECRET_PATTERNS:
        match = pattern.search(text)
        if match:
            violations.append(f"Potential real secret in {rel}: pattern '{pattern.pattern}'")

if violations:
    print("Public safety violations:")
    for violation in violations:
        print(f"- {violation}")
    raise SystemExit(1)
print("PASS: no obvious public safety violations found.")
EOF
# 11) CI workflow
cat > .github/workflows/dealix-control.yml <<'EOF'
name: Dealix Control Checks
on:
  pull_request:
  push:
    branches: [main]
jobs:
  dealix-control:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Verify required docs
        run: python scripts/verify_docs_complete.py
      - name: Verify architecture
        run: python scripts/verify_architecture.py
      - name: Verify public safety
        run: python scripts/verify_public_safety.py
      - name: Compile Python
        run: python -m compileall api dealix db integrations scripts
EOF
echo "== Running verification =="
python scripts/verify_docs_complete.py
python scripts/verify_architecture.py
python scripts/verify_public_safety.py
if [ -d "api" ] && [ -d "dealix" ]; then
  python -m compileall api dealix db integrations scripts || true
fi
echo "== Dealix Full Ops Setup Complete =="
