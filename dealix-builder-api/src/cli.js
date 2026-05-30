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
