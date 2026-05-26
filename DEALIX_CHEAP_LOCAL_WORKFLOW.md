# Dealix Cheap Local Workflow

This repository now uses `dealix-v2` as the local terminal-first platform.

## Why

The cheapest and most reliable path is:

1. **Build local CLI**: Run operations offline or locally first to ensure robust operational logic.
2. **Use ledgers and proof packs**: Record real-time business progress, value realized, capital assets generated, and governance logs.
3. **Use Aider/Ollama only for small edits**: Save cost and speed up iterations.
4. **Use OpenRouter only for hard tasks**: High-capacity models should only handle complex analytical tasks.
5. **Add API later only when the CLI is stable**: Ensure structural core is perfect before exposing REST interfaces.

## Commands

You can run the commands using our PowerShell wrapper:

```powershell
# Run the platform checkup
.\scripts\dealix-local.ps1 doctor

# List available services
.\scripts\dealix-local.ps1 services

# Score a business opportunity
.\scripts\dealix-local.ps1 score "paid B2B agency partner with monthly retainer and CRM data"

# Generate client pack workspace
.\scripts\dealix-local.ps1 client-pack --client "Demo Client" --sector "B2B Services" --problem "messy leads" --service "lead-intelligence"

# Log a value proof to the ledger
.\scripts\dealix-local.ps1 value --client "Demo Client" --service "lead-intelligence" --metric "qualified accounts ranked" --result "top 50 accounts ranked"

# Build a client proof pack report
.\scripts\dealix-local.ps1 proof-pack --client "Demo Client" --service "lead-intelligence" --metric "qualified accounts ranked" --result "top 50 accounts ranked"

# Build proposal document
.\scripts\dealix-local.ps1 proposal --client "Demo Client" --service "lead-intelligence" --problem "messy leads"

# View operational stats
.\scripts\dealix-local.ps1 dashboard

# Run monthly summary reports
.\scripts\dealix-local.ps1 monthly-review
```

## Testing

Run the test suite locally:

```powershell
# Run the test suite using pytest
pytest dealix-v2/tests/test_cli_local_v3.py
```
