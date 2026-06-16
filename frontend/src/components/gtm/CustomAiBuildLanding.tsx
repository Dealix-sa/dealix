"use client";

import Link from "next/link";
import { useLocale } from "next-intl";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

type Offer = {
  ar: string;
  en: string;
  price: string;
  duration_ar: string;
  duration_en: string;
  desc_ar: string;
  desc_en: string;
};

// Rail 2 — the custom Agentic-AI ladder (source: os/03_OFFERS.yml). Prices in SAR.
const OFFERS: Offer[] = [
  {
    ar: "تدقيق الـ Workflow بالذكاء الاصطناعي",
    en: "Agentic AI Workflow Audit",
    price: "5,000 – 25,000 SAR",
    duration_ar: "3–7 أيام",
    duration_en: "3–7 days",
    desc_ar: "نحلل workflow واحد ونطلع لكم خريطة كاملة لفرص AI Agents وخطة pilot واقعية.",
    desc_en: "We map one workflow into a full AI-agent opportunity map and a realistic pilot plan.",
  },
  {
    ar: "تجربة Workflow بالـ Agentic AI",
    en: "Agentic Workflow Pilot",
    price: "30,000 – 150,000 SAR",
    duration_ar: "20–35 يوم",
    duration_en: "20–35 days",
    desc_ar: "نبني نموذجاً عملياً يثبت القيمة على بياناتكم، مع نقاط موافقة بشرية مُفعّلة.",
    desc_en: "A working prototype that proves value on your data, with human approval points enabled.",
  },
  {
    ar: "أنظمة عمودية مخصصة",
    en: "Custom Vertical AI Systems",
    price: "40,000 – 750,000 SAR",
    duration_ar: "30–120 يوم",
    duration_en: "30–120 days",
    desc_ar: "أنظمة كاملة: الصيانة، التحكم بالمشاريع، المعرفة السيادية (RAG)، مركز القيادة التنفيذي، نظام الإيرادات.",
    desc_en: "Full systems: Maintenance, Project Controls, Sovereign Knowledge (RAG), Executive Command Center, Revenue AI OS.",
  },
  {
    ar: "حزمة حوكمة الذكاء الاصطناعي",
    en: "AI Governance Pack",
    price: "15,000 – 100,000 SAR",
    duration_ar: "14–30 يوم",
    duration_en: "14–30 days",
    desc_ar: "سياسة استخدام، مصفوفة صلاحيات، بوابات موافقة بشرية، وإطار تحكّم بالمخاطر — متوافق مع PDPL.",
    desc_en: "Usage policy, permission matrix, human approval gates, and a risk-control framework — PDPL-aligned.",
  },
  {
    ar: "الدعم والتطوير المستمر",
    en: "AI Ops Retainer",
    price: "8,000 – 80,000 SAR / شهر",
    duration_ar: "شهري",
    duration_en: "monthly",
    desc_ar: "نظامكم يتحسّن كل شهر — مراقبة، إصلاحات، تقارير، وتوسعة.",
    desc_en: "Your system improves every month — monitoring, fixes, reports, and expansion.",
  },
];

const STEPS = [
  { n: "1", ar: "أخبرنا وش تبي نبني", en: "Tell us what you want to build",
    d_ar: "القطاع، الـ workflow، والنتيجة المطلوبة.", d_en: "Sector, the workflow, and the outcome you want." },
  { n: "2", ar: "تدقيق + خطة pilot", en: "Audit + pilot plan",
    d_ar: "خريطة فرص AI وخطة pilot وتقدير تكلفة وعائد متوقع.", d_en: "AI opportunity map, pilot plan, cost estimate, expected ROI." },
  { n: "3", ar: "نبني ونثبت", en: "We build & prove",
    d_ar: "نموذج عملي على بياناتكم بنقاط موافقة بشرية.", d_en: "A working prototype on your data with human approval points." },
  { n: "4", ar: "إطلاق + دعم", en: "Launch + support",
    d_ar: "تشغيل، مراقبة، وتوسعة شهرية.", d_en: "Go-live, monitoring, and monthly expansion." },
];

export function CustomAiBuildLanding() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <div className="mx-auto w-full max-w-6xl px-4 py-10" dir={isAr ? "rtl" : "ltr"}>
      {/* Hero */}
      <section className="text-center">
        <Badge className="mb-4 bg-[#D4AF37] text-[#001F3F] hover:bg-[#D4AF37]">
          {isAr ? "ذكاء اصطناعي مخصص" : "Custom Agentic AI"}
        </Badge>
        <h1 className="text-3xl font-bold leading-tight text-[#001F3F] dark:text-white sm:text-4xl md:text-5xl">
          {isAr ? "ابنِ نظام الذكاء الاصطناعي المخصص لشركتك" : "Build your company's custom AI system"}
        </h1>
        <p className="mx-auto mt-4 max-w-2xl text-base text-slate-600 dark:text-slate-300 sm:text-lg">
          {isAr
            ? "من تدقيق آمن منخفض المخاطر إلى نظام يعمل على بياناتكم — محكوم، متوافق مع PDPL وZATCA، وبمبدأ الموافقة أولاً. لا scraping، ولا إرسال خارجي دون اعتمادكم."
            : "From a low-risk audit to a system running on your data — governed, PDPL & ZATCA aligned, approval-first. No scraping, and no external send without your sign-off."}
        </p>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <Button asChild className="bg-[#001F3F] text-white hover:bg-[#012a55]">
            <Link href={`/${locale}/dealix-diagnostic?intent=custom-ai`}>
              {isAr ? "ابدأ بتدقيق مجاني" : "Start with a free diagnostic"}
            </Link>
          </Button>
          <Button asChild variant="outline" className="border-[#001F3F] text-[#001F3F] dark:border-white dark:text-white">
            <Link href={`/${locale}/services`}>
              {isAr ? "شاهد كل الخدمات والأسعار" : "See all services & pricing"}
            </Link>
          </Button>
        </div>
      </section>

      {/* Offer ladder */}
      <section className="mt-14">
        <h2 className="mb-6 text-center text-2xl font-bold text-[#001F3F] dark:text-white">
          {isAr ? "سلّم الذكاء المخصص" : "The custom-AI ladder"}
        </h2>
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
          {OFFERS.map((o) => (
            <Card key={o.en} className="flex flex-col gap-3 border-t-4 border-t-[#D4AF37] p-5">
              <div className="flex items-baseline justify-between gap-2">
                <h3 className="text-lg font-semibold text-[#001F3F] dark:text-white">
                  {isAr ? o.ar : o.en}
                </h3>
              </div>
              <p className="text-sm font-medium text-[#D4AF37]">{o.price}</p>
              <p className="text-xs text-slate-500">{isAr ? o.duration_ar : o.duration_en}</p>
              <p className="text-sm text-slate-600 dark:text-slate-300">{isAr ? o.desc_ar : o.desc_en}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="mt-14">
        <h2 className="mb-6 text-center text-2xl font-bold text-[#001F3F] dark:text-white">
          {isAr ? "كيف نبدأ" : "How we start"}
        </h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {STEPS.map((s) => (
            <Card key={s.n} className="p-5">
              <div className="mb-2 flex h-9 w-9 items-center justify-center rounded-full bg-[#001F3F] font-bold text-white">
                {s.n}
              </div>
              <h3 className="font-semibold text-[#001F3F] dark:text-white">{isAr ? s.ar : s.en}</h3>
              <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{isAr ? s.d_ar : s.d_en}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* Doctrine + CTA */}
      <section className="mt-14 rounded-xl bg-[#001F3F] p-8 text-center text-white">
        <h2 className="text-2xl font-bold">
          {isAr ? "جاهز تبني نظامك؟" : "Ready to build your system?"}
        </h2>
        <p className="mx-auto mt-3 max-w-2xl text-sm text-slate-200">
          {isAr
            ? "ابدأ بتدقيق مجاني نحدّد فيه أين تظهر أكبر قيمة، ثم خطة pilot واضحة. النتائج تقديرية وغير مضمونة، وكل خطوة بموافقتكم."
            : "Start with a free diagnostic that pinpoints where the biggest value is, then a clear pilot plan. Outcomes are estimated, not guaranteed, and every step needs your approval."}
        </p>
        <div className="mt-5 flex flex-wrap items-center justify-center gap-3">
          <Button asChild className="bg-[#D4AF37] text-[#001F3F] hover:bg-[#c6a233]">
            <Link href={`/${locale}/dealix-diagnostic?intent=custom-ai`}>
              {isAr ? "ابدأ الآن" : "Start now"}
            </Link>
          </Button>
          <Button asChild variant="outline" className="border-white text-white hover:bg-white/10">
            <Link href={`/${locale}/trust-center`}>
              {isAr ? "كيف نحمي بياناتكم" : "How we protect your data"}
            </Link>
          </Button>
        </div>
      </section>
    </div>
  );
}
