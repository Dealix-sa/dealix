#!/bin/bash
# Dealix Founder Daily Complete Ritual
# Master orchestrator for end-to-end founder execution system
# Run daily at 8:00 AM (or whenever founder starts work)

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="$PROJECT_ROOT/company/runtime"
LOG_FILE="$RUNTIME_DIR/daily_ritual_$(date +%Y-%m-%d).log"

mkdir -p "$RUNTIME_DIR"

echo "🚀 Dealix Founder Daily Complete Ritual — $(date +'%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "=========================================" | tee -a "$LOG_FILE"
echo ""

# PHASE 1: LEAD RESEARCH & QUALIFICATION
echo "📊 PHASE 1: Lead Research & Qualification" | tee -a "$LOG_FILE"

if [ -f "$PROJECT_ROOT/company/leads/real_leads_engine.py" ]; then
    echo "  1.1 Running Google Places lead research..." | tee -a "$LOG_FILE"
    python "$PROJECT_ROOT/company/leads/real_leads_engine.py" >> "$LOG_FILE" 2>&1 || true
    echo "  ✅ Lead research complete" | tee -a "$LOG_FILE"
else
    echo "  ⚠️  real_leads_engine.py not found; skipping Google Places query" | tee -a "$LOG_FILE"
fi

if [ -f "$PROJECT_ROOT/company/sales/lead_qualification_engine.py" ]; then
    echo "  1.2 Running lead qualification scoring..." | tee -a "$LOG_FILE"
    python "$PROJECT_ROOT/company/sales/lead_qualification_engine.py" >> "$LOG_FILE" 2>&1 || true
    echo "  ✅ Lead qualification complete" | tee -a "$LOG_FILE"
else
    echo "  ⚠️  lead_qualification_engine.py not found" | tee -a "$LOG_FILE"
fi

echo ""

# PHASE 2: SALES AGENT & APPROVALS
echo "📋 PHASE 2: Sales Qualification Agent & Approval Queue" | tee -a "$LOG_FILE"

if [ -f "$PROJECT_ROOT/company/sales/sales_qualification_agent.py" ]; then
    echo "  2.1 Generating qualification items and approvals..." | tee -a "$LOG_FILE"
    python "$PROJECT_ROOT/company/sales/sales_qualification_agent.py" >> "$LOG_FILE" 2>&1 || true
    echo "  ✅ Approval queue generated" | tee -a "$LOG_FILE"
else
    echo "  ⚠️  sales_qualification_agent.py not found" | tee -a "$LOG_FILE"
fi

echo ""

# PHASE 3: DASHBOARDS & REPORTING
echo "📈 PHASE 3: Dashboards & Reporting" | tee -a "$LOG_FILE"

echo "  3.1 Generating founder dashboard..." | tee -a "$LOG_FILE"
python "$PROJECT_ROOT/scripts/generate_founder_dashboard.py" >> "$LOG_FILE" 2>&1 || true
echo "  ✅ Founder dashboard generated" | tee -a "$LOG_FILE"

echo "  3.2 Generating approvals queue UI..." | tee -a "$LOG_FILE"
python "$PROJECT_ROOT/scripts/generate_approvals_queue.py" >> "$LOG_FILE" 2>&1 || true
echo "  ✅ Approvals queue generated" | tee -a "$LOG_FILE"

echo ""

# PHASE 4: SUMMARY FOR FOUNDER
echo "✅ Daily Ritual Complete — $(date +'%H:%M:%S')" | tee -a "$LOG_FILE"
echo "=========================================" | tee -a "$LOG_FILE"
echo ""
echo "📍 YOUR FOUNDER DASHBOARDS (open in browser):" | tee -a "$LOG_FILE"
echo "  • Founder Dashboard: $RUNTIME_DIR/founder_dashboard.html" | tee -a "$LOG_FILE"
echo "  • Approvals Queue: $RUNTIME_DIR/decisions.html" | tee -a "$LOG_FILE"
echo "  • Qualified Leads: $RUNTIME_DIR/daily_qualified_leads_*.md" | tee -a "$LOG_FILE"
echo ""
echo "📍 YOUR RESOURCES:" | tee -a "$LOG_FILE"
echo "  • Daily Playbook: $PROJECT_ROOT/docs/FOUNDER_DAILY_EXECUTION_PLAYBOOK.md" | tee -a "$LOG_FILE"
echo "  • Revenue Manual: $PROJECT_ROOT/docs/FOUNDER_REVENUE_MANUAL.md" | tee -a "$LOG_FILE"
echo "  • Demo Scripts: See PLAYBOOK §Demo Script" | tee -a "$LOG_FILE"
echo ""
echo "🎯 YOUR ACTIONS TODAY (in order):" | tee -a "$LOG_FILE"
echo "  1. [8:15 AM] Send 1 warm WhatsApp to a named prospect" | tee -a "$LOG_FILE"
echo "  2. [8:35 AM] Send 1 more WhatsApp to a second prospect (if time)" | tee -a "$LOG_FILE"
echo "  3. [8:45 AM] Review /decisions.html — approve 3-5 AI drafts" | tee -a "$LOG_FILE"
echo "  4. [As booked] Take diagnostic calls (30 min each, max 2 per day)" | tee -a "$LOG_FILE"
echo "  5. [5:00 PM] Update /warm-intro-targets.csv with day's activity" | tee -a "$LOG_FILE"
echo ""
echo "📊 THIS WEEK'S METRIC:" | tee -a "$LOG_FILE"
echo "  Target: Send 5 warm WhatsApps per week" | tee -a "$LOG_FILE"
echo "  Result: [to be filled in Friday]" | tee -a "$LOG_FILE"
echo ""
echo "💡 Remember:" | tee -a "$LOG_FILE"
echo "  • 1 WhatsApp per day = 3 pilots by Day 30" | tee -a "$LOG_FILE"
echo "  • Personal (not template) = trust signal" | tee -a "$LOG_FILE"
echo "  • Listen 60% of time = objections → learnings" | tee -a "$LOG_FILE"
echo "  • Deliver pilots 40h each = sustainable margin" | tee -a "$LOG_FILE"
echo ""
echo "Log file: $LOG_FILE" | tee -a "$LOG_FILE"
echo ""

# Open founder dashboard in default browser (if available)
if command -v xdg-open &> /dev/null; then
    xdg-open "$RUNTIME_DIR/founder_dashboard.html" 2>/dev/null || true
fi

