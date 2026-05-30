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
