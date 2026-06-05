import { Section } from "@/components/wave3/Section";
import { PrimaryCta } from "@/components/wave3/PrimaryCta";

const OUTPUTS = [
  { ar: "Revenue Map — أين تتعطل فرصك", en: "Revenue Map — where your opportunities stall" },
  { ar: "Proof Register — الدليل لكل قرار", en: "Proof Register — evidence per decision" },
  { ar: "Approval Register — ما يحتاج موافقة بشرية", en: "Approval Register — what needs human approval" },
  { ar: "Next Action Board — خطوتك التالية", en: "Next Action Board — your next step" },
  { ar: "Executive Command Brief — صورة القرار", en: "Executive Command Brief — the decision picture" },
];

const DAYS = [
  { d: 1, ar: "Intake + Company Intelligence", en: "Intake + Company Intelligence" },
  { d: 2, ar: "Diagnostic Summary", en: "Diagnostic Summary" },
  { d: 3, ar: "Revenue Map", en: "Revenue Map" },
  { d: 4, ar: "Proof Register", en: "Proof Register" },
  { d: 5, ar: "Approval Register + Next Action Board", en: "Approval Register + Next Action Board" },
  { d: 6, ar: "Executive Command Brief", en: "Executive Command Brief" },
  { d: 7, ar: "Proof Pack + Upsell Recommendation", en: "Proof Pack + Upsell Recommendation" },
];

export function CommandSprintPage({ locale }: { locale: string }) {
  const isAr = locale === "ar";
  return (
    <div className={isAr ? "text-right" : "text-left"}>
      <p className="text-xs font-semibold uppercase tracking-widest text-gold-500">
        {isAr ? "الوتد التجاري الأول" : "First commercial wedge"}
      </p>
      <h1 className="mt-2 text-4xl font-bold font-display leading-tight">Dealix Command Sprint</h1>
      <p className="mt-4 text-lg text-muted-foreground leading-relaxed">
        {isAr
          ? "7 أيام ثابتة النطاق تعطيك صورة قرار قابلة للمراجعة. الوعد: وضوح — لا وعد بنتيجة مالية، وبدون أي إرسال تلقائي."
          : "A 7-day fixed-scope engagement giving you a review-ready decision picture. The promise: clarity — not a financial-result promise, and no automated sending."}
      </p>

      <Section eyebrow={isAr ? "المخرجات" : "Outputs"} title={isAr ? "ماذا تستلم" : "What you receive"}>
        <ul className="list-disc space-y-2 ps-5 text-muted-foreground">
          {OUTPUTS.map((o, i) => <li key={i}>{isAr ? o.ar : o.en}</li>)}
        </ul>
      </Section>

      <Section eyebrow={isAr ? "الجدول" : "Schedule"} title={isAr ? "خطة 7 أيام" : "The 7-day plan"}>
        <div className="grid gap-2">
          {DAYS.map((row) => (
            <div key={row.d} className="flex items-center gap-3 rounded-lg border border-border px-4 py-2 text-sm">
              <span className="font-bold text-gold-500">{isAr ? `يوم ${row.d}` : `Day ${row.d}`}</span>
              <span className="text-muted-foreground">{isAr ? row.ar : row.en}</span>
            </div>
          ))}
        </div>
      </Section>

      <div className="mt-6">
        <PrimaryCta locale={locale} href="/start" labelAr="ابدأ Command Sprint" labelEn="Start Command Sprint" />
      </div>
    </div>
  );
}
