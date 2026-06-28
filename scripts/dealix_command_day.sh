#!/usr/bin/env bash
# Dealix Command Day — أمر يومي واحد للمؤسس.
#
# Runs the daily engines in a SAFE, draft-only order and then builds the
# Unified Command Room. Doctrine-safe:
#   * Nothing is ever sent (no WhatsApp / email / LinkedIn).
#   * Each engine is best-effort: a missing API key or input never breaks the
#     chain (every step is guarded with `|| true`).
#   * No Docker, no `npm run dev`, no production deploy.
#
# Usage:
#   bash scripts/dealix_command_day.sh
#
# Output:
#   reports/command_room/index.html  (open in any browser, offline)
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 1

PY="${PYTHON:-python3}"

step() { printf '\n\033[1m▶ %s\033[0m\n' "$1"; }

step "1/5 micro_master — حزمة المؤسس الصباحية / morning pack"
"$PY" company/micro/micro_master.py || true

step "2/5 revenue_engine_v2 — خط الإيرادات (مسودات فقط) / draft-only pipeline"
"$PY" company/revenue_engine/revenue_engine_v2.py || true

step "3/5 intake_engine — تأهيل العملاء / client intake"
"$PY" company/intake/intake_engine.py || true

step "4/5 followup_engine — قائمة المتابعات / follow-up queue"
"$PY" company/crm/followup_engine.py || true

step "5/5 Unified Command Room — غرفة القيادة الموحّدة"
"$PY" scripts/dealix_unified_command_room.py || true

printf '\n\033[1m✓ تم. افتح اللوحة:\033[0m reports/command_room/index.html\n'
printf '  كل المسودات تنتظر مراجعتك — لا إرسال تلقائي.\n'
