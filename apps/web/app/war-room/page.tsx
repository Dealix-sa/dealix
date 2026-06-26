"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  FOUNDER_PRIORITIES,
  ACQUISITION_FUNNEL,
  DELIVERY_PIPELINE,
  DAILY_KPIS,
  RISK_MATRIX,
  type DailyKpi,
  type RiskItem,
} from "@/lib/company-os/company-os";

function getRiyadhTime(): Date {
  // UTC+3 for Riyadh
  const now = new Date();
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  return new Date(utc + 3 * 3600000);
}

function formatRiyadhClock(d: Date): string {
  const h = String(d.getHours()).padStart(2, "0");
  const m = String(d.getMinutes()).padStart(2, "0");
  const s = String(d.getSeconds()).padStart(2, "0");
  return `${h}:${m}:${s}`;
}

const ARABIC_DATE = "يوم الجمعة، ٢٧ يونيو ٢٠٢٦";

const SEVERITY_COLORS: Record<RiskItem["severity"], string> = {
  critical: "border-rose-500/60 bg-rose-500/10 text-rose-300",
  high: "border-orange-500/60 bg-orange-500/10 text-orange-300",
  medium: "border-amber-400/60 bg-amber-400/10 text-amber-300",
  low: "border-emerald-500/40 bg-emerald-500/10 text-emerald-300",
};

const SEVERITY_LABEL: Record<RiskItem["severity"], string> = {
  critical: "CRITICAL",
  high: "HIGH",
  medium: "MEDIUM",
  low: "LOW",
};

const KPI_COLOR_CLASSES: Record<DailyKpi["color"], { border: string; badge: string; text: string }> = {
  orange: { border: "border-orange-500/40", badge: "bg-orange-500/20 text-orange-300", text: "text-orange-300" },
  red: { border: "border-rose-500/40", badge: "bg-rose-500/20 text-rose-300", text: "text-rose-300" },
  gray: { border: "border-white/20", badge: "bg-white/10 text-white/50", text: "text-white/50" },
  amber: { border: "border-amber-400/40", badge: "bg-amber-400/20 text-amber-300", text: "text-amber-300" },
  emerald: { border: "border-emerald-500/40", badge: "bg-emerald-500/20 text-emerald-300", text: "text-emerald-300" },
};

const QUICK_LINKS = [
  { label: "Command Room", labelAr: "غرفة القيادة", href: "/app/command-room" },
  { label: "CRM", labelAr: "إدارة العملاء", href: "/app/crm" },
  { label: "Lead Engine", labelAr: "محرك العملاء", href: "/app/lead-engine" },
  { label: "Proposals", labelAr: "العروض", href: "/app/quotes" },
  { label: "Proof Vault", labelAr: "خزانة الإثبات", href: "/app/proof-vault" },
  { label: "Review Queue", labelAr: "طابور المراجعة", href: "/app/review-queue" },
  { label: "Client Delivery", labelAr: "تسليم العملاء", href: "/app/client-delivery" },
  { label: "Revenue OS", labelAr: "نظام الإيرادات", href: "/app/revenue-os" },
];

const FUNNEL_STAGES = [
  { label: "Discover", labelAr: "اكتشاف", count: 0, color: "bg-white/10" },
  { label: "Qualify", labelAr: "تأهيل", count: 0, color: "bg-amber-500/20" },
  { label: "Outreach", labelAr: "تواصل", count: 0, color: "bg-amber-400/30" },
  { label: "Meeting", labelAr: "اجتماع", count: 0, color: "bg-amber-300/30" },
  { label: "Proposal", labelAr: "عرض", count: 0, color: "bg-orange-400/30" },
  { label: "Close", labelAr: "إغلاق", count: 0, color: "bg-emerald-500/20" },
];

const SAFETY_GATES = [
  { label: "No Auto-Send", labelAr: "لا إرسال تلقائي", locked: true },
  { label: "Human Review Gate", labelAr: "بوابة المراجعة البشرية", locked: true },
  { label: "No Cold WhatsApp", labelAr: "لا واتساب بارد", locked: true },
  { label: "No LinkedIn Automation", labelAr: "لا أتمتة لينكدإن", locked: true },
  { label: "PDPL Compliant", labelAr: "متوافق مع PDPL", locked: true },
  { label: "No Guaranteed Claims", labelAr: "لا ادعاءات مضمونة", locked: true },
];

export default function WarRoomPage() {
  const [clock, setClock] = useState<string>("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const tick = () => setClock(formatRiyadhClock(getRiyadhTime()));
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <main className="min-h-screen bg-[#070A12] text-white" dir="rtl">
      {/* Top status bar */}
      <div className="border-b border-white/10 bg-[#0A0E1A]/80 px-6 py-2 flex items-center justify-between text-xs">
        <span className="text-amber-300 tracking-widest font-mono uppercase">
          DEALIX WAR ROOM · غرفة الحرب
        </span>
        <div className="flex items-center gap-4 text-white/50">
          <span dir="rtl">{ARABIC_DATE}</span>
          <span className="font-mono text-amber-300/80 tabular-nums" dir="ltr">
            {mounted ? clock : "--:--:--"} AST
          </span>
        </div>
      </div>

      {/* System status banner */}
      <div className="bg-emerald-900/30 border-b border-emerald-500/30 px-6 py-2 text-center">
        <span className="text-emerald-400 text-xs tracking-[0.4em] font-mono uppercase">
          DEALIX SYSTEMS OPERATIONAL · الأنظمة تعمل بشكل طبيعي
        </span>
      </div>

      <div className="mx-auto max-w-7xl px-4 py-8 space-y-8">

        {/* Header */}
        <header className="flex items-start justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-amber-300/70 font-mono">
              Founder War Room · غرفة حرب المؤسس
            </p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight">
              غرفة الحرب — CEO Command View
            </h1>
            <p className="mt-1 text-sm text-white/50">
              One view. Every morning. All critical signals.
            </p>
          </div>
          <div className="text-right text-xs text-white/40 space-y-1">
            <div>Riyadh · UTC+3</div>
            <div>90-Day Commercial Sprint</div>
            <div className="text-amber-300/60">Day 1 of 90</div>
          </div>
        </header>

        {/* KPI Metrics Grid */}
        <section>
          <h2 className="text-xs uppercase tracking-widest text-white/40 font-mono mb-3">
            KPI Dashboard · مؤشرات الأداء الرئيسية
          </h2>
          <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-6">
            {DAILY_KPIS.map((kpi) => {
              const c = KPI_COLOR_CLASSES[kpi.color];
              return (
                <div
                  key={kpi.id}
                  className={`rounded-xl border ${c.border} bg-white/5 p-4 flex flex-col justify-between min-h-[120px]`}
                >
                  <div>
                    <p className="text-xs text-white/40 leading-tight">{kpi.labelAr}</p>
                    <p className="text-[10px] text-white/25">{kpi.label}</p>
                  </div>
                  <div>
                    <p className={`text-2xl font-bold tabular-nums ${c.text}`}>
                      {kpi.current.toLocaleString()}
                      {kpi.unit === "SAR" ? "" : kpi.unit === "days" ? "" : ""}
                    </p>
                    {kpi.unit === "SAR" && (
                      <p className="text-[10px] text-white/30">SAR · هدف: {kpi.target.toLocaleString()}</p>
                    )}
                    {kpi.unit === "days" && (
                      <p className="text-[10px] text-white/30">يوم · هدف: {kpi.target}</p>
                    )}
                    {kpi.unit === "" && (
                      <p className="text-[10px] text-white/30">هدف: {kpi.target}</p>
                    )}
                    <span className={`mt-2 inline-block rounded px-2 py-0.5 text-[10px] font-mono ${c.badge}`}>
                      {kpi.statusLabel}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* Revenue Pipeline Funnel + CEO Moves */}
        <div className="grid gap-6 md:grid-cols-2">

          {/* Revenue funnel */}
          <section className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-sm font-semibold text-amber-300 mb-4">
              Revenue Pipeline Funnel · مسار خط الإيرادات
            </h2>
            <div className="space-y-2">
              {FUNNEL_STAGES.map((stage, i) => (
                <div key={stage.label} className="flex items-center gap-3">
                  <span className="w-5 text-xs text-white/30 font-mono text-left">{i + 1}</span>
                  <div className={`flex-1 rounded-lg ${stage.color} border border-white/10 px-3 py-2 flex justify-between items-center`}>
                    <div>
                      <span className="text-sm text-white/80">{stage.labelAr}</span>
                      <span className="text-xs text-white/30 mr-2">· {stage.label}</span>
                    </div>
                    <span className="font-mono text-lg font-bold text-white/60">{stage.count}</span>
                  </div>
                </div>
              ))}
            </div>
            <p className="mt-3 text-xs text-white/30">Total qualified leads in pipeline: 0</p>
          </section>

          {/* Today's CEO moves */}
          <section className="rounded-2xl border border-amber-400/20 bg-amber-400/5 p-6">
            <h2 className="text-sm font-semibold text-amber-300 mb-4">
              Today's CEO Moves · تحركات المؤسس اليوم
            </h2>
            <ol className="space-y-3">
              {FOUNDER_PRIORITIES.map((p) => (
                <li key={p.id} className="flex gap-3 items-start">
                  <span className="flex-shrink-0 w-6 h-6 rounded border border-white/20 bg-white/5 flex items-center justify-center text-xs text-amber-300 font-mono">
                    {p.rank}
                  </span>
                  <div className="flex-1">
                    <p className="text-sm text-white/90 font-medium leading-tight">{p.titleAr}</p>
                    <p className="text-xs text-white/40 mt-0.5">{p.title}</p>
                    <p className="text-xs text-amber-300/60 mt-0.5">
                      خلال {p.dueInDays} يوم{p.dueInDays === 1 ? "" : ""}
                    </p>
                  </div>
                </li>
              ))}
            </ol>
          </section>
        </div>

        {/* Risk Matrix */}
        <section className="rounded-2xl border border-rose-500/20 bg-rose-500/5 p-6">
          <h2 className="text-sm font-semibold text-rose-300 mb-4">
            Risk Matrix · مصفوفة المخاطر
          </h2>
          <div className="grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {RISK_MATRIX.map((risk) => (
              <div
                key={risk.id}
                className={`rounded-xl border p-4 ${SEVERITY_COLORS[risk.severity]}`}
              >
                <div className="flex items-start justify-between gap-2 mb-2">
                  <p className="text-sm font-medium leading-tight">{risk.titleAr}</p>
                  <span className="flex-shrink-0 text-[10px] font-mono px-1.5 py-0.5 rounded bg-black/20">
                    {SEVERITY_LABEL[risk.severity]}
                  </span>
                </div>
                <p className="text-xs text-white/50">{risk.mitigationAr}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Client Delivery Pipeline + Safety Gates */}
        <div className="grid gap-6 md:grid-cols-2">

          {/* Delivery pipeline */}
          <section className="rounded-2xl border border-white/10 bg-white/5 p-6">
            <h2 className="text-sm font-semibold text-amber-300 mb-4">
              Client Delivery Pipeline · خط تسليم العملاء
            </h2>
            <div className="space-y-2">
              {DELIVERY_PIPELINE.map((stage) => (
                <div key={stage.id} className="rounded-lg border border-white/10 bg-black/20 px-3 py-2">
                  <div className="flex justify-between items-center">
                    <p className="text-xs font-medium text-white/80">{stage.titleAr}</p>
                    <span className="text-[10px] font-mono text-white/30">{stage.dayRange}</span>
                  </div>
                  <p className="text-[11px] text-white/40 mt-0.5">{stage.title}</p>
                </div>
              ))}
            </div>
          </section>

          {/* Safety gates */}
          <section className="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-6">
            <h2 className="text-sm font-semibold text-emerald-300 mb-4">
              Safety Gates · بوابات الأمان
            </h2>
            <p className="text-xs text-white/40 mb-4">All gates locked = compliant operations</p>
            <div className="space-y-2">
              {SAFETY_GATES.map((gate) => (
                <div
                  key={gate.label}
                  className="flex items-center justify-between rounded-lg border border-emerald-500/20 bg-emerald-500/5 px-3 py-2"
                >
                  <div>
                    <p className="text-sm text-white/80">{gate.labelAr}</p>
                    <p className="text-xs text-white/30">{gate.label}</p>
                  </div>
                  <span className="text-xs font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
                    {gate.locked ? "LOCKED" : "OPEN"}
                  </span>
                </div>
              ))}
            </div>
          </section>
        </div>

        {/* Quick Links */}
        <section>
          <h2 className="text-xs uppercase tracking-widest text-white/40 font-mono mb-3">
            Quick Actions · الإجراءات السريعة
          </h2>
          <div className="grid grid-cols-2 gap-2 md:grid-cols-4">
            {QUICK_LINKS.map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-center hover:border-amber-400/40 hover:bg-amber-400/5 transition-colors"
              >
                <p className="text-sm font-medium text-white/90">{link.labelAr}</p>
                <p className="text-xs text-white/30 mt-0.5">{link.label}</p>
              </Link>
            ))}
          </div>
        </section>

        {/* Acquisition funnel reference */}
        <section className="rounded-2xl border border-white/10 bg-white/5 p-6">
          <h2 className="text-sm font-semibold text-amber-300 mb-4">
            Acquisition Playbook · دليل الاكتساب
          </h2>
          <div className="grid gap-2 md:grid-cols-3">
            {ACQUISITION_FUNNEL.map((step) => (
              <div key={step.id} className="rounded-lg border border-white/10 bg-black/20 p-3">
                <p className="text-xs font-medium text-white/80">{step.titleAr}</p>
                <p className="text-[11px] text-white/40">{step.title}</p>
                <p className="text-[11px] text-white/50 mt-1 leading-relaxed">{step.goalAr}</p>
              </div>
            ))}
          </div>
        </section>

      </div>

      {/* Footer */}
      <footer className="border-t border-white/10 px-6 py-4 text-center text-xs text-white/30 font-mono">
        Dealix War Room · Riyadh · PDPL-Compliant · No auto-send · Human review required before any external action
      </footer>
    </main>
  );
}
