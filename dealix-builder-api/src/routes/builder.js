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
