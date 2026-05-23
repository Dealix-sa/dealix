# Future SaaS Repo Structure

## Use Only After SaaS Architecture Gate

```txt
dealix/
├── apps/
│   ├── web/
│   └── admin/
├── api/
│   ├── routes/
│   ├── services/
│   └── auth/
├── workers/
│   ├── scoring/
│   ├── reports/
│   └── notifications/
├── db/
│   ├── schema/
│   └── migrations/
├── packages/
│   ├── ui/
│   ├── shared/
│   └── schemas/
├── ops_runtime/
├── control_plane/
├── execution_engine/
├── docs/
├── schemas/
└── .github/workflows/
```

## Product Rule
Do not create this structure before SaaS readiness.
