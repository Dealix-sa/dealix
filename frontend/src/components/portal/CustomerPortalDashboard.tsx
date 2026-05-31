"use client";

import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";

// ---------------------------------------------------------------------------
// Demo data — static placeholders until backend is connected
// ---------------------------------------------------------------------------

const DEMO_SPRINT = {
  current_day: 4,
  total_days: 7,
  client_name_ar: "شركة الأفق للتقنية",
  client_name_en: "Horizon Technology Co.",
  steps: [
    { day: 1, label_ar: "جمع البيانات", label_en: "Data collection", done: true },
    { day: 2, label_ar: "تدقيق العمليات", label_en: "Operations audit", done: true },
    { day: 3, label_ar: "تحليل الإيراد", label_en: "Revenue analysis", done: true },
    { day: 4, label_ar: "إعداد Proof Pack", label_en: "Proof Pack assembly", done: false, active: true },
    { day: 5, label_ar: "مراجعة النتائج", label_en: "Findings review", done: false },
    { day: 6, label_ar: "توصيات الإيراد", label_en: "Revenue recommendations", done: false },
    { day: 7, label_ar: "تسليم التقرير النهائي", label_en: "Final report delivery", done: false },
  ],
};

const DEMO_HEALTH = {
  score: 72,
  tier: "HEALTHY" as const,
  dimensions: [
    { label_ar: "جاهزية البيانات", label_en: "Data Readiness", score: 85 },
    { label_ar: "عمليات التأهيل", label_en: "Onboarding Ops", score: 60 },
    { label_ar: "جودة التسليم", label_en: "Delivery Quality", score: 78 },
    { label_ar: "الامتثال (ZATCA)", label_en: "ZATCA Compliance", score: 55 },
    { label_ar: "احتفاظ العملاء", label_en: "Client Retention", score: 80 },
    { label_ar: "الإيراد المتكرر", label_en: "Recurring Revenue", score: 70 },
  ],
};

const DEMO_DELIVERABLES = [
  {
    id: "D1",
    name_ar: "تقرير تدقيق البيانات",
    name_en: "Data Audit Report",
    status: "done" as const,
    due: "2026-05-28",
  },
  {
    id: "D2",
    name_ar: "خريطة العمليات",
    name_en: "Operations Map",
    status: "done" as const,
    due: "2026-05-29",
  },
  {
    id: "D3",
    name_ar: "تحليل مخاطر الإيراد",
    name_en: "Revenue Risk Analysis",
    status: "in-progress" as const,
    due: "2026-05-31",
  },
  {
    id: "D4",
    name_ar: "Proof Pack PDF كامل",
    name_en: "Full Proof Pack PDF",
    status: "pending" as const,
    due: "2026-06-02",
  },
  {
    id: "D5",
    name_ar: "توصيات ZATCA Phase 2",
    name_en: "ZATCA Phase 2 Recommendations",
    status: "pending" as const,
    due: "2026-06-03",
  },
];

const DEMO_DOCUMENTS = [
  { id: "L0", badge: "L0", name_ar: "ملخص تنفيذي", name_en: "Executive Summary", ready: true },
  { id: "L1", badge: "L1", name_ar: "تقرير تدقيق البيانات", name_en: "Data Audit Report", ready: true },
  { id: "L2", badge: "L2", name_ar: "خريطة العمليات", name_en: "Operations Map", ready: true },
  { id: "L3", badge: "L3", name_ar: "تحليل مخاطر الإيراد", name_en: "Revenue Risk Analysis", ready: false },
  { id: "L4", badge: "L4", name_ar: "خطة توصيات 90 يوم", name_en: "90-Day Recommendations Plan", ready: false },
];

const DEMO_NEXT_MILESTONE = {
  title_ar: "تسليم Proof Pack الكامل — اليوم 7",
  title_en: "Full Proof Pack Delivery — Day 7",
  description_ar: "سيتم إعداد Proof Pack الكامل وإرساله خلال يومين. يرجى التحقق من صحة البيانات المُرسلة.",
  description_en: "The complete Proof Pack will be assembled and sent within 2 days. Please verify the accuracy of submitted data.",
  required_from_client_ar: ["تأكيد بيانات الفاتورة الضريبية", "الموافقة على خريطة العمليات"],
  required_from_client_en: ["Confirm tax invoice data", "Approve operations map"],
  due_date: "2026-06-03",
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

type HealthTier = "CHAMPION" | "HEALTHY" | "AT_RISK";

const TIER_CONFIG: Record<HealthTier, { label_ar: string; label_en: string; color: string }> = {
  CHAMPION: { label_ar: "بطل", label_en: "Champion", color: "bg-green-100 text-green-800 border-green-300" },
  HEALTHY: { label_ar: "صحي", label_en: "Healthy", color: "bg-blue-100 text-blue-800 border-blue-300" },
  AT_RISK: { label_ar: "في خطر", label_en: "At Risk", color: "bg-red-100 text-red-800 border-red-300" },
};

const STATUS_CONFIG = {
  done: { label_ar: "مكتمل", label_en: "Done", color: "bg-green-100 text-green-800 border-green-300" },
  "in-progress": { label_ar: "قيد التنفيذ", label_en: "In Progress", color: "bg-amber-100 text-amber-800 border-amber-300" },
  pending: { label_ar: "قادم", label_en: "Pending", color: "bg-slate-100 text-slate-600 border-slate-300" },
};

// ---------------------------------------------------------------------------
// Section components
// ---------------------------------------------------------------------------

function SprintStatusCard({ isAr }: { isAr: boolean }) {
  const d = DEMO_SPRINT;
  const pct = Math.round(((d.current_day - 1) / (d.total_days - 1)) * 100);

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-[var(--dealix-deep-green)]">
          {isAr ? "حالة Sprint" : "Sprint Status"}
        </h2>
        <Badge variant="outline" className="text-xs">
          {isAr ? `اليوم ${d.current_day} / ${d.total_days}` : `Day ${d.current_day} / ${d.total_days}`}
        </Badge>
      </div>
      <p className="text-sm text-muted-foreground mb-4">
        {isAr ? d.client_name_ar : d.client_name_en}
      </p>
      <Progress value={pct} className="h-2 mb-6" />
      <div className="relative">
        <div className="flex justify-between">
          {d.steps.map((s) => (
            <div key={s.day} className="flex flex-col items-center gap-1.5 flex-1">
              <div
                className={`w-7 h-7 rounded-full border-2 flex items-center justify-center text-xs font-bold transition-colors ${
                  s.done
                    ? "border-[var(--dealix-deep-green)] bg-[var(--dealix-deep-green)] text-white"
                    : s.active
                    ? "border-[var(--dealix-gold)] bg-[var(--dealix-gold)]/10 text-[var(--dealix-gold)]"
                    : "border-border bg-background text-muted-foreground"
                }`}
              >
                {s.done ? "✓" : s.day}
              </div>
              <span
                className={`text-center leading-tight hidden sm:block ${
                  s.active ? "text-[var(--dealix-gold)] font-medium" : "text-muted-foreground"
                }`}
                style={{ fontSize: "0.6rem" }}
              >
                {isAr ? s.label_ar : s.label_en}
              </span>
            </div>
          ))}
        </div>
      </div>
    </Card>
  );
}

function HealthScoreCard({ isAr }: { isAr: boolean }) {
  const h = DEMO_HEALTH;
  const tierCfg = TIER_CONFIG[h.tier];

  return (
    <Card className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="font-semibold text-[var(--dealix-deep-green)]">
          {isAr ? "درجة الصحة" : "Health Score"}
        </h2>
        <Badge variant="outline" className={`text-xs ${tierCfg.color}`}>
          {isAr ? tierCfg.label_ar : tierCfg.label_en}
        </Badge>
      </div>
      <div className="text-center mb-6">
        <span className="text-5xl font-black text-[var(--dealix-deep-green)]">{h.score}</span>
        <span className="text-muted-foreground text-sm">/100</span>
      </div>
      <div className="space-y-3">
        {h.dimensions.map((dim) => (
          <div key={dim.label_en}>
            <div className="flex justify-between text-xs mb-1">
              <span className="text-muted-foreground">{isAr ? dim.label_ar : dim.label_en}</span>
              <span className="font-medium">{dim.score}</span>
            </div>
            <Progress value={dim.score} className="h-1.5" />
          </div>
        ))}
      </div>
    </Card>
  );
}

function DeliverablesTable({ isAr }: { isAr: boolean }) {
  return (
    <Card className="p-6">
      <h2 className="font-semibold text-[var(--dealix-deep-green)] mb-4">
        {isAr ? "قائمة التسليمات" : "Deliverables"}
      </h2>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b text-muted-foreground text-xs">
              <th className={`pb-2 font-medium ${isAr ? "text-right" : "text-left"}`}>
                {isAr ? "التسليم" : "Deliverable"}
              </th>
              <th className={`pb-2 font-medium ${isAr ? "text-right" : "text-left"}`}>
                {isAr ? "الحالة" : "Status"}
              </th>
              <th className={`pb-2 font-medium ${isAr ? "text-right" : "text-left"}`}>
                {isAr ? "تاريخ الاستحقاق" : "Due Date"}
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/40">
            {DEMO_DELIVERABLES.map((d) => {
              const sc = STATUS_CONFIG[d.status];
              return (
                <tr key={d.id} className="py-2">
                  <td className="py-3 font-medium">{isAr ? d.name_ar : d.name_en}</td>
                  <td className="py-3">
                    <Badge variant="outline" className={`text-xs ${sc.color}`}>
                      {isAr ? sc.label_ar : sc.label_en}
                    </Badge>
                  </td>
                  <td className="py-3 text-muted-foreground text-xs">{d.due}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </Card>
  );
}

function DocumentsSection({ isAr }: { isAr: boolean }) {
  return (
    <Card className="p-6">
      <h2 className="font-semibold text-[var(--dealix-deep-green)] mb-4">
        {isAr ? "وثائق Proof Pack" : "Proof Pack Documents"}
      </h2>
      <div className="space-y-3">
        {DEMO_DOCUMENTS.map((doc) => (
          <div
            key={doc.id}
            className="flex items-center justify-between p-3 rounded-lg border border-border/60 hover:border-[var(--dealix-deep-green)]/40 transition-colors"
          >
            <div className="flex items-center gap-3">
              <span
                className={`text-xs font-bold px-2 py-0.5 rounded ${
                  doc.ready
                    ? "bg-[var(--dealix-deep-green)] text-white"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                {doc.badge}
              </span>
              <span className="text-sm font-medium">{isAr ? doc.name_ar : doc.name_en}</span>
            </div>
            {doc.ready ? (
              <span className="text-xs text-[var(--dealix-deep-green)] font-medium">
                {isAr ? "متاح" : "Available"}
              </span>
            ) : (
              <span className="text-xs text-muted-foreground">
                {isAr ? "قيد الإعداد" : "In preparation"}
              </span>
            )}
          </div>
        ))}
      </div>
      <p className="text-xs text-muted-foreground mt-4">
        {isAr
          ? "ملاحظة: الوثائق الجاهزة ستُرسل عبر البريد الإلكتروني بعد مراجعة المؤسس."
          : "Note: Ready documents will be sent by email after founder review."}
      </p>
    </Card>
  );
}

function NextMilestoneCard({ isAr }: { isAr: boolean }) {
  const m = DEMO_NEXT_MILESTONE;
  const required = isAr ? m.required_from_client_ar : m.required_from_client_en;

  return (
    <Card className="p-6 border-[var(--dealix-gold)]/30 bg-[var(--dealix-gold)]/5">
      <h2 className="font-semibold text-[var(--dealix-deep-green)] mb-3">
        {isAr ? "الخطوة التالية" : "Next Milestone"}
      </h2>
      <p className="text-base font-bold">{isAr ? m.title_ar : m.title_en}</p>
      <p className="text-sm text-muted-foreground mt-1 mb-4">
        {isAr ? m.description_ar : m.description_en}
      </p>
      <div>
        <p className="text-xs font-semibold text-[var(--dealix-gold)] mb-2">
          {isAr ? "مطلوب من العميل:" : "Required from client:"}
        </p>
        <ul className="space-y-1">
          {required.map((item, i) => (
            <li key={i} className="flex items-start gap-2 text-sm">
              <span className="text-[var(--dealix-gold)] mt-0.5">-</span>
              {item}
            </li>
          ))}
        </ul>
      </div>
      <p className="text-xs text-muted-foreground mt-4">
        {isAr ? `الموعد النهائي: ${m.due_date}` : `Deadline: ${m.due_date}`}
      </p>
    </Card>
  );
}

// ---------------------------------------------------------------------------
// Main dashboard
// ---------------------------------------------------------------------------

export function CustomerPortalDashboard() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <div className="space-y-6" dir={isAr ? "rtl" : "ltr"}>
      <div>
        <h1 className="text-2xl font-bold text-[var(--dealix-deep-green)]">
          {isAr ? "بوابة العميل" : "Customer Portal"}
        </h1>
        <p className="text-sm text-muted-foreground mt-1">
          {isAr
            ? "بيانات تجريبية — سيتم ربطها بالنظام عند الإطلاق الكامل"
            : "Demo data — will be connected to backend at full launch"}
        </p>
      </div>

      <SprintStatusCard isAr={isAr} />

      <div className="grid gap-6 lg:grid-cols-2">
        <HealthScoreCard isAr={isAr} />
        <NextMilestoneCard isAr={isAr} />
      </div>

      <DeliverablesTable isAr={isAr} />
      <DocumentsSection isAr={isAr} />
    </div>
  );
}
