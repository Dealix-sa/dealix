# Development Troubleshooting Guide

Common issues and solutions for Dealix development and deployment.

## 🔧 Setup & Environment Issues

### `.env.local` File Not Found / Not Recognized

**Symptom:** Script fails with "environment variable X not found" or ".env file missing"

**Solutions:**
1. **Copy the template:**
   ```bash
   cp .env.example .env.local
   ```

2. **Verify file exists in root directory:**
   ```bash
   ls -la .env.local  # Should show the file
   ```

3. **Check it's being loaded:**
   ```bash
   source .env.local
   echo $DATABASE_URL  # Should print the value
   ```

4. **Verify Python finds it:**
   ```bash
   python3 -c "import os; from dotenv import load_dotenv; load_dotenv('.env.local'); print(os.getenv('DATABASE_URL'))"
   ```

**Prevention:** Always keep `.env.local` in gitignore (it is), never commit real credentials

---

### Missing Required Environment Variables

**Symptom:** Error: "OPENROUTER_API_KEY must be configured" or "DATABASE_URL missing"

**Solution:**
1. **Run the verification script:**
   ```bash
   python3 scripts/check.py
   ```
   This will show which variables are missing and which are critical vs optional.

2. **Fill in required variables** (marked [REQUIRED] in `.env.example`):
   ```bash
   # Edit .env.local and add:
   ENVIRONMENT=production
   DATABASE_URL=postgresql://user:pass@host:5432/dealix
   OPENROUTER_API_KEY=your_key_here
   ```

3. **Critical checklist:**
   - ✅ `ENVIRONMENT` set to `production` or `development`
   - ✅ `DATABASE_URL` points to accessible PostgreSQL
   - ✅ `APP_SECRET_KEY` is a 64-byte hex (or generate with `python -c "import secrets; print(secrets.token_hex(32))"`)
   - ✅ At least one LLM key: `ANTHROPIC_API_KEY` OR `OPENAI_API_KEY` OR `GROQ_API_KEY`
   - ✅ For payments: `MOYASAR_SECRET_KEY` and `MOYASAR_WEBHOOK_SECRET`

**After updating .env.local:**
```bash
# Reload in your shell
source .env.local
# Verify again
python3 scripts/check.py
```

---

### Database Connection Failed

**Symptom:** `psycopg2.OperationalError: could not connect to server: Connection refused` or `SSL/TLS handshake failed`

**Solutions:**

1. **Check database is running:**
   ```bash
   # If local Postgres
   pg_isready -h localhost -p 5432
   
   # If Railway/Render
   nc -zv <RAILWAY_DB_HOST> 5432
   ```

2. **Verify DATABASE_URL format:**
   ```bash
   # Should be one of:
   postgresql://user:password@host:5432/dbname
   postgresql+asyncpg://user:password@host:5432/dbname  # With asyncpg
   
   # Test it:
   psql postgresql://user:password@host:5432/dbname -c "SELECT version();"
   ```

3. **Check credentials:**
   ```bash
   # Extract from URL and test
   # Format: postgresql://USER:PASSWORD@HOST:PORT/DB
   PGPASSWORD=<PASSWORD> psql -U <USER> -h <HOST> -d <DB> -c "SELECT 1"
   ```

4. **Check network/firewall:**
   ```bash
   # Ping the host
   ping <DB_HOST>
   
   # Check if port is open (requires telnet or nc)
   nc -zv <DB_HOST> 5432
   ```

5. **For Railway:**
   ```bash
   # Get current database info from Railway
   railway link  # Select your project
   railway status  # Check connection
   
   # Regenerate DATABASE_URL from Railway dashboard
   ```

6. **Enable verbose logging to debug:**
   ```bash
   # Set in .env.local
   LOG_LEVEL=DEBUG
   SQLALCHEMY_ECHO=true
   
   # Then run the check
   python3 scripts/check.py
   ```

---

## 🐍 Python & Dependency Issues

### `ModuleNotFoundError: No module named 'dealix'`

**Symptom:** Python script fails with "cannot import dealix" or "ModuleNotFoundError: No module named 'company'"

**Solutions:**

1. **Install in development mode:**
   ```bash
   pip install -e .
   ```

2. **Verify PYTHONPATH includes dealix root:**
   ```bash
   echo $PYTHONPATH
   
   # If empty, add it:
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

3. **For company module specifically:**
   ```bash
   # Verify company/__init__.py exists
   ls -la company/__init__.py
   
   # Test import
   python3 -c "from company.micro.micro_master import run_micro_daily_pack; print('OK')"
   ```

---

### Dependency Version Conflicts

**Symptom:** `ERROR: pip's dependency resolver does not currently take into account...` or `Conflict: package X requires Y < 2.0, but you have Z`

**Solutions:**

1. **Fresh virtual environment:**
   ```bash
   python3 -m venv venv_fresh
   source venv_fresh/bin/activate
   pip install -r requirements.txt
   ```

2. **Update pip, setuptools, wheel:**
   ```bash
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

3. **Check for conflicting versions:**
   ```bash
   pip check  # Shows all conflicts
   ```

4. **Install with retry:**
   ```bash
   pip install -r requirements.txt --use-deprecated=legacy-resolver
   ```

---

### Poetry / uv Lock File Issues

**Symptom:** `poetry lock` fails or `uv pip sync` errors

**Solutions:**

1. **Regenerate lock file:**
   ```bash
   poetry lock --no-update  # If using poetry
   ```

2. **Clear cache:**
   ```bash
   poetry cache clear . --all
   # OR
   uv cache clean
   ```

---

## 🚀 Script & Automation Issues

### Script Fails: `command not found` or Permission Denied

**Symptom:** `bash: dealix_micro_day.sh: command not found` or `Permission denied`

**Solutions:**

1. **Make script executable:**
   ```bash
   chmod +x scripts/dealix_micro_day.sh
   chmod +x scripts/*.sh  # All scripts
   ```

2. **Run from correct directory:**
   ```bash
   # Wrong:
   bash dealix_micro_day.sh
   
   # Correct:
   bash scripts/dealix_micro_day.sh
   # OR
   cd scripts && bash dealix_micro_day.sh
   ```

3. **Check script exists:**
   ```bash
   ls -la scripts/dealix_micro_day.sh
   file scripts/dealix_micro_day.sh  # Should show "bash script"
   ```

---

### Daily Script Hangs or Times Out

**Symptom:** `dealix_revenue_day.sh` runs for 30+ minutes or never completes

**Solutions:**

1. **Check database connectivity:**
   ```bash
   python3 << 'EOF'
   import os
   from sqlalchemy import create_engine, text
   db_url = os.getenv("DATABASE_URL")
   engine = create_engine(db_url)
   with engine.connect() as conn:
       result = conn.execute(text("SELECT 1"))
       print("DB OK:", result.fetchone())
   EOF
   ```

2. **Run in dry-run mode:**
   ```bash
   # Set in .env.local
   DRY_RUN=true
   # Then run script - should complete in seconds
   bash scripts/dealix_revenue_day.sh
   ```

3. **Kill and check processes:**
   ```bash
   # Find hung processes
   ps aux | grep dealix
   ps aux | grep python
   
   # Kill specific process
   kill -9 <PID>
   ```

4. **Check for locks:**
   ```bash
   # Database locks
   psql $DATABASE_URL -c "SELECT * FROM pg_locks;"
   
   # File locks
   ls -la company/runtime/*.lock
   ```

5. **Enable verbose logging:**
   ```bash
   # .env.local
   LOG_LEVEL=DEBUG
   
   # Run with output
   bash scripts/dealix_revenue_day.sh 2>&1 | tee /tmp/revenue_debug.log
   ```

---

### Output Files Not Created

**Symptom:** Script runs but no output in `company/runtime/` or `company/reports/`

**Solutions:**

1. **Check directories exist:**
   ```bash
   mkdir -p company/runtime
   mkdir -p company/reports
   mkdir -p logs
   ```

2. **Verify write permissions:**
   ```bash
   touch company/runtime/test.txt
   touch company/reports/test.md
   rm company/runtime/test.txt company/reports/test.md
   
   # If permission denied:
   chmod 755 company/runtime company/reports logs
   ```

3. **Check script's output configuration:**
   ```bash
   # Look for output path in script
   grep -n "company/runtime" scripts/dealix_revenue_day.sh
   
   # Verify variable is set
   echo $OUTPUT_DIR
   ```

---

## 🔐 API & Authentication Issues

### API Request Fails: 401 Unauthorized / Invalid API Key

**Symptom:** `requests.exceptions.HTTPError: 401 Unauthorized` or "Invalid API key"

**Solutions:**

1. **Verify API key is set:**
   ```bash
   echo $OPENROUTER_API_KEY
   echo $ANTHROPIC_API_KEY
   echo $MOYASAR_SECRET_KEY
   ```

2. **Test API key directly:**
   ```bash
   # Anthropic example
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model": "claude-opus-4-8", "max_tokens": 100, "messages": [{"role": "user", "content": "Hi"}]}'
   ```

3. **Check key expiration:**
   - Log into provider dashboard (Anthropic, OpenRouter, etc.)
   - Verify API key is still active
   - If expired, generate new key and update `.env.local`

4. **Check rate limits:**
   ```bash
   # Test with small request
   python3 << 'EOF'
   import anthropic
   client = anthropic.Anthropic()
   msg = client.messages.create(
       model="claude-opus-4-8",
       max_tokens=10,
       messages=[{"role": "user", "content": "Hi"}]
   )
   print("Rate limit OK:", msg)
   EOF
   ```

---

### LLM Provider Timeout / Slow Responses

**Symptom:** LLM calls take 30+ seconds or timeout after 30s

**Solutions:**

1. **Check provider status:**
   - Anthropic: https://status.anthropic.com/
   - OpenAI: https://status.openai.com/
   - OpenRouter: https://status.openrouter.io/

2. **Configure timeout:**
   ```bash
   # .env.local
   LLM_REQUEST_TIMEOUT_SECONDS=60
   LLM_MAX_RETRIES=3
   LLM_RETRY_BACKOFF_SECONDS=5
   ```

3. **Try alternative provider:**
   ```bash
   # If OPENROUTER_API_KEY set and primary fails, fallback activates automatically
   # Make sure you have backup providers configured
   ```

---

## 📊 Data & Database Issues

### CSV Import/Export Fails

**Symptom:** `FileNotFoundError` when reading CSV or `permission denied` when writing

**Solutions:**

1. **Check file exists:**
   ```bash
   ls -la data/leads/*.csv
   ls -la company/outbox/*.csv
   ```

2. **Check file encoding:**
   ```bash
   # CSV should be UTF-8
   file data/leads/my_leads.csv
   
   # Convert if needed (example)
   iconv -f ISO-8859-1 -t UTF-8 bad_encoding.csv > fixed.csv
   ```

3. **Verify format:**
   ```bash
   # First 5 lines
   head -5 data/leads/my_leads.csv
   
   # Check for quotes/escaping
   head -1 data/leads/my_leads.csv | tr ',' '\n' | nl
   ```

---

### PostgreSQL Connection Pooling Issues

**Symptom:** "too many connections" or "remaining connection slots are reserved"

**Solutions:**

1. **Check active connections:**
   ```bash
   psql $DATABASE_URL -c "
   SELECT usename, count(*) FROM pg_stat_activity GROUP BY usename;
   "
   ```

2. **Kill idle connections:**
   ```bash
   psql $DATABASE_URL -c "
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
   WHERE state = 'idle' AND query_start < now() - interval '1 hour';
   "
   ```

3. **Configure connection pool in `.env.local`:**
   ```bash
   SQLALCHEMY_POOL_SIZE=5
   SQLALCHEMY_POOL_RECYCLE=3600
   SQLALCHEMY_MAX_OVERFLOW=10
   ```

---

## 🧪 Testing Issues

### Tests Fail with Import Errors

**Symptom:** `ImportError` or `ModuleNotFoundError` during `pytest`

**Solutions:**

1. **Run pytest with PYTHONPATH:**
   ```bash
   PYTHONPATH=. pytest tests/
   ```

2. **Check conftest.py:**
   ```bash
   ls -la tests/conftest.py
   cat tests/conftest.py | head -20
   ```

3. **Install in editable mode:**
   ```bash
   pip install -e .
   pytest tests/
   ```

---

### Tests Timeout

**Symptom:** `FAILED tests/... - ERROR at setup timeout`

**Solutions:**

1. **Increase pytest timeout:**
   ```bash
   pytest tests/ --timeout=300  # 5 minutes
   ```

2. **Check for hanging connections:**
   ```bash
   # Run with verbose output
   pytest tests/ -vv -s
   ```

---

## 🐳 Docker / Deployment Issues

### Docker Build Fails

**Symptom:** `docker build` errors with missing dependencies or build failures

**Solutions:**

1. **Check Docker is running:**
   ```bash
   docker --version
   docker ps
   ```

2. **Build with verbose output:**
   ```bash
   docker build -t dealix:latest . --progress=plain
   ```

3. **Check Dockerfile:**
   ```bash
   cat Dockerfile | head -20
   ```

**Note:** Per CLAUDE.md, avoid running Docker in CI/CD unless explicitly needed

---

### Railway Deployment Fails

**Symptom:** Deployment status shows "failed" or "crashed"

**Solutions:**

1. **Check Railway logs:**
   ```bash
   railway link
   railway logs -f
   ```

2. **Verify Railway config:**
   ```bash
   cat railway.json  # Or check Railway dashboard
   ```

3. **Test locally first:**
   ```bash
   python3 -c "from api.main import app; print('App loads OK')"
   ```

---

## 📞 Getting Help

If you're stuck:

1. **Run full diagnostics:**
   ```bash
   python3 scripts/check.py
   ```

2. **Check logs:**
   ```bash
   tail -50 logs/dealix_*.log
   tail -50 /tmp/dealix_debug.log
   ```

3. **Enable debug mode:**
   ```bash
   # .env.local
   DEBUG=true
   LOG_LEVEL=DEBUG
   
   # Re-run failing command
   ```

4. **Search existing issues:**
   - Check `docs/CI_QUARANTINE.md` for known CI failures
   - Check GitHub Issues for similar problems
   - Check Slack #engineering for recent discussions

5. **Report the issue:**
   - Include: error message, `.env.local` values (sanitized), OS/Python version, steps to reproduce
   - Don't include: real API keys, database URLs, or customer data
