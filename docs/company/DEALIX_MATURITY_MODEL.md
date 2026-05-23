# Dealix Maturity Model

| Stage | Capability                                                     |
|-------|----------------------------------------------------------------|
| 0     | manual founder ops, no console                                 |
| 1     | console reads private ops CSVs (current target)                |
| 2     | workers populate private ops CSVs automatically (current target) |
| 3     | shadow Postgres double-write                                   |
| 4     | Postgres primary, CSV export only                              |
| 5     | multi-tenant control plane, dedicated tenant runtimes          |

Stages 1 and 2 are what the Ultimate Operating Layer ships. Stages 3+
are roadmap; see `docs/data/POSTGRES_PRIMARY_MODE.md`.
