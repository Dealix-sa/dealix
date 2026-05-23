import { Router } from "express";
import { z } from "zod";
import { desc, eq, sql } from "drizzle-orm";
import { getDb, workers, type NewWorker } from "@workspace/db";
import { listAuditLog, getAuditLogForApproval } from "../../lib/auditLog.js";
import { requireInternalToken } from "../../middleware/internalAuth.js";
import { validateBody } from "../../middleware/validate.js";
import { env } from "../../env.js";
import { notFound } from "../../lib/errors.js";

export const internalRouter = Router();
internalRouter.use(requireInternalToken);

internalRouter.get("/audit", async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(String(req.query.limit ?? 100), 10) || 100, 1000);
    const rows = await listAuditLog(limit);
    res.json({
      entries: rows.map((r) => ({
        id: r.id,
        approvalId: r.approvalId,
        actor: r.actor,
        decision: r.decision,
        policyResult: r.policyResult,
        externalActionAllowed: r.externalActionAllowed,
        riskLevel: r.riskLevel,
        evidence: r.evidence,
        reason: r.reason,
        ipAddress: r.ipAddress,
        userAgent: r.userAgent,
        createdAt: r.createdAt.toISOString(),
      })),
      total: rows.length,
    });
  } catch (e) {
    next(e);
  }
});

internalRouter.get("/audit/approval/:approvalId", async (req, res, next) => {
  try {
    const rows = await getAuditLogForApproval(req.params.approvalId);
    res.json({ entries: rows, total: rows.length });
  } catch (e) {
    next(e);
  }
});

internalRouter.get("/workers/health", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db.select().from(workers).orderBy(desc(workers.updatedAt));
    const now = Date.now();
    const staleMs = env.WORKER_STALE_MINUTES * 60_000;
    const enriched = rows.map((w) => {
      const isStale =
        w.lastRunAt && now - w.lastRunAt.getTime() > staleMs && w.status === "running";
      return {
        id: w.id,
        name: w.name,
        type: w.type,
        status: isStale ? "stale" : w.status,
        lastRunAt: w.lastRunAt?.toISOString() || null,
        lastSuccessAt: w.lastSuccessAt?.toISOString() || null,
        lastErrorAt: w.lastErrorAt?.toISOString() || null,
        lastError: w.lastError,
        runCount: w.runCount,
        successCount: w.successCount,
        failureCount: w.failureCount,
        successRate:
          w.runCount > 0 ? Math.round((w.successCount / w.runCount) * 100) : 100,
        minutesSinceLastRun: w.lastRunAt
          ? Math.round((now - w.lastRunAt.getTime()) / 60_000)
          : null,
      };
    });
    res.json({
      workers: enriched,
      total: enriched.length,
      stale: enriched.filter((w) => w.status === "stale").length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const heartbeatSchema = z.object({
  status: z.enum(["idle", "running", "completed", "failed"]).optional(),
  success: z.boolean().optional(),
  error: z.string().optional(),
  metadata: z.record(z.unknown()).optional(),
});

internalRouter.post(
  "/workers/:name/heartbeat",
  validateBody(heartbeatSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof heartbeatSchema>;
      const db = getDb();
      const [existing] = await db
        .select()
        .from(workers)
        .where(eq(workers.name, String(req.params.name)))
        .limit(1);
      if (!existing) {
        const newW: NewWorker = {
          name: String(req.params.name),
          type: "agent",
          status: b.status || "idle",
          lastRunAt: new Date(),
          lastSuccessAt: b.success ? new Date() : null,
          lastErrorAt: b.error ? new Date() : null,
          lastError: b.error || null,
          runCount: 1,
          successCount: b.success ? 1 : 0,
          failureCount: b.error ? 1 : 0,
          metadata: b.metadata || {},
        };
        const [created] = await db.insert(workers).values(newW).returning();
        return res.status(201).json({ worker: created });
      }
      const updateSet: Record<string, unknown> = {
        status: b.status || existing.status,
        lastRunAt: new Date(),
        lastError: b.error ?? existing.lastError,
        metadata: b.metadata || existing.metadata,
        updatedAt: new Date(),
        runCount: sql`${workers.runCount} + 1`,
      };
      if (b.success) {
        updateSet.lastSuccessAt = new Date();
        updateSet.successCount = sql`${workers.successCount} + 1`;
      }
      if (b.error) {
        updateSet.lastErrorAt = new Date();
        updateSet.failureCount = sql`${workers.failureCount} + 1`;
      }
      const [updated] = await db
        .update(workers)
        .set(updateSet)
        .where(eq(workers.id, existing.id))
        .returning();
      res.json({ worker: updated });
    } catch (e) {
      next(e);
    }
  },
);

internalRouter.get("/status", (_req, res) => {
  res.json({
    service: "dealix-internal-trust-layer",
    version: "5.0.0",
    timestamp: new Date().toISOString(),
    config: {
      internalTokenConfigured: Boolean(env.DEALIX_INTERNAL_TOKEN),
      adminKeyConfigured: Boolean(env.DEALIX_ADMIN_API_KEY),
      aiProviderConfigured: Boolean(env.OPENAI_API_KEY || env.ANTHROPIC_API_KEY),
      workerStaleMinutes: env.WORKER_STALE_MINUTES,
    },
  });
});
