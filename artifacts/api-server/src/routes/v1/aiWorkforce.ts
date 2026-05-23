import { Router } from "express";
import { desc } from "drizzle-orm";
import { getDb, workers } from "@workspace/db";
import { wsHub } from "../../lib/wsHub.js";

export const aiWorkforceRouter = Router();

const DEFAULT_AGENTS = [
  {
    name: "outreach-agent",
    type: "outreach",
    description: "يصيغ ويُجدول رسائل التواصل المخصصة",
    capabilities: ["draft_email_ar", "draft_linkedin_ar", "schedule_followup"],
  },
  {
    name: "scoring-agent",
    type: "scoring",
    description: "يحسب ai_score للقيادات والصفقات",
    capabilities: ["lead_scoring", "deal_probability", "engagement_index"],
  },
  {
    name: "compliance-agent",
    type: "compliance",
    description: "يراجع الالتزام والسياسات قبل الإرسال الخارجي",
    capabilities: ["pdpl_check", "channel_policy", "consent_verify"],
  },
  {
    name: "intelligence-agent",
    type: "intelligence",
    description: "يستخرج معلومات من المصادر العامة ويثري الحسابات",
    capabilities: ["enrichment", "news_scan", "competitor_radar"],
  },
  {
    name: "orchestrator-agent",
    type: "orchestrator",
    description: "ينسق التشغيل اليومي الكامل",
    capabilities: ["morning_run", "evening_run", "weekly_retro"],
  },
];

aiWorkforceRouter.get("/agents", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db.select().from(workers).orderBy(desc(workers.updatedAt));
    const byName = new Map(rows.map((r) => [r.name, r]));
    const agents = DEFAULT_AGENTS.map((d) => {
      const row = byName.get(d.name);
      const lastRun = row?.lastRunAt;
      const minutesSince = lastRun
        ? Math.round((Date.now() - lastRun.getTime()) / 60_000)
        : null;
      const stale =
        !lastRun || minutesSince === null
          ? false
          : minutesSince > 30 && row?.status !== "idle";
      return {
        id: row?.id ?? d.name,
        name: d.name,
        type: d.type,
        description: d.description,
        capabilities: d.capabilities,
        status: stale ? "stale" : row?.status ?? "idle",
        lastRunAt: lastRun?.toISOString() ?? null,
        lastSuccessAt: row?.lastSuccessAt?.toISOString() ?? null,
        runCount: row?.runCount ?? 0,
        successCount: row?.successCount ?? 0,
        failureCount: row?.failureCount ?? 0,
        successRate:
          (row?.runCount ?? 0) > 0
            ? Math.round(((row?.successCount ?? 0) / (row?.runCount ?? 1)) * 100)
            : 100,
        minutesSinceLastRun: minutesSince,
      };
    });
    res.json({
      agents,
      total: agents.length,
      online: agents.filter((a) => a.status === "running" || a.status === "idle")
        .length,
      stale: agents.filter((a) => a.status === "stale").length,
      wsClients: wsHub.count(),
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});
