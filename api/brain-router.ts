import { z } from "zod";
import { count, desc, eq } from "drizzle-orm";
import { createRouter, publicQuery } from "./middleware";
import { getDb } from "./queries/connection";
import {
  assumptionsLog,
  companySignals,
  decisionsLog,
  experimentsLog,
  opportunityRegister,
  riskRegister,
} from "@db/schema";

const signalTypeSchema = z.enum([
  "revenue",
  "pain",
  "opportunity",
  "risk",
  "market",
  "competitor",
  "bottleneck",
]);

const decisionStatusSchema = z.enum([
  "pending",
  "in_progress",
  "completed",
  "cancelled",
  "deferred",
]);

const assumptionImpactSchema = z.enum(["high", "medium", "low"]);
const opportunityEffortSchema = z.enum(["low", "medium", "high"]);

export const brainRouter = createRouter({
  signalList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(companySignals)
      .orderBy(desc(companySignals.createdAt))
      .limit(100);
  }),

  signalByType: publicQuery.query(async () => {
    const db = getDb();
    const types = [
      "revenue",
      "pain",
      "opportunity",
      "risk",
      "bottleneck",
    ] as const;

    const results = await Promise.all(
      types.map(async (signalType) => {
        const rows = await db
          .select({ count: count() })
          .from(companySignals)
          .where(eq(companySignals.signalType, signalType));

        return [signalType, rows[0]?.count ?? 0] as const;
      }),
    );

    return Object.fromEntries(results);
  }),

  signalCreate: publicQuery
    .input(
      z.object({
        signalType: signalTypeSchema,
        source: z.string().optional(),
        description: z.string().min(3),
        strength: z.number().int().min(1).max(10).default(5),
        confidence: z.number().min(0).max(1).default(0.5),
      }),
    )
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(companySignals).values({
        signalType: input.signalType,
        source: input.source,
        description: input.description,
        strength: input.strength,
        confidence: input.confidence.toFixed(2),
      });
      return { success: true, id: Number(result[0].insertId) };
    }),

  decisionList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(decisionsLog)
      .orderBy(desc(decisionsLog.createdAt))
      .limit(100);
  }),

  decisionCreate: publicQuery
    .input(
      z.object({
        decision: z.string().min(3),
        owner: z.string().min(2),
        metric: z.string().optional(),
        assumption: z.string().optional(),
        nextAction: z.string().min(3),
        priority: z.number().int().min(1).max(10).default(5),
        status: decisionStatusSchema.default("pending"),
        dueDate: z.string().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(decisionsLog).values({
        decision: input.decision,
        owner: input.owner,
        metric: input.metric,
        assumption: input.assumption,
        nextAction: input.nextAction,
        priority: input.priority,
        status: input.status,
        dueDate: input.dueDate,
      });
      return { success: true, id: Number(result[0].insertId) };
    }),

  decisionStats: publicQuery.query(async () => {
    const db = getDb();
    const statuses = ["pending", "in_progress", "completed"] as const;

    const results = await Promise.all(
      statuses.map(async (status) => {
        const rows = await db
          .select({ count: count() })
          .from(decisionsLog)
          .where(eq(decisionsLog.status, status));
        return [status, rows[0]?.count ?? 0] as const;
      }),
    );

    const mapped = Object.fromEntries(results);
    return {
      pending: mapped.pending ?? 0,
      inProgress: mapped.in_progress ?? 0,
      completed: mapped.completed ?? 0,
      total:
        (mapped.pending ?? 0) +
        (mapped.in_progress ?? 0) +
        (mapped.completed ?? 0),
    };
  }),

  assumptionList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(assumptionsLog)
      .orderBy(desc(assumptionsLog.createdAt))
      .limit(100);
  }),

  assumptionCreate: publicQuery
    .input(
      z.object({
        assumption: z.string().min(3),
        source: z.string().optional(),
        impact: assumptionImpactSchema.default("medium"),
      }),
    )
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(assumptionsLog).values({
        assumption: input.assumption,
        source: input.source,
        impact: input.impact,
      });
      return { success: true, id: Number(result[0].insertId) };
    }),

  riskList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(riskRegister)
      .orderBy(desc(riskRegister.severity))
      .limit(100);
  }),

  riskCreate: publicQuery
    .input(
      z.object({
        risk: z.string().min(3),
        probability: z.number().int().min(1).max(5).default(3),
        impact: z.number().int().min(1).max(5).default(3),
        mitigation: z.string().optional(),
        owner: z.string().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const db = getDb();
      const severity = input.probability * input.impact;
      const result = await db.insert(riskRegister).values({
        risk: input.risk,
        probability: input.probability,
        impact: input.impact,
        severity,
        mitigation: input.mitigation,
        owner: input.owner,
      });
      return { success: true, id: Number(result[0].insertId) };
    }),

  opportunityList: publicQuery.query(async () => {
    const db = getDb();
    return db
      .select()
      .from(opportunityRegister)
      .orderBy(desc(opportunityRegister.priority))
      .limit(100);
  }),

  opportunityCreate: publicQuery
    .input(
      z.object({
        opportunity: z.string().min(3),
        potentialValue: z.string().default("0"),
        confidence: z.number().min(0).max(1).default(0.5),
        effort: opportunityEffortSchema.default("medium"),
        owner: z.string().optional(),
      }),
    )
    .mutation(async ({ input }) => {
      const db = getDb();
      const result = await db.insert(opportunityRegister).values({
        opportunity: input.opportunity,
        potentialValue: input.potentialValue,
        confidence: input.confidence.toFixed(2),
        effort: input.effort,
        owner: input.owner,
      });
      return { success: true, id: Number(result[0].insertId) };
    }),

  dashboardStats: publicQuery.query(async () => {
    const db = getDb();
    const [signals, decisions, activeRisks, opportunities, experiments] =
      await Promise.all([
        db.select({ count: count() }).from(companySignals),
        db.select({ count: count() }).from(decisionsLog),
        db
          .select({ count: count() })
          .from(riskRegister)
          .where(eq(riskRegister.status, "active")),
        db.select({ count: count() }).from(opportunityRegister),
        db.select({ count: count() }).from(experimentsLog),
      ]);

    return {
      signals: signals[0]?.count ?? 0,
      decisions: decisions[0]?.count ?? 0,
      activeRisks: activeRisks[0]?.count ?? 0,
      opportunities: opportunities[0]?.count ?? 0,
      experiments: experiments[0]?.count ?? 0,
    };
  }),
});