/**
 * Dealix seed — populates the database with realistic Saudi-market data.
 *
 * Usage: pnpm --filter @workspace/api-server run seed
 *
 * Idempotent: each insert checks for existing record by natural key.
 */
import bcrypt from "bcryptjs";
import { eq } from "drizzle-orm";
import {
  getDb,
  users,
  leads,
  deals,
  approvals,
  marketingCalendar,
  evidenceEvents,
  supportTickets,
  knowledgeBase,
  workers,
  type NewLead,
  type NewDeal,
  type NewApproval,
  type NewMarketingSlot,
  type NewEvidenceEvent,
  type NewSupportTicket,
  type NewKnowledgeArticle,
  type NewWorker,
} from "@workspace/db";
import { scoreLead } from "../lib/scoring.js";

async function seedAdmin() {
  const db = getDb();
  const email = "admin@dealix.ai";
  const existing = await db.select().from(users).where(eq(users.email, email)).limit(1);
  if (existing.length) {
    console.log(`[seed] admin already exists: ${email}`);
    return;
  }
  const hash = await bcrypt.hash("Dealix2024!", 12);
  await db.insert(users).values({
    email,
    passwordHash: hash,
    fullName: "Dealix Founder",
    company: "Dealix",
    role: "admin",
  });
  console.log(`[seed] admin user created: ${email} / Dealix2024!`);
}

const SAUDI_LEADS: Array<Partial<NewLead> & { company: string }> = [
  {
    company: "Saudi Aramco",
    contactName: "أحمد العتيبي",
    contactEmail: "ahmed.alotaibi@aramco.example",
    contactPhone: "+966501234567",
    industry: "oil_gas",
    city: "Dhahran",
    estimatedValue: "750000",
    priority: "p0",
    source: "warm_intro",
    notes: "Director of Revenue Ops — referral من شريك سابق. Interested في 90-day pilot.",
    stage: "qualified",
  },
  {
    company: "SABIC",
    contactName: "نورة الزهراني",
    contactEmail: "n.alzahrani@sabic.example",
    contactPhone: "+966502345678",
    industry: "petrochemical",
    city: "Riyadh",
    estimatedValue: "500000",
    priority: "p0",
    source: "demo_booked",
    notes: "VP Commercial — حجزت demo بعد LinkedIn outreach.",
    stage: "proposal",
  },
  {
    company: "STC Group",
    contactName: "خالد البقمي",
    contactEmail: "khalid.b@stc.example",
    industry: "telecom",
    city: "Riyadh",
    estimatedValue: "350000",
    priority: "p0",
    source: "abm",
    notes: "Enterprise Sales Lead — تمت 2 discovery sessions.",
    stage: "negotiation",
  },
  {
    company: "Neom Tech & Digital",
    contactName: "Sara Al Mansoori",
    contactEmail: "sara@neom.example",
    industry: "government",
    city: "Tabuk",
    estimatedValue: "1200000",
    priority: "p0",
    source: "warm_intro",
    notes: "Innovation Lab — مهتمين بحلول AI-native للسوق السعودي.",
    stage: "qualified",
  },
  {
    company: "Maaden",
    contactName: "محمد الشهراني",
    contactEmail: "m.shahrani@maaden.example",
    industry: "energy",
    city: "Jubail",
    estimatedValue: "280000",
    priority: "p1",
    source: "abm",
    notes: "Operations Director — pipeline stage مبكر.",
    stage: "lead",
  },
  {
    company: "Almarai",
    contactName: "Fatimah Al-Harbi",
    contactEmail: "fatimah@almarai.example",
    industry: "retail",
    city: "Riyadh",
    estimatedValue: "180000",
    priority: "p1",
    source: "content",
    notes: "Trade Marketing Manager — جاءت من LinkedIn post.",
    stage: "qualified",
  },
  {
    company: "Saudia Airlines",
    contactName: "عبدالعزيز السبيعي",
    contactEmail: "a.sebai@saudia.example",
    industry: "aviation",
    city: "Jeddah",
    estimatedValue: "420000",
    priority: "p1",
    source: "referral",
    stage: "lead",
  },
  {
    company: "stc Bank",
    contactName: "Lara Al Otaibi",
    contactEmail: "lara@stcbank.example",
    industry: "banking",
    city: "Riyadh",
    estimatedValue: "650000",
    priority: "p0",
    source: "warm_intro",
    notes: "Head of Acquisition — referral من شركة fintech سابقة.",
    stage: "qualified",
  },
  {
    company: "Riyad Bank",
    contactName: "Yousef Al Qahtani",
    contactEmail: "yousef@riyadbank.example",
    industry: "banking",
    city: "Riyadh",
    estimatedValue: "550000",
    priority: "p1",
    source: "abm",
    stage: "lead",
  },
  {
    company: "Al Rajhi Bank",
    contactName: "Mona Al Sharif",
    contactEmail: "mona@alrajhi.example",
    industry: "banking",
    city: "Riyadh",
    estimatedValue: "780000",
    priority: "p0",
    source: "warm_intro",
    stage: "qualified",
    notes: "Innovation Office — مهتمين بـ Founder Console v5 governance.",
  },
  {
    company: "Tabby",
    contactName: "Hassan Al Dossari",
    contactEmail: "hassan@tabby.example",
    industry: "fintech",
    city: "Riyadh",
    estimatedValue: "220000",
    priority: "p0",
    source: "content",
    notes: "Growth lead — جاء من مقال LinkedIn.",
    stage: "proposal",
  },
  {
    company: "Tamara",
    contactName: "Reem Al Mutairi",
    contactEmail: "reem@tamara.example",
    industry: "fintech",
    city: "Riyadh",
    estimatedValue: "190000",
    priority: "p1",
    source: "abm",
    stage: "lead",
  },
  {
    company: "Mrsool",
    contactName: "Sultan Al Ghamdi",
    contactEmail: "sultan@mrsool.example",
    industry: "logistics",
    city: "Riyadh",
    estimatedValue: "150000",
    priority: "p1",
    source: "demo_booked",
    stage: "qualified",
  },
  {
    company: "Foodics",
    contactName: "أمل العمري",
    contactEmail: "amal@foodics.example",
    industry: "saas_b2b",
    city: "Riyadh",
    estimatedValue: "95000",
    priority: "p1",
    source: "content",
    stage: "lead",
  },
  {
    company: "Salla",
    contactName: "Faisal Al Otaibi",
    contactEmail: "faisal@salla.example",
    industry: "ecommerce",
    city: "Jeddah",
    estimatedValue: "120000",
    priority: "p1",
    source: "abm",
    stage: "qualified",
  },
  {
    company: "Zid",
    contactName: "Bandar Al Harbi",
    contactEmail: "bandar@zid.example",
    industry: "ecommerce",
    city: "Riyadh",
    estimatedValue: "85000",
    priority: "p2",
    source: "content",
    stage: "lead",
  },
  {
    company: "Bayan Credit Bureau",
    contactName: "Ghassan Al Salem",
    contactEmail: "ghassan@bayan.example",
    industry: "finance",
    city: "Riyadh",
    estimatedValue: "260000",
    priority: "p1",
    source: "warm_intro",
    stage: "qualified",
  },
  {
    company: "Lean Technologies",
    contactName: "Hisham Al Faleh",
    contactEmail: "hisham@leantech.example",
    industry: "fintech",
    city: "Riyadh",
    estimatedValue: "175000",
    priority: "p0",
    source: "referral",
    stage: "proposal",
  },
  {
    company: "Geidea",
    contactName: "Maha Al Saleh",
    contactEmail: "maha@geidea.example",
    industry: "fintech",
    city: "Riyadh",
    estimatedValue: "230000",
    priority: "p1",
    source: "abm",
    stage: "lead",
  },
  {
    company: "Hala (HRDF)",
    contactName: "Ahmad Al Anazi",
    contactEmail: "ahmad@hala.example",
    industry: "logistics",
    city: "Riyadh",
    estimatedValue: "140000",
    priority: "p2",
    source: "content",
    stage: "lead",
  },
];

async function seedLeads() {
  const db = getDb();
  let inserted = 0;
  for (const l of SAUDI_LEADS) {
    const existing = await db
      .select()
      .from(leads)
      .where(eq(leads.company, l.company))
      .limit(1);
    if (existing.length) continue;
    const aiScore = scoreLead({
      estimatedValue: l.estimatedValue,
      industry: l.industry,
      contactEmail: l.contactEmail,
      contactPhone: l.contactPhone,
      notes: l.notes,
      source: l.source,
      engagementScore: 50,
    });
    const nextFollowUp = new Date(
      Date.now() + Math.floor(Math.random() * 7) * 24 * 3600 * 1000,
    );
    await db.insert(leads).values({
      ...l,
      aiScore,
      engagementScore: 40 + Math.floor(Math.random() * 40),
      nextFollowUpAt: nextFollowUp,
    } as NewLead);
    inserted++;
  }
  console.log(`[seed] leads inserted: ${inserted}`);
}

async function seedDeals() {
  const db = getDb();
  const allLeads = await db.select().from(leads).limit(10);
  if (!allLeads.length) {
    console.log("[seed] no leads to derive deals from, skipping");
    return;
  }
  const stages = ["lead", "qualified", "proposal", "negotiation", "closed_won"];
  let inserted = 0;
  for (let i = 0; i < Math.min(5, allLeads.length); i++) {
    const l = allLeads[i]!;
    const stage = stages[i % stages.length] as string;
    const existing = await db
      .select()
      .from(deals)
      .where(eq(deals.company, l.company))
      .limit(1);
    if (existing.length) continue;
    const closeDate = new Date(
      Date.now() + (30 + Math.floor(Math.random() * 90)) * 24 * 3600 * 1000,
    );
    const value = Number(l.estimatedValue) || 100000;
    const probability =
      stage === "lead"
        ? 15
        : stage === "qualified"
          ? 30
          : stage === "proposal"
            ? 55
            : stage === "negotiation"
              ? 75
              : 100;
    const newDeal: NewDeal = {
      leadId: l.id,
      title: `${l.company} — Managed Ops Q1 2026`,
      company: l.company,
      value: String(value),
      currency: "SAR",
      stage,
      probability,
      aiScore: l.aiScore,
      assignedTo: "founder@dealix.ai",
      closeDate,
      tags: ["managed-ops", "saudi"],
    };
    await db.insert(deals).values(newDeal);
    inserted++;
  }
  console.log(`[seed] deals inserted: ${inserted}`);
}

const APPROVAL_TEMPLATES: NewApproval[] = [
  {
    agentType: "outreach",
    action: "send_email_external",
    description: "إرسال warm intro إلى VP Sales في Aramco عبر شريك مشترك",
    target: "Aramco - VP Sales",
    riskLevel: "medium",
    policyClass: "A2",
    estimatedImpact: "فتح discovery 30 دقيقة",
    metadata: { template: "warm_intro_v3", attachments: ["proof-pack.pdf"] },
  },
  {
    agentType: "marketing",
    action: "publish_post",
    description: "نشر منشور LinkedIn حول Anti-waste check",
    target: "linkedin",
    riskLevel: "low",
    policyClass: "A2",
    estimatedImpact: "زيادة الوصول 12k impression",
  },
  {
    agentType: "outreach",
    action: "draft_proposal",
    description: "صياغة proposal مخصص لـ SABIC",
    target: "SABIC",
    riskLevel: "low",
    policyClass: "A1",
    estimatedImpact: "تقدم Pipeline +1 stage",
  },
  {
    agentType: "compliance",
    action: "channel_change",
    description: "تفعيل WhatsApp Business لقطاع البنوك",
    target: "channel_policy",
    riskLevel: "high",
    policyClass: "A3",
    estimatedImpact: "تغيير قناة اتصال — يتطلب PDPL review",
  },
  {
    agentType: "outreach",
    action: "draft",
    description: "إعداد follow-up sequence لـ STC",
    target: "STC Group",
    riskLevel: "low",
    policyClass: "A2",
    estimatedImpact: "متابعة 3 خطوات",
  },
  {
    agentType: "intelligence",
    action: "enrich_account",
    description: "إثراء بيانات حساب Neom من مصادر عامة",
    target: "Neom",
    riskLevel: "low",
    policyClass: "A1",
    estimatedImpact: "data_quality +",
  },
  {
    agentType: "marketing",
    action: "publish",
    description: "نشر case study على X (Twitter)",
    target: "x",
    riskLevel: "medium",
    policyClass: "A2",
    estimatedImpact: "زيادة awareness في الفئة",
  },
  {
    agentType: "scoring",
    action: "recompute_pipeline",
    description: "إعادة حساب probability لكل صفقات Q1",
    target: "all_deals",
    riskLevel: "low",
    policyClass: "A1",
    estimatedImpact: "تحديث dashboards",
  },
  {
    agentType: "outreach",
    action: "discount",
    description: "خصم 15% لـ pilot مع Tabby",
    target: "Tabby",
    riskLevel: "medium",
    policyClass: "A2",
    estimatedImpact: "تسريع close",
  },
  {
    agentType: "orchestrator",
    action: "weekly_retro",
    description: "تشغيل weekly retro automation",
    target: "internal",
    riskLevel: "low",
    policyClass: "A1",
    estimatedImpact: "تحسين planning",
  },
];

async function seedApprovals() {
  const db = getDb();
  const existing = await db.select().from(approvals).limit(1);
  if (existing.length) {
    console.log("[seed] approvals already exist, skipping");
    return;
  }
  await db.insert(approvals).values(APPROVAL_TEMPLATES);
  console.log(`[seed] approvals inserted: ${APPROVAL_TEMPLATES.length}`);
}

async function seedMarketingCalendar() {
  const db = getDb();
  const existing = await db.select().from(marketingCalendar).limit(1);
  if (existing.length) {
    console.log("[seed] marketing slots already exist, skipping");
    return;
  }
  const slots: NewMarketingSlot[] = [];
  const channels = ["linkedin", "x", "linkedin", "linkedin", "x", "blog", "linkedin"];
  const topics = [
    "كيف نختصر دورة البيع 30%",
    "Founder Console v5: 7 قرارات/يوم",
    "Case Study: 45 يوم نتيجة",
    "Anti-waste check يحمي ميزانيتك",
    "ABM في السوق السعودي",
    "Approval gates: كيف تمنع 7 رسائل خطأ",
    "Risk score لكل lead",
  ];
  for (let i = 0; i < 30; i++) {
    const d = new Date(Date.now() + i * 24 * 3600 * 1000);
    const idx = i % topics.length;
    slots.push({
      slotDate: d.toISOString().slice(0, 10),
      channel: channels[idx] as string,
      contentType: idx % 7 === 5 ? "blog" : "post",
      title: topics[idx] as string,
      bodyAr: `${topics[idx]}\n\nنشارك في Dealix رؤى عملية لقادة الإيرادات في السعودية. اكتشف كيف تحوّل عملياتك إلى محرّك نمو.`,
      bodyEn: `Dealix shares practical insights for revenue leaders in Saudi Arabia.`,
      status: i < 5 ? "planned" : i < 15 ? "scheduled" : "draft",
      utm: { utm_source: channels[idx] as string, utm_medium: "social", utm_campaign: "q1_2026" },
    });
  }
  await db.insert(marketingCalendar).values(slots);
  console.log(`[seed] marketing slots inserted: ${slots.length}`);
}

async function seedEvidence() {
  const db = getDb();
  const existing = await db.select().from(evidenceEvents).limit(1);
  if (existing.length) {
    console.log("[seed] evidence events already exist, skipping");
    return;
  }
  const events: NewEvidenceEvent[] = [
    { eventType: "demo_completed", company: "Saudi Aramco", motion: "warm_intro", offerId: "managed_ops_2999", notes: "ممتاز — التزم بمتابعة." },
    { eventType: "proposal_sent", company: "SABIC", motion: "abm", offerId: "custom_ai_25k" },
    { eventType: "contract_signed", company: "Tabby", motion: "content", offerId: "managed_ops_2999", notes: "أول صفقة Q1." },
    { eventType: "discovery_held", company: "Neom", motion: "warm_intro", offerId: "custom_ai_25k" },
    { eventType: "objection_handled", company: "STC Group", motion: "abm" },
    { eventType: "referral_received", company: "Riyad Bank", motion: "warm_intro" },
    { eventType: "demo_completed", company: "Lean Technologies", motion: "referral", offerId: "sprint_499" },
    { eventType: "case_study_published", company: "Tabby", motion: "content" },
    { eventType: "qbr_completed", company: "Mrsool", motion: "expansion" },
    { eventType: "discovery_held", company: "Almarai", motion: "content", offerId: "data_pack_1500" },
    { eventType: "demo_no_show", company: "Foodics", motion: "content" },
    { eventType: "follow_up_sent", company: "Maaden", motion: "abm" },
    { eventType: "linkedin_engagement", company: "Saudia Airlines", motion: "content" },
    { eventType: "proposal_sent", company: "Al Rajhi Bank", motion: "warm_intro", offerId: "custom_ai_25k" },
    { eventType: "discovery_held", company: "stc Bank", motion: "warm_intro" },
    { eventType: "objection_handled", company: "Tamara", motion: "abm" },
    { eventType: "discovery_held", company: "Geidea", motion: "abm" },
    { eventType: "follow_up_sent", company: "Bayan Credit Bureau", motion: "warm_intro" },
    { eventType: "demo_completed", company: "Salla", motion: "abm", offerId: "managed_ops_2999" },
    { eventType: "approval_blocked", company: "internal", motion: "governance", notes: "Founder Console منع رسالة قبل النشر — A3 class." },
  ];
  await db.insert(evidenceEvents).values(events);
  console.log(`[seed] evidence events inserted: ${events.length}`);
}

async function seedSupport() {
  const db = getDb();
  const existing = await db.select().from(supportTickets).limit(1);
  if (existing.length) {
    console.log("[seed] support tickets already exist, skipping");
    return;
  }
  const tickets: NewSupportTicket[] = [
    {
      subject: "كيف أحصل على API key؟",
      body: "السلام عليكم، نحتاج API key للربط مع نظامنا الداخلي. كيف نطلبه؟",
      customerEmail: "ops@sabic.example",
      customerName: "نورة الزهراني",
      company: "SABIC",
      category: "technical",
      priority: "normal",
    },
    {
      subject: "Invoice مطلوبة — Q4",
      body: "نحتاج نسخة من فواتير Q4 لمتطلبات المراجعة المالية.",
      customerEmail: "finance@tabby.example",
      customerName: "Hassan Al Dossari",
      company: "Tabby",
      category: "billing",
      priority: "high",
    },
    {
      subject: "تأخير في تسليم Weekly Brief",
      body: "لم نستلم Weekly Brief هذا الأسبوع. هل هناك تأخير؟",
      customerEmail: "rev@stc.example",
      customerName: "Khalid Al Bogami",
      company: "STC Group",
      category: "service",
      priority: "high",
    },
    {
      subject: "تعديل على pricing tier",
      body: "نريد ترقية من Managed Ops إلى Custom AI tier ابتداء من الشهر القادم.",
      customerEmail: "ops@aramco.example",
      customerName: "Ahmed Al Otaibi",
      company: "Saudi Aramco",
      category: "sales",
      priority: "high",
    },
    {
      subject: "خطأ في dashboard",
      body: "الـ KPI cards لا تتحدث منذ الصباح. error: 502.",
      customerEmail: "team@neom.example",
      customerName: "Sara Al Mansoori",
      company: "Neom",
      category: "technical",
      priority: "urgent",
    },
    {
      subject: "طلب حذف بيانات (PDPL)",
      body: "نطلب حذف بيانات contact x وفقاً لـ PDPL article 18.",
      customerEmail: "legal@riyadbank.example",
      customerName: "Yousef Al Qahtani",
      company: "Riyad Bank",
      category: "compliance",
      priority: "high",
    },
    {
      subject: "Demo Booking — Q2",
      body: "هل يمكن جدولة demo شامل لفريقنا الثلاثاء القادم؟ 5 أشخاص.",
      customerEmail: "innovation@alrajhi.example",
      customerName: "Mona Al Sharif",
      company: "Al Rajhi Bank",
      category: "sales",
      priority: "normal",
    },
    {
      subject: "Outreach drafts غير دقيقة",
      body: "الرسائل المولّدة تحتوي على معلومات غير صحيحة عن شركتنا. نحتاج تعديل.",
      customerEmail: "ops@maaden.example",
      customerName: "M. Al Shahrani",
      company: "Maaden",
      category: "service",
      priority: "high",
    },
    {
      subject: "Onboarding feedback",
      body: "Onboarding سار بسلاسة. شكراً للفريق. نقترح إضافة فيديو شرح للـ approvals.",
      customerEmail: "growth@tabby.example",
      customerName: "Hassan Al Dossari",
      company: "Tabby",
      category: "feedback",
      priority: "low",
    },
    {
      subject: "تكامل مع Salesforce",
      body: "متى سيتوفر تكامل Salesforce؟ نحتاجه قبل العقد التالي.",
      customerEmail: "tech@geidea.example",
      customerName: "Maha Al Saleh",
      company: "Geidea",
      category: "feature_request",
      priority: "normal",
    },
  ];
  await db.insert(supportTickets).values(tickets);
  console.log(`[seed] support tickets inserted: ${tickets.length}`);
}

async function seedKnowledge() {
  const db = getDb();
  const articles: NewKnowledgeArticle[] = [
    {
      slug: "what-is-dealix",
      titleAr: "ما هو Dealix؟",
      titleEn: "What is Dealix?",
      bodyAr:
        "Dealix هي منصة Revenue Operations مصمّمة للسوق السعودي، تدمج Founder Console للحوكمة، Pipeline ذكي، وعمل Outreach مؤتمت مع approvals gates لضمان كل قرار خارجي يمر بتدقيق صارم.",
      bodyEn:
        "Dealix is a RevOps platform built for the Saudi market — Founder Console governance, smart pipeline, automated outreach with approval gates.",
      category: "general",
      tags: ["overview", "platform"],
      keywords: ["dealix", "revops", "outreach", "pipeline", "saudi"],
    },
    {
      slug: "pricing-plans",
      titleAr: "خطط الأسعار",
      titleEn: "Pricing Plans",
      bodyAr:
        "نقدّم 5 خطط: Free Diagnostic (مجاناً), Revenue Sprint 499 SAR, Saudi Data Pack 1500 SAR, Managed Ops 2999-4999 SAR/شهر, Custom AI 5000-25000 SAR/شهر.",
      bodyEn:
        "Five tiers: Free Diagnostic, Sprint 499 SAR, Data Pack 1500 SAR, Managed Ops 2999-4999/mo, Custom AI 5000-25000/mo.",
      category: "pricing",
      keywords: ["price", "سعر", "plans", "خطط", "تكلفة"],
    },
    {
      slug: "founder-console-v5",
      titleAr: "Founder Console v5",
      titleEn: "Founder Console v5",
      bodyAr:
        "Founder Console v5 هي طبقة الثقة الداخلية: تصنّف كل قرار إلى A1/A2/A3، تطلب أدلة قبل التنفيذ، وتسجل كل قرار في audit_log لا يتغيّر.",
      bodyEn:
        "Founder Console v5 is the internal trust layer: classifies decisions as A1/A2/A3, requires evidence, immutable audit log.",
      category: "governance",
      keywords: ["governance", "founder", "approvals", "audit", "policy"],
    },
    {
      slug: "pdpl-compliance",
      titleAr: "الامتثال PDPL",
      titleEn: "PDPL Compliance",
      bodyAr:
        "Dealix يلتزم بنظام حماية البيانات الشخصية السعودي (PDPL). نخزن البيانات داخل المملكة، نطبق consent على outreach، ونوفر آليات حذف خلال 30 يوم.",
      bodyEn:
        "Dealix complies with Saudi PDPL: in-country data, consent-based outreach, 30-day deletion mechanisms.",
      category: "compliance",
      keywords: ["pdpl", "compliance", "data", "privacy", "خصوصية"],
    },
    {
      slug: "ai-outreach",
      titleAr: "Outreach بـ AI",
      titleEn: "AI-Powered Outreach",
      bodyAr:
        "نستخدم AI لتوليد drafts outreach مخصصة باللغة العربية، لكن كل رسالة خارجية تمر بـ approval gate قبل الإرسال.",
      bodyEn:
        "We use AI to draft personalized Arabic outreach; every external message goes through an approval gate.",
      category: "product",
      keywords: ["ai", "outreach", "drafts", "linkedin", "email"],
    },
  ];
  for (const a of articles) {
    const existing = await db
      .select()
      .from(knowledgeBase)
      .where(eq(knowledgeBase.slug, a.slug))
      .limit(1);
    if (existing.length) continue;
    await db.insert(knowledgeBase).values(a);
  }
  console.log(`[seed] knowledge articles ensured: ${articles.length}`);
}

async function seedWorkers() {
  const db = getDb();
  const defaults: NewWorker[] = [
    { name: "outreach-agent", type: "outreach", status: "idle", runCount: 24, successCount: 22, failureCount: 2, lastRunAt: new Date(Date.now() - 6 * 60_000) },
    { name: "scoring-agent", type: "scoring", status: "idle", runCount: 312, successCount: 308, failureCount: 4, lastRunAt: new Date(Date.now() - 11 * 60_000) },
    { name: "compliance-agent", type: "compliance", status: "idle", runCount: 89, successCount: 89, failureCount: 0, lastRunAt: new Date(Date.now() - 3 * 60_000) },
    { name: "intelligence-agent", type: "intelligence", status: "idle", runCount: 152, successCount: 148, failureCount: 4, lastRunAt: new Date(Date.now() - 9 * 60_000) },
    { name: "orchestrator-agent", type: "orchestrator", status: "idle", runCount: 31, successCount: 31, failureCount: 0, lastRunAt: new Date(Date.now() - 2 * 60_000) },
  ];
  for (const w of defaults) {
    const existing = await db.select().from(workers).where(eq(workers.name, w.name)).limit(1);
    if (existing.length) continue;
    await db.insert(workers).values({
      ...w,
      lastSuccessAt: w.lastRunAt,
    });
  }
  console.log(`[seed] workers ensured: ${defaults.length}`);
}

async function main() {
  console.log("[seed] starting...");
  try {
    await seedAdmin();
    await seedLeads();
    await seedDeals();
    await seedApprovals();
    await seedMarketingCalendar();
    await seedEvidence();
    await seedSupport();
    await seedKnowledge();
    await seedWorkers();
    console.log("[seed] complete ✓");
  } catch (e) {
    console.error("[seed] failed:", e);
    process.exitCode = 1;
  } finally {
    process.exit(process.exitCode || 0);
  }
}

main();
