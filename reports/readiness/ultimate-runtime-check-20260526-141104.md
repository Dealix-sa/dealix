# Dealix/Hermes Ultimate Runtime Check

Generated: 2026-05-26 14:11:04

- Passed: 14
- Failed: 0
- Verdict: PASS

| Test | OK | Code | Command |
|---|---|---:|---|
| dealix_status | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe dealix.py status` |
| verify_local_ai | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/verify_local_ai.py` |
| ledger_guard | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/ledger_guard.py` |
| manual_send_queue | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/build_manual_send_queue.py` |
| followup_queue | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/build_followup_queue.py` |
| lead_status_report | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/lead_status_report.py` |
| revenue_report | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/revenue_ledger.py report` |
| delivery_report | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/delivery_tracker.py report` |
| hermes_safe_init | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/hermes_safe_init.py` |
| hermes_opportunity_radar | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/hermes_opportunity_radar.py` |
| hermes_founder_brief | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/hermes_founder_brief.py` |
| hermes_trust_pack | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/hermes_trust_pack.py` |
| hermes_partner_init | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/hermes_partner_init.py` |
| hermes_partner_report | True | 0 | `C:\Users\samim\AppData\Local\Python\pythoncore-3.14-64\python.exe scripts/hermes_partner_os.py report` |

## Details

### dealix_status

- OK: True
- Code: 0

STDOUT:
```text
┌─────────────────────────────────────────────────────────┐
│ [Dealix] Dealix Executive Operating OS                  │
│ Hermes Executive Plane · Founder Edition · Saudi Arabia │
└─────────────────────────────────────────────────────────┘
      System Integrity Matrix       
┌──────────────────────┬───────────┐
│ Component            │ Status    │
├──────────────────────┼───────────┤
│ EXECUTION_LEDGER.md  │ [PASS] OK │
├──────────────────────┼───────────┤
│ REVENUE_LEDGER.md    │ [PASS] OK │
├──────────────────────┼───────────┤
│ PROOF_LEDGER.md      │ [PASS] OK │
├──────────────────────┼───────────┤
│ RISK_LEDGER.md       │ [PASS] OK │
├──────────────────────┼───────────┤
│ DECISION_LEDGER.md   │ [PASS] OK │
├──────────────────────┼───────────┤
│ proposal generator   │ [PASS] OK │
├──────────────────────┼───────────┤
│ proof pack generator │ [PASS] OK │
├──────────────────────┼───────────┤
│ governance check     │ [PASS] OK │
├──────────────────────┼───────────┤
│ command brief        │ [PASS] OK │
└──────────────────────┴───────────┘

dealix status = OK

```

STDERR:
```text

```

### verify_local_ai

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 VERIFYING LOCAL AI INTEGRITY 
==========================================
Test Prompt: 'Hello, say 'Dealix AI OK''
Response:    'Dealix AI OK'

LOCAL_AI_VERDICT=PASS

```

STDERR:
```text

```

### ledger_guard

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 RUNNING LEDGER GUARD - INTEGRITY MATRIX 
==========================================
  - EXECUTION_LEDGER.md: [PASS] Integrity check completed.
  - REVENUE_LEDGER.md: [PASS] Integrity check completed.
  - PROOF_LEDGER.md: [PASS] Integrity check completed.
  - RISK_LEDGER.md: [PASS] Integrity check completed.
  - DECISION_LEDGER.md: [PASS] Integrity check completed.

LEDGER_GUARD=PASS

```

STDERR:
```text

```

### manual_send_queue

- OK: True
- Code: 0

STDOUT:
```text
No leads ready for outreach.

```

STDERR:
```text

```

### followup_queue

- OK: True
- Code: 0

STDOUT:
```text
No leads need follow-up currently.

```

STDERR:
```text

```

### lead_status_report

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 GENERATING LEAD STATUS REPORT 
==========================================
[PASS] Lead status report generated at: reports\lead-status-20260526.md

```

STDERR:
```text

```

### revenue_report

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 DEALIX REVENUE LEDGER STATS 
==========================================
Total Collected Revenue: 5000 SAR
Active Paying Clients:   1

REVENUE_REPORT=PASS

```

STDERR:
```text

```

### delivery_report

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 ACTIVE SPRINT DELIVERY TRACKER 
==========================================
* Client:   Al-Majd Group
  Offer:    ai-trust
  Kickoff:  2026-05-26
  Progress: 80%
  Status:   delivery_started

DELIVERY_REPORT=PASS

```

STDERR:
```text

```

### hermes_safe_init

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 INITIALIZING HERMES LEDGERS SAFELY 
==========================================
  + Created ledger: hermes_signals.json
  + Created ledger: hermes_opportunities.json
  + Created ledger: hermes_outcomes.json
  + Created ledger: hermes_assets.json
  + Created ledger: hermes_decisions.json
  + Created ledger: hermes_relationships.json
  + Created ledger: hermes_deal_rooms.json
  + Created ledger: hermes_partners.json
  + Created ledger: hermes_productization.json

State: HERMES_CORE_V1_ACTIVE

```

STDERR:
```text

```

### hermes_opportunity_radar

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 SCANNING HERMES OPPORTUNITY RADAR 
==========================================
[PASS] Opportunity radar generated at: reports\hermes\opportunity-radar-20260526.md

```

STDERR:
```text

```

### hermes_founder_brief

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 COMPILING SAMI'S DAILY BRIEF - HERMES 
==========================================
[PASS] Sami daily brief generated at: reports\founder\sami-command-brief-20260526.md

```

STDERR:
```text

```

### hermes_trust_pack

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 COMPILING SOVEREIGN HERMES TRUST PACK 
==========================================
Trust Pack compiled successfully at: reports\trust\hermes-trust-pack-20260526.md

```

STDERR:
```text

```

### hermes_partner_init

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 INITIALIZING HERMES PARTNERS SCHEMA 
==========================================
Partners schema initialized successfully.

```

STDERR:
```text

```

### hermes_partner_report

- OK: True
- Code: 0

STDOUT:
```text
==========================================
 COMPILING HERMES PARTNERS REPORT 
==========================================
[PASS] Partners report compiled successfully at: reports\partners\partner-report-20260526.md

```

STDERR:
```text

```
