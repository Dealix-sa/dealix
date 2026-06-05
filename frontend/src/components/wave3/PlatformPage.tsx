import { Section } from "@/components/wave3/Section";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";

const LAYERS = [
  { ar: ["Revenue OS", "الفرص والمتابعة والعروض والخطوة التالية — الوتد التجاري."], en: ["Revenue OS", "Opportunities, follow-up, offers, next step — the commercial wedge."] },
  { ar: ["Proof OS", "طبقة الثقة: سجل إثبات قابل للتدقيق و Proof Pack."], en: ["Proof OS", "Trust layer: an auditable proof register and Proof Pack."] },
  { ar: ["Governance OS", "طبقة الأمان: موافقة بشرية وحدود واضحة."], en: ["Governance OS", "Safety layer: human approval and clear boundaries."] },
  { ar: ["Delivery OS", "طبقة التنفيذ: مصنع تسليم 7 أيام وسجل تسليم."], en: ["Delivery OS", "Fulfillment layer: a 7-day delivery factory and log."] },
  { ar: ["Market Intelligence OS", "طبقة النمو: إشارات القطاع ومكتبة الإجابات."], en: ["Market Intelligence OS", "Growth layer: sector signals and an answer library."] },
];

export function PlatformPage({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  return (
    <div className={isAr ? "text-right" : "text-left"}>
      <h1 className="text-4xl font-bold font-display leading-tight">
        {isAr ? "نظام تشغيل أعمال بالذكاء الاصطناعي — سعودي أولاً" : "An AI Business Operating System — Saudi-first"}
      </h1>
      <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
        {isAr
          ? "دييلكس ليس CRM ولا شات بوت ولا أداة عامة. هو طبقات تشغيل واحدة توضّح فرصك وإثباتك وقرارك التنفيذي القادم — بموافقة بشرية."
          : "Dealix is not a CRM, a chatbot, or a generic tool. It is one set of operating layers that clarifies your opportunities, proof, and next executive decision — with human approval."}
      </p>

      <Section eyebrow={isAr ? "الطبقات" : "The layers"} title={isAr ? "طبقات Business OS" : "Business OS layers"}>
        <div className="grid gap-3 sm:grid-cols-2">
          {LAYERS.map((l, i) => {
            const [t, d] = isAr ? l.ar : l.en;
            return (
              <div key={i} className="rounded-xl border border-border p-5">
                <p className="font-semibold text-gold-500">{t}</p>
                <p className="mt-1 text-sm text-muted-foreground">{d}</p>
              </div>
            );
          })}
        </div>
      </Section>

      <Section eyebrow={isAr ? "كيف نبدأ" : "How we start"} title={isAr ? "تبدأ من Command Sprint" : "You start with a Command Sprint"}>
        <p className="text-muted-foreground leading-relaxed">
          {isAr
            ? "الوتد الأول هو Command Sprint: 7 أيام ثابتة النطاق تنتج خريطة فرص وسجل إثبات وملخصاً تنفيذياً — كـ Proof Pack."
            : "The first wedge is the Command Sprint: a 7-day fixed scope producing a revenue map, a proof register, and an executive brief — as a Proof Pack."}
        </p>
      </Section>

      <div className="mt-6">
        <PrimaryCta locale={locale} href="/dealix-diagnostic" labelAr="احجز تشخيصاً" labelEn="Book Diagnostic" />
      </div>
    </div>
  );
}
