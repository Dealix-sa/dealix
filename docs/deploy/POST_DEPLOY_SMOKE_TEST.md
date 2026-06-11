# Post-Deploy Smoke Test

## Script
```bash
python3 scripts/post_deploy_smoke.py --base-url https://your-domain.com
```

## Pages Checked
- `/`
- `/sales-machine`
- `/lead-engine`
- `/offers`
- `/pricing`
- `/command-center`
- `/api/health/commercial-os`

## Expected
All return HTTP 200.

## If Fail
1. Check Vercel/Railway deployment logs
2. Verify environment variables
3. Run local reproduction
4. Escalate to on-call if production
