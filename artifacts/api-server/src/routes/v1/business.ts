import { Router } from "express";
import { z } from "zod";
import { validateBody } from "../../middleware/validate.js";

export const businessRouter = Router();

const verticalRecommendSchema = z.object({
  industry: z.string().optional(),
  size: z.enum(["smb", "mid", "enterprise"]).optional(),
  budget: z.number().optional(),
});

businessRouter.post(
  "/verticals/recommend",
  validateBody(verticalRecommendSchema),
  (req, res) => {
    const { industry, size } = req.body as z.infer<typeof verticalRecommendSchema>;
    const verticals = [
      { id: "saas_b2b", name: "B2B SaaS", fit: 92, why: "Outbound مكثف يعمل" },
      { id: "fintech", name: "Fintech", fit: 88, why: "Risk + compliance توافق قوي" },
      { id: "logistics", name: "Logistics", fit: 78, why: "Pipeline طويل لكن قيمة عالية" },
      { id: "retail_ops", name: "Retail Ops", fit: 70, why: "متطلبات تنفيذية أكبر" },
    ].sort((a, b) => b.fit - a.fit);
    res.json({
      input: { industry: industry || null, size: size || "mid" },
      recommendations: verticals.slice(0, 3),
      generatedAt: new Date().toISOString(),
    });
  },
);

const planSchema = z.object({
  goal: z.enum(["pipeline", "revenue", "retention", "expansion"]),
  horizon: z.enum(["30d", "60d", "90d"]).optional(),
});

businessRouter.post(
  "/recommend-plan",
  validateBody(planSchema),
  (req, res) => {
    const { goal, horizon = "90d" } = req.body as z.infer<typeof planSchema>;
    const playbooks: Record<string, string[]> = {
      pipeline: [
        "ABM Top 50 بتخصيص رسائل/شركة",
        "Warm intros 9/أسبوع من شركاء سابقين",
        "Sequencing 5 خطوات: email → LinkedIn → email → call → break",
      ],
      revenue: [
        "إغلاق صفقات قائمة قبل أي outreach جديد",
        "Upsell على pilot customers الحاليين",
        "Pricing review للحزم Top 3",
      ],
      retention: [
        "QBR لكل عميل في first 60 يوم",
        "Health score أسبوعي + early warning",
        "Founder check-in شهري للحسابات الأكبر",
      ],
      expansion: [
        "ابني case study من نتيجة بقطاع X",
        "افتح منطقة 2 (UAE / Egypt)",
        "Channel partners 3 lined up",
      ],
    };
    res.json({
      goal,
      horizon,
      plan: playbooks[goal] ?? [],
      kpis: [
        `${goal === "revenue" ? "Closed-won SAR" : "Qualified leads"} = هدف أسبوعي`,
        "Cycle time لكل مرحلة",
        "Approval gates passed",
      ],
      generatedAt: new Date().toISOString(),
    });
  },
);

businessRouter.get("/gtm/first-10", (_req, res) => {
  res.json({
    title: "First 10 Customers Playbook",
    steps: [
      { n: 1, title: "حدد ICP بدقة", do: "3 معايير صلبة + 2 إشارات شراء" },
      { n: 2, title: "قائمة 50 حساب مستهدف", do: "بنفسك، يدوي، اسم + قرارَين" },
      { n: 3, title: "Warm intro لـ 10 حسابات", do: "من شبكتك المباشرة" },
      { n: 4, title: "Outbound لـ 40 حساب", do: "Sequence 5 خطوات" },
      { n: 5, title: "Discovery call 25 دقيقة", do: "أسئلة pain، budget، timeline" },
      { n: 6, title: "Proposal من صفحة واحدة", do: "السعر، النطاق، التسليم" },
      { n: 7, title: "Pilot صغير 30 يوم", do: "نتيجة قابلة للقياس" },
      { n: 8, title: "Convert pilot إلى عقد", do: "نتيجة موثقة + توصية" },
      { n: 9, title: "اطلب 2 referrals", do: "بعد أول نتيجة موثقة" },
      { n: 10, title: "Case study + repeat", do: "كرر مع تحسين conversion" },
    ],
    targetTimeline: "90 يوم",
    successCriteria: "10 عقود موقعة، 3 منها case studies",
  });
});

businessRouter.get("/sales-script", (_req, res) => {
  res.json({
    name: "Discovery Call — 25 min",
    languages: ["ar", "en"],
    structure: [
      {
        section: "Opening (2 min)",
        scriptAr:
          "شكراً على وقتك. هدفي اليوم نفهم وضع الإيرادات عندكم ونرى إذا فيه fit. تمام؟",
        scriptEn:
          "Thanks for the time. My goal today is to understand your revenue motion and see if there's fit. Sound good?",
      },
      {
        section: "Pain Discovery (8 min)",
        scriptAr:
          "خبرني، ما أكبر تحدّيين حالياً في توليد الإيراد؟ وما الذي جربتم لحلهم؟",
        scriptEn:
          "Tell me, what are the top 2 revenue challenges right now? What have you tried?",
      },
      {
        section: "Quantify (5 min)",
        scriptAr:
          "كم تكلفكم هذي التحديات شهرياً؟ كم لو حلّيناهم القيمة لكم؟",
        scriptEn: "How much do these cost monthly? What's the upside if solved?",
      },
      {
        section: "Solution Fit (5 min)",
        scriptAr:
          "نشتغل مع شركات مشابهة سعودية. خلني أعرض كيف نحل المشكلة في 30 يوم.",
        scriptEn:
          "We work with similar Saudi companies. Let me show how we solve this in 30 days.",
      },
      {
        section: "Next Step (5 min)",
        scriptAr:
          "إذا فيه fit مبدئي، نقترح Pilot صغير 30 يوم بسعر محدد. تناسب الأسبوع الجاي؟",
        scriptEn: "If there's initial fit, we propose a 30-day pilot. Next week work?",
      },
    ],
  });
});

businessRouter.get("/proof-pack/demo", (_req, res) => {
  res.json({
    title: "Dealix Proof Pack — Demo",
    sections: [
      {
        title: "Case Study: Tech SMB في الرياض",
        outcome: "+38% pipeline في 45 يوم",
        method: "ABM Top 30 + outreach مخصص + qualification محسّن",
        evidenceLevel: "L3 (موثق بشهادة عميل)",
      },
      {
        title: "Case Study: Fintech ناشئ",
        outcome: "4 demos مؤهلة/أسبوع (كان 0)",
        method: "Warm intros + content + LinkedIn outreach",
        evidenceLevel: "L2 (موثق بـ metrics CRM)",
      },
      {
        title: "Operational Highlight",
        outcome: "Approval gates منعت 7 رسائل غير مطابقة في 30 يوم",
        method: "Founder Console v5 — policy A1/A2/A3",
        evidenceLevel: "L4 (audit log)",
      },
    ],
    generatedAt: new Date().toISOString(),
    callToAction: {
      label: "احجز Discovery Call 25 دقيقة",
      url: "/booking",
    },
  });
});
