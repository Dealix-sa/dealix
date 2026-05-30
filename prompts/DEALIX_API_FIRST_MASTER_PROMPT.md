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
