import { Router } from "express";
import { z } from "zod";
import { and, desc, eq, gte, inArray, sql, lt, or, isNull } from "drizzle-orm";
import { getDb, leads } from "@workspace/db";
import { validateBody } from "../../../middleware/validate.js";
import { requireAdminKey } from "../../../middleware/requireAdminKey.js";
import { scoreLead } from "../../../lib/scoring.js";
import { aiChat } from "../../../lib/ai.js";
import { notFound } from "../../../lib/errors.js";

export const warRoomRouter = Router();
warRoomRouter.use(requireAdminKey);

function toApi(l: typeof leads.$inferSelect) {
  return {
    id: l.id,
    company: l.company,
    contactName: l.contactName,
    contactEmail: l.contactEmail,
    contactPhone: l.contactPhone,
    industry: l.industry,
    city: l.city,
    stage: l.stage,
    status: l.status,
    priority: l.priority,
    aiScore: l.aiScore,
    engagementScore: l.engagementScore,
    estimatedValue: Number(l.estimatedValue),
    currency: l.currency,
    notes: l.notes,
    tags: l.tags,
    source: l.source,
    lastContactedAt: l.lastContactedAt?.toISOString() || null,
    nextFollowUpAt: l.nextFollowUpAt?.toISOString() || null,
    createdAt: l.createdAt.toISOString(),
    updatedAt: l.updatedAt.toISOString(),
  };
}

warRoomRouter.get("/", async (req, res, next) => {
  try {
    const db = getDb();
    const dueToday = req.query.due_today === "true" || req.query.due_today === "1";
    const needsFollowUp =
      req.query.needs_follow_up === "true" || req.query.needs_follow_up === "1";
    const topN = Math.min(parseInt(String(req.query.top_n ?? 50), 10) || 50, 500);
    const statusIn = req.query.status_in
      ? String(req.query.status_in).split(",").map((s) => s.trim()).filter(Boolean)
      : null;

    const conds = [] as ReturnType<typeof eq>[];
    if (dueToday) {
      conds.push(
        and(
          gte(leads.nextFollowUpAt, new Date(new Date().setHours(0, 0, 0, 0))),
          lt(leads.nextFollowUpAt, new Date(new Date().setHours(23, 59, 59, 999))),
        )!,
      );
    }
    if (needsFollowUp) {
      conds.push(
        or(
          lt(leads.nextFollowUpAt, new Date()),
          isNull(leads.nextFollowUpAt),
        )!,
      );
    }
    if (statusIn && statusIn.length) {
      conds.push(inArray(leads.status, statusIn));
    }

    const rows = conds.length
      ? await db
          .select()
          .from(leads)
          .where(and(...conds))
          .orderBy(desc(leads.aiScore))
          .limit(topN)
      : await db
          .select()
          .from(leads)
          .orderBy(desc(leads.aiScore))
          .limit(topN);

    res.json({
      targets: rows.map(toApi),
      total: rows.length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

warRoomRouter.get("/summary", async (_req, res, next) => {
  try {
    const db = getDb();
    const [s] = await db
      .select({
        total: sql<number>`count(*)::int`,
        p0: sql<number>`count(*) filter (where ${leads.priority} = 'p0')::int`,
        dueToday: sql<number>`count(*) filter (
          where ${leads.nextFollowUpAt} >= date_trunc('day', now())
            and ${leads.nextFollowUpAt} < date_trunc('day', now()) + interval '1 day'
        )::int`,
        overdue: sql<number>`count(*) filter (where ${leads.nextFollowUpAt} < now())::int`,
        avgScore: sql<number>`coalesce(avg(${leads.aiScore}),0)::int`,
      })
      .from(leads);
    res.json({
      summary: {
        totalTargets: s?.total || 0,
        p0Targets: s?.p0 || 0,
        dueToday: s?.dueToday || 0,
        overdue: s?.overdue || 0,
        avgAiScore: s?.avgScore || 0,
      },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

warRoomRouter.get("/today-pack", async (_req, res, next) => {
  try {
    const db = getDb();
    const today = await db
      .select()
      .from(leads)
      .where(
        or(
          and(
            gte(leads.nextFollowUpAt, new Date(new Date().setHours(0, 0, 0, 0))),
            lt(leads.nextFollowUpAt, new Date(new Date().setHours(23, 59, 59, 999))),
          ),
          eq(leads.priority, "p0"),
        )!,
      )
      .orderBy(desc(leads.aiScore))
      .limit(20);
    res.json({
      pack: {
        date: new Date().toISOString().slice(0, 10),
        targets: today.map(toApi),
        recommendations: [
          "ابدأ بأعلى 3 AI score",
          "أرسل warm intro لـ p0 قبل الظهر",
          "قبل الإغلاق: حدّث nextFollowUpAt لكل lead متّصل به اليوم",
        ],
      },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const newTargetSchema = z.object({
  company: z.string().min(1),
  contactName: z.string().optional(),
  contactEmail: z.string().email().optional(),
  contactPhone: z.string().optional(),
  industry: z.string().optional(),
  city: z.string().optional(),
  estimatedValue: z.number().optional(),
  priority: z.enum(["p0", "p1", "p2"]).optional(),
  notes: z.string().optional(),
  tags: z.array(z.string()).optional(),
});

warRoomRouter.post("/", validateBody(newTargetSchema), async (req, res, next) => {
  try {
    const b = req.body as z.infer<typeof newTargetSchema>;
    const aiScore = scoreLead({
      estimatedValue: b.estimatedValue,
      industry: b.industry,
      contactEmail: b.contactEmail,
      contactPhone: b.contactPhone,
      notes: b.notes,
    });
    const db = getDb();
    const [created] = await db
      .insert(leads)
      .values({
        company: b.company,
        contactName: b.contactName || null,
        contactEmail: b.contactEmail || null,
        contactPhone: b.contactPhone || null,
        industry: b.industry || null,
        city: b.city || null,
        estimatedValue: b.estimatedValue ? String(b.estimatedValue) : "0",
        priority: b.priority || "p1",
        notes: b.notes || null,
        tags: b.tags || [],
        aiScore,
        source: "war_room",
      })
      .returning();
    res.status(201).json({ target: toApi(created!) });
  } catch (e) {
    next(e);
  }
});

const patchSchema = z.object({
  stage: z.string().optional(),
  status: z.string().optional(),
  priority: z.enum(["p0", "p1", "p2"]).optional(),
  notes: z.string().optional(),
  nextFollowUpAt: z.string().optional(),
  tags: z.array(z.string()).optional(),
  engagementScore: z.number().min(0).max(100).optional(),
});

warRoomRouter.patch("/:id", validateBody(patchSchema), async (req, res, next) => {
  try {
    const b = req.body as z.infer<typeof patchSchema>;
    const db = getDb();
    const [existing] = await db
      .select()
      .from(leads)
      .where(eq(leads.id, String(req.params.id)))
      .limit(1);
    if (!existing) throw notFound("Lead not found");
    const next: Partial<typeof leads.$inferInsert> = {
      stage: b.stage ?? existing.stage,
      status: b.status ?? existing.status,
      priority: b.priority ?? existing.priority,
      notes: b.notes ?? existing.notes,
      tags: b.tags ?? existing.tags,
      engagementScore: b.engagementScore ?? existing.engagementScore,
      nextFollowUpAt: b.nextFollowUpAt
        ? new Date(b.nextFollowUpAt)
        : existing.nextFollowUpAt,
      updatedAt: new Date(),
    };
    if (b.engagementScore != null) {
      next.aiScore = scoreLead({
        estimatedValue: existing.estimatedValue,
        industry: existing.industry,
        contactEmail: existing.contactEmail,
        contactPhone: existing.contactPhone,
        notes: next.notes,
        engagementScore: b.engagementScore,
      });
    }
    const [updated] = await db
      .update(leads)
      .set(next)
      .where(eq(leads.id, String(req.params.id)))
      .returning();
    res.json({ target: toApi(updated!) });
  } catch (e) {
    next(e);
  }
});

warRoomRouter.post("/:id/generate-outreach", async (req, res, next) => {
  try {
    const db = getDb();
    const [row] = await db.select().from(leads).where(eq(leads.id, String(req.params.id))).limit(1);
    if (!row) throw notFound("Lead not found");
    const userPrompt = [
      `الشركة: ${row.company}`,
      `جهة الاتصال: ${row.contactName || "(غير معروف)"}`,
      `القطاع: ${row.industry || "(غير محدد)"}`,
      `الملاحظات: ${row.notes || "(لا توجد)"}`,
      `القيمة المقدرة: ${row.estimatedValue} ${row.currency}`,
      "",
      "اكتب رسالة outreach باللغة العربية (3-5 جمل) تربط فائدة Dealix بهدف تجاري واضح للشركة. أنهِ بـ CTA واحد لحجز discovery call 25 دقيقة.",
    ].join("\n");
    const result = await aiChat({
      systemPrompt:
        "أنت محرر مبيعات سعودي محترف يكتب باللغة العربية الفصحى بأسلوب احترافي ومهذب.",
      userPrompt,
      language: "ar",
      temperature: 0.6,
      maxTokens: 500,
    });
    res.json({
      leadId: row.id,
      draft: result.text,
      provider: result.provider,
      model: result.model,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const importSchema = z.object({
  csv_text: z.string().min(1),
});

warRoomRouter.post(
  "/import-targets",
  validateBody(importSchema),
  async (req, res, next) => {
    try {
      const csv = (req.body as z.infer<typeof importSchema>).csv_text;
      const rows = parseCsv(csv);
      const db = getDb();
      const inserted: string[] = [];
      for (const r of rows) {
        if (!r.company) continue;
        const aiScore = scoreLead({
          estimatedValue: r.estimatedValue,
          industry: r.industry,
          contactEmail: r.contactEmail,
          contactPhone: r.contactPhone,
          notes: r.notes,
        });
        const [c] = await db
          .insert(leads)
          .values({
            company: r.company,
            contactName: r.contactName || null,
            contactEmail: r.contactEmail || null,
            contactPhone: r.contactPhone || null,
            industry: r.industry || null,
            city: r.city || null,
            estimatedValue: r.estimatedValue ? String(r.estimatedValue) : "0",
            notes: r.notes || null,
            priority: (r.priority as "p0" | "p1" | "p2") || "p1",
            aiScore,
            source: "csv_import",
          })
          .returning({ id: leads.id });
        if (c) inserted.push(c.id);
      }
      res.json({ inserted: inserted.length, ids: inserted });
    } catch (e) {
      next(e);
    }
  },
);

function parseCsv(text: string): Array<{
  company?: string;
  contactName?: string;
  contactEmail?: string;
  contactPhone?: string;
  industry?: string;
  city?: string;
  estimatedValue?: number;
  notes?: string;
  priority?: string;
}> {
  const lines = text.split(/\r?\n/).filter((l) => l.trim());
  if (!lines.length) return [];
  const header = lines[0]!.split(",").map((h) => h.trim().toLowerCase());
  const map: Record<string, string> = {
    company: "company",
    name: "contactName",
    contact: "contactName",
    "contact_name": "contactName",
    email: "contactEmail",
    "contact_email": "contactEmail",
    phone: "contactPhone",
    "contact_phone": "contactPhone",
    industry: "industry",
    sector: "industry",
    city: "city",
    value: "estimatedValue",
    "estimated_value": "estimatedValue",
    notes: "notes",
    priority: "priority",
  };
  return lines.slice(1).map((line) => {
    const cells = line.split(",").map((c) => c.trim());
    const row: Record<string, string | number> = {};
    header.forEach((h, i) => {
      const key = map[h];
      if (!key) return;
      const v = cells[i] ?? "";
      if (key === "estimatedValue") row[key] = parseFloat(v) || 0;
      else row[key] = v;
    });
    return row as { company?: string };
  });
}
