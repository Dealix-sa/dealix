"use client";

import Link from "next/link";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { useBi, StatusPill, Disclosure, type Bi, type LaunchStatus } from "@/components/gtm/launch/kit";

type Entry = {
  title: Bi;
  body: Bi;
  cta: Bi;
  href: string;
  status: LaunchStatus;
  best: Bi;
};

const ENTRIES: Entry[] = [
  {
    title: { ar: "احسب Business OS Score", en: "Get your Business OS Score" },
    body: { ar: "تقييم ذاتي مجاني في دقيقتين. نتيجة تقديرية فورية، بلا تسجيل.", en: "A free two-minute self-assessment. Instant estimated score, no signup." },
    cta: { ar: "ابدأ التقييم", en: "Start the assessment" },
    href: "/business-os-score",
    status: "BETA",
    best: { ar: "الأنسب إذا كنت تستكشف", en: "Best if you're exploring" },
  },
  {
    title: { ar: "ابدأ التشخيص", en: "Run the diagnostic" },
    body: { ar: "تشخيص محكوم لإيراد شركتك مع Proof Pack — مبني على بياناتك.", en: "A governed diagnostic of your company's revenue with a Proof Pack — built from your data." },
    cta: { ar: "ابدأ التشخيص", en: "Start the diagnostic" },
    href: "/dealix-diagnostic",
    status: "BETA",
    best: { ar: "الأنسب إذا أردت دليلًا على بياناتك", en: "Best if you want proof on your data" },
  },
  {
    title: { ar: "ابدأ Command Sprint", en: "Start a Command Sprint" },
    body: { ar: "الإسفين التجاري الأول: ثماني وحدات تبني إيقاع التشغيل وتثبت القيمة.", en: "The first commercial wedge: eight modules that build the operating rhythm and prove value." },
    cta: { ar: "اعرف المزيد", en: "Learn more" },
    href: "/command-sprint",
    status: "BETA",
    best: { ar: "الأنسب إذا كنت جاهزًا للبدء", en: "Best if you're ready to begin" },
  },
];

export function StartHub() {
  const { t, base, isAr } = useBi();
  return (
    <PublicGtmShell>
      <div
        className="px-6 py-16 md:py-20"
        style={{ background: "linear-gradient(160deg,#00060d 0%,#001226 60%,#001832 100%)" }}
      >
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="font-arabic text-3xl font-bold text-white md:text-4xl">
            {isAr ? "ابدأ من هنا" : "Start here"}
          </h1>
          <p className="mx-auto mt-4 max-w-xl text-white/65">
            {isAr
              ? "ثلاث نقاط بداية لنظام تشغيل أعمالك. اختر الأنسب لمرحلتك — وكلها تقود إلى نفس الإيقاع."
              : "Three entry points into your Business OS. Pick what fits your stage — all lead to the same rhythm."}
          </p>
        </div>

        <div className="mx-auto mt-12 grid max-w-5xl gap-5 md:grid-cols-3">
          {ENTRIES.map((e) => (
            <div
              key={e.href}
              className="flex flex-col gap-4 rounded-2xl border border-white/10 bg-white/[0.04] p-6 transition-colors hover:border-gold-400/30"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-gold-300">{t(e.best)}</span>
                <StatusPill status={e.status} />
              </div>
              <h2 className="text-lg font-bold text-white">{t(e.title)}</h2>
              <p className="flex-1 text-sm leading-relaxed text-white/60">{t(e.body)}</p>
              <Link
                href={`${base}${e.href}`}
                className="mt-2 inline-flex items-center justify-center rounded-xl bg-gradient-to-r from-gold-500 to-gold-400 px-5 py-2.5 text-sm font-bold text-navy-500 shadow-md shadow-gold-500/20 transition-colors hover:from-gold-400 hover:to-gold-300"
              >
                {t(e.cta)}
              </Link>
            </div>
          ))}
        </div>
      </div>
      <Disclosure />
    </PublicGtmShell>
  );
}
