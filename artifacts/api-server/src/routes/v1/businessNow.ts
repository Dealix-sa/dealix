import { Router } from "express";
import { z } from "zod";
import { sql } from "drizzle-orm";
import { getDb, leads, deals, approvals } from "@workspace/db";
import { validateBody } from "../../middleware/validate.js";
import { requireAdminKey } from "../../middleware/requireAdminKey.js";

export const businessNowRouter = Router();

businessNowRouter.get("/snapshot", async (_req, res, next) => {
  try {
    const db = getDb();
    const [leadStats] = await db
      .select({
        total: sql<number>`count(*)::int`,
        p0: sql<number>`count(*) filter (where ${leads.priority} = 'p0')::int`,
        new7: sql<number>`count(*) filter (where ${leads.createdAt} >= now() - interval '7 days')::int`,
      })
      .from(leads);
    const [dealStats] = await db
      .select({
        active: sql<number>`count(*) filter (where ${deals.stage} not in ('closed_won','closed_lost'))::int`,
        pipelineValue: sql<number>`coalesce(sum(${deals.value}) filter (where ${deals.stage} not in ('closed_won','closed_lost')), 0)`,
      })
      .from(deals);
    const [appStats] = await db
      .select({
        pending: sql<number>`count(*) filter (where ${approvals.status} = 'pending')::int`,
      })
      .from(approvals);

    res.json({
      generatedAt: new Date().toISOString(),
      pulse: {
        leadsTotal: leadStats?.total || 0,
        leadsNew7: leadStats?.new7 || 0,
        leadsP0: leadStats?.p0 || 0,
        dealsActive: dealStats?.active || 0,
        pipelineValueSAR: Number(dealStats?.pipelineValue || 0),
        approvalsPending: appStats?.pending || 0,
      },
      focus: [
        "متابعة P0 leads خلال 24 ساعة",
        "إغلاق Approvals المتأخرة قبل نهاية اليوم",
        "Outreach لـ Top 5 accounts معلّقة",
      ],
      flags: [],
    });
  } catch (e) {
    next(e);
  }
});

businessNowRouter.get("/commercial-strategy", (_req, res) => {
  res.json({
    horizon: "Q1 2026",
    motions: [
      {
        id: "warm_intros",
        title: "Warm Introductions",
        description: "9 outreach عبر شركاء سابقين/connectors",
        weeklyTarget: 9,
        priority: "p0",
      },
      {
        id: "abm_top50",
        title: "ABM Top 50",
        description: "حسابات سعودية مستهدفة بـ outreach مخصص",
        weeklyTarget: 25,
        priority: "p0",
      },
      {
        id: "linkedin_content",
        title: "LinkedIn Content",
        description: "3 منشورات/أسبوع لبناء سلطة المؤسس",
        weeklyTarget: 3,
        priority: "p1",
      },
      {
        id: "demos_booked",
        title: "Discovery Demos",
        description: "هدف 5 demos مؤهلة/أسبوع",
        weeklyTarget: 5,
        priority: "p0",
      },
    ],
    targets: {
      mrr: { current: 0, q1: 50_000, currency: "SAR" },
      pipelineValue: { current: 0, q1: 500_000, currency: "SAR" },
      activeClients: { current: 0, q1: 8 },
    },
    riskFactors: [
      "Founder bandwidth — أتمتة المهام المتكررة ضرورية",
      "Pipeline depth — يحتاج 3x الهدف",
      "Cycle length — السوق السعودي 60-90 يوم",
    ],
  });
});

const simulateSchema = z.object({
  weeklyWarmIntros: z.number().min(0).max(50),
  weeklyAbmTouches: z.number().min(0).max(200),
  conversionRate: z.number().min(0).max(1),
  avgDealValue: z.number().min(0),
  cycleDays: z.number().min(1).max(365),
});

businessNowRouter.post(
  "/commercial-strategy/simulate",
  validateBody(simulateSchema),
  (req, res) => {
    const body = req.body as z.infer<typeof simulateSchema>;
    const weeklyTouches = body.weeklyWarmIntros + body.weeklyAbmTouches;
    const monthlyDeals = Math.round(weeklyTouches * 4 * body.conversionRate);
    const monthlyRevenue = monthlyDeals * body.avgDealValue;
    const quarterRevenue = Math.round(monthlyRevenue * 3 * 0.85);
    res.json({
      inputs: body,
      results: {
        weeklyTouches,
        monthlyDeals,
        monthlyRevenue,
        quarterRevenue,
        annualRunRate: monthlyRevenue * 12,
        timeToFirstDeal: `${Math.ceil(body.cycleDays / 30)} months`,
        currency: "SAR",
      },
      sensitivity: {
        ifConversionUp10pct: Math.round(monthlyRevenue * 1.1),
        ifAvgValueUp20pct: Math.round(monthlyRevenue * 1.2),
        ifBothUp: Math.round(monthlyRevenue * 1.32),
      },
    });
  },
);

businessNowRouter.get(
  "/operator-signals",
  requireAdminKey,
  async (_req, res, next) => {
    try {
      const db = getDb();
      const [stats] = await db
        .select({
          leads: sql<number>`count(*)::int`,
          stalePipeline: sql<number>`count(*) filter (where ${leads.nextFollowUpAt} < now())::int`,
        })
        .from(leads);
      res.json({
        signals: [
          {
            id: "follow_up_overdue",
            severity: "warning",
            count: stats?.stalePipeline || 0,
            message: "Leads تحتاج متابعة متأخرة",
          },
          {
            id: "weekly_outreach_target",
            severity: "info",
            count: 9,
            message: "هدف أسبوعي: 9 warm intros",
          },
        ],
        generatedAt: new Date().toISOString(),
      });
    } catch (e) {
      next(e);
    }
  },
);
