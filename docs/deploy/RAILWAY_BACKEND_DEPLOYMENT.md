# Railway Backend Deployment

## Prerequisites
- Railway account
- PostgreSQL and Redis services provisioned

## Steps
1. Connect GitHub repo to Railway project
2. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
3. Add environment variables from `docs/deploy/ENVIRONMENT_VARIABLES.md`
4. Run `bash scripts/railway_prod_bootstrap.sh` once for Alembic + seed

## Health Check
- `GET /api/health/commercial-os` should return 200

## Post-Deploy
- Run `bash scripts/founder_production_smoke.sh`
- Verify `GET /api/v1/business-now/snapshot`
