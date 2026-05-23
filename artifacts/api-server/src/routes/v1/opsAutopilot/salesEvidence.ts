import { Router } from "express";
import { z } from "zod";
import { desc, eq, sql } from "drizzle-orm";
import { getDb, deals, evidenceEvents, leads } from "@workspace/db";
import { validateBody } from "../../../middleware/validate.js";
import { requireAdminKey } from "../../../middleware/requireAdminKey.js";
import { aiChat } from "../../../lib/ai.js";
import { notFound } from "../../../lib/errors.js";

export const salesRouter = Router();
export const evidenceRouter = Router();
export const founderEvidenceRouter = Router();
export const opsLeadsRouter = Router();

salesRouter.use(requireAdminKey);
evidenceRouter.use(requireAdminKey);
founderEvidenceRouter.use(requireAdminKey);
opsLeadsRouter.use(requireAdminKey);

salesRouter.get("/pipeline", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db.select().from(deals).orderBy(desc(deals.lastActivityAt)).limit(200);
    const byStage = new Map<string, typeof rows>();
    for (const r of rows) {
      const arr = byStage.get(r.stage) || [];
      arr.push(r);
      byStage.set(r.stage, arr);
    }
    res.json({
      stages: Array.from(byStage.entries()).map(([k, v]) => ({
        stage: k,
        count: v.length,
        value: v.reduce((s, d) => s + Number(d.value), 0),
      })),
      deals: rows.map((d) => ({
        id: d.id,
        title: d.title,
        company: d.company,
        value: Number(d.value),
        stage: d.stage,
        aiScore: d.aiScore,
        probability: d.probability,
        lastActivity: d.lastActivityAt.toISOString(),
      })),
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

salesRouter.get("/objections", (_req, res) => {
  res.json({
    objections: [
      { slug: "price", title: "السعر مرتفع", frequency: "high" },
      { slug: "timing", title: "الوقت غير مناسب", frequency: "high" },
      { slug: "authority", title: "أحتاج موافقة الإدارة", frequency: "medium" },
      { slug: "trust", title: "الثقة في spec الجديد", frequency: "medium" },
      { slug: "incumbent", title: "لدينا مزود حالي", frequency: "high" },
    ],
  });
});

evidenceRouter.get("/events", async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(String(req.query.limit ?? 80), 10) || 80, 500);
    const db = getDb();
    const rows = await db
      .select()
      .from(evidenceEvents)
      .orderBy(desc(evidenceEvents.createdAt))
      .limit(limit);
    res.json({
      events: rows.map((e) => ({
        id: e.id,
        eventType: e.eventType,
        company: e.company,
        motion: e.motion,
        offerId: e.offerId,
        notes: e.notes,
        payload: e.payload,
        createdAt: e.createdAt.toISOString(),
      })),
      total: rows.length,
    });
  } catch (e) {
    next(e);
  }
});

const evidenceAppendSchema = z.object({
  event_type: z.string().min(1),
  company: z.string().min(1),
  notes: z.string().optional(),
  motion: z.string().optional(),
  offer_id: z.string().optional(),
});

founderEvidenceRouter.post(
  "/csv-append",
  validateBody(evidenceAppendSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof evidenceAppendSchema>;
      const db = getDb();
      const [created] = await db
        .insert(evidenceEvents)
        .values({
          eventType: b.event_type,
          company: b.company,
          notes: b.notes || null,
          motion: b.motion || null,
          offerId: b.offer_id || null,
          payload: { source: "founder_csv_append" },
        })
        .returning();
      res.status(201).json({ event: created });
    } catch (e) {
      next(e);
    }
  },
);

opsLeadsRouter.get("/", async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(String(req.query.limit ?? 80), 10) || 80, 500);
    const db = getDb();
    const rows = await db.select().from(leads).orderBy(desc(leads.updatedAt)).limit(limit);
    res.json({
      leads: rows.map((l) => ({
        id: l.id,
        company: l.company,
        contactName: l.contactName,
        stage: l.stage,
        status: l.status,
        priority: l.priority,
        aiScore: l.aiScore,
        estimatedValue: Number(l.estimatedValue),
        nextFollowUpAt: l.nextFollowUpAt?.toISOString() || null,
      })),
      total: rows.length,
    });
  } catch (e) {
    next(e);
  }
});

opsLeadsRouter.get("/:id/meeting-brief", async (req, res, next) => {
  try {
    const locale = String(req.query.locale || "ar");
    const db = getDb();
    const [row] = await db.select().from(leads).where(eq(leads.id, String(req.params.id))).limit(1);
    if (!row) throw notFound("Lead not found");
    const result = await aiChat({
      systemPrompt:
        locale === "ar"
          ? "أنت محلل GTM يحضّر brief اجتماع للمؤسس بالعربية الواضحة في 5 نقاط."
          : "You are a GTM analyst preparing a clear 5-point meeting brief for the founder.",
      userPrompt: [
        `Company: ${row.company}`,
        `Contact: ${row.contactName || "(unknown)"}`,
        `Industry: ${row.industry || "(none)"}`,
        `Stage: ${row.stage}`,
        `AI Score: ${row.aiScore}`,
        `Estimated Value: ${row.estimatedValue}`,
        `Notes: ${row.notes || "(none)"}`,
        "",
        "Produce: (1) goal, (2) two specific qualifying questions, (3) one objection to anticipate, (4) one fact to mention, (5) suggested next step.",
      ].join("\n"),
      language: locale === "ar" ? "ar" : "en",
      maxTokens: 500,
    });
    res.json({
      leadId: row.id,
      locale,
      brief: result.text,
      provider: result.provider,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const advanceSchema = z.object({
  notes: z.string().optional(),
  newStage: z.string().optional(),
});

opsLeadsRouter.post(
  "/:id/advance-stage",
  validateBody(advanceSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof advanceSchema>;
      const db = getDb();
      const [row] = await db.select().from(leads).where(eq(leads.id, String(req.params.id))).limit(1);
      if (!row) throw notFound("Lead not found");
      const order = ["lead", "qualified", "proposal", "negotiation", "closed_won"];
      const i = order.indexOf(row.stage);
      const nextStage = b.newStage || order[Math.min(order.length - 1, i + 1)] || row.stage;
      const [updated] = await db
        .update(leads)
        .set({
          stage: nextStage,
          notes: b.notes ? `${row.notes || ""}\n[advance] ${b.notes}` : row.notes,
          updatedAt: new Date(),
        })
        .where(eq(leads.id, row.id))
        .returning();
      const ai = await aiChat({
        systemPrompt:
          "أنت مدير عمليات بيع تقترح الخطوة التالية القابلة للتنفيذ في جملتين بالعربية.",
        userPrompt: `Lead ${row.company} انتقل إلى ${nextStage}. الملاحظات: ${b.notes || ""}. اقترح الخطوة التالية.`,
        language: "ar",
        maxTokens: 200,
      });
      res.json({
        lead: updated,
        nextStep: ai.text,
        provider: ai.provider,
      });
    } catch (e) {
      next(e);
    }
  },
);
