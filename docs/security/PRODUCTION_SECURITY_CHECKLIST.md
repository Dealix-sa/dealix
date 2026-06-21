# Production Security Checklist

## Pre-Deploy
- [ ] `scripts/check_no_secrets.py` passes
- [ ] No `.env` files in repo
- [ ] DATABASE_URL uses SSL
- [ ] APP_SECRET_KEY rotated and >32 bytes
- [ ] Moyasar keys are live/sandbox correct

## Runtime
- [ ] HTTPS only
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Admin endpoints behind API key
- [ ] Error messages do not leak stack traces

## Monitoring
- [ ] Health check endpoint active
- [ ] Failed login alerting
- [ ] Unusual outbound traffic alerting

## Incident Response
- [ ] On-call rotation defined
- [ ] Rollback procedure tested
- [ ] Backup verified within 7 days
