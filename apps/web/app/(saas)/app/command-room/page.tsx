"use client";

import Link from "next/link";
import { COMPANY_STATUS, DAILY_KPIS, RISK_MATRIX } from "@/lib/company-os/company-os";

const STATUS_COLORS = {
  operational: "border-emerald-500/40 bg-emerald-500/10 text-emerald-400",
  building: "border-amber-400/40 bg-amber-400/10 text-amber-400",
  blocked: "border-rose-500/40 bg-rose-500/10 text-rose-400",
  planned: "border-white/20 bg-white/5 text-white/40",
};

const STATUS_LABELS = {
  operational: "تشغيل · OPERATIONAL",
  building: "بناء · BUILDING",
  blocked: "محظور · BLOCKED",
  planned: "مخطط · PLANNED",
};

const QUICK_ACTIONS = [
  { label: "مراجعة طابور التواصل", sublabel: "Review Outreach Queue", href: "/app/review-queue", urgent: true },
  { label: "إنشاء عرض جديد", sublabel: "Generate Proposal", href: "/app/quotes", urgent: true },
  { label: "تسجيل عنصر إثبات", sublabel: "Log Proof Item", href: "/app/proof-vault", urgent: false },
  { label: "متابعة العملاء المحتملين", sublabel: "Follow Up Leads", href: "/app/crm", urgent: false },
  { label: "تقرير التسليم الأسبوعي", sublabel: "Weekly Delivery Report", href: "/app/delivery-os", urgent: false },
  { label: "مراجعة مؤشرات الأداء", sublabel: "Review KPIs", href: "/app/kpi-finance", urgent: false },
];

export default function CommandRoomPage() {
  const systems = Object.values(COMPANY_STATUS);
  const criticalRisks = RISK_MATRIX.filter((r) => r.severity === "critical" || r.severity === "high");

  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      <div className="mx-auto max-w-7xl px-4 py-8 space-y-8">

        {/* Header */}
        <header>
          <p className="text-xs uppercase tracking-[0.35em] text-amber-300/70 font-mono">
            Command Room · غرفة القيادة
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">
            مركز القيادة الموحد
          </h1>
          <p className="mt-1 text-sm text-white/50">
            All 7 operating systems. One dashboard. Real-time operational status.
          </p>
        </header>

        {/* Daily KPI strip */}
        <section className="rounded-2xl border border-white/10 bg-white/5 p-5">
          <h2 className="text-xs uppercase tracking-widest text-white/40 font-mono mb-4">
            Live KPIs · المؤشرات الحية
          </h2>
          <div className="grid grid-cols-3 gap-3 md:grid-cols-6">
            {DAILY_KPIS.map((kpi) => (
              <div key={kpi.id} className="text-center">
                <p className="text-2xl font-bold tabular-nums text-white/90">
                  {kpi.current.toLocaleString()}
                </p>
                <p className="text-[11px] text-white/40 leading-tight mt-1">{kpi.labelAr}</p>
                <p className="text-[10px] text-white/20">{kpi.unit}</p>
              </div>
            ))}
          </div>
        </section>

        {/* 7 Operating Systems */}
        <section>
          <h2 className="text-sm font-semibold text-amber-300 mb-4">
            الأنظمة التشغيلية السبعة · 7 Operating Systems
          </h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            {systems.map((sys) => (
              <Link
                key={sys.id}
                href={sys.link}
                className={`rounded-2xl border p-5 block hover:opacity-90 transition-opacity ${STATUS_COLORS[sys.status]}`}
              >
                <div className="flex items-start justify-between gap-2 mb-3">
                  <h3 className="text-sm font-semibold text-white leading-tight">{sys.nameAr}</h3>
                  <span className="flex-shrink-0 text-[10px] font-mono px-1.5 py-0.5 rounded bg-black/30">
                    {STATUS_LABELS[sys.status]}
                  </span>
                </div>
                <p className="text-xs text-white/50 leading-relaxed">{sys.descriptionAr}</p>
                <p className="text-[10px] text-white/25 mt-2">{sys.name}</p>
              </Link>
            ))}
          </div>
        </section>

        {/* Quick Actions */}
        <section>
          <h2 className="text-sm font-semibold text-amber-300 mb-4">
            الإجراءات السريعة · Quick Actions
          </h2>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {QUICK_ACTIONS.map((action) => (
              <Link
                key={action.href}
                href={action.href}
                className={`rounded-xl border px-5 py-4 flex items-center justify-between hover:opacity-90 transition-opacity ${
                  action.urgent
                    ? "border-rose-500/40 bg-rose-500/10"
                    : "border-white/10 bg-white/5"
                }`}
              >
                <div>
                  <p className="text-sm font-medium text-white/90">{action.label}</p>
                  <p className="text-xs text-white/40 mt-0.5">{action.sublabel}</p>
                </div>
                {action.urgent && (
                  <span className="text-[10px] font-mono text-rose-400 bg-rose-500/20 px-2 py-0.5 rounded">
                    URGENT
                  </span>
                )}
              </Link>
            ))}
          </div>
        </section>

        {/* Active Risks */}
        <section className="rounded-2xl border border-rose-500/20 bg-rose-500/5 p-6">
          <h2 className="text-sm font-semibold text-rose-300 mb-4">
            المخاطر الرئيسية النشطة · Active Critical Risks
          </h2>
          <div className="space-y-3">
            {criticalRisks.map((risk) => (
              <div
                key={risk.id}
                className="flex items-start gap-4 rounded-xl border border-white/10 bg-black/20 p-4"
              >
                <span className={`flex-shrink-0 text-[10px] font-mono px-2 py-1 rounded ${
                  risk.severity === "critical"
                    ? "bg-rose-500/30 text-rose-300"
                    : "bg-orange-500/30 text-orange-300"
                }`}>
                  {risk.severity.toUpperCase()}
                </span>
                <div>
                  <p className="text-sm font-medium text-white/90">{risk.titleAr}</p>
                  <p className="text-xs text-white/50 mt-1">{risk.mitigationAr}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Today's operational summary */}
        <section className="rounded-2xl border border-white/10 bg-white/5 p-6">
          <h2 className="text-sm font-semibold text-amber-300 mb-4">
            الملخص التشغيلي اليوم · Today's Operational Summary
          </h2>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="rounded-xl border border-white/10 bg-black/20 p-4">
              <p className="text-xs uppercase tracking-widest text-white/30 font-mono mb-2">المرحلة</p>
              <p className="text-lg font-bold text-amber-300">اليوم الأول</p>
              <p className="text-xs text-white/40">Day 1 of 90-Day Sprint</p>
            </div>
            <div className="rounded-xl border border-white/10 bg-black/20 p-4">
              <p className="text-xs uppercase tracking-widest text-white/30 font-mono mb-2">الأولوية</p>
              <p className="text-lg font-bold text-white/90">تصفير المراجعة</p>
              <p className="text-xs text-white/40">Clear review queue first</p>
            </div>
            <div className="rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4">
              <p className="text-xs uppercase tracking-widest text-white/30 font-mono mb-2">الامتثال</p>
              <p className="text-lg font-bold text-emerald-400">متوافق</p>
              <p className="text-xs text-white/40">PDPL · No auto-send</p>
            </div>
          </div>
        </section>

        {/* Sub-page links */}
        <section>
          <h2 className="text-xs uppercase tracking-widest text-white/40 font-mono mb-3">
            All Pages · جميع الصفحات
          </h2>
          <div className="grid grid-cols-3 gap-2 md:grid-cols-6">
            {[
              { label: "CRM", href: "/app/crm" },
              { label: "Leads", href: "/app/lead-engine" },
              { label: "Deals", href: "/app/deals" },
              { label: "Agents", href: "/app/agents" },
              { label: "Pipeline", href: "/app/pipeline" },
              { label: "Outreach", href: "/app/outreach-lab" },
              { label: "Delivery", href: "/app/delivery-os" },
              { label: "Proof", href: "/app/proof-vault" },
              { label: "Reviews", href: "/app/review-queue" },
              { label: "Revenue", href: "/app/revenue-os" },
              { label: "KPIs", href: "/app/kpi-finance" },
              { label: "Brain", href: "/app/company-brain-os" },
            ].map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="rounded-lg border border-white/10 bg-white/5 px-3 py-2 text-center text-xs text-white/60 hover:text-white hover:border-white/20 transition-colors"
              >
                {link.label}
              </Link>
            ))}
          </div>
        </section>

      </div>
    </main>
  );
}
