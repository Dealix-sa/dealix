import { Router } from "express";
import { sql } from "drizzle-orm";
import { getDb, deals, leads, approvals } from "@workspace/db";

export const transformationRouter = Router();

transformationRouter.get("/kpi-snapshot", async (_req, res, next) => {
  try {
    const db = getDb();
    const [stats] = await db
      .select({
        avgCycle: sql<number>`coalesce(
          extract(epoch from avg(${deals.updatedAt} - ${deals.createdAt})) / 86400,
          0
        )::int`,
        avgScore: sql<number>`coalesce(avg(${leads.aiScore}),0)::int`,
      })
      .from(deals)
      .leftJoin(leads, sql`true`);

    const [pending] = await db
      .select({
        c: sql<number>`count(*) filter (where ${approvals.status} = 'pending')::int`,
      })
      .from(approvals);

    res.json({
      generatedAt: new Date().toISOString(),
      kpis: [
        {
          id: "cycle_days",
          label: "متوسط دورة الصفقة (يوم)",
          value: stats?.avgCycle || 0,
          target: 45,
          format: "number",
        },
        {
          id: "avg_ai_score",
          label: "متوسط AI Score",
          value: stats?.avgScore || 0,
          target: 75,
          format: "number",
        },
        {
          id: "approvals_open",
          label: "Approvals مفتوحة",
          value: pending?.c || 0,
          target: 0,
          format: "number",
        },
      ],
      transformationMaturity: {
        current: 2.3,
        target: 4.0,
        scale: "1=manual ↔ 5=fully autonomous",
      },
    });
  } catch (e) {
    next(e);
  }
});
