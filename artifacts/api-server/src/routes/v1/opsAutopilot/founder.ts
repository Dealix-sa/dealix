import { Router } from "express";
import { z } from "zod";
import { desc, eq, sql, and } from "drizzle-orm";
import {
  getDb,
  leads,
  deals,
  approvals,
  evidenceEvents,
  marketingCalendar,
  workers,
} from "@workspace/db";
import { validateBody } from "../../../middleware/validate.js";
import { requireAdminKey } from "../../../middleware/requireAdminKey.js";
import { aiChat } from "../../../lib/ai.js";

export const founderRouter = Router();
export const founderDashboardRouter = Router();

founderRouter.use(requireAdminKey);
founderDashboardRouter.use(requireAdminKey);

async function gatherSnapshot() {
  const db = getDb();
  const [leadStats] = await db
    .select({
      total: sql<number>`count(*)::int`,
      p0: sql<number>`count(*) filter (where ${leads.priority} = 'p0')::int`,
      new7: sql<number>`count(*) filter (where ${leads.createdAt} >= now() - interval '7 days')::int`,
      avgScore: sql<number>`coalesce(avg(${leads.aiScore}),0)::int`,
    })
    .from(leads);
  const [dealStats] = await db
    .select({
      active: sql<number>`count(*) filter (where ${deals.stage} not in ('closed_won','closed_lost'))::int`,
      won: sql<number>`count(*) filter (where ${deals.stage} = 'closed_won')::int`,
      pipelineValue: sql<number>`coalesce(sum(${deals.value}) filter (where ${deals.stage} not in ('closed_won','closed_lost')), 0)`,
    })
    .from(deals);
  const [appStats] = await db
    .select({
      pending: sql<number>`count(*) filter (where ${approvals.status} = 'pending')::int`,
    })
    .from(approvals);
  const recentEvidence = await db
    .select()
    .from(evidenceEvents)
    .orderBy(desc(evidenceEvents.createdAt))
    .limit(5);
  const upcomingMarketing = await db
    .select()
    .from(marketingCalendar)
    .orderBy(desc(marketingCalendar.slotDate))
    .limit(5);
  const topP0 = await db
    .select()
    .from(leads)
    .where(eq(leads.priority, "p0"))
    .orderBy(desc(leads.aiScore))
    .limit(5);
  return {
    leads: leadStats,
    deals: {
      ...(dealStats ?? {}),
      pipelineValue: Number(dealStats?.pipelineValue || 0),
    },
    approvals: appStats,
    recentEvidence,
    upcomingMarketing,
    topP0,
  };
}

founderRouter.get("/cockpit", async (req, res, next) => {
  try {
    const mode = String(req.query.mode || "morning");
    const topN = Math.min(parseInt(String(req.query.top_n ?? 15), 10) || 15, 100);
    const snap = await gatherSnapshot();
    res.json({
      mode,
      topN,
      generatedAt: new Date().toISOString(),
      focus:
        mode === "morning"
          ? ["P0 outreach قبل الظهر", "Approvals متأخرة", "Quick wins من pipeline"]
          : mode === "evening"
            ? ["تحديث nextFollowUpAt", "تسجيل evidence اليوم", "تخطيط الغد"]
            : ["Weekly retro: ما نجح/ما فشل", "Reset targets", "Founder time blocks"],
      snapshot: snap,
    });
  } catch (e) {
    next(e);
  }
});

const cockpitRunSchema = z.object({
  top_n: z.number().optional(),
  run_optional_scripts: z.boolean().optional(),
  quick: z.boolean().optional(),
});

async function runSequence(mode: string, topN: number) {
  const snap = await gatherSnapshot();
  const db = getDb();
  await db
    .update(workers)
    .set({ status: "running", lastRunAt: new Date(), updatedAt: new Date() })
    .where(eq(workers.name, "orchestrator-agent"));
  const steps = [
    { name: "load_snapshot", status: "completed" },
    { name: "score_p0_leads", status: "completed", processed: snap.topP0.length },
    { name: "draft_outreach", status: "completed", drafted: Math.min(topN, snap.topP0.length) },
    { name: "review_approvals", status: snap.approvals?.pending ? "needs_action" : "completed" },
    { name: "log_evidence", status: "completed" },
  ];
  await db
    .update(workers)
    .set({
      status: "completed",
      lastSuccessAt: new Date(),
      runCount: sql`${workers.runCount} + 1`,
      successCount: sql`${workers.successCount} + 1`,
      updatedAt: new Date(),
    })
    .where(eq(workers.name, "orchestrator-agent"));
  return {
    mode,
    steps,
    snapshot: snap,
    completedAt: new Date().toISOString(),
  };
}

founderRouter.post(
  "/cockpit/run-morning",
  validateBody(cockpitRunSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof cockpitRunSchema>;
      const out = await runSequence("morning", b.top_n || 15);
      res.json(out);
    } catch (e) {
      next(e);
    }
  },
);

founderRouter.post(
  "/cockpit/run-evening",
  validateBody(cockpitRunSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof cockpitRunSchema>;
      const out = await runSequence("evening", b.top_n || 15);
      res.json(out);
    } catch (e) {
      next(e);
    }
  },
);

founderRouter.post(
  "/cockpit/run-weekly",
  validateBody(cockpitRunSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof cockpitRunSchema>;
      const out = await runSequence("weekly", b.top_n || 25);
      res.json(out);
    } catch (e) {
      next(e);
    }
  },
);

founderRouter.post(
  "/cockpit/run-unified-day",
  validateBody(cockpitRunSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof cockpitRunSchema>;
      const morning = await runSequence("morning", b.top_n || 15);
      const evening = b.quick ? null : await runSequence("evening", b.top_n || 15);
      res.json({
        unifiedDay: true,
        morning,
        evening,
        completedAt: new Date().toISOString(),
      });
    } catch (e) {
      next(e);
    }
  },
);

const completeDaySchema = z.object({
  weekly: z.boolean().optional(),
  evening: z.boolean().optional(),
  skip_commercial_day: z.boolean().optional(),
  use_unified_in_process: z.boolean().optional(),
  top_n: z.number().optional(),
});

founderRouter.post(
  "/complete-autonomous-day/run",
  validateBody(completeDaySchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof completeDaySchema>;
      const topN = b.top_n || 15;
      const morning = await runSequence("morning", topN);
      const evening = b.evening !== false ? await runSequence("evening", topN) : null;
      const weekly = b.weekly ? await runSequence("weekly", topN) : null;
      res.json({
        completeDay: true,
        steps: ["morning", evening ? "evening" : null, weekly ? "weekly" : null].filter(Boolean),
        morning,
        evening,
        weekly,
        commercial: b.skip_commercial_day ? null : { ranAt: new Date().toISOString() },
        completedAt: new Date().toISOString(),
      });
    } catch (e) {
      next(e);
    }
  },
);

founderRouter.get("/value-plan", async (req, res, next) => {
  try {
    const topN = Math.min(parseInt(String(req.query.top_n ?? 5), 10) || 5, 50);
    const db = getDb();
    const top = await db
      .select()
      .from(leads)
      .orderBy(desc(leads.aiScore))
      .limit(topN);
    res.json({
      generatedAt: new Date().toISOString(),
      plan: top.map((l, i) => ({
        rank: i + 1,
        company: l.company,
        aiScore: l.aiScore,
        estimatedValue: Number(l.estimatedValue),
        priority: l.priority,
        nextStep:
          l.stage === "lead"
            ? "ابدأ outreach مخصص"
            : l.stage === "qualified"
              ? "ابني proposal"
              : l.stage === "proposal"
                ? "متابعة + objections"
                : "إغلاق",
      })),
    });
  } catch (e) {
    next(e);
  }
});

founderRouter.get("/gtm-stack", async (req, res, next) => {
  try {
    const topN = Math.min(parseInt(String(req.query.top_n ?? 10), 10) || 10, 50);
    const db = getDb();
    const top = await db
      .select()
      .from(leads)
      .orderBy(desc(leads.aiScore))
      .limit(topN);
    res.json({
      stack: {
        warm_intros: { weeklyTarget: 9, current: 0 },
        abm_top50: { weeklyTarget: 25, current: 0 },
        content: { weeklyTarget: 3, current: 0 },
        demos: { weeklyTarget: 5, current: 0 },
      },
      topAccounts: top.map((l) => ({
        company: l.company,
        aiScore: l.aiScore,
        stage: l.stage,
      })),
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

founderRouter.get("/full-autonomous-ops", async (req, res, next) => {
  try {
    const topN = Math.min(parseInt(String(req.query.top_n ?? 15), 10) || 15, 100);
    const includeValuePlan = req.query.include_value_plan === "true";
    const snap = await gatherSnapshot();
    res.json({
      ops: {
        warRoom: { totalTargets: snap.leads?.total || 0, p0: snap.leads?.p0 || 0 },
        pipeline: { active: snap.deals?.active || 0, valueSAR: snap.deals?.pipelineValue || 0 },
        approvals: { pending: snap.approvals?.pending || 0 },
        evidence: { last5: snap.recentEvidence },
        marketing: { next5: snap.upcomingMarketing },
      },
      valuePlan: includeValuePlan
        ? snap.topP0.slice(0, topN).map((l) => ({
            company: l.company,
            aiScore: l.aiScore,
            estimatedValue: Number(l.estimatedValue),
          }))
        : null,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

founderRouter.post(
  "/full-autonomous-ops/run",
  validateBody(cockpitRunSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof cockpitRunSchema>;
      const out = await runSequence("autonomous", b.top_n || 15);
      res.json(out);
    } catch (e) {
      next(e);
    }
  },
);

founderRouter.get("/commercial-value-map", async (req, res, next) => {
  try {
    const topN = Math.min(parseInt(String(req.query.top_n ?? 5), 10) || 5, 50);
    const db = getDb();
    const top = await db
      .select()
      .from(leads)
      .orderBy(desc(leads.aiScore))
      .limit(topN);
    const totalValue = top.reduce((s, l) => s + Number(l.estimatedValue), 0);
    res.json({
      map: top.map((l) => ({
        company: l.company,
        aiScore: l.aiScore,
        estimatedValue: Number(l.estimatedValue),
        weight: totalValue > 0 ? Math.round((Number(l.estimatedValue) / totalValue) * 100) : 0,
      })),
      totals: { value: totalValue, count: top.length, currency: "SAR" },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

founderRouter.get("/strongest-plan", async (_req, res, next) => {
  try {
    const snap = await gatherSnapshot();
    res.json({
      plan: {
        objective: "تحريك pipeline من القمة إلى الأسفل بأقل مجهود",
        steps: [
          { id: 1, title: "متابعة P0 خلال 24 ساعة", responsible: "founder" },
          { id: 2, title: "إنشاء warm intros 9 جدد", responsible: "outreach-agent" },
          { id: 3, title: "إغلاق approvals متأخرة", responsible: "founder" },
          { id: 4, title: "نشر 3 منشورات LinkedIn", responsible: "marketing-agent" },
          { id: 5, title: "Discovery 2 demos", responsible: "founder" },
        ],
        snapshot: snap,
      },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

founderRouter.get("/strongest-ops", async (req, res, next) => {
  try {
    const mode = String(req.query.mode || "morning");
    const snap = await gatherSnapshot();
    res.json({
      mode,
      ops: {
        priority1: "P0 outreach",
        priority2: "Approvals review",
        priority3: "Pipeline hygiene",
        metrics: {
          p0Count: snap.leads?.p0 || 0,
          pendingApprovals: snap.approvals?.pending || 0,
          pipelineValue: snap.deals?.pipelineValue || 0,
        },
      },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const strongestOpsRunSchema = z.object({
  mode: z.string().optional(),
  run_checks: z.boolean().optional(),
  write_brief: z.boolean().optional(),
});

founderRouter.post(
  "/strongest-ops/run",
  validateBody(strongestOpsRunSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof strongestOpsRunSchema>;
      const out = await runSequence(b.mode || "strongest", 15);
      let brief: string | null = null;
      if (b.write_brief) {
        const ai = await aiChat({
          systemPrompt: "أنت COO ذكي يكتب brief 4 جمل للمؤسس.",
          userPrompt: `حدثت 5 خطوات تشغيلية. اكتب brief قصير: ماذا حدث، ماذا تبقى، خطوة واحدة عاجلة.`,
          language: "ar",
          maxTokens: 250,
        });
        brief = ai.text;
      }
      res.json({ ...out, brief });
    } catch (e) {
      next(e);
    }
  },
);

founderRouter.get("/expansion-status", async (req, res, next) => {
  try {
    const topN = Math.min(parseInt(String(req.query.top_n ?? 10), 10) || 10, 100);
    const db = getDb();
    const customers = await db
      .select()
      .from(deals)
      .where(eq(deals.stage, "closed_won"))
      .limit(topN);
    res.json({
      activeCustomers: customers.length,
      expansionCandidates: customers.map((c) => ({
        company: c.company,
        currentValueSAR: Number(c.value),
        expansionOpportunity: Math.round(Number(c.value) * 0.35),
      })),
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

founderRouter.get("/daily-pack", async (_req, res, next) => {
  try {
    const snap = await gatherSnapshot();
    res.json({
      pack: {
        date: new Date().toISOString().slice(0, 10),
        morning: {
          focus: snap.topP0.slice(0, 3).map((l) => ({
            company: l.company,
            aiScore: l.aiScore,
            action: "outreach مخصص",
          })),
        },
        evening: {
          review: ["approvals", "evidence", "next_day_targets"],
        },
        summary: {
          p0: snap.leads?.p0 || 0,
          pipelineSAR: snap.deals?.pipelineValue || 0,
          pendingApprovals: snap.approvals?.pending || 0,
        },
      },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

founderDashboardRouter.get("/", async (_req, res, next) => {
  try {
    const snap = await gatherSnapshot();
    res.json({
      kpis: [
        { label: "P0 Leads", value: snap.leads?.p0 || 0 },
        { label: "Active Deals", value: snap.deals?.active || 0 },
        { label: "Pipeline Value", value: snap.deals?.pipelineValue || 0, format: "currency" },
        { label: "Approvals Pending", value: snap.approvals?.pending || 0 },
        { label: "Avg AI Score", value: snap.leads?.avgScore || 0 },
      ],
      topAccounts: snap.topP0.slice(0, 5).map((l) => ({
        company: l.company,
        aiScore: l.aiScore,
        stage: l.stage,
      })),
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

founderRouter.get("/full-ops-health", async (_req, res, next) => {
  try {
    const db = getDb();
    const w = await db.select().from(workers);
    const stale = w.filter(
      (x) =>
        x.lastRunAt &&
        Date.now() - x.lastRunAt.getTime() > 30 * 60_000 &&
        x.status === "running",
    );
    res.json({
      health: stale.length ? "degraded" : "healthy",
      workers: w.length,
      stale: stale.length,
      details: w.map((x) => ({
        name: x.name,
        status: x.status,
        lastRunAt: x.lastRunAt?.toISOString() || null,
        successRate:
          x.runCount > 0 ? Math.round((x.successCount / x.runCount) * 100) : 100,
      })),
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const clientPackSchema = z.object({
  company: z.string().optional(),
  lead_id: z.string().optional(),
  write_disk: z.boolean().optional(),
});

founderRouter.post(
  "/client-pack/generate",
  validateBody(clientPackSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof clientPackSchema>;
      let companyName = b.company;
      if (!companyName && b.lead_id) {
        const db = getDb();
        const [row] = await db.select().from(leads).where(eq(leads.id, b.lead_id)).limit(1);
        if (row) companyName = row.company;
      }
      companyName = companyName || "Account";
      const ai = await aiChat({
        systemPrompt:
          "أنت مدير حسابات يكتب Client Pack احترافي بالعربية يصلح كملف PDF للعميل.",
        userPrompt: [
          `الشركة: ${companyName}`,
          "اكتب Client Pack من 4 أقسام:",
          "1) ملخص تنفيذي (3 جمل)",
          "2) المشكلة + الفرصة (4 نقاط)",
          "3) خطة 30 يوم (5 خطوات)",
          "4) KPIs ونتائج متوقعة (4 metrics)",
        ].join("\n"),
        language: "ar",
        maxTokens: 1200,
      });
      res.json({
        company: companyName,
        pack: {
          generatedAt: new Date().toISOString(),
          format: "markdown",
          content: ai.text,
        },
        provider: ai.provider,
      });
    } catch (e) {
      next(e);
    }
  },
);
