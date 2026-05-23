import { Router } from "express";
import { desc } from "drizzle-orm";
import { getDb, deals } from "@workspace/db";

export const pipelineRouter = Router();

const STAGES = [
  { id: "lead", name: "Lead", color: "#94a3b8" },
  { id: "qualified", name: "Qualified", color: "#60a5fa" },
  { id: "proposal", name: "Proposal", color: "#a78bfa" },
  { id: "negotiation", name: "Negotiation", color: "#f59e0b" },
  { id: "closed_won", name: "Closed Won", color: "#10b981" },
  { id: "closed_lost", name: "Closed Lost", color: "#ef4444" },
] as const;

pipelineRouter.get("/summary", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db.select().from(deals).orderBy(desc(deals.lastActivityAt));
    const byStage = STAGES.map((s) => {
      const items = rows.filter((r) => r.stage === s.id);
      return {
        stage: s.id,
        name: s.name,
        color: s.color,
        count: items.length,
        totalValue: items.reduce((sum, d) => sum + Number(d.value), 0),
        deals: items.map((d) => ({
          id: d.id,
          title: d.title,
          company: d.company,
          value: Number(d.value),
          currency: d.currency,
          stage: d.stage,
          probability: d.probability,
          aiScore: d.aiScore,
          assignedTo: d.assignedTo,
          closeDate: d.closeDate?.toISOString(),
          lastActivity: d.lastActivityAt.toISOString(),
          tags: d.tags,
        })),
      };
    });
    res.json({
      stages: byStage,
      totals: {
        deals: rows.length,
        value: rows.reduce((sum, d) => sum + Number(d.value), 0),
        currency: "SAR",
      },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});
