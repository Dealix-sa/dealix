# Server Deployment Checklist

## Purpose

Run Dealix workers safely on the connected server.

## Required

- repo cloned at `/opt/dealix`
- private ops at `/opt/dealix-ops-private`
- Python 3.11+
- logs directory at `/var/log/dealix`
- `.env` configured locally, not committed
- GitHub deploy key or pull method configured
- cron or systemd timers installed
- `main` branch protected
- GitHub checks required

## Commands

```bash
sudo mkdir -p /opt/dealix /opt/dealix-ops-private /var/log/dealix
sudo chown -R $USER:$USER /opt/dealix /opt/dealix-ops-private /var/log/dealix
cd /opt/dealix
python scripts/bootstrap_private_ops.py --private-ops /opt/dealix-ops-private
make company-check PRIVATE_OPS=/opt/dealix-ops-private
```

## Cron Install

```bash
crontab deploy/cron/dealix_crontab.example
```

## Safety

- no automatic external sending
- no secrets in repo
- logs reviewed weekly
- workers fail loudly

## Compliance Anchors

- CST anti-spam rules respected: no bulk telecom outreach.
- PDPL / SDAIA personal data principles respected: only public business
  contact paths are stored, opt-outs honored.
- NIST AI RMF: Govern / Map / Measure / Manage applied to every worker.
