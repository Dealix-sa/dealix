#!/usr/bin/env bash
# L9 — Business Evidence + Private Ops contracts.
# Hard: verify_service_readiness_matrix.py (CI runs it).
# Advisory: verify_company_ready.py.
# CSV contracts: validate if $PRIVATE_OPS set; exit 2 (PARTIAL) if unset.
set -uo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO"

JSON=0
PRIVATE_OPS="${PRIVATE_OPS:-}"
REQUIRE_PRIVATE=0
STRICT="${DEALIX_STRICT_BUSINESS:-0}"
for ((i=1; i<=$#; i++)); do
  arg="${!i}"
  case "$arg" in
    --json) JSON=1 ;;
    --private-ops) j=$((i+1)); PRIVATE_OPS="${!j}" ;;
    --private-ops=*) PRIVATE_OPS="${arg#*=}" ;;
    --require-private-ops) REQUIRE_PRIVATE=1 ;;
    --strict) STRICT=1 ;;
  esac
done

FAIL=0; WARN=0
FAIL_NAMES=(); WARN_NAMES=()
log_dir="$(mktemp -d)"
trap 'rm -rf "$log_dir"' EXIT

run_hard() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  else
    FAIL=$((FAIL+1)); FAIL_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name"; tail -5 "$log" | sed 's/^/        /'; }
  fi
}

run_advisory() {
  local name="$1"; shift
  local log="$log_dir/$name.log"
  if "$@" >"$log" 2>&1; then
    [ "$JSON" -eq 0 ] && echo "  [OK]   $name"
  elif [ "$STRICT" = "1" ]; then
    FAIL=$((FAIL+1)); FAIL_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && { echo "  [FAIL] $name (strict)"; tail -3 "$log" | sed 's/^/        /'; }
  else
    WARN=$((WARN+1)); WARN_NAMES+=("$name")
    [ "$JSON" -eq 0 ] && echo "  [WARN] $name (advisory)"
  fi
}

# Hard: verify_service_readiness_matrix (CI enforces this)
[ -f scripts/verify_service_readiness_matrix.py ] && \
  run_hard "verify-service-readiness-matrix" python3 scripts/verify_service_readiness_matrix.py

# Advisory: verify_company_ready (not in main CI)
[ -f scripts/verify_company_ready.py ] && \
  run_advisory "verify-company-ready" python3 scripts/verify_company_ready.py

# Private ops CSV contracts
if [ -z "$PRIVATE_OPS" ]; then
  WARN=$((WARN+1))
  WARN_NAMES+=("private-ops-unset")
  [ "$JSON" -eq 0 ] && echo "  [WARN] PRIVATE_OPS not set; skipping CSV contracts"
elif [ ! -d "$PRIVATE_OPS" ]; then
  WARN=$((WARN+1))
  WARN_NAMES+=("private-ops-missing-dir")
  [ "$JSON" -eq 0 ] && echo "  [WARN] PRIVATE_OPS=$PRIVATE_OPS not a directory; skipping CSV contracts"
else
  PRIVATE_OPS="$PRIVATE_OPS" python3 - "$JSON" <<'PYEOF'
import csv
import json as _json
import os
import sys

PRIVATE_OPS = os.environ["PRIVATE_OPS"]
JSON = sys.argv[1] == "1"

REQUIRED = {
    "growth/market_accounts.csv": [
        "account_id","company","website","country","city","sector",
        "business_type","offer","source","discovered_at","status","next_action"],
    "intelligence/lead_intelligence_base.csv": [
        "account_id","company","sector","website","country","city",
        "business_type","offer","buyer_titles","public_contact_path",
        "source","fit_score","priority","why_fit","status",
        "last_researched","last_contacted","reply_status","next_action"],
    "outreach/outreach_queue.csv": [
        "outreach_id","account_id","company","channel",
        "recipient_or_contact_path","message","approval_status",
        "send_status","sent_at","next_action"],
    "outreach/suppression_list.csv": [
        "company","contact","reason","source","date","status"],
    "outreach/conversation_log.csv": [
        "date","account_id","company","channel","reply_type",
        "summary","routed_to","next_action"],
    "sales/proposal_queue.csv": [
        "date","account_id","company","trigger","proposal_type",
        "amount_sar","status","due_date","next_action"],
    "finance/payment_capture_queue.csv": [
        "company","proposal_value","proposal_date","followup_stage",
        "status","next_followup_date","next_action"],
    "client_success/retention_queue.csv": [
        "company","delivery_date","feedback_status","health_score",
        "retainer_status","proof_status","referral_status","next_action"],
}

def read_headers(path):
    with open(path, newline="", encoding="utf-8") as f:
        return next(csv.reader(f), [])

def read_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

errors = []
warnings = []

for rel, required in REQUIRED.items():
    p = os.path.join(PRIVATE_OPS, rel)
    if not os.path.isfile(p):
        errors.append(f"missing CSV: {rel}")
        continue
    try:
        headers = read_headers(p)
    except Exception as e:
        errors.append(f"{rel}: parse error {e}")
        continue
    missing = [h for h in required if h not in headers]
    if missing:
        errors.append(f"{rel}: missing headers {missing}")

def safe_rows(rel):
    p = os.path.join(PRIVATE_OPS, rel)
    if not os.path.isfile(p):
        return None
    try:
        return read_rows(p)
    except Exception:
        return None

intel = safe_rows("intelligence/lead_intelligence_base.csv") or []
outreach = safe_rows("outreach/outreach_queue.csv") or []
suppression = safe_rows("outreach/suppression_list.csv") or []
conv = safe_rows("outreach/conversation_log.csv") or []
proposals = safe_rows("sales/proposal_queue.csv") or []
payments = safe_rows("finance/payment_capture_queue.csv") or []

suppressed = {(r.get("company") or "").strip().lower()
              for r in suppression
              if (r.get("status") or "").lower() in {"active","suppressed","do-not-contact"}}

sent_rows = [r for r in outreach if (r.get("send_status") or "").lower() == "sent"]
positive = [r for r in conv if (r.get("reply_type") or "").lower() in {"positive","interested","yes"}]

for row in outreach:
    company = (row.get("company") or "").strip().lower()
    if company in suppressed:
        errors.append(f"outreach queued for suppressed company: {company}")
    if (row.get("send_status") or "").lower() == "sent" \
       and (row.get("approval_status") or "").lower() != "approved":
        errors.append(f"sent outreach without approval: {row.get('company')}")

if intel and len(intel) < 25:
    warnings.append(f"lead intelligence below proof minimum: {len(intel)}/25")
if sent_rows and not conv:
    errors.append("outreach sent but conversation_log empty")
if positive and not proposals:
    warnings.append("positive replies exist but no proposals queued")
if proposals and not payments:
    errors.append("proposals exist but payment_capture_queue empty")

if not JSON:
    if not errors and not warnings:
        print("  [OK]   private-ops CSV contracts")
    for e in errors:
        print(f"  [FAIL] {e}")
    for w in warnings:
        print(f"  [WARN] {w}")

with open("/tmp/dealix_l9_csv_result.json","w") as f:
    _json.dump({"errors": errors, "warnings": warnings}, f)

sys.exit(1 if errors else 0)
PYEOF
  py_exit=$?
  if [ "$py_exit" -ne 0 ]; then
    FAIL=$((FAIL+1)); FAIL_NAMES+=("private-ops-csv-contracts")
  fi
fi

EXIT=0; VERDICT="PASS"; SUMMARY="business evidence clean"
if [ "$FAIL" -gt 0 ]; then
  EXIT=1; VERDICT="FAIL"; SUMMARY="$FAIL hard step(s) failed"
elif [ "$REQUIRE_PRIVATE" -eq 1 ] && [ -z "$PRIVATE_OPS" ]; then
  EXIT=1; VERDICT="FAIL"; SUMMARY="PRIVATE_OPS required but not provided"
elif [ "$WARN" -gt 0 ]; then
  EXIT=2; VERDICT="PARTIAL"; SUMMARY="$WARN advisory step(s) warned"
fi

if [ "$JSON" -eq 1 ]; then
  printf '{"layer":9,"verdict":"%s","failures":[' "$VERDICT"
  for i in "${!FAIL_NAMES[@]}"; do
    [ "$i" -gt 0 ] && printf ','
    printf '"%s"' "${FAIL_NAMES[$i]}"
  done
  printf '],"warnings":['
  for i in "${!WARN_NAMES[@]}"; do
    [ "$i" -gt 0 ] && printf ','
    printf '"%s"' "${WARN_NAMES[$i]}"
  done
  printf '],"private_ops":%s,"summary":"%s"}\n' \
    "$([ -n "$PRIVATE_OPS" ] && echo "\"$PRIVATE_OPS\"" || echo "null")" \
    "$SUMMARY"
fi

rm -f /tmp/dealix_l9_csv_result.json
exit "$EXIT"
