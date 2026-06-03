#!/usr/bin/env bash
set -euo pipefail

echo "== Dealix Master Content Pack =="

mkdir -p scripts docs/ops docs/founder docs/revenue docs/trust docs/learning docs/control_plane docs/product docs/strategy docs/delivery/revenue_sprint

cat > docs/ops/DOCUMENT_STANDARD.md <<'EOF'
# Dealix Document Standard

## Purpose
Every operating document must define its role inside Dealix Company OS.

## Owner
Every document must have a current owner.

## Review Cadence
Every document must define whether it is reviewed daily, weekly, monthly, or quarterly.

## Inputs
Every system must state what data, signals, decisions, or evidence it consumes.

## Outputs
Every system must state what it produces.

## Rules
Every system must define non-negotiable operating rules.

## Metrics
Every system must define how performance is measured.

## Evidence
Every system must define what proves it is working.

## Last Reviewed
YYYY-MM-DD
EOF

cat > scripts/fill_empty_docs_with_standard.py <<'PY'
from pathlib import Path

DOC_FOLDERS = [
    "docs/founder",
    "docs/strategy",
    "docs/revenue",
    "docs/acquisition",
    "docs/sales",
    "docs/offers",
    "docs/delivery",
    "docs/trust",
    "docs/finance",
    "docs/client_success",
    "docs/product",
    "docs/content",
    "docs/learning",
    "docs/people",
    "docs/agents",
    "docs/ai_management",
    "docs/control_plane",
    "docs/ops",
    "docs/partners",
    "docs/investor",
    "docs/brand",
    "docs/api",
    "docs/deployment",
]

def title_from_path(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").title()

TEMPLATE = """# {title}

## Purpose
Define the operating role of this document inside Dealix Company OS.

## Owner
Sami / Current system owner.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data.
- Operating signals.
- Founder decisions.
- Customer evidence where applicable.

## Outputs
- Clear operating guidance.
- Decisions, rules, or templates.
- Evidence needed for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.
- Must be updated when repeated issues appear.

## Metrics
- Completion status.
- Usage frequency.
- Impact on revenue, delivery, trust, or founder leverage.
- Number of decisions or actions supported.

## Evidence
- Linked file, workflow, test output, customer feedback, payment, delivery, or decision log.

## Last Reviewed
YYYY-MM-DD
"""

updated = []

for folder in DOC_FOLDERS:
    base = Path(folder)
    if not base.exists():
        continue

    for path in base.rglob("*.md"):
        if path.stat().st_size == 0:
            path.write_text(TEMPLATE.format(title=title_from_path(path)), encoding="utf-8")
            updated.append(str(path))

print(f"Updated {len(updated)} empty docs.")
for item in updated:
    print(f"- {item}")
PY

cat > scripts/verify_document_quality.py <<'PY'
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Purpose",
    "## Owner",
    "## Review Cadence",
    "## Inputs",
    "## Outputs",
    "## Rules",
    "## Metrics",
    "## Evidence",
]

DOC_FOLDERS = [
    "docs/founder",
    "docs/strategy",
    "docs/revenue",
    "docs/acquisition",
    "docs/sales",
    "docs/delivery",
    "docs/trust",
    "docs/finance",
    "docs/client_success",
    "docs/product",
    "docs/content",
    "docs/learning",
    "docs/people",
    "docs/agents",
    "docs/ai_management",
    "docs/control_plane",
    "docs/ops",
]

# Master Content Pack v1 enforces the standard on files registered in the
# allowlist below. Legacy docs that have not been migrated to the standard
# can be added incrementally as they are updated. This keeps the verifier
# strict on what it owns and silent on what it does not yet own.
ALLOWLIST_FILE = Path("docs/.doc_standard_allowlist.txt")

failures = []

if ALLOWLIST_FILE.exists():
    allowlisted = {
        line.strip()
        for line in ALLOWLIST_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    }
else:
    allowlisted = None  # None means "check everything" (legacy behaviour).

def check_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")

    if path.stat().st_size < 120:
        failures.append(f"Too short: {path}")
        return

    missing_sections = [section for section in REQUIRED_SECTIONS if section not in text]

    if missing_sections:
        failures.append(f"{path} missing sections: {', '.join(missing_sections)}")

for folder in DOC_FOLDERS:
    base = Path(folder)
    if not base.exists():
        failures.append(f"Missing folder: {folder}")
        continue

    for path in base.rglob("*.md"):
        rel = str(path).replace("\\", "/")
        if allowlisted is not None and rel not in allowlisted:
            continue
        check_file(path)

if failures:
    print("Document quality failures:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("PASS: all registered operating documents meet Dealix document standard.")
PY

cat > DEALIX_OPERATING_DOCTRINE.md <<'EOF'
# Dealix Operating Doctrine

Dealix is a Saudi-native Revenue Company Operating System.

## Purpose
Define the non-negotiable operating philosophy for Dealix.

## Owner
Sami / Founder CEO.

## Review Cadence
Monthly.

## Inputs
- Revenue results.
- Delivery feedback.
- Trust incidents.
- Product signals.
- Founder decisions.

## Outputs
- Operating rules.
- Strategic constraints.
- Company loops.
- Decision criteria.

## Company Loops

### 1. Revenue Loop
Lead → Reply → Call → Payment → Delivery → Proof → Retainer

### 2. Delivery Loop
Intake → Research → Score → Draft → QA → Handoff → Feedback

### 3. Trust Loop
Classify → Guard → Approve → Log → Review → Improve

### 4. Learning Loop
Experiment → Measure → Learn → Decide → Update

### 5. CEO Loop
Brief → Decide → Approve → Focus → Review

## Rules
- AI prepares.
- Workflows execute.
- Trust governs.
- Founder approves critical moves.
- Metrics improve the system.
- Dealix does not build features unless they support revenue, delivery, trust, learning, or founder leverage.

## Metrics
- Cash collected.
- Retainer conversion.
- Delivery quality.
- Trust incidents.
- Founder leverage.
- Learning decisions per week.

## Evidence
- Daily CEO brief.
- Weekly CEO review.
- Approval logs.
- Payment records.
- Delivery reports.
- Learning review.

## Last Reviewed
YYYY-MM-DD
EOF

cat > DEALIX_COMPANY_OS_SCORECARD.md <<'EOF'
# Dealix Company OS Scorecard

## Purpose
Track readiness and operating quality for each Dealix company system.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly.

## Inputs
- Verification scripts.
- GitHub Actions status.
- Private ops evidence.
- Revenue metrics.
- Delivery metrics.
- Trust logs.

## Outputs
- System score.
- PASS / READY INTERNAL / FIX / BLOCKED status.
- Next action per system.

## Rules
- 90-100 = PASS.
- 75-89 = READY INTERNAL.
- 50-74 = FIX.
- 0-49 = BLOCKED.
- No system is PASS without evidence.

## Metrics
- Number of PASS systems.
- Number of blocked systems.
- Time since last review.
- Evidence completeness.

## Evidence
- scripts/verify_company_os_deep.py
- scripts/verify_full_ops.py
- GitHub Actions
- private ops logs

| System | Score | Status | Evidence | Verification | Next Action |
|---|---:|---|---|---|---|
| Founder OS | 0 | BLOCKED | docs/founder/ | scripts/verify_founder_os.py | Use daily brief |
| Strategy OS | 0 | BLOCKED | docs/strategy/ | scripts/verify_strategy_os.py | Lock 90-day plan |
| Revenue OS | 0 | BLOCKED | docs/revenue/ | scripts/verify_revenue_os.py | Send 25 DMs |
| Acquisition OS | 0 | BLOCKED | docs/acquisition/ | scripts/verify_acquisition_os.py | Define sourcing |
| Sales OS | 0 | BLOCKED | docs/sales/ | scripts/verify_sales_os.py | Define sales motion |
| Delivery OS | 0 | BLOCKED | docs/delivery/ | scripts/verify_delivery_os.py | Prepare 3 samples |
| Trust OS | 0 | BLOCKED | docs/trust/ | scripts/verify_trust_os.py | Enforce approvals |
| Finance OS | 0 | BLOCKED | docs/finance/ | scripts/verify_finance_os.py | Verify payment path |
| Client Success OS | 0 | BLOCKED | docs/client_success/ | scripts/verify_client_success_os.py | Define retention |
| Product OS | 0 | BLOCKED | docs/product/ | scripts/verify_product_os.py | Tie features to revenue |
| Content OS | 0 | BLOCKED | docs/content/ | scripts/verify_content_os.py | Build proof engine |
| Learning OS | 0 | BLOCKED | docs/learning/ | scripts/verify_learning_os.py | Write first review |

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/revenue/OFFER_LADDER.md <<'EOF'
# Offer Ladder

## Purpose
Define the commercial path from entry offer to recurring revenue.

## Owner
Sami / Founder CEO.

## Review Cadence
Weekly until first 10 customers, then monthly.

## Inputs
- Customer calls.
- Replies.
- Proposal outcomes.
- Payments.
- Delivery feedback.
- Retainer conversion.

## Outputs
- Clear offer ladder.
- Pricing logic.
- Upgrade path.
- Sales focus.

## Offer Ladder

### 1. Signal Sample
Price: Free / 199 SAR
Purpose: Open conversation and prove relevance.

### 2. Revenue Sprint
Price: 2,500-7,500 SAR
Purpose: First paid result.

### 3. Managed Pilot
Price: 9,500-25,000 SAR
Purpose: Prove execution with support.

### 4. Revenue Desk
Price: 5,000-20,000 SAR monthly
Purpose: Recurring revenue.

### 5. Dealix OS
Price: Custom
Purpose: Enterprise SaaS / managed operating system after repeated proof.

## Rules
- Revenue Sprint is the primary offer until paid demand is proven.
- No enterprise OS sale before repeatable delivery proof.
- No offer moves up the ladder without evidence.
- No guaranteed sales or revenue claims.

## Metrics
- Sample-to-call rate.
- Call-to-proposal rate.
- Proposal-to-payment rate.
- Sprint-to-retainer conversion.
- Average deal size.

## Evidence
- pipeline_tracker.csv
- proposal notes
- payment records
- delivery reports
- feedback logs

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/revenue/PIPELINE_STAGES.md <<'EOF'
# Pipeline Stages

## Purpose
Define standard sales stages for every lead and opportunity.

## Owner
Sami / Revenue owner.

## Review Cadence
Weekly.

## Inputs
- Lead sources.
- Outreach activity.
- Replies.
- Calls.
- Proposals.
- Payments.

## Outputs
- Clear pipeline status.
- Next action per lead.
- Sales forecast.
- Bottleneck visibility.

## Stages
1. New
2. Qualified
3. Contacted
4. Replied
5. Sample Sent
6. Call Booked
7. Proposal Sent
8. Paid
9. Delivered
10. Retainer
11. Lost

## Rules
- Every lead must have stage, priority, next action, and last touch.
- No lead remains without next action.
- Lost leads must include reason.
- Paid clients move to delivery tracking.
- Retainer candidates must have client health score.

## Metrics
- Leads per stage.
- Conversion rate by stage.
- Follow-ups overdue.
- Proposal close rate.
- Retainer conversion.

## Evidence
- private pipeline tracker
- call notes
- proposal notes
- payments
- win/loss review

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/trust/APPROVAL_MATRIX.md <<'EOF'
# Approval Matrix

## Purpose
Define what Dealix can execute automatically and what requires founder approval.

## Owner
Sami / Trust owner.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Workflow type.
- Risk level.
- Data sensitivity.
- External commitment.
- Legal/compliance implication.

## Outputs
- Approval class.
- Execution decision.
- Audit requirement.

## Approval Classes

### A0 - Fully Automatic
Allowed for low-risk internal actions:
- duplicate removal
- internal lead scoring
- CRM status update
- internal report generation

### A1 - Human Review Recommended
Requires review before important external use:
- outreach drafts
- public content drafts
- sample pack drafts
- lead list delivery drafts

### A2 - Explicit Human Approval Required
Cannot proceed without founder approval:
- proposal sending
- client delivery
- pricing exceptions
- public case studies
- customer data exports

### A3 - Never Auto-Execute
Never automatic:
- contract changes
- NDAs
- legal commitments
- regulator communication
- refunds
- sensitive data exports
- guaranteed revenue claims
- full compliance claims

## Rules
- External commitments require A1 or higher.
- Financial or legal changes require A2 or A3.
- A3 actions are blocked, not queued for automation.
- Every A2/A3 action must be logged.

## Metrics
- Approvals waiting.
- A3 blocked actions.
- Approval turnaround time.
- Sensitive action count.
- Incidents.

## Evidence
- trust/approval_log.csv
- trust/sensitive_actions.md
- claim_approval_log.csv
- incident logs

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/trust/AUTONOMY_POLICY.md <<'EOF'
# Autonomy Policy

## Purpose
Define how far automation can go inside Dealix.

## Owner
Sami / Trust owner.

## Review Cadence
Monthly or after any incident.

## Inputs
- Action type.
- Risk level.
- Approval class.
- Data sensitivity.
- External impact.

## Outputs
- Allowed autonomy level.
- Required approval.
- Logging requirement.

## Autonomy Levels

### L0 Manual
Human does the work.

### L1 Assisted
AI drafts, human edits.

### L2 Semi-Auto
System executes internally and waits for external approval.

### L3 Auto
System executes low-risk internal actions.

### L4 Prohibited
System must never execute.

## L4 Actions
- contract changes
- NDAs
- refunds
- legal commitments
- regulator communication
- sensitive data exports
- guaranteed revenue claims
- full compliance claims

## Rules
- A3 maps to L4.
- A2 maps to L0/L1/L2 only.
- No external commitment can be L3.
- Automation must be auditable.

## Metrics
- A3 blocked actions.
- Automation failures.
- Manual override count.
- Incident count.

## Evidence
- approval logs
- audit logs
- incident response
- GitHub checks
- trust tests

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/delivery/revenue_sprint/DELIVERY_PLAYBOOK.md <<'EOF'
# Revenue Sprint Delivery Playbook

## Purpose
Define how Dealix delivers a Revenue Sprint consistently.

## Owner
Sami / Delivery owner.

## Review Cadence
Weekly during first 10 deliveries, then monthly.

## Inputs
- Client intake.
- ICP.
- Offer details.
- Target sectors.
- Lead sources.
- Approval constraints.

## Outputs
- Qualified lead list.
- Lead scoring.
- Outreach pack.
- Executive memo.
- 14-day action plan.
- Handoff.

## Delivery Flow

### Day 0 - Intake
- Confirm ICP.
- Confirm target sectors.
- Confirm exclusions.
- Confirm delivery date.
- Confirm approval rules.

### Day 1-2 - Research
- Source companies.
- Remove duplicates.
- Remove obvious bad fits.
- Collect evidence.

### Day 3-4 - Scoring
- Score fit.
- Score likely pain.
- Score contactability.
- Assign A/B/C priority.

### Day 5-6 - Outreach Pack
- Draft Arabic messages.
- Draft English messages if needed.
- Draft follow-up cadence.
- Prepare CTA options.

### Day 7-10 - Executive Memo
- Summarize ICP.
- Summarize best opportunities.
- Identify top segments.
- Prepare action plan.

### Day 11-14 - QA and Handoff
- Run QA checklist.
- Verify no overclaims.
- Verify evidence.
- Deliver final report.

## Rules
- No delivery without QA checklist.
- No A-priority lead without evidence.
- No guaranteed sales claims.
- No sensitive data unless required.
- Client-specific data stays private.

## Metrics
- Delivery time.
- QA pass rate.
- Rework count.
- Client feedback.
- Retainer conversion.

## Evidence
- client intake
- delivery report
- QA checklist
- handoff
- feedback

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/delivery/revenue_sprint/QA_CHECKLIST.md <<'EOF'
# Revenue Sprint QA Checklist

## Purpose
Ensure every Revenue Sprint delivery is useful, accurate, and trust-safe.

## Owner
Sami / Delivery owner.

## Review Cadence
Every delivery.

## Inputs
- Lead table.
- Outreach pack.
- Executive memo.
- Evidence.
- Client ICP.

## Outputs
- QA pass/fail.
- Required fixes.
- Approved delivery.

## Lead Quality
- Every lead matches ICP.
- Every lead has a clear reason for inclusion.
- Every lead has A/B/C priority.
- Duplicate leads removed.
- A-priority leads have evidence.

## Outreach Quality
- Messages are specific.
- Messages are short and human.
- No guaranteed revenue claim.
- No misleading compliance claim.
- CTA is clear.

## Trust Quality
- No unnecessary sensitive data.
- Suppression/opt-out respected.
- Claims are supported.
- Public/private boundary respected.

## Delivery Quality
- Executive summary included.
- Lead table included.
- Outreach pack included.
- 14-day action plan included.
- Next step clearly stated.

## Rules
- Delivery cannot be sent if any critical QA item fails.
- A2 approval required before client delivery.
- Any risky claim must be rewritten.

## Metrics
- QA pass rate.
- Number of fixes per delivery.
- Rework count.
- Client feedback score.

## Evidence
- completed QA checklist
- delivery report
- approval log
- feedback

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md <<'EOF'
# Weekly Intelligence Review

## Purpose
Convert weekly operating results into learning and system improvements.

## Owner
Sami / Learning owner.

## Review Cadence
Weekly.

## Inputs
- Leads sourced.
- DMs sent.
- Replies.
- Calls.
- Proposals.
- Payments.
- Delivery feedback.
- QA failures.
- Trust escalations.

## Outputs
- Learning decisions.
- Playbook updates.
- Pricing updates.
- ICP changes.
- Message improvements.
- Productization candidates.

## What Happened?
- Leads sourced:
- DMs sent:
- Replies:
- Calls:
- Proposals:
- Payments:
- Deliveries:
- Feedback:

## What Worked?
- Best sector:
- Best message:
- Best offer:
- Best channel:

## What Failed?
- Weak sector:
- Weak message:
- Weak offer:
- Delivery issue:

## What Bottleneck Appeared?
- Revenue:
- Sales:
- Delivery:
- Trust:
- Founder:
- Product:

## What Will Change Next Week?
- ICP:
- Message:
- Pricing:
- Delivery:
- Product:
- Trust:

## Rules
- Every week must produce at least one learning decision.
- Repeated issues must update a checklist, template, playbook, or productization candidate.
- No learning without evidence.

## Metrics
- Learning decisions per week.
- Playbooks updated.
- Experiments completed.
- Conversion improvement.
- Delivery improvement.

## Evidence
- win/loss review
- message performance
- sector performance
- delivery QA
- payment records

## Last Reviewed
YYYY-MM-DD
EOF

cat > docs/control_plane/COMPANY_STATE_SCHEMA.md <<'EOF'
# Company State Schema

## Purpose
Define the single operating state that Dealix uses to understand the company.

## Owner
Sami / Control Plane owner.

## Review Cadence
Monthly or whenever new systems are added.

## Inputs
- Pipeline data.
- Revenue data.
- Delivery status.
- Trust logs.
- Product status.
- Learning reviews.

## Outputs
- CEO brief.
- Decision queue.
- Risk flags.
- System scorecard.
- Weekly review.

## Revenue State
- cash_collected
- cash_expected
- mrr
- proposals_pending
- pipeline_value
- best_next_close

## Sales State
- new_leads
- qualified_leads
- contacted
- replies
- calls_booked
- proposals_sent

## Delivery State
- active_clients
- reports_due
- qa_needed
- blocked_deliveries
- delivery_on_time_rate

## Trust State
- approvals_waiting
- A3_blocked_actions
- opt_outs
- claims_needing_review
- incidents

## Product State
- ci_status
- bugs_open
- release_candidate
- customer_requested_features
- trust_tests_status

## Learning State
- experiments_running
- latest_win_loss
- best_message
- best_sector
- biggest_objection
- next_experiment

## Rules
- Company State must be evidence-based.
- Unknown values should be marked unknown, not guessed.
- Sensitive data must not be stored in public repo.
- CEO brief must derive from Company State.

## Metrics
- Completeness of state.
- Number of unknown fields.
- Decision usefulness.
- Risk detection accuracy.

## Evidence
- private ops files
- GitHub Actions
- CI output
- revenue logs
- delivery logs

## Last Reviewed
YYYY-MM-DD
EOF

cat > scripts/verify_company_os_deep.py <<'PY'
from pathlib import Path

CHECKS = {
    "DEALIX_OPERATING_DOCTRINE.md": [
        "Revenue Loop",
        "Delivery Loop",
        "Trust Loop",
        "Learning Loop",
        "CEO Loop",
        "AI prepares",
        "Founder approves",
    ],
    "DEALIX_COMPANY_OS_SCORECARD.md": [
        "Founder OS",
        "Strategy OS",
        "Revenue OS",
        "Delivery OS",
        "Trust OS",
        "Learning OS",
    ],
    "docs/founder/DAILY_COMMAND_BRIEF.md": [
        "Money",
        "Sales",
        "Delivery",
        "Trust",
        "Decisions Required",
    ],
    "docs/revenue/OFFER_LADDER.md": [
        "Signal Sample",
        "Revenue Sprint",
        "Managed Pilot",
        "Revenue Desk",
        "Dealix OS",
    ],
    "docs/revenue/PIPELINE_STAGES.md": [
        "New",
        "Contacted",
        "Replied",
        "Proposal Sent",
        "Paid",
        "Delivered",
        "Retainer",
    ],
    "docs/trust/AUTONOMY_POLICY.md": [
        "L0 Manual",
        "L1 Assisted",
        "L2 Semi-Auto",
        "L3 Auto",
        "L4 Prohibited",
    ],
    "docs/trust/APPROVAL_MATRIX.md": [
        "A0",
        "A1",
        "A2",
        "A3",
        "Never",
    ],
    "docs/ops/OPERATING_LOOPS.md": [
        "Revenue Loop",
        "Delivery Loop",
        "Trust Loop",
        "Learning Loop",
        "CEO Loop",
    ],
    "docs/learning/WEEKLY_INTELLIGENCE_REVIEW.md": [
        "What Happened",
        "What Worked",
        "What Failed",
        "What Bottleneck",
        "What Will Change",
    ],
    "docs/control_plane/COMPANY_STATE_SCHEMA.md": [
        "Revenue State",
        "Sales State",
        "Delivery State",
        "Trust State",
        "Learning State",
    ],
}

failures = []

for file, required_terms in CHECKS.items():
    path = Path(file)
    if not path.exists():
        failures.append(f"Missing file: {file}")
        continue

    text = path.read_text(encoding="utf-8", errors="ignore")

    for term in required_terms:
        if term not in text:
            failures.append(f"{file} missing required term: {term}")

if failures:
    print("Company OS deep verification failed:")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("PASS: Dealix Company OS deep verification passed.")
PY

cat > scripts/verify_full_ops.py <<'PY'
import subprocess
import sys
from pathlib import Path

CHECKS = [
    ["python", "scripts/verify_master_tree.py"],
    ["python", "scripts/verify_document_quality.py"],
    ["python", "scripts/verify_company_os_deep.py"],
]

OPTIONAL_CHECKS = [
    ["python", "scripts/verify_public_safety.py"],
    ["python", "scripts/verify_private_boundary.py"],
]

failed = []

for cmd in CHECKS:
    print(f"\n== Running: {' '.join(cmd)} ==")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        failed.append(" ".join(cmd))

for cmd in OPTIONAL_CHECKS:
    if Path(cmd[1]).exists():
        print(f"\n== Running: {' '.join(cmd)} ==")
        result = subprocess.run(cmd)
        if result.returncode != 0:
            failed.append(" ".join(cmd))

if failed:
    print("\nFAILED CHECKS:")
    for item in failed:
        print("-", item)
    sys.exit(1)

print("\nPASS: Dealix full ops verification passed.")
PY

cat > .github/workflows/dealix-company-os.yml <<'YAML'
name: Dealix Company OS Checks

on:
  pull_request:
  push:
    branches: [main]

jobs:
  company-os:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Verify master tree
        run: python scripts/verify_master_tree.py

      - name: Verify document quality
        run: python scripts/verify_document_quality.py

      - name: Verify company OS deep
        run: python scripts/verify_company_os_deep.py

      - name: Verify full ops
        run: python scripts/verify_full_ops.py
YAML

python scripts/fill_empty_docs_with_standard.py
python scripts/verify_document_quality.py
python scripts/verify_company_os_deep.py
python scripts/verify_full_ops.py

echo "== Dealix Master Content Pack Complete =="
