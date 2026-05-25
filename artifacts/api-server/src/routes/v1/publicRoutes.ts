import { Router } from "express";
import { z } from "zod";
import { or, ilike } from "drizzle-orm";
import {
  getDb,
  leads,
  knowledgeBase,
  publicLeadSchema,
} from "@workspace/db";
import { validateBody } from "../../middleware/validate.js";
import { scoreLead, scoreRisk } from "../../lib/scoring.js";
import { badRequest } from "../../lib/errors.js";

export const publicRouter = Router();

publicRouter.post(
  "/leads",
  validateBody(publicLeadSchema),
  async (req, res, next) => {
    try {
      const body = req.body as z.infer<typeof publicLeadSchema>;
      const aiScore = scoreLead({
        contactEmail: body.contactEmail,
        contactPhone: body.contactPhone,
        industry: body.industry,
        notes: body.notes,
        source: body.source || "landing",
      });
      const db = getDb();
      const [created] = await db
        .insert(leads)
        .values({
          company: body.company,
          contactName: body.contactName || null,
          contactEmail: body.contactEmail || null,
          contactPhone: body.contactPhone || null,
          industry: body.industry || null,
          city: body.city || null,
          notes: body.notes || null,
          source: body.source || "landing",
          aiScore,
        })
        .returning();
      res.status(201).json({
        ok: true,
        leadId: created!.id,
        aiScore,
        nextStep: aiScore >= 70 ? "founder_call" : "nurture",
      });
    } catch (e) {
      next(e);
    }
  },
);

const riskSchema = z.object({
  industry: z.string().optional(),
  monthlyRevenue: z.number().optional(),
  yearsActive: z.number().optional(),
  hasFinanceTeam: z.boolean().optional(),
  usesCRM: z.boolean().optional(),
  hasSubscriptions: z.boolean().optional(),
});

publicRouter.post(
  "/risk-score",
  validateBody(riskSchema),
  async (req, res, next) => {
    try {
      const result = scoreRisk(req.body as z.infer<typeof riskSchema>);
      res.json({
        ...result,
        recommendations:
          result.level === "high"
            ? [
                "ابدأ بـ Risk Assessment مدفوع قبل أي التزام",
                "اطلب وثائق المراجعة المالية الأخيرة",
                "ضع escrow أو ضمان أداء",
              ]
            : result.level === "medium"
              ? [
                  "Discovery call 45 دقيقة",
                  "اطلب تاريخ تشغيل آخر 12 شهر",
                  "ابدأ بـ pilot صغير محدود النطاق",
                ]
              : [
                  "تابع للمرحلة التالية في pipeline",
                  "ابني proposal كامل",
                  "حدد close date خلال 30 يوم",
                ],
        generatedAt: new Date().toISOString(),
      });
    } catch (e) {
      next(e);
    }
  },
);

const bookingSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  phone: z.string().optional(),
  company: z.string().optional(),
  preferredTime: z.string().optional(),
  topic: z.string().optional(),
});

publicRouter.post(
  "/booking-request",
  validateBody(bookingSchema),
  async (req, res, next) => {
    try {
      const body = req.body as z.infer<typeof bookingSchema>;
      const db = getDb();
      await db.insert(leads).values({
        company: body.company || body.name,
        contactName: body.name,
        contactEmail: body.email,
        contactPhone: body.phone || null,
        notes: `Demo request: ${body.topic || "general"} | preferred: ${body.preferredTime || "any"}`,
        source: "booking_form",
        priority: "p0",
      });
      res.status(201).json({
        ok: true,
        bookingId: `book_${Date.now()}`,
        confirmationMessage:
          "تم استلام طلبك. سيتواصل معك فريقنا خلال 24 ساعة لتأكيد الموعد.",
      });
    } catch (e) {
      next(e);
    }
  },
);

publicRouter.get("/knowledge/answer", async (req, res, next) => {
  try {
    const q = String(req.query.q || "").trim();
    if (!q) throw badRequest("Query parameter 'q' required");
    const db = getDb();
    const tokens = q
      .toLowerCase()
      .split(/\s+/)
      .filter((t) => t.length > 1)
      .slice(0, 6);
    const conditions = tokens.flatMap((t) => [
      ilike(knowledgeBase.titleAr, `%${t}%`),
      ilike(knowledgeBase.titleEn, `%${t}%`),
      ilike(knowledgeBase.bodyAr, `%${t}%`),
      ilike(knowledgeBase.bodyEn, `%${t}%`),
    ]);
    const rows = conditions.length
      ? await db
          .select()
          .from(knowledgeBase)
          .where(or(...conditions))
          .limit(5)
      : await db.select().from(knowledgeBase).limit(5);
    const best = rows[0];
    res.json({
      query: q,
      found: rows.length > 0,
      best: best
        ? {
            slug: best.slug,
            title: best.titleAr,
            body: best.bodyAr,
            category: best.category,
          }
        : null,
      related: rows.slice(1).map((r) => ({
        slug: r.slug,
        title: r.titleAr,
        category: r.category,
      })),
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

publicRouter.get("/pricing/plans", (_req, res) => {
  res.json({
    currency: "SAR",
    plans: [
      {
        id: "free_diagnostic",
        name: "Free Diagnostic",
        price: 0,
        period: "one-time",
        description: "تشخيص مبدئي لعمليات الإيراد",
        features: [
          "20 دقيقة مكالمة",
          "Revenue health scorecard",
          "تقرير من 3 صفحات",
        ],
        cta: "احجز الآن",
      },
      {
        id: "sprint_499",
        name: "Revenue Sprint",
        price: 499,
        period: "one-time",
        description: "7 أيام تشغيل بيع وتسويق مكثف",
        features: [
          "Pipeline cleanup",
          "10 outreach drafts",
          "تقرير نهاية الأسبوع",
        ],
        cta: "ابدأ Sprint",
      },
      {
        id: "data_pack_1500",
        name: "Saudi Data Pack",
        price: 1500,
        period: "one-time",
        description: "بيانات حسابات سعودية مؤهلة (50 حساب)",
        features: [
          "50 ABM accounts",
          "Decision-makers + emails",
          "Tech stack signals",
        ],
        cta: "اطلب الحزمة",
        popular: true,
      },
      {
        id: "managed_ops_2999",
        name: "Managed Ops",
        price: 2999,
        period: "monthly",
        description: "تشغيل عمليات بيع كامل بقيادة Dealix",
        features: [
          "Outbound 200 رسالة/شهر",
          "Pipeline management",
          "Weekly briefings",
          "Approval gates",
        ],
        cta: "ابدأ الآن",
      },
      {
        id: "custom_ai_25k",
        name: "Custom AI",
        price: 5000,
        priceMax: 25000,
        period: "monthly",
        description: "بنية AI مخصصة لقطاعك",
        features: [
          "Custom AI agents",
          "Data integration",
          "Founder Console access",
          "On-call support",
        ],
        cta: "تواصل مع المؤسس",
      },
    ],
  });
});
