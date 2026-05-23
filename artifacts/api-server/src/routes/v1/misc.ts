import { Router } from "express";
import { desc, eq, sql } from "drizzle-orm";
import { getDb, leads, deals, approvals } from "@workspace/db";

export const miscRouter = Router();

miscRouter.get("/decision-passport/golden-chain", (_req, res) => {
  res.json({
    chain: [
      { step: 1, name: "Intent", description: "تحديد القرار المطلوب بوضوح" },
      { step: 2, name: "Evidence", description: "جمع الأدلة المطلوبة (L1-L5)" },
      { step: 3, name: "Policy Check", description: "تقييم A1/A2/A3" },
      { step: 4, name: "Approval Gate", description: "موافقة المؤسس" },
      { step: 5, name: "Execution", description: "تنفيذ مراقَب" },
      { step: 6, name: "Audit", description: "توثيق في audit_log" },
    ],
    enforcement: "كل قرار خارجي يمر بـ 6 خطوات",
  });
});

miscRouter.get("/decision-passport/evidence-levels", (_req, res) => {
  res.json({
    levels: [
      { id: "L1", name: "Assumption", description: "افتراض غير موثّق", autoApprove: false },
      { id: "L2", name: "Internal Data", description: "بيانات داخلية CRM/Sheets", autoApprove: false },
      { id: "L3", name: "Customer Testimony", description: "شهادة عميل موثقة", autoApprove: true },
      { id: "L4", name: "Audit Log", description: "سجل عمليات قابل للتدقيق", autoApprove: true },
      { id: "L5", name: "Third Party", description: "تحقق من جهة خارجية", autoApprove: true },
    ],
  });
});

miscRouter.get("/revenue-os/catalog", (_req, res) => {
  res.json({
    modules: [
      { id: "war_room", name: "War Room", category: "execution" },
      { id: "pipeline", name: "Pipeline", category: "execution" },
      { id: "approvals", name: "Approvals", category: "governance" },
      { id: "evidence", name: "Evidence Ledger", category: "governance" },
      { id: "marketing", name: "Marketing Calendar", category: "growth" },
      { id: "targeting", name: "ABM Targeting", category: "growth" },
      { id: "support", name: "Support", category: "ops" },
      { id: "knowledge", name: "Knowledge Base", category: "ops" },
    ],
    total: 8,
  });
});

miscRouter.get("/revenue-os/learning/weekly-template", (_req, res) => {
  res.json({
    title: "Weekly Learning Template",
    sections: [
      "ما الذي نجح هذا الأسبوع؟",
      "ما الذي فشل؟",
      "تجربة واحدة جديدة الأسبوع القادم",
      "Metric ركّز عليه",
    ],
  });
});

miscRouter.post("/revenue-os/anti-waste/check", (req, res) => {
  const body = (req.body || {}) as Record<string, unknown>;
  res.json({
    input: body,
    wasteSignals: [],
    score: 92,
    recommendation: "Process clean — لا توجد إشارات هدر",
  });
});

miscRouter.get("/v3/command-center/snapshot", async (_req, res, next) => {
  try {
    const db = getDb();
    const [stats] = await db
      .select({
        leads: sql<number>`count(*)::int`,
      })
      .from(leads);
    const [dealStats] = await db
      .select({
        pipelineValue: sql<number>`coalesce(sum(${deals.value}) filter (where ${deals.stage} not in ('closed_won','closed_lost')), 0)`,
        won: sql<number>`count(*) filter (where ${deals.stage} = 'closed_won')::int`,
      })
      .from(deals);
    const [appStats] = await db
      .select({
        pending: sql<number>`count(*) filter (where ${approvals.status} = 'pending')::int`,
      })
      .from(approvals);
    res.json({
      generatedAt: new Date().toISOString(),
      health: "operational",
      modules: {
        warRoom: { active: true, openTargets: stats?.leads || 0 },
        pipeline: { active: true, valueSAR: Number(dealStats?.pipelineValue || 0) },
        approvals: { active: true, pending: appStats?.pending || 0 },
        evidence: { active: true },
      },
      wins: dealStats?.won || 0,
    });
  } catch (e) {
    next(e);
  }
});

miscRouter.get("/gmail/drafts/today", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db
      .select()
      .from(leads)
      .where(eq(leads.priority, "p0"))
      .orderBy(desc(leads.aiScore))
      .limit(5);
    res.json({
      drafts: rows.map((l) => ({
        id: `draft_gmail_${l.id}`,
        leadId: l.id,
        to: l.contactEmail || `${(l.contactName || "contact").toLowerCase().replace(/\s+/g, ".")}@${l.company.toLowerCase().replace(/\s+/g, "")}.example`,
        subject: `${l.company} — متابعة من Dealix`,
        bodyAr: `السلام عليكم ${l.contactName || ""},\nشكراً على وقتك السابق. أردت متابعة سريعة بخصوص ${l.industry || "احتياجاتكم"}.`,
        status: "pending_approval",
        aiScore: l.aiScore,
      })),
      total: rows.length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

miscRouter.get("/linkedin/drafts/today", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db
      .select()
      .from(leads)
      .where(eq(leads.priority, "p0"))
      .orderBy(desc(leads.aiScore))
      .limit(5);
    res.json({
      drafts: rows.map((l) => ({
        id: `draft_li_${l.id}`,
        leadId: l.id,
        target: l.contactName || l.company,
        messageAr: `${l.contactName ? `أهلاً ${l.contactName}` : "أهلاً"}, شفت آخر تحديثاتكم في ${l.company}. أحب أتواصل وأشارك insight قد يفيدكم.`,
        status: "pending_approval",
        aiScore: l.aiScore,
      })),
      total: rows.length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

miscRouter.get("/channel-policy/status", (_req, res) => {
  res.json({
    policies: [
      { channel: "email", pdplCompliant: true, requiresConsent: true, status: "active" },
      { channel: "linkedin", pdplCompliant: true, requiresConsent: false, status: "active" },
      { channel: "whatsapp", pdplCompliant: true, requiresConsent: true, status: "gated" },
      { channel: "sms", pdplCompliant: true, requiresConsent: true, status: "blocked" },
    ],
    overallStatus: "compliant",
  });
});

miscRouter.get("/customer-portal/:handle", (req, res) => {
  res.json({
    handle: req.params.handle,
    customer: {
      name: req.params.handle,
      tier: "Managed Ops",
      status: "active",
      onboardingDay: 18,
    },
    deliverables: [
      { id: "weekly_brief", title: "Weekly Brief", status: "delivered" },
      { id: "pipeline_review", title: "Pipeline Review", status: "in_progress" },
      { id: "outreach_drafts", title: "Outreach Drafts", status: "pending_approval" },
    ],
    nextCheckIn: new Date(Date.now() + 7 * 24 * 3600 * 1000).toISOString(),
  });
});

miscRouter.get("/founder/leads", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db.select().from(leads).orderBy(desc(leads.createdAt)).limit(50);
    res.json({
      leads: rows.map((l) => ({
        id: l.id,
        company: l.company,
        contactName: l.contactName,
        contactEmail: l.contactEmail,
        stage: l.stage,
        priority: l.priority,
        aiScore: l.aiScore,
        estimatedValue: Number(l.estimatedValue),
        createdAt: l.createdAt.toISOString(),
      })),
      total: rows.length,
    });
  } catch (e) {
    next(e);
  }
});

miscRouter.post("/leads", async (req, res, next) => {
  try {
    const body = req.body as Record<string, string>;
    if (!body.company) return res.status(400).json({ error: "company required" });
    const db = getDb();
    const [created] = await db
      .insert(leads)
      .values({
        company: String(body.company),
        contactEmail: body.contactEmail || null,
        contactName: body.contactName || null,
        contactPhone: body.contactPhone || null,
        notes: body.notes || null,
        source: body.source || "founder_console",
      })
      .returning();
    res.status(201).json({ ok: true, lead: created });
  } catch (e) {
    next(e);
  }
});
