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
