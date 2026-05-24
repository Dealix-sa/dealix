# Dealix Operating Dashboard (Markdown v1)

**Update:** weekly (minimum) — or daily during heavy delivery.

> For the Streamlit app guide see [`../docs/DASHBOARD.md`](../docs/DASHBOARD.md). For the API-driven HTML founder dashboard see [`V5_FOUNDER_RUNBOOK.md`](V5_FOUNDER_RUNBOOK.md).

## Services

**Sellable:**

- Lead Intelligence Sprint
- AI Quick Win Sprint
- Company Brain Sprint

**Beta:**

- (none — promoted to Sellable in v5 closure)

**Not Ready:**

- Support Desk
- Enterprise AI OS

*(Edit to match [`registry/SERVICE_READINESS_MATRIX.yaml`](registry/SERVICE_READINESS_MATRIX.yaml).)*

## Sales

| | This week |
|---|-----------|
| Leads | |
| Calls | |
| Proposals | |
| Closed | |

## Delivery

| | Count |
|---|--------|
| Active projects | |
| QA pending | |
| Proof packs due | |

## Product

| | Notes |
|---|--------|
| Features shipped | |
| Manual steps repeated (candidates) | |
| Bugs / incidents | |

## Governance

| | Notes |
|---|--------|
| PII incidents | |
| Approvals pending | |
| Blocked actions | |

## Quality

| | Value |
|---|--------|
| Average QA | |
| Reports delivered | |
| Rework count | |

## Streamlit app guide

النظرة العامة — لوحة Streamlit لمتابعة الإنتاج وإدارة العملاء.

| الصفحة | المصدر | الوصف |
|-------|--------|------|
| Overview | `/health/deep` + `/admin/costs` | حالة عامة + KPIs |
| Leads | `/api/v1/leads` | جدول + تحديث الحالة |
| Approvals | `/api/v1/cro/approvals` | قبول/رفض قرارات Policy Engine |
| Evidence | `/api/v1/cro/evidence` | سجل القرارات والدليل |
| Costs | `/api/v1/admin/costs` | تحليل إنفاق LLM (model/provider/task) |
| Audit | `/api/v1/admin/audit` | سجل التكاملات |

**Run locally:**

```bash
pip install streamlit pandas httpx
export DEALIX_API_URL=https://api.dealix.me
export DEALIX_ADMIN_API_KEY=<admin-key>
streamlit run dashboard/app.py --server.port 8501
```

**Reverse proxy (nginx):**

```nginx
server {
    listen 443 ssl http2;
    server_name dashboard.dealix.sa;
    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 600s;
    }
}
```

**Access:** X-API-Key only; the dashboard talks to the API internally.

**Last updated:** 2026-05-24 — Owner: ______________
