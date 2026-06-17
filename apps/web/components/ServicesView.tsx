import {
  SERVICE_LADDER,
  COMMAND_SPRINT,
  GOVERNANCE_AR,
  GOVERNANCE_EN,
  VALUE_DISCLAIMER,
  type Offering,
  type Accent,
} from "../lib/offerings";

type Locale = "ar" | "en";

const ACCENT: Record<Accent, { border: string; text: string; chip: string }> = {
  slate:   { border: "border-slate-400/30 bg-slate-400/5",   text: "text-slate-300",   chip: "bg-slate-400/15 text-slate-200" },
  cyan:    { border: "border-cyan-400/40 bg-cyan-400/5",     text: "text-cyan-300",    chip: "bg-cyan-400/15 text-cyan-200" },
  emerald: { border: "border-emerald-400/40 bg-emerald-400/10", text: "text-emerald-300", chip: "bg-emerald-400/15 text-emerald-200" },
  violet:  { border: "border-violet-400/40 bg-violet-400/5", text: "text-violet-300",  chip: "bg-violet-400/15 text-violet-200" },
  gold:    { border: "border-amber-300/40 bg-amber-300/5",   text: "text-amber-200",   chip: "bg-amber-300/15 text-amber-100" },
  amber:   { border: "border-amber-400/40 bg-amber-400/5",   text: "text-amber-300",   chip: "bg-amber-400/15 text-amber-200" },
};

const T = {
  ar: {
    eyebrow: "خدمات Dealix · Governed AI Revenue",
    h1: "أقوى خدمات تشغيل الإيراد بالذكاء الاصطناعي — للشركات السعودية",
    sub: "من تشخيص مجاني خلال ٢٤ ساعة، إلى سبرنت إثبات بـ٤٩٩ ريال، إلى تشغيل شهري وغرفة قيادة تنفيذية. وكله approval-first: الذكاء الاصطناعي يكتب ويحلّل، وأنت توافق وترسل.",
    ctaCustom: "عندك طلب خاص؟ وش تبي نسوّي ←",
    ctaFree: "ابدأ التشخيص المجاني",
    flagship: "العرض الرئيسي",
    sprintIncludes: "يشمل خلال ١٠ أيام",
    sprintCta: "اطلب Command Sprint",
    ladderTitle: "السلّم الكامل",
    ladderSub: "ابدأ من حيث يناسبك — وكل رتبة تبني على التي قبلها.",
    includes: "تشمل",
    kpi: "التزام KPI",
    request: "اطلب هذه الخدمة",
    startFree: "ابدأ مجاناً",
    customTitle: "وش تبي نسوّي؟ — Custom AI",
    customBody: "ما لقيت الخدمة المناسبة؟ اوصف التحدّي وراح نصمّم لك حلّاً مخصّصاً بنفس مبدأ الموافقة أولاً.",
    customCta: "اطلب حلّاً مخصّصاً",
    govTitle: "الحوكمة في كل خدمة",
    home: "الرئيسية",
    lang: "English",
    langHref: "/services",
  },
  en: {
    eyebrow: "Dealix Services · Governed AI Revenue",
    h1: "The strongest governed AI revenue services — for Saudi B2B.",
    sub: "From a free 24-hour diagnostic, to a 499 SAR proof sprint, to monthly ops and an executive command center. All approval-first: the AI drafts and analyses, you approve and send.",
    ctaCustom: "Have a custom need? Tell us what to build →",
    ctaFree: "Start the free diagnostic",
    flagship: "Flagship",
    sprintIncludes: "In 10 working days",
    sprintCta: "Request a Command Sprint",
    ladderTitle: "The full ladder",
    ladderSub: "Start where you are — each rung builds on the one before it.",
    includes: "Includes",
    kpi: "KPI commitment",
    request: "Request this service",
    startFree: "Start free",
    customTitle: "Tell us what to build — Custom AI",
    customBody: "Didn't find the right fit? Describe the challenge and we'll design a custom solution on the same approval-first principle.",
    customCta: "Request a custom build",
    govTitle: "Governance in every service",
    home: "Home",
    lang: "العربية",
    langHref: "/ar/services",
  },
};

function OfferingCard({ o, locale }: { o: Offering; locale: Locale }) {
  const a = ACCENT[o.accent];
  const t = T[locale];
  const ar = locale === "ar";
  const name = ar ? o.nameAr : o.nameEn;
  const price = ar ? o.priceAr : o.priceEn;
  const unit = ar ? o.unitAr : o.unitEn;
  const duration = ar ? o.durationAr : o.durationEn;
  const tagline = ar ? o.taglineAr : o.taglineEn;
  const deliverables = ar ? o.deliverablesAr : o.deliverablesEn;
  const kpi = ar ? o.kpiAr : o.kpiEn;
  const free = o.id === "free_mini_diagnostic";
  const href = ar ? "/ar/custom" : "/custom";

  return (
    <article className={`relative flex flex-col rounded-3xl border ${a.border} p-7`}>
      <div className="flex items-center justify-between">
        <span className={`rounded-full px-3 py-1 text-[0.7rem] font-black ${a.chip}`}>{o.rung}</span>
        {o.featured && (
          <span className="rounded-full bg-white/10 px-3 py-1 text-[0.7rem] font-bold text-white/80">
            {ar ? "موصى به" : "Recommended"}
          </span>
        )}
      </div>
      <h3 className="mt-4 text-xl font-black text-slate-100">{name}</h3>
      <p className={`mt-2 text-2xl font-black ${a.text}`}>{price}</p>
      <p className="text-xs text-slate-400">{unit} · {duration}</p>
      <p className="mt-4 text-sm leading-7 text-slate-300">{tagline}</p>

      <p className="mt-5 text-[0.7rem] font-bold uppercase tracking-wide text-slate-500">{t.includes}</p>
      <ul className="mt-2 space-y-1.5 text-sm text-slate-400">
        {deliverables.map((d) => (
          <li key={d} className="flex gap-2">
            <span className={a.text}>✓</span>
            <span className="leading-6">{d}</span>
          </li>
        ))}
      </ul>

      <div className="mt-5 rounded-xl border border-white/10 bg-white/[0.03] p-3">
        <p className="text-[0.7rem] font-bold uppercase tracking-wide text-slate-500">{t.kpi}</p>
        <p className="mt-1 text-xs leading-6 text-slate-300">{kpi}</p>
      </div>

      <a
        href={href}
        className={`mt-6 block rounded-2xl border ${a.border} px-5 py-3 text-center text-sm font-black ${a.text} hover:bg-white/5`}
      >
        {free ? t.startFree : t.request}
      </a>
    </article>
  );
}

export default function ServicesView({ locale }: { locale: Locale }) {
  const t = T[locale];
  const ar = locale === "ar";
  const customHref = ar ? "/ar/custom" : "/custom";
  const homeHref = ar ? "/ar" : "/";
  const governance = ar ? GOVERNANCE_AR : GOVERNANCE_EN;
  const sprintDeliverables = ar ? COMMAND_SPRINT.deliverablesAr : COMMAND_SPRINT.deliverablesEn;

  return (
    <main dir={ar ? "rtl" : "ltr"} className="min-h-screen bg-[#06111f] text-white">
      {/* Top bar */}
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
        <a href={homeHref} className="text-lg font-black text-white">Dealix</a>
        <nav className="flex items-center gap-5 text-sm text-slate-400">
          <a href={homeHref} className="hover:text-white">{t.home}</a>
          <a href={t.langHref} className="hover:text-white">{t.lang}</a>
          <a href={customHref} className="rounded-xl bg-cyan-400 px-4 py-2 font-black text-[#06111f] hover:bg-cyan-300">
            {ar ? "طلب خاص" : "Custom"}
          </a>
        </nav>
      </header>

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 pt-10 pb-14 md:pt-16">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          {t.eyebrow}
        </p>
        <h1 className="max-w-5xl text-4xl font-black leading-[1.15] md:text-6xl">{t.h1}</h1>
        <p className="mt-7 max-w-3xl text-lg leading-9 text-slate-300">{t.sub}</p>
        <div className="mt-9 flex flex-wrap gap-4">
          <a href={customHref} className="rounded-2xl bg-cyan-400 px-8 py-4 text-lg font-black text-[#06111f] hover:bg-cyan-300">
            {t.ctaCustom}
          </a>
          <a href={customHref} className="rounded-2xl border border-white/20 px-8 py-4 text-lg font-semibold text-white hover:bg-white/10">
            {t.ctaFree}
          </a>
        </div>
      </section>

      {/* Flagship — Command Sprint */}
      <section className="mx-auto max-w-6xl px-6 pb-16">
        <div className="rounded-4xl border border-amber-300/30 bg-gradient-to-b from-amber-300/[0.07] to-transparent p-8 md:p-12">
          <span className="rounded-full bg-amber-300/15 px-3 py-1 text-[0.7rem] font-black text-amber-100">{t.flagship}</span>
          <div className="mt-5 flex flex-col gap-8 md:flex-row md:items-start md:justify-between">
            <div className="md:max-w-xl">
              <h2 className="text-3xl font-black text-amber-100">{COMMAND_SPRINT.nameEn}</h2>
              <p className="mt-2 text-2xl font-black text-white">{ar ? COMMAND_SPRINT.priceAr : COMMAND_SPRINT.priceEn}</p>
              <p className="text-sm text-slate-400">{ar ? COMMAND_SPRINT.unitAr : COMMAND_SPRINT.unitEn}</p>
              <p className="mt-5 text-base leading-8 text-slate-200">{ar ? COMMAND_SPRINT.taglineAr : COMMAND_SPRINT.taglineEn}</p>
              <a href={customHref} className="mt-7 inline-block rounded-2xl bg-amber-300 px-8 py-3.5 font-black text-[#06111f] hover:bg-amber-200">
                {t.sprintCta}
              </a>
            </div>
            <div className="md:min-w-[19rem] md:max-w-sm">
              <p className="text-[0.7rem] font-bold uppercase tracking-wide text-amber-200/70">{t.sprintIncludes}</p>
              <ul className="mt-3 space-y-2 text-sm text-slate-300">
                {sprintDeliverables.map((d) => (
                  <li key={d} className="flex gap-2"><span className="text-amber-300">✓</span><span className="leading-6">{d}</span></li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* The ladder */}
      <section className="mx-auto max-w-6xl px-6 pb-16">
        <h2 className="text-3xl font-black">{t.ladderTitle}</h2>
        <p className="mt-3 max-w-2xl text-slate-400">{t.ladderSub}</p>
        <div className="mt-9 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {SERVICE_LADDER.map((o) => (
            <OfferingCard key={o.id} o={o} locale={locale} />
          ))}
        </div>
      </section>

      {/* Custom band */}
      <section className="mx-auto max-w-6xl px-6 pb-16">
        <div className="rounded-4xl border border-cyan-300/20 bg-cyan-400/5 p-10 text-center md:p-14">
          <h2 className="text-3xl font-black md:text-4xl">{t.customTitle}</h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-300">{t.customBody}</p>
          <a href={customHref} className="mt-8 inline-block rounded-2xl bg-white px-10 py-4 text-xl font-black text-[#06111f] hover:bg-slate-100">
            {t.customCta}
          </a>
        </div>
      </section>

      {/* Governance */}
      <section className="border-t border-white/5 bg-white/[0.02] py-14">
        <div className="mx-auto max-w-6xl px-6">
          <h2 className="text-2xl font-black">{t.govTitle}</h2>
          <div className="mt-6 grid gap-3 md:grid-cols-2">
            {governance.map((g) => (
              <div key={g} className="flex items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.03] px-5 py-4">
                <span className="mt-0.5 text-emerald-400">✓</span>
                <p className="text-sm leading-7 text-slate-300">{g}</p>
              </div>
            ))}
          </div>
          <p className="mt-8 text-center text-xs text-slate-500">{VALUE_DISCLAIMER}</p>
        </div>
      </section>
    </main>
  );
}
