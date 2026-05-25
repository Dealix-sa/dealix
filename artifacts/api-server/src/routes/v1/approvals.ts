import { Router } from "express";
import { z } from "zod";
import { eq, desc } from "drizzle-orm";
import { getDb, approvals } from "@workspace/db";
import { evaluatePolicy } from "../../lib/policyEvaluator.js";
import { writeAuditLog } from "../../lib/auditLog.js";
import { validateBody } from "../../middleware/validate.js";
import { notFound, badRequest } from "../../lib/errors.js";

export const approvalsRouter = Router();

function toApi(a: typeof approvals.$inferSelect) {
  return {
    id: a.id,
    agentType: a.agentType,
    action: a.action,
    description: a.description,
    target: a.target,
    riskLevel: a.riskLevel,
    policyClass: a.policyClass,
    status: a.status,
    estimatedImpact: a.estimatedImpact,
    metadata: a.metadata,
    requestedAt: a.requestedAt.toISOString(),
    reviewedAt: a.reviewedAt?.toISOString(),
    reviewedBy: a.reviewedBy,
    rejectionReason: a.rejectionReason,
  };
}

approvalsRouter.get("/pending", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db
      .select()
      .from(approvals)
      .where(eq(approvals.status, "pending"))
      .orderBy(desc(approvals.requestedAt))
      .limit(200);
    res.json({ approvals: rows.map(toApi), total: rows.length });
  } catch (e) {
    next(e);
  }
});

approvalsRouter.get("/history", async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(String(req.query.limit ?? 50), 10) || 50, 500);
    const db = getDb();
    const rows = await db
      .select()
      .from(approvals)
      .orderBy(desc(approvals.requestedAt))
      .limit(limit);
    res.json({ approvals: rows.map(toApi), total: rows.length });
  } catch (e) {
    next(e);
  }
});

approvalsRouter.get("/:id", async (req, res, next) => {
  try {
    const db = getDb();
    const [row] = await db
      .select()
      .from(approvals)
      .where(eq(approvals.id, String(req.params.id)))
      .limit(1);
    if (!row) throw notFound("Approval not found");
    res.json(toApi(row));
  } catch (e) {
    next(e);
  }
});

const approveSchema = z.object({
  who: z.string().min(1),
  reason: z.string().optional(),
});

approvalsRouter.post(
  "/:id/approve",
  validateBody(approveSchema),
  async (req, res, next) => {
    try {
      const db = getDb();
      const [row] = await db
        .select()
        .from(approvals)
        .where(eq(approvals.id, String(req.params.id)))
        .limit(1);
      if (!row) throw notFound("Approval not found");
      if (row.status !== "pending") {
        throw badRequest(`Approval already ${row.status}`);
      }
      const decision = evaluatePolicy({
        agentType: row.agentType,
        action: row.action,
        riskLevel: row.riskLevel,
        target: row.target,
        policyClass: row.policyClass,
        metadata: row.metadata,
      });
      const { who, reason } = req.body as z.infer<typeof approveSchema>;
      const [updated] = await db
        .update(approvals)
        .set({
          status: decision.policyClass === "A3" ? "blocked" : "approved",
          reviewedAt: new Date(),
          reviewedBy: who,
          policyClass: decision.policyClass,
          updatedAt: new Date(),
        })
        .where(eq(approvals.id, row.id))
        .returning();
      await writeAuditLog({
        approvalId: row.id,
        actor: who,
        decision: decision.policyClass === "A3" ? "blocked" : "approve",
        policyResult: decision as unknown as Record<string, unknown>,
        externalActionAllowed: decision.external_action_allowed,
        riskLevel: decision.riskLevel,
        evidence: { source: "founder_console", reason: reason || null },
        ipAddress: req.ip || null,
        userAgent: req.headers["user-agent"] || null,
        reason: reason || null,
      });
      res.json({
        approval: toApi(updated!),
        policy: decision,
        external_action_allowed: decision.external_action_allowed,
      });
    } catch (e) {
      next(e);
    }
  },
);

const rejectSchema = z.object({
  who: z.string().min(1),
  reason: z.string().min(1),
});

approvalsRouter.post(
  "/:id/reject",
  validateBody(rejectSchema),
  async (req, res, next) => {
    try {
      const db = getDb();
      const [row] = await db
        .select()
        .from(approvals)
        .where(eq(approvals.id, String(req.params.id)))
        .limit(1);
      if (!row) throw notFound("Approval not found");
      if (row.status !== "pending") {
        throw badRequest(`Approval already ${row.status}`);
      }
      const { who, reason } = req.body as z.infer<typeof rejectSchema>;
      const [updated] = await db
        .update(approvals)
        .set({
          status: "rejected",
          reviewedAt: new Date(),
          reviewedBy: who,
          rejectionReason: reason,
          updatedAt: new Date(),
        })
        .where(eq(approvals.id, row.id))
        .returning();
      await writeAuditLog({
        approvalId: row.id,
        actor: who,
        decision: "reject",
        policyResult: { reason },
        externalActionAllowed: false,
        riskLevel: row.riskLevel as "low" | "medium" | "high",
        evidence: { source: "founder_console", reason },
        ipAddress: req.ip || null,
        userAgent: req.headers["user-agent"] || null,
        reason,
      });
      res.json({ approval: toApi(updated!) });
    } catch (e) {
      next(e);
    }
  },
);

const editSchema = z.object({
  who: z.string().min(1),
  notes: z.string().min(1),
});

approvalsRouter.post(
  "/:id/request-edit",
  validateBody(editSchema),
  async (req, res, next) => {
    try {
      const db = getDb();
      const [row] = await db
        .select()
        .from(approvals)
        .where(eq(approvals.id, String(req.params.id)))
        .limit(1);
      if (!row) throw notFound("Approval not found");
      const { who, notes } = req.body as z.infer<typeof editSchema>;
      await writeAuditLog({
        approvalId: row.id,
        actor: who,
        decision: "request_edit",
        policyResult: { notes },
        externalActionAllowed: false,
        riskLevel: row.riskLevel as "low" | "medium" | "high",
        evidence: { source: "founder_console", notes },
        ipAddress: req.ip || null,
        userAgent: req.headers["user-agent"] || null,
        reason: notes,
      });
      res.json({ ok: true, approvalId: row.id });
    } catch (e) {
      next(e);
    }
  },
);
