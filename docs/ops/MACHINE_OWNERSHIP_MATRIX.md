# Machine Ownership Matrix — Dealix

## الدور — Role

سجل كل ماكينة (automation/agent/workflow) في Dealix — مع owner واضح، input/output، KPI، failure mode، و disable switch.

> "ماكينة بدون owner = ماكينة معطلة بانتظار حادث."

## المصدر الواحد — Single source of truth

```
registries/machine_registry.yaml
```

ويُتحقَّق منه عبر:

```
scripts/verify_machine_registry.py
```

## الحقول الإلزامية — Required fields

كل machine يجب أن يحتوي:

- `id`
- `name`
- `layer` (brand|trust|growth|sales|finance|agent|ops|launch|data|control)
- `purpose`
- `owner` (`founder` افتراضياً)
- `input` (مصدر بيانات)
- `output` (مخرَج)
- `source_of_truth` (path / table)
- `approval_class` (low|medium|high)
- `trust_gate` (none|review|hard_block)
- `worker` (agent / cron / manual)
- `kpi` (مؤشر نجاح واحد قابل للقياس)
- `failure_mode` (ما الذي قد يكسرها)
- `recovery_path` (ما يفعله الـ owner)
- `disable_switch` (env var أو ملف يوقفها فوراً)

## الماكينات المسجلة — Registered machines

(القائمة الكاملة في `registries/machine_registry.yaml`)

- brand_system, founder_console, control_plane
- ceo_copilot, market_intelligence, account_scoring
- outbound_draft, linkedin_queue, email_draft, contact_form_queue
- followup, reply_router
- sample_factory, proposal_factory, payment_capture
- delivery_qa, retention, proof_approval, partner_referral
- content_to_demand, eval_gate, policy_as_code, audit_log
- worker_orchestrator, finance_os, data_quality, security_gate
- launch_command

## القواعد — Rules

- لا machine جديدة بدون row في `machine_registry.yaml`.
- لا `disable_switch` فارغ — كل machine يجب أن يكون قابلاً للإيقاف.
- `kpi` يجب أن يكون قابلاً للقياس (لا "improve experience").
- ماكينة بدون نشاط 30 يوم → review → archive أو kill.

## الملكية — Ownership

- Owner of matrix: Founder.
- Verifier: `scripts/verify_machine_registry.py`.
- Cadence: مراجعة شهرية في أول يوم.
