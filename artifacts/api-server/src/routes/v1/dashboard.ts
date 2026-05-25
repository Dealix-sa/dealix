import { Router } from "express";
import { sql, eq, gte } from "drizzle-orm";
import { getDb, leads, deals, approvals } from "@workspace/db";

export const dashboardRouter = Router();

dashboardRouter.get("/metrics", async (_req, res, next) => {
  try {
    const db = getDb();
    const since30 = new Date(Date.now() - 30 * 24 * 3600 * 1000);
    const sincePrev30 = new Date(Date.now() - 60 * 24 * 3600 * 1000);

    const [leadStats] = await db
      .select({
        total: sql<number>`count(*)::int`,
        new30: sql<number>`count(*) filter (where ${leads.createdAt} >= ${since30})::int`,
        prev30: sql<number>`count(*) filter (where ${leads.createdAt} >= ${sincePrev30} and ${leads.createdAt} < ${since30})::int`,
        avgScore: sql<number>`coalesce(avg(${leads.aiScore}),0)::int`,
      })
      .from(leads);

    const [dealStats] = await db
      .select({
        total: sql<number>`count(*)::int`,
        wonValue: sql<number>`coalesce(sum(${deals.value}) filter (where ${deals.stage} = 'closed_won'),0)`,
        wonValuePrev: sql<number>`coalesce(sum(${deals.value}) filter (where ${deals.stage} = 'closed_won' and ${deals.updatedAt} < ${since30}),0)`,
        openCount: sql<number>`count(*) filter (where ${deals.stage} not in ('closed_won','closed_lost'))::int`,
        wonCount: sql<number>`count(*) filter (where ${deals.stage} = 'closed_won')::int`,
        lostCount: sql<number>`count(*) filter (where ${deals.stage} = 'closed_lost')::int`,
        avgProbability: sql<number>`coalesce(avg(${deals.probability}) filter (where ${deals.stage} not in ('closed_won','closed_lost')),0)::int`,
      })
      .from(deals);

    const [approvalStats] = await db
      .select({
        pending: sql<number>`count(*) filter (where ${approvals.status} = 'pending')::int`,
        approved30: sql<number>`count(*) filter (where ${approvals.status} = 'approved' and ${approvals.reviewedAt} >= ${since30})::int`,
      })
      .from(approvals);

    const wonValue = Number(dealStats?.wonValue || 0);
    const wonValuePrev = Number(dealStats?.wonValuePrev || 0);
    const revenueChange =
      wonValuePrev > 0
        ? Math.round(((wonValue - wonValuePrev) / wonValuePrev) * 100)
        : wonValue > 0
          ? 100
          : 0;

    const won = dealStats?.wonCount || 0;
    const lost = dealStats?.lostCount || 0;
    const conversion = won + lost > 0 ? Math.round((won / (won + lost)) * 100) : 0;

    const leadChange =
      (leadStats?.prev30 ?? 0) > 0
        ? Math.round((((leadStats?.new30 ?? 0) - (leadStats?.prev30 ?? 0)) / (leadStats?.prev30 ?? 1)) * 100)
        : (leadStats?.new30 ?? 0) > 0 ? 100 : 0;

    res.json({
      generatedAt: new Date().toISOString(),
      currency: "SAR",
      kpis: [
        {
          label: "إيرادات الشهر",
          value: wonValue,
          change: revenueChange,
          trend: revenueChange >= 0 ? "up" : "down",
          icon: "dollar-sign",
          format: "currency",
        },
        {
          label: "صفقات نشطة",
          value: dealStats?.openCount || 0,
          change: 0,
          trend: "neutral",
          icon: "briefcase",
          format: "number",
        },
        {
          label: "Leads جدد (30 يوم)",
          value: leadStats?.new30 || 0,
          change: leadChange,
          trend: leadChange >= 0 ? "up" : "down",
          icon: "users",
          format: "number",
        },
        {
          label: "معدل التحويل",
          value: conversion,
          change: 0,
          trend: "neutral",
          icon: "trending-up",
          format: "percentage",
        },
        {
          label: "متوسط AI Score",
          value: leadStats?.avgScore || 0,
          change: 0,
          trend: "neutral",
          icon: "brain",
          format: "number",
        },
        {
          label: "Approvals معلّقة",
          value: approvalStats?.pending || 0,
          change: 0,
          trend: "neutral",
          icon: "shield",
          format: "number",
        },
      ],
      summary: {
        revenueMonth: wonValue,
        revenueMonthPrev: wonValuePrev,
        revenueChange,
        dealsActive: dealStats?.openCount || 0,
        dealsWon: won,
        dealsLost: lost,
        conversionRate: conversion,
        leadsTotal: leadStats?.total || 0,
        leadsNew30: leadStats?.new30 || 0,
        approvalsPending: approvalStats?.pending || 0,
        approvalsApproved30: approvalStats?.approved30 || 0,
        avgPipelineProbability: dealStats?.avgProbability || 0,
        avgLeadScore: leadStats?.avgScore || 0,
      },
    });
  } catch (e) {
    next(e);
  }
});

dashboardRouter.get("/revenue-series", async (_req, res, next) => {
  try {
    const db = getDb();
    const months = 6;
    const rows = await db
      .select({
        month: sql<string>`to_char(date_trunc('month', ${deals.updatedAt}), 'YYYY-MM')`,
        revenue: sql<number>`coalesce(sum(${deals.value}) filter (where ${deals.stage} = 'closed_won'), 0)`,
        dealsCount: sql<number>`count(*) filter (where ${deals.stage} = 'closed_won')::int`,
      })
      .from(deals)
      .where(gte(deals.updatedAt, new Date(Date.now() - months * 31 * 24 * 3600 * 1000)))
      .groupBy(sql`date_trunc('month', ${deals.updatedAt})`)
      .orderBy(sql`date_trunc('month', ${deals.updatedAt})`);

    res.json({
      series: rows.map((r) => ({
        month: r.month,
        revenue: Number(r.revenue),
        target: Math.round(Number(r.revenue) * 1.2),
        deals: r.dealsCount,
      })),
    });
  } catch (e) {
    next(e);
  }
});
