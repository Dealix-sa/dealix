# API Commercial Launch QA

فحص جاهزية الـ API للتدشين التجاري — يعتمد على فحص الكود الثابت، لا على السيرفر الخارجي فقط.
API readiness QA for the commercial launch — based on **static code inspection**, not only a live server.

## Scope
The commercial-launch surface must add **no external-send capability** to the API.

## Static check
```bash
python scripts/api_commercial_static_check.py
# -> outputs/final_launch_control/api_commercial_static_check.json (pass: true)
```
The check scans `api/` for any commercial-tagged endpoint and asserts it contains **no**
external-send patterns (mail transport, message-to-recipient, bulk/outbound send).

## Manual / live checks (founder/ops, on deploy)
- [ ] `/health` returns OK
- [ ] Commercial read-only endpoints (if added) return data without side effects
- [ ] No send endpoints exist
- [ ] No messaging-provider send
- [ ] No mail transport
- [ ] No unsafe POST that triggers external delivery

## Decision
- **GO** for read-only commercial endpoints and health.
- **NO-GO** for any endpoint that sends externally — none may be added under this launch.
