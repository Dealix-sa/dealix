# Control Plane API

All endpoints below sit under `/api/v1/internal/control/`.

| Method | Path                              | Purpose                          |
|--------|-----------------------------------|----------------------------------|
| GET    | /summary                          | rolled-up control summary        |
| GET    | /policies                         | policy YAML, parsed              |
| GET    | /agents                           | agent registry, parsed           |
| POST   | /agents/{id}/disable              | record an agent disable          |
| POST   | /agents/{id}/enable               | record an agent enable           |
| GET    | /scorecard                        | operating scorecard payload       |
| GET    | /risks                            | open trust flags                 |

Auth: requires `X-Dealix-Internal-Token` header when
`DEALIX_INTERNAL_TOKEN` is set in the environment.
