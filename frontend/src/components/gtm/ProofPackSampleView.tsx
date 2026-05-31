"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

type SectionRow = { id: string; title_ar: string; title_en?: string; status?: string; value?: string };

const SAMPLE_SECTIONS_AR = [
  {
    id: "s1",
    title: "مصادر العملاء المحتملين",
    level: "L3",
    status: "مكتمل",
    statusColor: "emerald",
    content: "تم تحليل مصادر الـ leads: 45% من LinkedIn، 30% إحالات، 25% بحث عضوي. جودة بيانات CRM: 62% مكتملة. توصية: تنظيف 38% قبل أي outreach.",
    actions: ["تنظيف بيانات CRM", "توثيق مصدر كل lead", "إضافة consent timestamp"],
  },
  {
    id: "s2",
    title: "ملاك القرارات",
    level: "L2",
    status: "يحتاج مدخلات",
    statusColor: "amber",
    content: "فجوة: 6 من 10 leads ليس لها مالك واضح بعد 5 أيام من الوصول. متوسط وقت الاستجابة: 72 ساعة (المستهدف: 24 ساعة). تحتاج: تعيين مالك لكل lead في CRM.",
    actions: ["تعيين مالك لكل lead", "إعداد SLA 24 ساعة", "تفعيل تنبيه تجاوز المهلة"],
  },
  {
    id: "s3",
    title: "سجل الأدلة",
    level: "L1",
    status: "محدود",
    statusColor: "red",
    content: "أقل من 30% من المحادثات موثّقة في CRM. 4 صفقات مُغلَقة بدون سجل follow-up. مخاطر: صعوبة التدقيق والإثبات عند الاختلاف مع العميل.",
    actions: ["توثيق كل محادثة في CRM", "إضافة نموذج evidence لكل صفقة", "ربط WhatsApp بـ CRM"],
  },
  {
    id: "s4",
    title: "قرارات الإيراد",
    level: "L3",
    status: "مكتمل",
    statusColor: "emerald",
    content: "تحديد 3 فرص توسع فورية: (1) 3 عملاء على عقد سنوي قابل للتجديد، (2) 2 عروض معلّقة منذ 30+ يوم، (3) قطاع لوجستيات = أعلى معدل تحويل.",
    actions: ["تجديد 3 عقود سنوية", "متابعة 2 عروض معلّقة", "التوسع في قطاع اللوجستيات"],
  },
];

const SAMPLE_SECTIONS_EN = [
  {
    id: "s1",
    title: "Lead Sources",
    level: "L3",
    status: "Complete",
    statusColor: "emerald",
    content: "Lead source analysis: 45% LinkedIn, 30% referrals, 25% organic search. CRM data quality: 62% complete. Recommendation: clean 38% before any outreach.",
    actions: ["Clean CRM data", "Document source per lead", "Add consent timestamp"],
  },
  {
    id: "s2",
    title: "Decision Owners",
    level: "L2",
    status: "Needs Input",
    statusColor: "amber",
    content: "Gap: 6 of 10 leads have no clear owner after 5 days. Average response time: 72 hours (target: 24 hours). Needed: assign owner per lead in CRM.",
    actions: ["Assign owner per lead", "Set 24-hour SLA", "Enable deadline alert"],
  },
  {
    id: "s3",
    title: "Evidence Log",
    level: "L1",
    status: "Limited",
    statusColor: "red",
    content: "Less than 30% of conversations documented in CRM. 4 closed deals without follow-up record. Risk: difficulty auditing and proving in case of client dispute.",
    actions: ["Document every conversation in CRM", "Add evidence form per deal", "Link WhatsApp to CRM"],
  },
  {
    id: "s4",
    title: "Revenue Decisions",
    level: "L3",
    status: "Complete",
    statusColor: "emerald",
    content: "3 immediate expansion opportunities: (1) 3 clients on renewable annual contracts, (2) 2 pending proposals 30+ days, (3) logistics sector = highest conversion rate.",
    actions: ["Renew 3 annual contracts", "Follow up 2 pending proposals", "Expand in logistics sector"],
  },
];

const STATUS_COLORS: Record<string, string> = {
  emerald: "border-emerald-500/30 bg-emerald-50 dark:bg-emerald-950/20 text-emerald-700 dark:text-emerald-300",
  amber: "border-amber-500/30 bg-amber-50 dark:bg-amber-950/20 text-amber-700 dark:text-amber-300",
  red: "border-red-500/30 bg-red-50 dark:bg-red-950/20 text-red-700 dark:text-red-300",
};

const STATIC_SECTIONS_AR: SectionRow[] = [
  { id: "1", title_ar: "خريطة مسارات الإيراد المُتسرِّب", title_en: "Revenue Leakage Workflow Map", status: "مكتمل", value: "١٨٪ تسرب غير مُفسَّر" },
  { id: "2", title_ar: "تقييم جودة CRM والمصادر", title_en: "CRM & Source Quality Assessment", status: "مكتمل", value: "٦٣٪ من السجلات تحتاج إثراء" },
  { id: "3", title_ar: "خريطة حدود الموافقة", title_en: "Approval Boundary Map", status: "مكتمل", value: "٤ إجراءات بدون حوكمة" },
  { id: "4", title_ar: "فجوات مسار الأدلة", title_en: "Evidence Trail Gaps", status: "مكتمل", value: "٩ قرارات بدون audit trail" },
  { id: "5", title_ar: "تقييم جاهزية ZATCA", title_en: "ZATCA Readiness Assessment", status: "مكتمل", value: "Wave 24 — يونيو ٢٠٢٦" },
  { id: "6", title_ar: "أعلى ٣ قرارات محكومة بدليل", title_en: "Top 3 Evidence-Governed Decisions", status: "قابل للتنفيذ فوراً", value: "" },
];

const DECISION_ITEMS_AR = [
  { n: "١", title: "إعادة تفعيل ٢٣ فرصة معلّقة في CRM", impact: "إيراد مُحتمل: 185,000 ر.س", timeline: "أسبوع ١" },
  { n: "٢", title: "ضبط موافقة PDPL على ٤ workflow", impact: "تجنّب غرامة نظامية: 5M ر.س", timeline: "أسبوع ٢" },
  { n: "٣", title: "ربط نظام الفوترة بـ ZATCA تلقائياً", impact: "امتثال Wave 24 قبل الموعد", timeline: "أسبوع ٣" },
];

const DECISION_ITEMS_EN = [
  { n: "1", title: "Re-activate 23 stalled CRM opportunities", impact: "Potential revenue: 185,000 SAR", timeline: "Week 1" },
  { n: "2", title: "Add PDPL consent to 4 workflows", impact: "Avoid regulatory penalty: 5M SAR", timeline: "Week 2" },
  { n: "3", title: "Connect invoicing system to ZATCA", impact: "Wave 24 compliance before deadline", timeline: "Week 3" },
];

const STATUS_COLORS: Record<string, string> = {
  "مكتمل": "bg-emerald-500/10 text-emerald-700 dark:text-emerald-400",
  "قابل للتنفيذ فوراً": "bg-primary/10 text-primary",
  "pending_inputs": "bg-muted text-muted-foreground",
};

export function ProofPackSampleView() {
  const locale = useLocale();
  const isAr = locale === "ar";
  const [data, setData] = useState<SamplePayload | null>(null);
  const [apiReady, setApiReady] = useState(false);

  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    fetch(`${base}/api/v1/public/proof-pack/sample?locale=${locale}`)
      .then((r) => r.json())
      .then((d) => { setData(d); setApiReady(true); })
      .catch(() => { setApiReady(false); });
  }, [locale]);

  const apiRows: SectionRow[] = apiReady && data
    ? (data.draft?.sections ?? (data.outline ?? []).map((t, i) => ({ id: String(i), title_ar: t, status: "pending_inputs" })))
    : [];

  const rows = apiRows.length > 0 ? apiRows : STATIC_SECTIONS_AR;
  const decisions = isAr ? DECISION_ITEMS_AR : DECISION_ITEMS_EN;

  return (
    <div className="max-w-2xl mx-auto space-y-8" dir={isAr ? "rtl" : "ltr"}>
      <header className={isAr ? "text-right" : ""}>
        <Badge variant="outline" className="mb-3 text-xs border-emerald-500/40 text-emerald-700 dark:text-emerald-400 bg-emerald-50/50 dark:bg-emerald-950/20">
          {isAr ? "عيّنة — Proof Pack فعلي" : "Sample — Real Proof Pack Format"}
        </Badge>
        <h1 className="text-2xl font-bold">
          {isAr
            ? data?.title_ar ?? "Proof Pack — شركة مثال: الواحة للاستشارات"
            : data?.title_en ?? "Proof Pack — Sample: Alwaha Consulting Co."}
        </h1>
        <p className="mt-2 text-sm text-muted-foreground leading-relaxed">
          {isAr
            ? data?.disclaimer_ar ?? "هذا نموذج توضيحي لما تحصل عليه بعد تشخيص ٧ أيام. الأرقام تمثيلية — Proof Pack الحقيقي يعتمد على بيانات شركتك الفعلية."
            : data?.disclaimer_en ?? "This is an illustrative sample of what you receive after a 7-day diagnostic. Numbers are representative — your real Proof Pack uses your actual company data."}
        </p>

        {/* Meta info */}
        <div className="mt-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            { label: isAr ? "المستوى" : "Level", value: "L3 / 4" },
            { label: isAr ? "الأقسام" : "Sections", value: "4" },
            { label: isAr ? "الإجراءات" : "Actions", value: "12" },
            { label: isAr ? "المدة" : "Duration", value: isAr ? "7 أيام" : "7 Days" },
          ].map((m) => (
            <div key={m.label} className="rounded-lg border border-border/50 bg-card/50 p-3 text-center">
              <p className="text-xs text-muted-foreground">{m.label}</p>
              <p className="mt-0.5 font-bold text-lg">{m.value}</p>
            </div>
          ))}
        </div>
      </header>

      {/* Sections Grid */}
      <Card className="p-5 space-y-0 divide-y divide-border/50">
        <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide pb-3">
          {isAr ? "أقسام التقرير" : "Report Sections"}
        </p>
        {rows.map((s) => (
          <div key={s.id} className="flex items-center justify-between py-3 gap-4">
            <div className="flex-1 min-w-0">
              <p className="font-medium text-sm truncate">{isAr ? s.title_ar : (s.title_en ?? s.title_ar)}</p>
            </div>
            <div className="flex items-center gap-2 flex-shrink-0">
              {s.value && <span className="text-xs text-muted-foreground hidden sm:inline">{s.value}</span>}
              {s.status && (
                <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${STATUS_COLORS[s.status] ?? STATUS_COLORS["pending_inputs"]}`}>
                  {s.status}
                </span>
              )}
            </div>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">{isAr ? "أقسام مكتملة" : "Complete sections"}</span>
            <span className="font-bold text-emerald-600">2 / 4</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">{isAr ? "إجراءات فورية" : "Immediate actions"}</span>
            <span className="font-bold">12</span>
          </div>
          <div className="flex justify-between">
            <span className="text-muted-foreground">{isAr ? "التوصية" : "Recommendation"}</span>
            <span className="font-bold text-amber-600">{isAr ? "Sprint 7 أيام" : "7-Day Sprint"}</span>
          </div>
        </div>
        <div className="mt-4 rounded-lg border border-amber-500/20 bg-amber-50/50 dark:bg-amber-950/20 p-3 text-sm text-amber-800 dark:text-amber-300">
          {isAr
            ? "توصية: المستوى L3 يؤهّل للتوصية بـ Sprint. لا Retainer شهري قبل الوصول لـ L4 في الأقسام الرئيسية."
            : "Recommendation: L3 level qualifies for Sprint recommendation. No monthly Retainer before reaching L4 in main sections."}
        </div>
      </Card>

      {/* Top 3 Decisions */}
      <section>
        <h2 className="text-base font-semibold mb-3">
          {isAr ? "أعلى ٣ قرارات قابلة للتنفيذ" : "Top 3 Executable Decisions"}
        </h2>
        <div className="space-y-3">
          {decisions.map((d) => (
            <div key={d.n} className="flex gap-3 p-4 rounded-xl border border-border/60 bg-card/50">
              <span className="flex-shrink-0 w-7 h-7 rounded-full bg-primary/10 text-primary flex items-center justify-center font-bold text-xs">
                {d.n}
              </span>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm">{d.title}</p>
                <div className="mt-1 flex flex-wrap gap-3">
                  <span className="text-xs text-emerald-700 dark:text-emerald-400">{d.impact}</span>
                  <span className="text-xs text-muted-foreground">{isAr ? `الجدول: ${d.timeline}` : `Timeline: ${d.timeline}`}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Trust Footer */}
      <div className="rounded-lg border border-border/40 bg-muted/20 p-4">
        <p className="text-xs text-muted-foreground leading-relaxed">
          {isAr
            ? "كل قرار في Proof Pack مدعوم بـ audit trail موثّق · لا إرسال خارجي آلي · PDPL compliant · الأرقام مُحققة قبل التسليم"
            : "Every Proof Pack decision backed by documented audit trail · No automated outbound · PDPL compliant · All numbers verified before delivery"}
        </p>
      </div>

      {/* CTAs */}
      <div className="flex gap-3 flex-wrap">
        <Button asChild size="lg">
          <Link href={`/${locale}/dealix-diagnostic`}>
            {isAr ? "احصل على Proof Pack الخاص بك" : "Get Your Proof Pack"}
          </Link>
        </Button>
        <Button asChild variant="outline" size="lg">
          <Link href={`/${locale}/risk-score`}>
            {isAr ? "Risk Score المجاني" : "Free Risk Score"}
          </Link>
        </Button>
      </div>
    </div>
  );
}
