import { Router } from "express";
import { z } from "zod";
import { desc, eq } from "drizzle-orm";
import { getDb, supportTickets, knowledgeBase } from "@workspace/db";
import { validateBody } from "../../../middleware/validate.js";
import { requireAdminKey } from "../../../middleware/requireAdminKey.js";
import { aiChat } from "../../../lib/ai.js";
import { notFound, badRequest } from "../../../lib/errors.js";
import { or, ilike } from "drizzle-orm";

export const supportRouter = Router();
export const knowledgeAdminRouter = Router();
export const invoicesRouter = Router();

supportRouter.use(requireAdminKey);
knowledgeAdminRouter.use(requireAdminKey);
invoicesRouter.use(requireAdminKey);

supportRouter.get("/tickets", async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(String(req.query.limit ?? 80), 10) || 80, 500);
    const db = getDb();
    const rows = await db
      .select()
      .from(supportTickets)
      .orderBy(desc(supportTickets.createdAt))
      .limit(limit);
    res.json({
      tickets: rows.map((t) => ({
        id: t.id,
        subject: t.subject,
        body: t.body,
        customerEmail: t.customerEmail,
        customerName: t.customerName,
        company: t.company,
        category: t.category,
        priority: t.priority,
        status: t.status,
        sentiment: t.sentiment,
        aiClassification: t.aiClassification,
        aiDraftResponse: t.aiDraftResponse,
        createdAt: t.createdAt.toISOString(),
      })),
      total: rows.length,
    });
  } catch (e) {
    next(e);
  }
});

supportRouter.post("/tickets/:id/classify", async (req, res, next) => {
  try {
    const db = getDb();
    const [t] = await db
      .select()
      .from(supportTickets)
      .where(eq(supportTickets.id, String(req.params.id)))
      .limit(1);
    if (!t) throw notFound("Ticket not found");
    const txt = `${t.subject}\n${t.body}`.toLowerCase();
    const category = /price|سعر|دفع|invoice/.test(txt)
      ? "billing"
      : /bug|error|crash|خطأ|عطل/.test(txt)
        ? "technical"
        : /cancel|إلغاء|refund/.test(txt)
          ? "churn_risk"
          : /demo|عرض|تجربة/.test(txt)
            ? "sales"
            : "general";
    const priority = /urgent|عاجل|production/.test(txt) ? "urgent" : t.priority;
    const sentiment = /شكراً|excellent|great/.test(txt)
      ? "positive"
      : /angry|frustrated|disappointed/.test(txt)
        ? "negative"
        : "neutral";
    const [updated] = await db
      .update(supportTickets)
      .set({
        category,
        priority,
        sentiment,
        aiClassification: { category, priority, sentiment, classifier: "v1" },
        updatedAt: new Date(),
      })
      .where(eq(supportTickets.id, t.id))
      .returning();
    res.json({ ticket: updated });
  } catch (e) {
    next(e);
  }
});

supportRouter.post("/tickets/:id/draft-response", async (req, res, next) => {
  try {
    const db = getDb();
    const [t] = await db
      .select()
      .from(supportTickets)
      .where(eq(supportTickets.id, String(req.params.id)))
      .limit(1);
    if (!t) throw notFound("Ticket not found");
    const ai = await aiChat({
      systemPrompt:
        "أنت ممثل دعم فني سعودي محترف. تكتب ردود لطيفة وعملية باللغة العربية الفصحى.",
      userPrompt: [
        `موضوع: ${t.subject}`,
        `نص الطلب: ${t.body}`,
        `العميل: ${t.customerName || "العميل"} (${t.company || "—"})`,
        `الفئة: ${t.category}`,
        "",
        "اكتب رداً (3-5 جمل): إقرار + تشخيص + خطوة تالية واضحة + ETA. أنهِ بشكراً.",
      ].join("\n"),
      language: "ar",
      maxTokens: 600,
    });
    const [updated] = await db
      .update(supportTickets)
      .set({
        aiDraftResponse: ai.text,
        updatedAt: new Date(),
      })
      .where(eq(supportTickets.id, t.id))
      .returning();
    res.json({
      ticket: updated,
      draft: ai.text,
      provider: ai.provider,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

knowledgeAdminRouter.get("/search", async (req, res, next) => {
  try {
    const q = String(req.query.q || "").trim();
    if (!q) throw badRequest("Query 'q' required");
    const db = getDb();
    const tokens = q
      .toLowerCase()
      .split(/\s+/)
      .filter((t) => t.length > 1)
      .slice(0, 6);
    const conds = tokens.flatMap((t) => [
      ilike(knowledgeBase.titleAr, `%${t}%`),
      ilike(knowledgeBase.titleEn, `%${t}%`),
      ilike(knowledgeBase.bodyAr, `%${t}%`),
      ilike(knowledgeBase.bodyEn, `%${t}%`),
    ]);
    const rows = conds.length
      ? await db.select().from(knowledgeBase).where(or(...conds)).limit(10)
      : await db.select().from(knowledgeBase).limit(10);
    res.json({
      query: q,
      results: rows.map((r) => ({
        slug: r.slug,
        titleAr: r.titleAr,
        titleEn: r.titleEn,
        category: r.category,
        snippet: r.bodyAr.slice(0, 240),
      })),
      total: rows.length,
    });
  } catch (e) {
    next(e);
  }
});

const invoiceSchema = z.object({
  company: z.string().min(1),
  amount: z.number().min(0),
  currency: z.string().default("SAR"),
  description: z.string().optional(),
  dueInDays: z.number().min(0).max(120).default(14),
});

invoicesRouter.post(
  "/draft",
  validateBody(invoiceSchema),
  (req, res) => {
    const b = req.body as z.infer<typeof invoiceSchema>;
    const number = `INV-${new Date().getFullYear()}-${Math.floor(Math.random() * 90000 + 10000)}`;
    const issueDate = new Date();
    const dueDate = new Date(Date.now() + b.dueInDays * 24 * 3600 * 1000);
    const vat = b.amount * 0.15;
    res.json({
      invoice: {
        number,
        company: b.company,
        amount: b.amount,
        vat,
        total: b.amount + vat,
        currency: b.currency,
        description: b.description || "خدمات Dealix RevOps",
        issueDate: issueDate.toISOString(),
        dueDate: dueDate.toISOString(),
        status: "draft",
        terms: "Net 14 — تحويل بنكي. مع تطبيق VAT 15%.",
      },
    });
  },
);
