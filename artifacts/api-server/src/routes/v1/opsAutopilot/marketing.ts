import { Router } from "express";
import { z } from "zod";
import { and, desc, eq, gte, lt, sql } from "drizzle-orm";
import { getDb, marketingCalendar, approvals } from "@workspace/db";
import { validateBody } from "../../../middleware/validate.js";
import { requireAdminKey } from "../../../middleware/requireAdminKey.js";
import { notFound } from "../../../lib/errors.js";

export const marketingRouter = Router();
marketingRouter.use(requireAdminKey);

function toApi(s: typeof marketingCalendar.$inferSelect) {
  return {
    id: s.id,
    slotDate: s.slotDate,
    channel: s.channel,
    contentType: s.contentType,
    title: s.title,
    bodyAr: s.bodyAr,
    bodyEn: s.bodyEn,
    status: s.status,
    utm: s.utm,
    isPublished: s.isPublished,
    publishedAt: s.publishedAt?.toISOString() || null,
    metadata: s.metadata,
    createdAt: s.createdAt.toISOString(),
  };
}

marketingRouter.get("/calendar", async (req, res, next) => {
  try {
    const limit = Math.min(parseInt(String(req.query.limit ?? 80), 10) || 80, 365);
    const db = getDb();
    const rows = await db
      .select()
      .from(marketingCalendar)
      .orderBy(desc(marketingCalendar.slotDate))
      .limit(limit);
    res.json({
      slots: rows.map(toApi),
      total: rows.length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const patchSchema = z.object({
  title: z.string().optional(),
  bodyAr: z.string().optional(),
  bodyEn: z.string().optional(),
  status: z.string().optional(),
  channel: z.string().optional(),
  slotDate: z.string().optional(),
  utm: z.record(z.string()).optional(),
});

marketingRouter.patch("/calendar/:id", validateBody(patchSchema), async (req, res, next) => {
  try {
    const b = req.body as z.infer<typeof patchSchema>;
    const db = getDb();
    const [updated] = await db
      .update(marketingCalendar)
      .set({
        ...(b.title != null ? { title: b.title } : {}),
        ...(b.bodyAr != null ? { bodyAr: b.bodyAr } : {}),
        ...(b.bodyEn != null ? { bodyEn: b.bodyEn } : {}),
        ...(b.status != null ? { status: b.status } : {}),
        ...(b.channel != null ? { channel: b.channel } : {}),
        ...(b.slotDate != null ? { slotDate: b.slotDate } : {}),
        ...(b.utm != null ? { utm: b.utm } : {}),
        updatedAt: new Date(),
      })
      .where(eq(marketingCalendar.id, String(req.params.id)))
      .returning();
    if (!updated) throw notFound("Slot not found");
    res.json({ slot: toApi(updated) });
  } catch (e) {
    next(e);
  }
});

marketingRouter.get("/calendar/:id/publish-kit", async (req, res, next) => {
  try {
    const db = getDb();
    const [row] = await db
      .select()
      .from(marketingCalendar)
      .where(eq(marketingCalendar.id, String(req.params.id)))
      .limit(1);
    if (!row) throw notFound("Slot not found");
    const utmParams = new URLSearchParams({
      utm_source: row.channel,
      utm_medium: "social",
      utm_campaign: row.contentType,
      utm_content: row.id.slice(0, 8),
      ...row.utm,
    });
    res.json({
      slotId: row.id,
      channel: row.channel,
      title: row.title,
      contentAr: row.bodyAr,
      contentEn: row.bodyEn,
      utmString: utmParams.toString(),
      previewUrl: `https://dealix.sa/m/${row.id.slice(0, 8)}?${utmParams.toString()}`,
      assets: {
        coverImage: `https://placehold.co/1200x630/0ea5e9/fff?text=${encodeURIComponent(row.title.slice(0, 40))}`,
        hashtags: ["#Dealix", "#RevOps", "#السعودية", "#مبيعات_B2B"],
      },
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const utmSchema = z.object({
  source: z.string().min(1),
  medium: z.string().min(1),
  campaign: z.string().min(1),
  term: z.string().optional(),
  content: z.string().optional(),
  url: z.string().url(),
});

marketingRouter.post("/utm", validateBody(utmSchema), (req, res) => {
  const b = req.body as z.infer<typeof utmSchema>;
  const u = new URL(b.url);
  u.searchParams.set("utm_source", b.source);
  u.searchParams.set("utm_medium", b.medium);
  u.searchParams.set("utm_campaign", b.campaign);
  if (b.term) u.searchParams.set("utm_term", b.term);
  if (b.content) u.searchParams.set("utm_content", b.content);
  res.json({ url: u.toString() });
});

marketingRouter.get("/social-today", async (_req, res, next) => {
  try {
    const start = new Date(new Date().setHours(0, 0, 0, 0));
    const end = new Date(new Date().setHours(23, 59, 59, 999));
    const db = getDb();
    const rows = await db
      .select()
      .from(marketingCalendar)
      .where(
        and(
          gte(marketingCalendar.slotDate, start.toISOString().slice(0, 10)),
          lt(marketingCalendar.slotDate, end.toISOString().slice(0, 10) + "Z"),
        ),
      )
      .orderBy(desc(marketingCalendar.slotDate))
      .limit(20);
    res.json({
      today: rows.map(toApi),
      total: rows.length,
      date: new Date().toISOString().slice(0, 10),
    });
  } catch (e) {
    next(e);
  }
});

const markSchema = z.object({
  id: z.string(),
  status: z.enum(["published", "scheduled", "draft", "cancelled"]).optional(),
});

marketingRouter.post(
  "/social-today/mark",
  validateBody(markSchema),
  async (req, res, next) => {
    try {
      const b = req.body as z.infer<typeof markSchema>;
      const db = getDb();
      const [updated] = await db
        .update(marketingCalendar)
        .set({
          status: b.status || "published",
          isPublished: (b.status || "published") === "published",
          publishedAt: (b.status || "published") === "published" ? new Date() : null,
          updatedAt: new Date(),
        })
        .where(eq(marketingCalendar.id, b.id))
        .returning();
      if (!updated) throw notFound("Slot not found");
      res.json({ slot: toApi(updated) });
    } catch (e) {
      next(e);
    }
  },
);

marketingRouter.post("/queue-approval", async (_req, res, next) => {
  try {
    const db = getDb();
    const [created] = await db
      .insert(approvals)
      .values({
        agentType: "marketing",
        action: "publish_marketing_calendar_week",
        description: "نشر محتوى التسويق لهذا الأسبوع — 5 منشورات عبر LinkedIn و3 عبر X",
        target: "linkedin+x",
        riskLevel: "low",
        policyClass: "A2",
        estimatedImpact: "زيادة وصول العلامة لمدة 7 أيام",
      })
      .returning();
    res.json({ approval: created });
  } catch (e) {
    next(e);
  }
});

marketingRouter.post("/weekly-pack/apply", async (_req, res, next) => {
  try {
    const db = getDb();
    const today = new Date();
    const slots: Array<typeof marketingCalendar.$inferInsert> = [];
    const channels = ["linkedin", "x", "linkedin", "linkedin", "x"];
    const titles = [
      "كيف نختصر دورة البيع 30%",
      "Founder Console: 7 قرارات/يوم",
      "Case Study: نتيجة 45 يوم",
      "Anti-waste check يحمي ميزانيتك",
      "ABM في السوق السعودي",
    ];
    for (let i = 0; i < 5; i++) {
      const d = new Date(today.getTime() + i * 24 * 3600 * 1000);
      slots.push({
        slotDate: d.toISOString().slice(0, 10),
        channel: channels[i] as string,
        contentType: "post",
        title: titles[i] as string,
        bodyAr: `${titles[i]} — اشترك في Dealix.\nاحجز discovery 25 دقيقة.`,
        status: "planned",
      });
    }
    const inserted = await db.insert(marketingCalendar).values(slots).returning();
    res.json({ inserted: inserted.length, slots: inserted.map(toApi) });
  } catch (e) {
    next(e);
  }
});

marketingRouter.get("/objection-draft", async (req, res, next) => {
  try {
    const slug = String(req.query.slug || "price");
    const drafts: Record<string, { titleAr: string; bodyAr: string }> = {
      price: {
        titleAr: "السعر مرتفع",
        bodyAr:
          "أتفهم تماماً. اسمح لي بأن أوضح: ما تدفعه هو احتيار. كم تكلفك فرصة ضائعة شهرياً بسبب pipeline ضعيف؟ نعمل على إثبات قيمة في 30 يوم؛ إذا لم تتحقق، تتوقف بدون التزام.",
      },
      timing: {
        titleAr: "الوقت غير مناسب",
        bodyAr:
          "متى يكون مناسباً؟ نشتغل على بناء أساس قابل للقياس لذا حتى لو بدأنا بعد 60 يوم، تكلفة الانتظار تتراكم. اقترح pilot صغير الآن نحدد نتائجه مع نهاية الربع.",
      },
      authority: {
        titleAr: "أحتاج موافقة الإدارة",
        bodyAr:
          "تماماً. ساعدني أفهم كيف ينظر المدير لاتخاذ قرار كهذا. هل أستطيع تجهيز Proof Pack من صفحة موجهة لاهتماماتهم؟ نلتقي الثلاثاء 15 دقيقة معك ومعهم؟",
      },
    };
    res.json({
      slug,
      draft: drafts[slug] || drafts.price,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});
