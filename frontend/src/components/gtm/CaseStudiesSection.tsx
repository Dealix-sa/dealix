"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

/* ─────────────────────────────────────────────────────────────────────────
   Honest methodology — illustrative engagement STRUCTURE, not claimed client
   results. No invented metrics, names, cities, or consent claims
   (non-negotiables #4/#5). Real, consented case studies replace this once a
   Proof Pack is delivered.
   ───────────────────────────────────────────────────────────────────────── */

const STAGES: {
  id: string;
  tag: { ar: string; en: string };
  challenge: { ar: string; en: string };
  approach: { ar: string; en: string };
  evidence: { ar: string; en: string };
}[] = [
  {
    id: "diagnose",
    tag: { ar: "المرحلة ١ — التشخيص", en: "Stage 1 — Diagnose" },
    challenge: { ar: "لا تعرف أين تتسرّب الفرص في pipeline الحالي.", en: "You don't know where opportunities leak in the current pipeline." },
    approach: { ar: "Risk Score مجاني ثم تشخيص محكوم خلال 48 ساعة لأهم 10 leads.", en: "Free Risk Score, then a governed 48-hour diagnostic on your top 10 leads." },
    evidence: { ar: "خريطة فجوات + مالك واضح لكل lead.", en: "A gap map + a clear owner per lead." },
  },
  {
    id: "prove",
    tag: { ar: "المرحلة ٢ — الإثبات", en: "Stage 2 — Prove" },
    challenge: { ar: "الإدارة ترفض الأدلة غير الموثّقة.", en: "Management rejects undocumented proof." },
    approach: { ar: "Proof Pack ثنائي اللغة بمستويات أدلة L0–L5.", en: "Bilingual Proof Pack with L0–L5 evidence levels." },
    evidence: { ar: "PDF جاهز للعرض على العميل أو الإدارة.", en: "A PDF ready to present to a client or management." },
  },
  {
    id: "operate",
    tag: { ar: "المرحلة ٣ — التشغيل", en: "Stage 3 — Operate" },
    challenge: { ar: "تحتاج تحسّناً مستمراً لا حدثاً لمرة واحدة.", en: "You need continuous improvement, not a one-off." },
    approach: { ar: "Managed Ops شهري: OKR أسبوعي + Approval Center.", en: "Monthly Managed Ops: weekly OKR + Approval Center." },
    evidence: { ar: "Proof Pack شهري محكوم بموافقة على كل خطوة.", en: "A monthly governed Proof Pack with approval at every step." },
  },
];

interface CaseStudiesSectionProps {
  className?: string;
}

export function CaseStudiesSection({ className = "" }: CaseStudiesSectionProps) {
  const locale = useLocale();
  const isAr = locale === "ar";
  const base = `/${locale}`;

  return (
    <section className={`space-y-10 ${className}`} dir={isAr ? "rtl" : "ltr"}>
      <div className={isAr ? "text-right" : "text-left"}>
        <p className="text-sm font-semibold text-[#C9974B] uppercase tracking-wide mb-2">
          {isAr ? "كيف تسير الرحلة" : "How an engagement works"}
        </p>
        <h2 className="text-3xl font-bold">
          {isAr ? "هيكل التعامل — شخّص ثم أثبت ثم شغّل" : "Engagement structure — Diagnose, Prove, Operate"}
        </h2>
        <p className="mt-3 text-muted-foreground max-w-2xl leading-relaxed">
          {isAr
            ? "هذا هيكل توضيحي لمسار العمل — وليس نتيجة عميل. قصص النجاح الحقيقية الموثّقة تظهر هنا بعد أول مشروع مُسلَّم وبموافقة أصحابها."
            : "This is an illustrative workflow structure — not a client result. Real, documented success stories appear here after the first delivered project, with owner consent."}
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {STAGES.map((s) => (
          <Card key={s.id} className="flex flex-col border-border/60 bg-card/50 overflow-hidden">
            <div className="bg-[#0A1628] px-5 py-3">
              <p className="text-[#C9974B] text-sm font-semibold">{isAr ? s.tag.ar : s.tag.en}</p>
            </div>
            <div className={`flex flex-col flex-1 p-5 space-y-4 ${isAr ? "text-right" : "text-left"}`}>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">{isAr ? "التحدي" : "Challenge"}</p>
                <p className="text-sm text-muted-foreground leading-relaxed">{isAr ? s.challenge.ar : s.challenge.en}</p>
              </div>
              <div>
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">{isAr ? "المنهج" : "Approach"}</p>
                <p className="text-sm text-muted-foreground leading-relaxed">{isAr ? s.approach.ar : s.approach.en}</p>
              </div>
              <div className="border-s-2 border-[#C9974B] ps-3">
                <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground mb-1">{isAr ? "الدليل" : "Evidence"}</p>
                <p className="text-sm text-foreground leading-relaxed">{isAr ? s.evidence.ar : s.evidence.en}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 rounded-xl border border-border/60 bg-card/30 px-6 py-4">
        <p className="text-xs text-muted-foreground max-w-lg">
          {isAr
            ? "هيكل توضيحي — الأدلة الموثّقة تُسلَّم في Proof Pack. لا أرقام عملاء مُختلقة."
            : "Illustrative structure — documented evidence is delivered in the Proof Pack. No invented client metrics."}
        </p>
        <Button asChild size="sm" className="bg-[#C9974B] text-[#0A1628] hover:bg-[#b8863a] font-semibold whitespace-nowrap">
          <Link href={`${base}/dealix-diagnostic`}>{isAr ? "ابدأ التشخيص" : "Start Diagnostic"}</Link>
        </Button>
      </div>
    </section>
  );
}
