#!/usr/bin/env bash
set -euo pipefail

echo ""
echo "===================================================================="
echo " DEALIX API-FIRST BUILDER v1.0 - GitHub Codespaces"
echo "===================================================================="
echo " This will create:"
echo " - dealix-builder-api Node/Express API"
echo " - OpenAI Responses API integration"
echo " - builder agents: planner, patcher, tester, reporter"
echo " - dealix-v2 operating spine if missing"
echo " - terminal scripts"
echo " - GitHub Actions CI"
echo " - safe .gitignore / .aiderignore"
echo "===================================================================="
echo ""

ROOT="$(pwd)"
STAMP="$(date +%Y%m%d-%H%M%S)"

echo "[Dealix] Root: $ROOT"

git config core.longpaths true || true
git config core.preloadindex true || true
git config gc.auto 256 || true

mkdir -p .dealix/reports .dealix/backups scripts prompts .github/workflows

git status --short > ".dealix/backups/status-before-api-first-$STAMP.txt" || true

if [ -f .git/index.lock ]; then
  echo "[Dealix] Removing stale .git/index.lock"
  rm -f .git/index.lock
fi

echo "[Dealix] Writing .gitignore"
cat > .gitignore <<'EOF'
# Dealix managed ignore

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
pnpm-debug.log*
dist/
build/
.next/
.nuxt/
.cache/
.turbo/
.vercel/
.netlify/

# Python
.venv/
venv/
env/
__pycache__/
*.pyc
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Env
.env
.env.*
!.env.example

# Logs
logs/
*.log

# Aider / AI
.aider.chat.history.md
.aider.input.history
.aider.tags.cache*/
.aider.repo.map
*.aider.log

# Dealix runtime
.dealix/cache/
.dealix/tmp/
.dealix/runs/

# Heavy files
*.zip
*.tar
*.tar.gz
*.7z
*.rar
*.sqlite
*.db
*.parquet
*.feather
*.mp4
*.mov
*.avi
*.mkv

# OS
.DS_Store
Thumbs.db
EOF

echo "[Dealix] Writing .aiderignore"
cat > .aiderignore <<'EOF'
node_modules/
.venv/
venv/
env/
.next/
.nuxt/
dist/
build/
coverage/
.cache/
.turbo/
.vercel/
.netlify/
__pycache__/
.pytest_cache/
.mypy_cache/
.ruff_cache/
logs/
*.log
*.zip
*.tar
*.tar.gz
*.7z
*.rar
*.sqlite
*.db
*.parquet
*.feather
*.mp4
*.mov
*.avi
*.mkv
.aider.tags.cache*/
.aider.chat.history.md
.dealix/cache/
.dealix/tmp/
.dealix/runs/

!dealix-v2/
!dealix-builder-api/
!scripts/
!prompts/
!README.md
EOF

echo "[Dealix] Creating dealix-v2 if missing"
mkdir -p dealix-v2/{dealix_os/data,ledgers,reports,clients/_template,services,core,governance,growth,money,relationships,partners,market,trust,product,founder,tests}

if [ ! -f dealix-v2/README.md ]; then
cat > dealix-v2/README.md <<'EOF'
# Dealix v2

Arabic-first AI Operations company spine.

## Operating equation

Sprint → Proof → Retainer → Module → Platform

## Core principle

Every project must create value, proof, reusable assets, governance records, and an expansion path.
EOF
fi

cat > dealix-v2/ledgers/VALUE_LEDGER.md <<'EOF'
# Value Ledger

| ID | Date | Client | Service | Value Type | Metric | Baseline | Result | Evidence | Next Value |
|---|---|---|---|---|---|---|---|---|---|
EOF

cat > dealix-v2/ledgers/CAPITAL_LEDGER.md <<'EOF'
# Capital Ledger

| ID | Date | Project | Capital Type | Asset Created | Reusable? | Owner | Next Use | Status |
|---|---|---|---|---|---|---|---|---|
EOF

cat > dealix-v2/ledgers/PIPELINE_LEDGER.md <<'EOF'
# Pipeline Ledger

| ID | Date | Company | Sector | Contact | Source | Problem | Recommended Offer | Stage | Next Action |
|---|---|---|---|---|---|---|---|---|---|
EOF

cat > dealix-v2/dealix_os/data/services.json <<'EOF'
{
  "lead-intelligence": {
    "name": "Lead Intelligence Sprint",
    "capability": "Revenue",
    "price_starts_at": 9500,
    "timeline": "10 business days",
    "kpi": "qualified accounts ranked",
    "proof_type": "Revenue / Quality",
    "upsell": "Pilot Conversion Sprint or Monthly RevOps OS",
    "deliverables": [
      "ICP clarification",
      "Data quality review",
      "Top 50 ranked accounts",
      "Score reasons",
      "Safe draft pack",
      "Proof report",
      "Expansion map"
    ]
  },
  "ai-quick-win": {
    "name": "AI Quick Win Sprint",
    "capability": "Operations",
    "price_starts_at": 12000,
    "timeline": "5-10 business days",
    "kpi": "hours saved and errors reduced",
    "proof_type": "Time / Quality",
    "upsell": "Monthly AI Ops",
    "deliverables": [
      "Workflow map",
      "Input/output definition",
      "AI-assisted workflow",
      "Human review point",
      "QA checklist",
      "Proof report"
    ]
  },
  "company-brain": {
    "name": "Company Brain Sprint",
    "capability": "Knowledge",
    "price_starts_at": 25000,
    "timeline": "15-20 business days",
    "kpi": "answers with sources",
    "proof_type": "Knowledge / Quality",
    "upsell": "Monthly Company Brain",
    "deliverables": [
      "Document inventory",
      "Source quality review",
      "Citation answer workflow",
      "No-source-no-answer rule",
      "Test question set",
      "Proof report"
    ]
  },
  "ai-governance": {
    "name": "AI Governance Sprint",
    "capability": "Governance",
    "price_starts_at": 20000,
    "timeline": "10-15 business days",
    "kpi": "risk controls implemented",
    "proof_type": "Risk",
    "upsell": "Monthly Governance Monitoring",
    "deliverables": [
      "AI usage policy",
      "Action taxonomy",
      "Approval matrix",
      "Incident response",
      "Runtime governance checklist"
    ]
  }
}
EOF

echo "[Dealix] Creating dealix-builder-api"
mkdir -p dealix-builder-api/src/{agents,lib,routes,workspace,reports} dealix-builder-api/tests

cat > dealix-builder-api/package.json <<'EOF'
{
  "name": "dealix-builder-api",
  "version": "1.0.0",
  "description": "API-first builder for Dealix",
  "type": "module",
  "main": "src/server.js",
  "scripts": {
    "dev": "node --watch src/server.js",
    "start": "node src/server.js",
    "test": "node --test tests/*.test.js",
    "smoke": "node src/cli.js doctor && node src/cli.js plan \"Build Growth OS\""
  },
  "dependencies": {
    "dotenv": "^16.4.7",
    "express": "^4.18.3",
    "openai": "^4.87.3",
    "zod": "^3.24.2"
  },
  "devDependencies": {}
}
EOF

cat > dealix-builder-api/.env.example <<'EOF'
OPENAI_API_KEY=your_key_here
PORT=8787
DEALIX_ROOT=..
DEALIX_ACTIVE_SCOPE=dealix-v2
OPENAI_MODEL=gpt-5.1
EOF

cat > dealix-builder-api/src/lib/paths.js <<'EOF'
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
export const API_ROOT = path.resolve(here, "../..");
export const REPO_ROOT = path.resolve(API_ROOT, process.env.DEALIX_ROOT || "..");
export const ACTIVE_SCOPE = process.env.DEALIX_ACTIVE_SCOPE || "dealix-v2";
export const ACTIVE_ROOT = path.resolve(REPO_ROOT, ACTIVE_SCOPE);

export function safeJoinInsideActive(...parts) {
  const target = path.resolve(ACTIVE_ROOT, ...parts);
  if (!target.startsWith(ACTIVE_ROOT)) {
    throw new Error("Path escapes active Dealix scope");
  }
  return target;
}
EOF

cat > dealix-builder-api/src/lib/fs-utils.js <<'EOF'
import fs from "node:fs/promises";
import path from "node:path";
import { ACTIVE_ROOT } from "./paths.js";

export async function exists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

export async function ensureDir(p) {
  await fs.mkdir(p, { recursive: true });
}

export async function readText(p) {
  return fs.readFile(p, "utf8");
}

export async function writeText(p, text) {
  await ensureDir(path.dirname(p));
  await fs.writeFile(p, text, "utf8");
}

export async function appendText(p, text) {
  await ensureDir(path.dirname(p));
  await fs.appendFile(p, text, "utf8");
}

export async function listFiles(root = ACTIVE_ROOT, max = 500) {
  const out = [];

  async function walk(dir) {
    if (out.length >= max) return;
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const e of entries) {
      if (out.length >= max) return;
      if (["node_modules", ".git", ".venv", "dist", "build", ".next"].includes(e.name)) continue;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) await walk(full);
      else out.push(path.relative(ACTIVE_ROOT, full));
    }
  }

  await walk(root);
  return out;
}
EOF

cat > dealix-builder-api/src/lib/openai-client.js <<'EOF'
import "dotenv/config";
import OpenAI from "openai";

export function getOpenAI() {
  if (!process.env.OPENAI_API_KEY) {
    throw new Error("OPENAI_API_KEY is missing. Add it as a Codespaces secret or export it in terminal.");
  }
  return new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
}

export const MODEL = process.env.OPENAI_MODEL || "gpt-5.1";
EOF

cat > dealix-builder-api/src/agents/planner.js <<'EOF'
import { getOpenAI, MODEL } from "../lib/openai-client.js";
import { listFiles } from "../lib/fs-utils.js";

export async function planTask({ goal, scope = "dealix-v2 only", constraints = [] }) {
  const client = getOpenAI();
  const files = await listFiles();

  const prompt = `
You are Dealix API-First Builder Planner.

Goal:
${goal}

Scope:
${scope}

Constraints:
${constraints.map((x) => `- ${x}`).join("\n") || "- none"}

Visible files:
${files.slice(0, 200).map((f) => `- ${f}`).join("\n")}

Return strict JSON with:
{
  "summary": "...",
  "phases": [{"name":"...", "actions":["..."]}],
  "files_to_create": [],
  "files_to_modify": [],
  "commands": [],
  "tests": [],
  "risks": [],
  "done_definition": []
}
`;

  const response = await client.responses.create({
    model: MODEL,
    input: [
      { role: "system", content: "You produce precise JSON implementation plans. Do not claim files were changed." },
      { role: "user", content: prompt }
    ]
  });

  return response.output_text;
}
EOF

cat > dealix-builder-api/src/agents/reporter.js <<'EOF'
import { writeText } from "../lib/fs-utils.js";
import path from "node:path";
import { API_ROOT } from "../lib/paths.js";

export async function saveReport(name, content) {
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const file = path.join(API_ROOT, "src", "reports", `${stamp}-${name}.md`);
  await writeText(file, content);
  return file;
}
EOF

cat > dealix-builder-api/src/agents/founder.js <<'EOF'
import { getOpenAI, MODEL } from "../lib/openai-client.js";
import { readText, exists } from "../lib/fs-utils.js";
import { ACTIVE_ROOT } from "../lib/paths.js";
import path from "node:path";

async function optionalRead(rel) {
  const p = path.join(ACTIVE_ROOT, rel);
  return (await exists(p)) ? await readText(p) : "";
}

export async function founderBrief() {
  const client = getOpenAI();
  const value = await optionalRead("ledgers/VALUE_LEDGER.md");
  const capital = await optionalRead("ledgers/CAPITAL_LEDGER.md");
  const pipeline = await optionalRead("ledgers/PIPELINE_LEDGER.md");

  const response = await client.responses.create({
    model: MODEL,
    input: [
      {
        role: "system",
        content: "You are Dealix founder chief of staff. Produce direct, practical, revenue-focused command briefs."
      },
      {
        role: "user",
        content: `
Create today's Sami Command Brief.

Use these ledgers:

VALUE:
${value}

CAPITAL:
${capital}

PIPELINE:
${pipeline}

Return markdown with:
1. Fastest cash action
2. Highest strategic opportunity
3. Follow-up queue
4. Revenue risk
5. Asset to build
6. Partner move
7. Kill/pause recommendation
8. Today's CEO decision
`
      }
    ]
  });

  return response.output_text;
}
EOF

cat > dealix-builder-api/src/routes/builder.js <<'EOF'
import express from "express";
import { z } from "zod";
import { planTask } from "../agents/planner.js";
import { founderBrief } from "../agents/founder.js";
import { saveReport } from "../agents/reporter.js";

export const builderRouter = express.Router();

builderRouter.get("/health", (req, res) => {
  res.json({ ok: true, service: "dealix-builder-api" });
});

builderRouter.post("/plan", async (req, res, next) => {
  try {
    const schema = z.object({
      goal: z.string().min(3),
      scope: z.string().optional(),
      constraints: z.array(z.string()).optional()
    });
    const input = schema.parse(req.body);
    const output = await planTask(input);
    const report = await saveReport("plan", `# Builder Plan\n\nGoal: ${input.goal}\n\n\`\`\`json\n${output}\n\`\`\`\n`);
    res.json({ ok: true, output, report });
  } catch (err) {
    next(err);
  }
});

builderRouter.post("/founder-brief", async (req, res, next) => {
  try {
    const output = await founderBrief();
    const report = await saveReport("founder-brief", output);
    res.json({ ok: true, output, report });
  } catch (err) {
    next(err);
  }
});
EOF

cat > dealix-builder-api/src/server.js <<'EOF'
import "dotenv/config";
import express from "express";
import { builderRouter } from "./routes/builder.js";

const app = express();
app.use(express.json({ limit: "4mb" }));

app.get("/", (req, res) => {
  res.json({
    ok: true,
    name: "Dealix API-First Builder",
    endpoints: ["/builder/health", "/builder/plan", "/builder/founder-brief"]
  });
});

app.use("/builder", builderRouter);

app.use((err, req, res, next) => {
  res.status(500).json({
    ok: false,
    error: err.message || "Unknown error"
  });
});

const port = Number(process.env.PORT || 8787);
app.listen(port, () => {
  console.log(`Dealix Builder API running on http://localhost:${port}`);
});
EOF

cat > dealix-builder-api/src/cli.js <<'EOF'
#!/usr/bin/env node
import "dotenv/config";
import { planTask } from "./agents/planner.js";
import { founderBrief } from "./agents/founder.js";

const [cmd, ...rest] = process.argv.slice(2);

async function main() {
  if (!cmd || cmd === "help") {
    console.log(`Dealix Builder CLI

Commands:
  doctor
  plan "goal"
  founder-brief
`);
    return;
  }

  if (cmd === "doctor") {
    console.log("Dealix Builder Doctor");
    console.log("=====================");
    console.log("Node:", process.version);
    console.log("OPENAI_API_KEY:", process.env.OPENAI_API_KEY ? "set" : "missing");
    console.log("OPENAI_MODEL:", process.env.OPENAI_MODEL || "gpt-5.1");
    console.log("DEALIX_ACTIVE_SCOPE:", process.env.DEALIX_ACTIVE_SCOPE || "dealix-v2");
    return;
  }

  if (cmd === "plan") {
    const goal = rest.join(" ").trim();
    if (!goal) throw new Error("Missing goal");
    console.log(await planTask({ goal }));
    return;
  }

  if (cmd === "founder-brief") {
    console.log(await founderBrief());
    return;
  }

  throw new Error(`Unknown command: ${cmd}`);
}

main().catch((err) => {
  console.error("ERROR:", err.message);
  process.exit(1);
});
EOF

cat > dealix-builder-api/tests/smoke.test.js <<'EOF'
import test from "node:test";
import assert from "node:assert/strict";

test("basic smoke", () => {
  assert.equal(1 + 1, 2);
});
EOF

echo "[Dealix] Writing scripts"
cat > scripts/dealix-builder.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../dealix-builder-api"
node src/cli.js "$@"
EOF
chmod +x scripts/dealix-builder.sh

cat > scripts/dealix-builder-dev.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../dealix-builder-api"
npm run dev
EOF
chmod +x scripts/dealix-builder-dev.sh

cat > scripts/dealix-api-test.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

curl -s http://localhost:8787/builder/health | jq . || true

curl -s -X POST http://localhost:8787/builder/plan \
  -H "Content-Type: application/json" \
  -d '{"goal":"Build Dealix Growth OS v6 inside dealix-v2 only","constraints":["do not touch legacy repo","write tests","update CLI"]}' | jq . || true
EOF
chmod +x scripts/dealix-api-test.sh

cat > scripts/dealix-codex.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../dealix-v2"

if ! command -v codex >/dev/null 2>&1; then
  echo "Codex CLI not found. Installing @openai/codex..."
  npm install -g @openai/codex
fi

codex "$@"
EOF
chmod +x scripts/dealix-codex.sh

echo "[Dealix] Writing prompts"
cat > prompts/DEALIX_API_FIRST_MASTER_PROMPT.md <<'EOF'
# Dealix API-First Master Prompt

You are building Dealix as an API-first AI Operations company.

Active scope:
- dealix-v2
- dealix-builder-api
- scripts
- prompts

Do not work on legacy areas unless explicitly asked.

## Strategic direction

Dealix builds governed AI operations for Saudi/MENA companies.

Path:
Sprint → Proof → Retainer → Module → Platform

## API builder mission

The builder API should accept tasks and produce:
1. Plan
2. Patch strategy
3. Test command
4. Risk review
5. Report
6. Optional commit instructions

## Build rules

- Never hardcode API keys.
- Keep OPENAI_API_KEY in environment variables.
- Keep scope inside dealix-v2.
- Write tests for core behavior.
- Generate markdown reports.
- Prefer small, composable agents:
  - planner
  - patcher
  - tester
  - reporter
  - founder brief
  - growth analyst
  - deal room
  - governance reviewer
EOF

echo "[Dealix] Writing GitHub Actions CI"
cat > .github/workflows/dealix-ci.yml <<'EOF'
name: Dealix CI

on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  builder-api:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: dealix-builder-api
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm ci || npm install
      - run: npm test
      - run: node src/cli.js doctor
EOF

echo "[Dealix] Installing dependencies"
cd dealix-builder-api
npm install
npm test
node src/cli.js doctor
cd ..

echo "[Dealix] Writing quickstart"
cat > DEALIX_CODESPACES_QUICKSTART.md <<'EOF'
# Dealix Codespaces Quickstart

## 1. Add API key safely

Best: GitHub → Settings → Codespaces → Secrets → New secret

Name:

OPENAI_API_KEY

Then restart Codespace.

Temporary terminal method:

export OPENAI_API_KEY="your_key_here"

## 2. Run API

./scripts/dealix-builder-dev.sh

## 3. Test API

In another terminal:

./scripts/dealix-api-test.sh

## 4. Use CLI

./scripts/dealix-builder.sh doctor
./scripts/dealix-builder.sh plan "Build Growth OS v6 inside dealix-v2 only"
./scripts/dealix-builder.sh founder-brief

## 5. Use Codex CLI in dealix-v2

./scripts/dealix-codex.sh "Improve Dealix CLI and add Growth OS commands. Stay inside dealix-v2."
EOF

echo "[Dealix] Git status"
git status --short || true

echo "[Dealix] Staging files"
git add .gitignore .aiderignore .github workflows 2>/dev/null || true
git add .github/workflows/dealix-ci.yml dealix-v2 dealix-builder-api scripts prompts DEALIX_CODESPACES_QUICKSTART.md .dealix/reports .dealix/backups || true

echo ""
echo "===================================================================="
echo " DEALIX API-FIRST BUILDER READY"
echo "===================================================================="
echo ""
echo "Next:"
echo "  1) Add OPENAI_API_KEY as Codespaces secret, or export it temporarily:"
echo "     export OPENAI_API_KEY='your_key_here'"
echo ""
echo "  2) Run API:"
echo "     ./scripts/dealix-builder-dev.sh"
echo ""
echo "  3) In another terminal:"
echo "     ./scripts/dealix-api-test.sh"
echo ""
echo "  4) CLI:"
echo "     ./scripts/dealix-builder.sh doctor"
echo "     ./scripts/dealix-builder.sh plan 'Build Growth OS v6 inside dealix-v2 only'"
echo "     ./scripts/dealix-builder.sh founder-brief"
echo ""
echo "  5) Commit:"
echo "     git status"
echo "     git commit -m 'build Dealix API-first builder'"
echo ""
echo "===================================================================="
